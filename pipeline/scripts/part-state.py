#!/usr/bin/env python3
"""Per-PART state machine - the unit of atomicity (bead nhbplus-corpus-kgb).

Spec: stage-1/stage-1-spec.md section 5. A unit may be many parts; a part is
one submission attempt. `reserved` means spend committed and nothing sent.
`sent` means the socket opened. Different facts, recorded in order, before a
crash can erase either.

States: queued -> reserved -> sent -> settled | lost

On-disk layout (section 5.1):
  units/<UNIT_ID>/state.json              part state, atomically written
  units/<UNIT_ID>/receipt.json            THE unit of durability, one file:
      status, http_status, committed amount, part hash, request placeholder,
      INPUT_CHANNEL_COUNT, response_complete - one os.replace, never two.
  units/<UNIT_ID>/part-NN.bin             bytes as submitted
  units/<UNIT_ID>/response-part-NN.json   streamed response + response_complete
  units/<UNIT_ID>/assembled.json          emitted only for complete units

Atomic write (four steps, named syscalls):
  1. write <path>.tmp in the SAME directory (cross-dir rename is not atomic)
  2. f.flush() then os.fsync(fd) - without fsync, `sent` is a lie
  3. os.replace(tmp, path) - atomic on POSIX and NTFS
  4. fsync the containing directory so the rename itself is durable

Recovery table:
  no part file                        -> redo, no spend
  reserved                            -> release commit, re-reserve, submit
  sent, no file, http unset           -> PAID_UNKNOWN, operator decides
  sent, partial file                  -> PAID_UNKNOWN, operator decides
  sent, 402                           -> NOT BILLED: whole part to secondary
  sent, 429                           -> NOT BILLED: exponential backoff 2s/60s
  sent, 400                           -> NOT BILLED: re-prepare, resubmit
  sent, 504/timeout/truncated        -> PAID_UNKNOWN, then lost (only paid non-200)

A part in PAID_UNKNOWN is never resubmitted by any code path: submit()
refuses when the on-disk state is PAID_UNKNOWN. `lost` is terminal.
`queued` replays carry no commit and never report PAID_UNKNOWN.
"""
import hashlib
import json
import os

QUEUED = "queued"
RESERVED = "reserved"
SENT = "sent"
SETTLED = "settled"
LOST = "lost"
PAID_UNKNOWN = "PAID_UNKNOWN"

BACKOFF_BASE_S = 2
BACKOFF_CAP_S = 60

REQUIRED_RECEIPT_KEYS = ("status", "http_status", "committed_usd",
                         "part_sha256", "request", "input_channel_count",
                         "response_complete")


class PaidUnknown(Exception):
    """Raised when a part needs the operator. Never auto-resubmitted."""


class Refused(Exception):
    """Raised when a transition is illegal (e.g. submit on PAID_UNKNOWN)."""


def backoff_delay_s(attempt):
    """Exponential backoff, base 2 s, cap 60 s. attempt counts from 0."""
    return min(BACKOFF_CAP_S, BACKOFF_BASE_S * (2 ** attempt))


def atomic_write_json(path, obj):
    """Four-step durable write. Returns the bytes written."""
    data = json.dumps(obj, sort_keys=True).encode("utf-8")
    tmp = path + ".tmp"
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    try:
        fd = os.open(d, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except (OSError, AttributeError):
        pass  # platform without directory fsync; rename itself is still atomic
    return data


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_receipt(unit_dir):
    rp = os.path.join(unit_dir, "receipt.json")
    if not os.path.exists(rp):
        raise Refused("no receipt: nothing reserved, nothing sent")
    return read_json(rp)


def validate_receipt(receipt):
    """The schema check: response_complete deleted -> the machine fails."""
    missing = [k for k in REQUIRED_RECEIPT_KEYS if k not in receipt]
    if missing:
        raise Refused(f"receipt schema missing keys: {missing}")
    return True


def admit(unit_dir, part_id):
    """queued: no spend, no socket, no file beyond the state itself."""
    state = {"part": part_id, "status": QUEUED, "committed_usd": 0.0,
             "paid_unknown": False}
    atomic_write_json(os.path.join(unit_dir, "state.json"), state)
    return state


def reserve(unit_dir, part_id, amount_usd, part_sha256, request, input_channels):
    """reserved: spend committed, nothing sent. Single atomic receipt."""
    state = read_json(os.path.join(unit_dir, "state.json"))
    if state["status"] != QUEUED:
        raise Refused(f"reserve from {state['status']}, need queued")
    if state.get("paid_unknown"):
        raise Refused("reserve on PAID_UNKNOWN part")
    receipt = {"status": RESERVED, "http_status": None,
               "committed_usd": amount_usd, "part_sha256": part_sha256,
               "request": request, "input_channel_count": input_channels,
               "response_complete": False}
    validate_receipt(receipt)
    atomic_write_json(os.path.join(unit_dir, "receipt.json"), receipt)
    state.update({"status": RESERVED, "committed_usd": amount_usd})
    atomic_write_json(os.path.join(unit_dir, "state.json"), state)
    return receipt


def mark_sent(unit_dir, extras=None):
    """sent: durable BEFORE the socket opens. The whole protection.
    extras (e.g. sent_ts) merge into the receipt in the same atomic write,
    never into the seven load-bearing keys."""
    refund = read_receipt(unit_dir)
    if refund["status"] != RESERVED:
        raise Refused(f"mark_sent from {refund['status']}, need reserved")
    if refund.get("paid_unknown"):
        raise Refused("mark_sent on PAID_UNKNOWN part")
    refund["status"] = SENT
    for k, v in (extras or {}).items():
        if k in REQUIRED_RECEIPT_KEYS:
            raise Refused(f"extras may not overwrite receipt key {k}")
        refund[k] = v
    atomic_write_json(os.path.join(unit_dir, "receipt.json"), refund)
    state = read_json(os.path.join(unit_dir, "state.json"))
    state["status"] = SENT
    atomic_write_json(os.path.join(unit_dir, "state.json"), state)
    return refund


def submit(unit_dir):
    """The ONE place a socket may open. Refuses PAID_UNKNOWN outright."""
    state = read_json(os.path.join(unit_dir, "state.json"))
    if state.get("paid_unknown"):
        raise PaidUnknown("part is PAID_UNKNOWN: operator decides, never auto-resubmit")
    receipt = read_receipt(unit_dir)
    validate_receipt(receipt)
    if receipt["status"] == SENT and receipt.get("http_status") is None:
        # A restart found sent-but-no-outcome: the in-flight crash.
        state["paid_unknown"] = True
        atomic_write_json(os.path.join(unit_dir, "state.json"), state)
        raise PaidUnknown("sent with no outcome on restart: PAID_UNKNOWN")
    if receipt["status"] != SENT:
        raise Refused(f"submit from {receipt['status']}, need sent")
    return receipt


def settle(unit_dir, http_status, response_complete, response_path=None, extras=None):
    """Record the vendor verdict. Returns (status, action). extras merge."""
    receipt = read_receipt(unit_dir)
    validate_receipt(receipt)
    if receipt["status"] != SENT:
        raise Refused(f"settle from {receipt['status']}, need sent")
    state = read_json(os.path.join(unit_dir, "state.json"))
    receipt["http_status"] = http_status
    receipt["response_complete"] = bool(response_complete)

    if http_status == 200 and response_complete:
        receipt["status"] = SETTLED
        action = "skip"
    elif http_status == 402:
        # Credit exhausted. NOT BILLED. Whole part to secondary.
        action = "reroute_secondary"
        # committed released here; re-commit happens against the secondary
        # ledger at resubmission time. `lost` untouched.
    elif http_status == 429:
        # Rate limited. NOT BILLED, retryable. Never lost.
        action = "retry_backoff"
    elif http_status == 400:
        # Malformed. NOT BILLED. Re-prepare from the receipt, resubmit.
        action = "reprepare_resubmit"
        receipt["status"] = RESERVED
        receipt["http_status"] = None
    elif http_status in (504, None) or not response_complete:
        # Vendor gave up after accepting the bytes, or the stream truncated:
        # genuinely paid without a transcript. PAID_UNKNOWN, then lost.
        state["paid_unknown"] = True
        receipt["status"] = LOST
        action = "paid_unknown_then_lost"
    else:
        raise Refused(f"unhandled http_status {http_status}")

    for k, v in (extras or {}).items():
        if k in REQUIRED_RECEIPT_KEYS:
            raise Refused(f"extras may not overwrite receipt key {k}")
        receipt[k] = v
    atomic_write_json(os.path.join(unit_dir, "receipt.json"), receipt)
    # State follows the receipt on every terminal path: resume must see
    # settled/lost in state.json, not just in the receipt (live 2026-10-16:
    # settled units kept state=sent, a keep-loop skipped them, 2 transcripts
    # wiped and $2.69 re-billed).
    if action in ("skip", "paid_unknown_then_lost"):
        atomic_write_json(os.path.join(unit_dir, "state.json"),
                          {**state, "status": receipt["status"]})
    elif action == "reroute_secondary":
        atomic_write_json(os.path.join(unit_dir, "state.json"),
                          {**state, "status": RESERVED, "committed_usd": 0.0,
                           "rerouted_to_secondary": True})
    return receipt["status"], action


def recover(unit_dir):
    """Restart classifier. Returns (verdict, action)."""
    state_path = os.path.join(unit_dir, "state.json")
    receipt_path = os.path.join(unit_dir, "receipt.json")
    if not os.path.exists(state_path):
        return ("nothing_happened", "redo")
    state = read_json(state_path)
    if state.get("paid_unknown"):
        return (PAID_UNKNOWN, "operator_decides")
    if state["status"] == QUEUED:
        return (QUEUED, "replay_idempotent_no_commit")
    if not os.path.exists(receipt_path):
        # reserved state without a receipt is impossible via the API, but a
        # crash between the two writes must still resolve safe: no receipt
        # means no commit evidence, so redo from admission.
        return ("nothing_happened", "redo")
    receipt = read_json(receipt_path)
    validate_receipt(receipt)
    # Receipt wins on terminal states (md5 single-authority): a settled/lost
    # receipt skips even if state lags (state is updated on the same path,
    # but a crash between the two writes must still resolve safe).
    if receipt.get("status") in (SETTLED, LOST):
        return (receipt["status"], "skip")
    st, http, complete = receipt["status"], receipt.get("http_status"), receipt.get("response_complete")
    if st == RESERVED:
        return (RESERVED, "release_commit_rereserve_submit")
    if st == SETTLED or st == LOST:
        return (st, "skip")
    if st == SENT and http is None:
        return (PAID_UNKNOWN, "operator_decides")
    return (st, "operator_decides")


def unit_complete(part_statuses, assembled_exists):
    """A unit is complete when every part is settled/lost AND the note exists.
    Partial transcripts are never published as notes."""
    if not assembled_exists:
        return False
    return bool(part_statuses) and all(s in (SETTLED, LOST) for s in part_statuses)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

#!/usr/bin/env bash
# Scaled ENOSPC proof for the 4 GiB loopback cap (bead nhbplus-corpus-06k).
# Usage: proof-loopback.sh <img-mb> <fill-mb> <workdir>
# Proves the kernel mechanism at any scale: writes past the volume size fail
# fast with ENOSPC, nothing spills to the host fs, the mount recovers by
# deleting the filler (no remount). VM-scale recipe (3952 MiB img, mega-get
# exit 232) is pipeline/scripts/provision-loopback.sh.
set -u
IMG_MB="${1:?img size MiB}"; FILL_MB="${2:?fill size MiB}"; WD="${3:?workdir}"
IMG="$WD/cap-proof.img"; MNT="$WD/cap-proof-mnt"
rm -f "$IMG"; mkdir -p "$MNT"
dd if=/dev/zero of="$IMG" bs=1M count="$IMG_MB" status=none
mkfs.ext4 -q -F "$IMG"
mount -o loop "$IMG" "$MNT" || { echo "MOUNT-FAILED (need root/loop support)"; exit 2; }
echo "mounted: $(df -m "$MNT" | tail -1)"
set +e
dd if=/dev/zero of="$MNT/fill" bs=1M count="$FILL_MB" status=none 2>"$WD/dd.err"
DD_EXIT=$?
set -e
echo "dd-exit=$DD_EXIT (expect nonzero: No space left on device)"
tail -c 300 "$WD/dd.err"; echo
echo "after-fill: $(df -m "$MNT" | tail -1)"
rm -f "$MNT/fill"
echo "after-delete: $(df -m "$MNT" | tail -1)"
umount "$MNT"
echo "RECOVERED without remount"
rm -f "$IMG"
if [ "$DD_EXIT" -eq 0 ]; then echo "UNPROVEN: fill fit, use a bigger FILL_MB"; exit 1; fi
echo "ENOSPC-PROVEN img=${IMG_MB}MiB fill=${FILL_MB}MiB"

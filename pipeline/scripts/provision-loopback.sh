#!/usr/bin/env bash
# VM recipe: 4 GiB loopback cap + mega-get exit-232 proof (bead nhbplus-corpus-06k).
# Runs on the Azure VM (ext4, megacmd installed), NOT on the operator PC.
# W0-Cap reference: 3,936 MiB written into a 3,952 MiB volume -> mega-get
# exits 232 "Insufficient disk space" in 0 s, no host spill, recovers
# without a remount. Scaled mechanism proof: proof-loopback.sh (WSL, logged).
set -euo pipefail
IMG="${1:-$HOME/nhbplus-loop.img}"
MNT="${2:-$HOME/nhbplus-work}"
IMG_MB=4060   # ~3.96 GiB image; usable ~3,952 MiB after ext4 overhead
dd if=/dev/zero of="$IMG" bs=1M count="$IMG_MB" status=progress
mkfs.ext4 -q -F "$IMG"
mkdir -p "$MNT"
sudo mount -o loop "$IMG" "$MNT"
sudo chown "$(id -u):$(id -g)" "$MNT"
df -m "$MNT" | tail -1
echo "--- ENOSPC drill: fill to 3,936 MiB, then one more fetch must exit 232 ---"
dd if=/dev/zero of="$MNT/drill-fill" bs=1M count=3936 status=none || true
df -m "$MNT" | tail -1
echo "--- mount stays up for the whole run; NEVER unmount mid-run ---"
echo "LOOP_READY img=$IMG mnt=$MNT"

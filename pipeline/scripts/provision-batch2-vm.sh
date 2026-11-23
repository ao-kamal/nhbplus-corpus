#!/usr/bin/env bash
# Provision a fresh batch-2 VM. Run AFTER the operator commissions new Azure
# and `az login` succeeds with write access on the new subscription.
# Reads nothing from secrets files; SSH key path is the existing one.
set -euo pipefail

RG="nhbplus-batch2"
VM="nhbplus-batch2-vm"
LOC="austriaeast"          # same region as the first run (EU, worked)
SIZE="Standard_D2s_v5"     # 2 vCPU / 8 GB — the size proven on run #1
IMG="Canonical:ubuntu-24_04-lts:server:latest"
SSHKEY="$HOME/.ssh/nhbplus_azure_vm.pub"   # WSL path; override if needed

echo "=== preflight: write access ==="
az group create --name "$RG" --location "$LOC" 2>&1 | tail -2

echo "=== create VM ==="
az vm create \
  --resource-group "$RG" --name "$VM" --location "$LOC" \
  --image "$IMG" --size "$SIZE" --admin-username azureuser \
  --ssh-key-values "$SSHKEY" \
  --public-ip-sku Standard --no-wait 2>&1 | tail -5

echo "=== waiting for VM ==="
az vm wait --resource-group "$RG" --name "$VM" --created 2>&1 | tail -2

IP=$(az vm list-ip-addresses --resource-group "$RG" --name "$VM" \
      --query '[].virtualMachine.network.publicIpAddresses[].ipAddress' -o tsv)
echo "VM_IP=$IP"

echo "=== open SSH only ==="
az vm open-port --resource-group "$RG" --name "$VM" --port 22 --priority 100 2>&1 | tail -2

echo "=== verify reachability ==="
for i in 1 2 3 4 5; do
  if ssh -i "$HOME/.ssh/nhbplus_azure_vm" -o BatchMode=yes -o ConnectTimeout=10 \
      "azureuser@$IP" 'echo VM_READY; nproc; free -h | head -2; df -h / | tail -1' 2>/dev/null; then
    break
  fi
  echo "waiting for ssh ($i/5)..."
  sleep 20
done

echo "=== next steps on the VM (run via ssh) ==="
echo "1. apt install megacmd + pypdf"
echo "2. provision-loopback.sh (4 GiB, loopback)"
echo "3. restore keys from .env.private at use time"
echo "4. run bulk-run.py over batch-2 worklist"
echo "PROVISION_DONE ip=$IP"

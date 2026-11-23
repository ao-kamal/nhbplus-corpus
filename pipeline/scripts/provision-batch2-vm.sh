#!/usr/bin/env bash
# Provision batch-2 VM. Reads the SSH public key from the Windows-side file.
set -euo pipefail

RG="nhbplus-batch2"
VM="nhbplus-batch2-vm"
LOC="austriaeast"
SIZE="Standard_D2s_v5"

PUB=/mnt/c/Users/layiw/.ssh/nhbplus_azure_vm.pub
PRIV=/root/.ssh/nhbplus_azure_vm

echo "preflight: public key"
[ -f "$PUB" ] || { echo "MISSING $PUB"; exit 1; }
wc -c "$PUB"
head -c 40 "$PUB"; echo

echo "=== create resource group ==="
az group create --name "$RG" --location "$LOC" -o none

echo "=== create VM ==="
az vm create \
  --resource-group "$RG" --name "$VM" --location "$LOC" \
  --image Canonical:ubuntu-24_04-lts:server:latest \
  --size "$SIZE" --admin-username azureuser \
  --ssh-key-values "$(cat "$PUB")" \
  --public-ip-sku Standard --no-wait

echo "=== wait for VM ==="
az vm wait --resource-group "$RG" --name "$VM" --created

IP=$(az vm list-ip-addresses --resource-group "$RG" --name "$VM" \
      --query '[].virtualMachine.network.publicIpAddresses[].ipAddress' -o tsv)
echo "VM_IP=$IP"

echo "=== open SSH ==="
az vm open-port --resource-group "$RG" --name "$VM" --port 22 --priority 100 -o none

echo "=== verify SSH ==="
for i in 1 2 3 4 5 6; do
  if ssh -i "$PRIV" -o BatchMode=yes -o ConnectTimeout=10 \
      -o StrictHostKeyChecking=accept-new \
      "azureuser@$IP" 'echo VM_READY; nproc; free -h | head -2; df -h / | tail -1' 2>/dev/null; then
    echo "SSH_OK"
    break
  fi
  echo "waiting for ssh ($i/6)..."
  sleep 20
done
echo "PROVISION_DONE ip=$IP"

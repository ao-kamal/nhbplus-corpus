#!/usr/bin/env pwsh
# PROBE DRIVER - full handle sweep across every folder in the share.
# One dev-browser run per folder (its ~30s per-run budget cannot contain a
# recursive sweep). Resumable: existing results are skipped.
param([string]$OutDir = "")
$ErrorActionPreference = "Stop"
if (-not $OutDir) { $OutDir = Join-Path $PSScriptRoot "..\out" }
$OutDir = [System.IO.Path]::GetFullPath($OutDir)
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$seeds  = (Get-Content "$OutDir\seeds.txt" -Raw).Trim().Split(",")
$tpl    = Get-Content "$PSScriptRoot\mega-handle-template.js" -Raw
$result = @{}

foreach ($seed in $seeds) {
  $f = Join-Path $OutDir "handles-$seed.json"
  if (Test-Path $f) { Write-Host "  $seed : cached"; $result[$seed] = Get-Content $f -Raw | ConvertFrom-Json; continue }
  $js = $tpl.Replace("__H__", $seed)
  $tmp = Join-Path $env:TEMP "hs-$seed.js"
  [System.IO.File]::WriteAllText($tmp, $js, (New-Object System.Text.UTF8Encoding $false))
  $raw = & dev-browser run $tmp 2>&1 | Out-String
  $m = [regex]::Match($raw, "(?m)^JSON=(.*)$")
  if ($m.Success) {
    $rows = $m.Groups[1].Value | ConvertFrom-Json
    $rows | ConvertTo-Json -Depth 5 -Compress | Set-Content $f -Encoding utf8
    $result[$seed] = $rows
    Write-Host "  $seed : $($rows.Count) rows"
  } else {
    Write-Host "  $seed : NO JSON - recorded FAILED, not skipped"
    $result[$seed] = @()
  }
}
Write-Host "DONE"
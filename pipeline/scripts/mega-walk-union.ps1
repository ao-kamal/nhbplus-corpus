#!/usr/bin/env pwsh
# PROBE DRIVER - NOT PIPELINE CODE.
# Definitive census. Uses INCREMENTAL SCROLL-UNION because the MEGA grid is
# virtualised and un-mounts rows you scroll past: a single count measures a
# WINDOW. On 2025/Feb this technique found 66 rows where a single-shot count
# found 36 - 83% more.
#
# Usage: .\mega-walk-union.ps1 -Seeds <csv> -Tag union

param(
  [Parameter(Mandatory = $true)][string]$Seeds,
  [string]$Tag = "union",
  [string]$OutDir = ""
)
$ErrorActionPreference = "Stop"
if (-not $OutDir) { $OutDir = Join-Path $PSScriptRoot "..\out" }
$OutDir = [System.IO.Path]::GetFullPath($OutDir)
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$tpl = Get-Content "$PSScriptRoot\mega-walk-union-template.js" -Raw

$results = @()
foreach ($seed in ($Seeds -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ })) {
  $js = $tpl.Replace("__H__", $seed).Replace("__L__", "$Tag/$seed")
  $tmp = Join-Path $env:TEMP "union-$seed.js"
  [System.IO.File]::WriteAllText($tmp, $js, (New-Object System.Text.UTF8Encoding $false))

  $raw = & dev-browser run $tmp 2>&1 | Out-String
  $a = [regex]::Match($raw, "(?m)^ROWS_JSON=(.*)$")
  if (-not $a.Success) {
    Write-Host "   $seed : NO ROWS (paint failure) - recorded FAILED, not skipped"
    $results += [pscustomobject]@{ handle = $seed; count = -1; rows = @() }
    continue
  }
  try {
    $rows = $a.Groups[1].Value | ConvertFrom-Json
    $results += [pscustomobject]@{ handle = $seed; count = $rows.Count; rows = $rows }
    Write-Host "   $seed : $($rows.Count) rows"
  } catch {
    Write-Host "   $seed : PARSE FAILED"
    $results += [pscustomobject]@{ handle = $seed; count = -1; rows = @() }
  }
}
$results | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $OutDir "$Tag.json") -Encoding utf8
Write-Host ""
Write-Host "WROTE $Tag.json"
Write-Host ("TOTAL rows " + (($results | ForEach-Object { $_.count } | Measure-Object -Sum).Sum))
Write-Host ("FAILED folders " + (@($results | Where-Object { $_.count -lt 0 }).Count))
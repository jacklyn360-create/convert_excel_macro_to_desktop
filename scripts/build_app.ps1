$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

pyinstaller --name "ResponseTracker" --onefile --windowed main.py

Write-Host "Build complete. Output is in the dist folder."

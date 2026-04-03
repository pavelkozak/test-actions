# SSH key pair for GitHub Actions -> server deploy.
# Requires OpenSSH Client (Windows Settings -> Apps -> Optional features).
#
# Run:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
#   .\scripts\generate-ssh-deploy-key.ps1
#
# Key has no passphrase (-N "") for CI. For a passphrase, run ssh-keygen manually.

param(
    [string] $OutDir = (Join-Path $env:USERPROFILE ".ssh"),
    [string] $KeyName = "gha_deploy_vpe04",
    [string] $Comment = "github-actions-deploy"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command ssh-keygen -ErrorAction SilentlyContinue)) {
    Write-Error "ssh-keygen not found. Install OpenSSH Client (Windows optional feature)."
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$privatePath = Join-Path $OutDir $KeyName
$publicPath = "$privatePath.pub"

if ((Test-Path $privatePath) -or (Test-Path $publicPath)) {
    Write-Error "Files already exist: $privatePath or $publicPath. Remove them or use -KeyName."
}

# Empty passphrase: use cmd /c so -N "" is passed correctly (PowerShell drops empty -N args).
$commentEsc = $Comment -replace '"', "'"
$cmd = 'ssh-keygen -t ed25519 -C "' + $commentEsc + '" -f "' + $privatePath + '" -q -N ""'
$p = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $cmd -NoNewWindow -Wait -PassThru
if ($p.ExitCode -ne 0) {
    Write-Error "ssh-keygen exited with code $($p.ExitCode)"
}

Write-Host ""
Write-Host "Private key -> GitHub secret SSH_PRIVATE_KEY (entire file):" -ForegroundColor Yellow
Write-Host "  $privatePath"
Write-Host ""
Write-Host "Public key -> one line in server ~/.ssh/authorized_keys:" -ForegroundColor Green
Get-Content -Raw $publicPath | Write-Host -NoNewline
Write-Host ""
Write-Host ""
Write-Host "Copy public key to clipboard:" -ForegroundColor Cyan
Get-Content -Raw $publicPath | Set-Clipboard
Write-Host "  Done (if Set-Clipboard is available)."
Write-Host ""

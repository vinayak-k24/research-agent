$ErrorActionPreference = "Stop"

$SetupDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path (Join-Path $SetupDir "..")).Path
$VenvDir = Join-Path $ProjectRoot ".venv"
$EnvExamplePath = Join-Path $SetupDir ".env.example"
$EnvFilePath = Join-Path $ProjectRoot ".env"
$RequirementsPath = Join-Path $ProjectRoot "requirements.txt"

Set-Location $ProjectRoot

Write-Host "=== ManuscriptShield AI: Environment Setup ==="

# 1. Create virtual environment in the project root
if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating Python virtual environment at $VenvDir..."
    python -m venv $VenvDir
}

# 2. Activate virtual environment
. (Join-Path $VenvDir "Scripts\Activate.ps1")

# 3. Upgrade pip and install project dependencies
Write-Host "Installing dependencies from requirements.txt..."
python -m pip install --upgrade pip
python -m pip install -r $RequirementsPath

# 4. Initialize .env at the project root if missing
if (-not (Test-Path $EnvFilePath)) {
    Write-Host "Copying .env.example to $EnvFilePath..."
    Copy-Item $EnvExamplePath $EnvFilePath
    Write-Host "⚠️ Please update .env with your FOUNDRY_PROJECT_ENDPOINT!"
}

# 5. Check Azure CLI login
Write-Host "Checking Azure CLI authentication status..."
$azureOk = $false
try {
    az account show | Out-Null
    $azureOk = $true
} catch {
    $azureOk = $false
}

if ($azureOk) {
    Write-Host "✅ Azure CLI is authenticated."
} else {
    Write-Host "⚠️ Not logged in to Azure CLI. Please run 'az login' before proceeding."
}

Write-Host "=== Setup Completed Successfully ==="

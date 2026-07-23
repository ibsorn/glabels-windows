$ErrorActionPreference = 'Stop'

# The installer registers itself as "gLabels 4" (CPACK_PACKAGE_INSTALL_REGISTRY_KEY)
# with a DisplayName of "gLabels 4 Label Designer".
$key = Get-UninstallRegistryKey -SoftwareName 'gLabels 4*'

if (-not $key) {
    Write-Warning "gLabels does not appear to be installed; nothing to uninstall."
    return
}

if ($key.Count -gt 1) {
    Write-Warning "Found $($key.Count) matching installations; not guessing which to remove:"
    $key | ForEach-Object { Write-Warning "  $($_.DisplayName) - $($_.UninstallString)" }
    return
}

$packageArgs = @{
    packageName    = $env:ChocolateyPackageName
    fileType       = 'exe'
    file           = $key.UninstallString.Trim('"')
    # "_?=<dir>" makes the NSIS uninstaller run synchronously, so Chocolatey does
    # not report success while the uninstall is still in flight.
    silentArgs     = "/S _?=$(Split-Path $key.UninstallString.Trim('"'))"
    validExitCodes = @(0)
}

Uninstall-ChocolateyPackage @packageArgs

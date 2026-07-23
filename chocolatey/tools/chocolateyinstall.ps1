$ErrorActionPreference = 'Stop'

# 64-bit only: upstream is built for x64, and no 32-bit build is published.
if (-not (Get-OSArchitectureWidth 64)) {
    throw 'gLabels is only available as a 64-bit build. This machine is 32-bit.'
}

$packageArgs = @{
    packageName    = $env:ChocolateyPackageName
    fileType       = 'exe'
    url64bit       = 'https://github.com/ibsorn/glabels-windows/releases/download/win-3.99-master639/gLabels-3.99-master639-win64-setup.exe'
    checksum64     = '670B329289E21A468199262591342EDCAE24E0B8770912CCABA9160E8CC4CA3A'
    checksumType64 = 'sha256'

    # CPack's NSIS installer. "/S" is NSIS silent mode; the installer declares
    # RequestExecutionLevel admin, so it elevates on its own.
    silentArgs     = '/S'
    validExitCodes = @(0)

    # Matches the DisplayName written to the uninstall registry key, so that
    # Chocolatey's auto-uninstaller can find it later.
    softwareName   = 'gLabels 4*'
}

Install-ChocolateyPackage @packageArgs

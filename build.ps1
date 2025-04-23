# 
# Build latest dashboards as simhubdash archives
#

Set-PSDebug -Trace 0

$SettingsObject = Get-Content -Path settings.json | ConvertFrom-Json

If (!(test-path $SettingsObject.out))
{
    New-Item -ItemType Directory -Path $SettingsObject.out
}

Write-Host "Creating app for" $SettingsObject.name "-" $SettingsObject.version
$app = @{
    Path = $SettingsObject.bld
    CompressionLevel = "Fastest"
    DestinationPath = $SettingsObject.out + "\" `
    + $SettingsObject.name + "-" + $SettingsObject.version + ".zip"
}
Compress-Archive @app


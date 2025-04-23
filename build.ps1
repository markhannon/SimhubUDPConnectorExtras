# 
# Build latest dashboards as simhubdash archives
#

$SettingsObject = Get-Content -Path settings.json | ConvertFrom-Json

New-Item -ItemType Directory -Path $SettingsObject.out

foreach ($dashboard in $SettingsObject.dashboards)
{
    Write-Host "Creating SimHubDash for" $dashboard.name "-" $dashboard.version
    $simhubdash = @{
        Path = $SettingsObject.src + "\" + $dashboard.name
        CompressionLevel = "Fastest"
        DestinationPath = $SettingsObject.out + "\" `
        + $dashboard.name + "-" + $dashboard.version + ".simhubdash"
    }
    Compress-Archive @simhubdash
}

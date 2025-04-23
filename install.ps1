# 
# Install latests dashboards to simhub
#

$SettingsObject = Get-Content -Path settings.json | ConvertFrom-Json

Set-PSDebug -Trace 1

foreach ($item in $SettingsObject.dashboards)
{
    $src = $SettingsObject.src
    $dst = $SettingsObject.dst
    $dashboard = $item.name
    robocopy `
    $src\$dashboard `
    $dst\$dashboard `
    /xd "$src\$dashboard\_Backups" `
    /xd "$src\$dashboard\.git" `
    /xd "$src\$dashboard\.gitignore" `
    /mir
}
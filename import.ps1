# 
# Import latests dashboards from simhub
#

$SettingsObject = Get-Content -Path settings.json | ConvertFrom-Json

Set-PSDebug -Trace 1

foreach ($item in $SettingsObject.apps)
{
    $src = $SettingsObject.dst
    $dst = $SettingsObject.src
    $app = $item.name
    robocopy `
    $src\$app `
    $dst\$app `
    /xd "$src\$app\.git" `
    /xd "$src\$app\.gitignore" `
    /mir
}
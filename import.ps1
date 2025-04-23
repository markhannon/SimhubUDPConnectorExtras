# 
# Import latests apps from AC
#

Set-PSDebug -Trace 0

$SettingsObject = Get-Content -Path settings.json | ConvertFrom-Json

$src = $SettingsObject.dst
$dst = $SettingsObject.src
$app = $SettingsObject.name

robocopy `
$src\$app `
$dst\$app `
/xd $src\$app\.git `
/xd $src\$app\.gitignore `
/mir

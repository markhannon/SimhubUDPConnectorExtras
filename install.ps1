# 
# Install latests apps to AC
#

Set-PSDebug -Trace 0

$SettingsObject = Get-Content -Path settings.json | ConvertFrom-Json

$src = $SettingsObject.src
$dst = $SettingsObject.dst
$app = $SettingsObject.name

robocopy `
$src\$app `
$dst\$app `
/xd $src\$app\.git `
/xd $src\$app\.gitignore `
/mir
# If you work somewhere where the wallpaper for your desktop is set by a group policy, 
# feel free to use the powershell script below to remove the registry setting preventing
# you from changing your wallpaper

$path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\System\"
$value = "Wallpaper"

$registryKeyExists = (Get-ItemProperty $path).$value -ne $null
if ($registryKeyExists)
{
    Remove-ItemProperty -Path $path -Name $value
    Write-Host "Key $value Deleted"
}
else
{
    Write-Host "The value does not exist"
}

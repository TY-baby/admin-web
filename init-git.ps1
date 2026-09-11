$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$RemoteUrl = "git@github.com:TY-baby/admin-web.git"
$Branch = "my-project"
if (Test-Path ".git") { Write-Host "已存在 .git，跳过 init" -ForegroundColor Yellow }
else { git init; git checkout -b $Branch; git remote add origin $RemoteUrl }
git add -A
git commit -m "feat: 初始化 my-project（web-pc 官网 + web-front 推流后台 + web-back FastAPI）"
git push -u origin $Branch
Write-Host "推送完成，服务器拉取: git clone -b $Branch $RemoteUrl /www/my-project" -ForegroundColor Green
# Railway部署指南 v2 - 修復版

## 🚀 部署步驟

### 1. GitHub準備
1. 創建新的GitHub倉庫（公開）
2. 上傳本項目所有文件

### 2. Railway部署
1. 前往 https://railway.app
2. 登錄GitHub帳戶
3. 點擊 "New Project" → "Deploy from GitHub repo"
4. 選擇您的項目倉庫

### 3. 環境變數設置
在Railway項目變數中添加：
```
BOT_TOKEN = 您的Potato_Chat機器人Token
```

### 4. 自動部署
Railway將會：
- 自動檢測Python 3.11環境
- 安裝requirements_railway.txt依賴
- 啟動potato_bot.py

## 📋 配置文件說明

### 修復的問題
- ✅ 修正nixpacks.toml語法（使用正確的variables和phases配置）
- ✅ 恢復railway.json完整配置
- ✅ 確保NIXPACKS正確構建Python項目

### 核心配置文件
- `nixpacks.toml` - 構建器配置（已修復語法）
- `railway.json` - Railway平台配置
- `requirements_railway.txt` - 精簡依賴
- `Procfile` - 備用啟動命令

## 🔧 故障排除

**構建失敗？**
1. 檢查所有文件是否已上傳到GitHub
2. 確認nixpacks.toml語法正確
3. 查看Railway構建日誌

**部署成功但機器人無響應？**
1. 確認BOT_TOKEN環境變數正確
2. 檢查token是否有效
3. 確認機器人已添加到群組

## ✅ 預期結果
- Python 3.11環境自動配置
- 依賴自動安裝
- 機器人24小時運行
- 自動重啟機制
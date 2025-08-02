# Railway部署指南

## 快速部署步驟

### 1. 準備GitHub倉庫
1. 創建新的GitHub倉庫（公開）
2. 上傳本項目所有文件

### 2. Railway部署
1. 前往 https://railway.app
2. 使用GitHub帳戶登錄
3. 點擊 "New Project"
4. 選擇 "Deploy from GitHub repo"
5. 選擇您的項目倉庫

### 3. 配置環境變數
在Railway項目設置中添加：
- `BOT_TOKEN` = 您的Potato Chat機器人Token

### 4. 自動部署
Railway會自動：
- 檢測Python項目
- 安裝dependencies
- 啟動機器人

## 部署配置文件說明

- `railway.json` - Railway基本配置
- `nixpacks.toml` - NIXPACKS構建器配置
- `requirements_railway.txt` - Python依賴包
- `Procfile` - 啟動命令
- `runtime.txt` - Python版本指定

## 故障排除

**部署失敗？**
1. 檢查BOT_TOKEN環境變數是否正確設置
2. 確認所有文件都已上傳到GitHub
3. 查看Railway構建日誌獲取詳細錯誤信息

**機器人無響應？**
1. 確認BOT_TOKEN有效
2. 檢查機器人是否已添加到聊天群組
3. 查看Railway部署日誌
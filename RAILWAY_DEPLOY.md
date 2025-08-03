# Railway部署指南 - 終極版

## 🚀 終極版特色

### 相比前版本的重大升級
- ✅ 3個API數據源整合（IP-API + IPWhois + IPInfo）
- ✅ 專業級信息展示格式
- ✅ 智能IP評分系統（0-100分）
- ✅ 全面安全風險檢測
- ✅ 仿照專業網站的詳細展示

## 📋 部署步驟

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
- 啟動終極版potato_bot.py

## 🔧 配置文件說明

### 核心配置文件
- `nixpacks.toml` - 構建器配置（已修復語法）
- `railway.json` - Railway平台配置
- `requirements_railway.txt` - 精簡依賴
- `potato_bot.py` - 終極版主程序

### 新增功能需求
終極版需要的依賴包括：
```
pytelegrambotapi>=4.28.0
requests>=2.32.4
```

## 📊 終極版展示效果

### 專業信息展示格式
```
🌍 IP信息查詢

IP地址: 8.8.8.8
數字地址: 134744072
國家/地區: 美國

📍 位置信息
🥇 IP-API 美國 弗吉尼亞州 Ashburn Google LLC
🥈 IPWhois 美國 加利福尼亞州 Mountain View Google LLC
🥉 IPInfo 美國 加利福尼亞 Google LLC

🌐 網絡信息
ASN: AS15169 Google LLC
企業: Google Public DNS
時區: America/New_York
經緯度: 39.03, -77.5

🏷️ IP標籤: IPv4

📊 IP評分: 🟢 70/100 (滿分為100分，分數越高越好)

🛡️ IP情報
代理類型: ISP原生IP
VPN: 否
數據中心: 是
移動網絡: 否
風險因素: 數據中心
檢測時間: 2025-08-03 09:45:23

💰 當地貨幣: US Dollar ($)

📊 數據來源: IP-API + IPWhois + IPInfo
```

## 🛠️ 故障排除

**部署失敗？**
1. 檢查所有文件是否已上傳到GitHub
2. 確認BOT_TOKEN環境變數正確設置
3. 查看Railway構建日誌獲取詳細錯誤

**機器人無響應？**
1. 確認BOT_TOKEN有效且正確
2. 檢查機器人已添加到群組
3. 查看Railway運行日誌

**API查詢失敗？**
- 終極版有3個API容錯機制
- 即使1-2個API失敗，仍能正常工作
- 所有API均為免費服務，無需額外配置

## ✅ 預期結果

- 3個API數據源自動整合
- 專業級詳細信息展示
- 智能評分和風險檢測
- 24小時穩定運行
- 毫秒級響應速度

這是目前最先進的IP查詢機器人解決方案！
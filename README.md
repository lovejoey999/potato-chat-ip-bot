# Potato Chat IP地理位置查詢機器人 - 增強版

一個功能豐富的中文IP地理位置查詢機器人，支持Potato Chat平台，使用多個API數據源提供更準確詳細的IP地理位置信息查詢服務。

## 功能特色

- 🔍 **自動IP識別** - 無需命令，直接發送IP地址即可查詢
- 🌐 **IPv4/IPv6支持** - 支持所有IP地址格式
- 📊 **多API數據源** - IP-API.com + IPWhois.io 雙重保障
- 🛡️ **安全風險評估** - 代理、VPN、託管服務檢測
- 💰 **貨幣信息** - 顯示當地貨幣和匯率
- 🚀 **24小時運行** - 雲端部署，持續服務
- 🇨🇳 **中文界面** - 完全中文化用戶體驗

## 快速部署

### Railway部署（推薦）

1. 將項目上傳到GitHub
2. 在Railway中選擇GitHub倉庫
3. 添加環境變數 `BOT_TOKEN`
4. 自動部署完成

### 本地開發

```bash
pip install -r requirements_railway.txt
export BOT_TOKEN="你的機器人token"
python potato_bot.py
```

## 文件結構

```
├── potato_bot.py              # 主程序
├── requirements_railway.txt   # 部署依賴
├── railway.json              # Railway配置
├── nixpacks.toml             # 構建配置
├── Procfile                  # 啟動命令
├── setup.py                  # Python項目配置
└── README.md                 # 說明文檔
```

## 技術架構

- **Python 3.11** - 運行環境
- **pyTelegramBotAPI** - Telegram Bot框架
- **IP-API.com** - 主要IP地理位置查詢服務（中文支持）
- **IPWhois.io** - 備用API服務（詳細信息）
- **Railway** - 雲端部署平台

## API數據源

1. **IP-API.com** - 免費API，支持中文回應，45次/分鐘
2. **IPWhois.io** - 備用API，提供貨幣信息和國旗圖標
3. **自動容錯** - 一個API失敗時自動切換到備用API

## 使用方法

1. 添加機器人到Potato Chat群組
2. 直接發送IP地址（如：8.8.8.8）
3. 機器人自動回覆詳細地理位置信息

## 環境變數

- `BOT_TOKEN` - Potato Chat機器人Token（必需）

## 更新日誌

- v1.0.0 - 初始版本，支持IP地理位置查詢
- v1.1.0 - 增加IPv6支持和風險評估功能
- v2.0.0 - 多API數據源，增強版查詢功能，更詳細的信息顯示
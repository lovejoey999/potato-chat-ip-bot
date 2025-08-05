# 🌍 中文IP地理位置查詢機器人 (終極版V4.5)

一個功能豐富的中文Potato Chat IP查詢機器人，提供專業級即時IP地理位置信息查詢服務，採用12個API源多重驗證技術。

## ✨ 核心功能

- 🌍 **IPv4/IPv6全支持** - 完整支持所有IP地址格式
- 🔍 **12個API源驗證** - 多重數據源確保準確性
- 🏢 **詳細ISP信息** - 包含組織、ASN、網絡類型
- 🎯 **精確地理定位** - 國家、省份、城市完整信息
- 🛡️ **安全檢測** - 代理/VPN/數據中心/移動網絡識別
- 📊 **風險評分** - 智能IP風險評估(0-100分)
- 🌐 **完整中文化** - 所有地名和信息全中文顯示
- ⚡ **即時查詢** - 無需命令，直接發送IP即可查詢

## 🔗 API數據源 (12個)

### 主要數據源
- **IP-API** - 中文原生支持，主要數據源
- **Internet** (IPWhois) - 詳細ISP和網絡信息
- **Moe** (IPInfo) - 精確地理定位
- **Kiwi** (IPapi.co) - 免費高質量數據
- **Maxmind** (IPGeolocation) - 權威地理數據庫
- **Eassi** (FreeGeoIP) - 輔助驗證源

### 增強數據源
- **Moe+** - IPInfo增強版
- **Ease** - IPStack替代源
- **CZ88** - 中國IP數據庫
- **Leak** (IPLeak) - 專業檢測源
- **IP2Location** - 商用級數據庫
- **Digital Element** - 企業級定位服務

## 🚀 技術特點

- **多源驗證技術** - 12個API同時查詢確保數據準確性
- **智能故障轉移** - API失效時自動切換備用源
- **專業顯示格式** - 仿照專業IP查詢網站的藍標籤展示
- **完整中文本地化** - 200+地理位置名稱中文翻譯
- **IPv6全面支持** - 支持所有IPv6格式檢測和查詢
- **智能IP識別** - 自動識別私有IP、本地IP、公網IP
- **實時時間戳** - 每次查詢顯示準確查詢時間

## 🎯 使用方法

### 基本查詢
直接發送IP地址給機器人，無需任何命令：
```
8.8.8.8
2001:4860:4860::8888
114.114.114.114
```

### 批量查詢
一次最多可查詢5個IP地址：
```
8.8.8.8 1.1.1.1 114.114.114.114
```

### 命令支援
- `/start` - 歡迎信息和機器人介紹
- `/help` - 詳細使用說明

## 📋 系統要求

- Python 3.7+
- pyTelegramBotAPI 4.0+
- requests 庫
- Potato Chat Bot Token

## 🔧 安裝部署

### 本地運行
1. 克隆項目：
```bash
git clone https://github.com/your-username/potato-ip-bot.git
cd potato-ip-bot
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 設置環境變數：
```bash
export BOT_TOKEN="你的Potato_Chat_Bot_Token"
```

4. 運行機器人：
```bash
python potato_bot.py
```

### Railway雲端部署
使用本項目的Railway配置文件可一鍵部署：

1. Fork本項目到您的GitHub
2. 在Railway中連接GitHub倉庫
3. 設置環境變數 `BOT_TOKEN`
4. 自動部署並24/7運行

詳細部署說明請參考 `RAILWAY_DEPLOY.md`

## 🔍 查詢結果示例

```
🌍 IP信息查詢 - 終極版

IP地址: 8.8.8.8
數字地址: 134744072
IP類型: 📡 IPv4公網地址
查詢時間: 2025-08-05 19:35:42

🌎 基本信息
國家/地區: 🇺🇸 美國
省份/州: 加利福尼亞州
城市: 山景城
郵政編碼: 94043
時區: America/Los_Angeles
坐標: 37.4056,-122.0775

📍 12源位置對比
🔹 IP-API 美國 加利福尼亞州 山景城 Google LLC
🔹 Internet 美國 加利福尼亞州 山景城 Google LLC
🔹 Moe 美國 加利福尼亞州 山景城 Google LLC
🔹 Kiwi 美國 加利福尼亞州 山景城 Google LLC
🔹 Maxmind 美國 加利福尼亞州 山景城 Google LLC
🔹 Eassi 美國 加利福尼亞州 山景城 Google LLC
🔹 Moe+ 美國 加利福尼亞州 山景城 Google LLC
🔹 Ease 美國 加利福尼亞州 山景城 Google LLC
🔹 CZ88 美國 加利福尼亞州 山景城 Google LLC
🔹 Leak 美國 加利福尼亞州 山景城 Google LLC
🔹 IP2Location 美國 加利福尼亞州 山景城 Google LLC
🔹 Digital Element 美國 加利福尼亞州 山景城 Google LLC

🏢 ISP信息
運營商: Google LLC
組織: Google LLC
ASN: AS15169 Google LLC

🛡️ 安全檢測
代理檢測: ❌ 非代理
VPN檢測: ❌ 非VPN
數據中心: ✅ 數據中心IP
移動網絡: ❌ 非移動網絡

📊 IP風險評分: 15分 (低風險)
- 地理位置一致性: ✅ 100%
- ISP信譽度: ✅ 高
- 代理/VPN風險: ✅ 無
- 數據中心IP: ⚠️ 是
```

## 📊 項目統計

- **代碼行數**: 1000+ 行Python代碼
- **API整合**: 12個專業IP地理位置API
- **中文詞典**: 200+地理位置中文翻譯
- **功能支援**: IPv4/IPv6/批量查詢/安全檢測
- **部署平台**: Replit開發 + Railway生產

## 🔄 版本歷史

### V4.5 (2025-08-05) - 終極版
- ✅ 新增6個API源達到12源驗證
- ✅ 完整IPv6支持和識別
- ✅ 專業級中文本地化
- ✅ 修復API準確性問題

### V4.0 (2025-08-03) - 專業版
- ✅ 重構為專業IP查詢平台
- ✅ 6個API源多重驗證
- ✅ IP風險評分系統
- ✅ 安全檢測功能

### V3.0 (2025-08-02)
- ✅ 雙平台支持(Telegram + Potato Chat)
- ✅ IPv6支持
- ✅ 批量查詢功能

## 🤝 貢獻

歡迎提交Issue和Pull Request來改進這個項目！

## 📄 許可證

MIT License - 詳見 LICENSE 文件

## 📞 聯絡

如有問題或建議，請通過GitHub Issues聯絡我們。

---
**Made with ❤️ for Chinese IP lookup community**
# 🚀 Railway一鍵部署指南

## 快速部署步驟

### 1. 準備工作
1. 註冊Railway賬號: https://railway.app
2. 準備Potato Chat Bot Token
3. Fork本倉庫到你的GitHub

### 2. 連接Railway
1. 登錄Railway控制台
2. 點擊 "New Project"
3. 選擇 "Deploy from GitHub repo"
4. 授權並選擇你fork的倉庫

### 3. 配置環境變量
在Railway項目設置中添加：
```
BOT_TOKEN = 你的Potato_Chat_Bot_Token
```

### 4. 自動部署
- Railway會自動檢測Python項目
- 自動安裝requirements.txt中的依賴
- 自動運行Procfile中的啟動命令

### 5. 部署完成
- 查看Logs確認機器人啟動成功
- 在Potato Chat中測試機器人功能

## 🔧 配置文件說明

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python potato_bot.py"
  }
}
```

### Procfile
```
worker: python potato_bot.py
```

### requirements.txt
```
requests==2.31.0
```

### runtime.txt
```
python-3.11.0
```

## 📊 部署後檢查

### 1. 查看日誌
```
✅ 中文IP地理位置查詢機器人(終極版)正在啟動...
機器人連接成功：您的機器人名稱
機器人ID: 12345678
終極版機器人正在運行中，按 Ctrl+C 停止
```

### 2. 測試功能
發送測試IP：
- `8.8.8.8` (IPv4測試)
- `2001:4860:4860::8888` (IPv6測試)

預期回復：
```
🌍 IP信息查詢 - 終極版
...完整的查詢結果...
```

## 🛠️ 故障排除

### 常見問題

**1. 機器人無法啟動**
- 檢查BOT_TOKEN是否正確設置
- 確認Token格式無誤
- 查看Railway部署日誌

**2. 查詢無回應**
- 檢查API網絡連接
- 查看錯誤日誌
- 確認IP地址格式正確

**3. 部署失敗**
- 檢查requirements.txt格式
- 確認Python版本兼容
- 查看構建日誌詳情

### 日誌分析
```bash
# 正常啟動日誌
✅ 中文IP地理位置查詢機器人(終極版)正在啟動...
機器人連接成功：IPcheck2025
機器人ID: 10460052

# 查詢日誌
收到消息 - 用戶: 用戶名 (12345678)
檢測到的IP地址: ['8.8.8.8']
消息發送成功 - Message ID: 142501
成功查詢IP: 8.8.8.8

# 錯誤日誌
❌ 錯誤：未找到BOT_TOKEN環境變數！
API查詢失敗: Connection timeout
```

## 🔄 更新部署

### 自動更新
1. 推送代碼到GitHub倉庫
2. Railway自動檢測更改
3. 自動觸發重新部署
4. 零停機更新完成

### 手動重啟
1. 進入Railway項目控制台
2. 點擊 "Redeploy"
3. 等待部署完成

## 📈 監控和維護

### 性能監控
- CPU使用率：< 5%
- 內存使用：< 100MB
- 響應時間：1-3秒
- 在線時間：99.9%+

### 日常維護
- 定期查看日誌
- 監控API可用性
- 更新依賴版本
- 備份重要配置

---
**🎉 恭喜！你的專業級IP查詢機器人已成功部署到Railway！**
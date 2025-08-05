# Railway 部署指南

## 部署步驟

### 1. 創建Railway帳戶
- 前往 https://railway.app
- 使用GitHub帳戶註冊（推薦）
- 驗證電子郵件

### 2. 創建新項目
1. 點擊 "New Project"
2. 選擇 "Deploy from GitHub repo"
3. 連接您的GitHub帳戶
4. 選擇包含機器人代碼的倉庫

### 3. 配置環境變數
在Railway項目設置中添加：
```
BOT_TOKEN=您的Potato Chat機器人Token
```

### 4. 部署設置
Railway會自動檢測Python項目並使用：
- `requirements.txt` 安裝依賴
- `Procfile` 定義啟動命令
- `runtime.txt` 指定Python版本

### 5. 監控和日誌
- 在Railway控制面板查看部署狀態
- 查看實時日誌監控機器人運行
- 設置警報通知

## 費用說明
- 免費計劃：每月$5額度
- 您的機器人預計月消費：$1-3
- 超額後會暫停，下月自動恢復

## 優勢
✓ 24/7持續運行
✓ 自動重啟故障恢復
✓ 實時日誌監控
✓ 簡單的GitHub集成
✓ 免費額度充足

## 替代方案
如果Railway免費額度不夠，可考慮：
- Render（免費但會休眠）
- Fly.io（免費額度）
- VPS服務（$5/月起）
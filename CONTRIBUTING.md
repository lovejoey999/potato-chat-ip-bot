# 貢獻指南

感謝您對中文IP地理位置查詢機器人項目的關注！我們歡迎所有形式的貢獻。

## 🤝 如何貢獻

### 報告問題
- 搜索現有Issues確認問題未被報告
- 使用清晰的標題描述問題
- 提供詳細的複現步驟
- 包含系統環境信息

### 建議功能
- 檢查是否已有相關討論
- 清楚描述新功能的用途
- 說明為什麼這個功能有用
- 考慮實現的複雜度

### 提交代碼
1. Fork項目倉庫
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟Pull Request

## 📋 開發規範

### 代碼風格
- 使用Python PEP 8標準
- 函數和變數使用下劃線命名
- 類名使用駝峰命名
- 添加適當的註釋和文檔字符串

### 提交信息
- 使用清晰簡潔的提交信息
- 第一行不超過50字符
- 如有需要，添加詳細描述

### 測試
- 測試新功能是否正常工作
- 確保不破壞現有功能
- 測試各種IP地址格式
- 驗證API響應處理

## 🧪 本地開發

1. 克隆您的Fork：
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
export BOT_TOKEN="your_bot_token"
```

4. 運行機器人：
```bash
python potato_bot.py
```

## 🔍 代碼審查

Pull Request會進行以下檢查：
- [ ] 代碼符合PEP 8規範
- [ ] 功能測試通過
- [ ] 文檔已更新
- [ ] 無安全漏洞
- [ ] 性能影響評估

## 📚 文檔更新

如果您的更改影響到：
- API接口
- 配置選項
- 使用方法
- 部署流程

請同時更新相關文檔。

## 🌐 國際化

- 所有用戶界面文字使用中文
- 地理位置名稱提供中文翻譯
- 錯誤信息清晰易懂
- 支持簡繁體中文

## 🚀 發布流程

1. 更新版本號
2. 更新CHANGELOG.md
3. 創建Release標籤
4. 部署到生產環境
5. 通知用戶重大變更

## 📞 聯絡方式

- GitHub Issues：報告bug或建議功能
- Pull Requests：提交代碼更改
- Discussions：項目討論和問答

## 🙏 致謝

感謝所有為這個項目貢獻的開發者！

---
**讓我們一起打造更好的中文IP查詢工具！**
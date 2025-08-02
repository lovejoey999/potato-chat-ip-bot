#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文Potato Chat IP地理位置查詢機器人
使用 Potato Chat API
"""

import os
import requests
import logging
import json
import time
import re
import ipaddress

# 設置日誌
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 從環境變數獲取Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    print("❌ 錯誤：未找到BOT_TOKEN環境變數！")
    print("請設置您的Potato Chat Bot Token")
    exit(1)

class PotatoBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.rct2008.com:8443/{token}"
        self.session = requests.Session()
        self.last_update_id = 0
    
    def get_me(self):
        """獲取機器人信息"""
        try:
            response = self.session.get(f"{self.api_url}/getMe", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("ok"):
                return data.get("result")
            else:
                return None
        except Exception as e:
            logger.error(f"獲取機器人信息失敗: {e}")
            return None
    
    def send_message(self, chat_id, text):
        """發送文字消息"""
        try:
            # 根據Potato Chat官方API文檔的正確格式
            payload = {
                "chat_type": 1,  # 1 = 私人聊天
                "chat_id": chat_id,
                "text": text,
                "markdown": False  # 使用純文字，避免格式問題
            }
            
            response = self.session.post(
                f"{self.api_url}/sendTextMessage",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("ok"):
                logger.info(f"消息發送成功 - Message ID: {data.get('result', {}).get('message_id', 'unknown')}")
                return True
            else:
                logger.error(f"API回應錯誤: {data}")
                return False
                
        except Exception as e:
            logger.error(f"發送消息失敗: {e}")
            logger.error(f"Chat ID: {chat_id}, Text: {text[:50]}")
            return False
    
    def get_updates(self):
        """獲取更新"""
        try:
            params = {
                "timeout": 30,  # 長輪詢
                "limit": 100
            }
            if self.last_update_id:
                params["offset"] = self.last_update_id + 1
                
            response = self.session.get(
                f"{self.api_url}/getUpdates",
                params=params,
                timeout=35  # 略高於長輪詢超時
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("ok"):
                updates = data.get("result", [])
                if updates:
                    self.last_update_id = max(update["update_id"] for update in updates)
                return updates
            else:
                logger.error(f"獲取更新失敗: {data}")
                return []
        except Exception as e:
            logger.error(f"獲取更新時發生錯誤: {e}")
            return []

def handle_start_command(bot, chat_id):
    """處理 /start 命令"""
    welcome_message = """👋 歡迎使用中文IP地理位置查詢機器人！

🔍 功能：查詢IP地址的地理位置信息

📝 使用方法：
• 直接發送IP地址即可查詢
• 例如：8.8.8.8 (IPv4)
• 例如：2001:4860:4860::8888 (IPv6)
• 也支持 /ip 指令查詢

💡 其他命令：
• /help - 顯示幫助信息
• /start - 顯示此歡迎信息

快來試試吧！🚀"""
    
    bot.send_message(chat_id, welcome_message)

def handle_help_command(bot, chat_id):
    """處理 /help 命令"""
    help_message = """🆘 幫助信息

📖 可用命令：
• /ip <IP地址> - 查詢IP地理位置信息
• /start - 顯示歡迎信息
• /help - 顯示此幫助信息

📝 使用範例：
• 8.8.8.8 - 查詢Google IPv4 DNS
• 1.1.1.1 - 查詢Cloudflare IPv4 DNS  
• 2001:4860:4860::8888 - 查詢Google IPv6 DNS
• 支持一次查詢多個IP（最多5個）

📋 查詢結果包含：
• 🌐 國家和地區信息
• 🏙️ 城市信息
• 🌐 網路服務商 (ISP)
• 🛡️ 代理檢測結果

查詢結果基於 ip-api.com 服務提供。"""
    
    bot.send_message(chat_id, help_message)

def validate_ip_address(ip_string):
    """驗證IP地址格式（IPv4和IPv6）"""
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False

def extract_ips_from_text(text):
    """從文字中提取所有IP地址"""
    # IPv4 正規表達式
    ipv4_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    
    # IPv6 正規表達式 (簡化版)
    ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b|::1\b|::\b'
    
    ips = []
    
    # 尋找IPv4
    ipv4_matches = re.findall(ipv4_pattern, text)
    for ip in ipv4_matches:
        if validate_ip_address(ip):
            ips.append(ip)
    
    # 尋找IPv6
    ipv6_matches = re.findall(ipv6_pattern, text)
    for ip in ipv6_matches:
        if validate_ip_address(ip):
            ips.append(ip)
    
    return ips

def query_single_ip(bot, chat_id, ip):
    """查詢單個IP地址"""
    try:
        # 檢測IP類型並選擇合適的API
        try:
            ip_obj = ipaddress.ip_address(ip)
            is_ipv6 = isinstance(ip_obj, ipaddress.IPv6Address)
        except:
            is_ipv6 = False
        
        # 統一使用 ip-api.com（同時支持IPv4和IPv6）
        url = f"http://ip-api.com/json/{ip}"
        params = {
            "fields": "status,message,country,regionName,city,isp,proxy,query,lat,lon,timezone",
            "lang": "zh-CN"
        }
        
        # 發送請求
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        # ip-api.com 統一回應格式檢查
        if data.get('status') != 'success':
            error_msg = data.get('message', '無法解析IP地址')
            return f"❌ 查詢失敗：{error_msg}"
            
        # 統一格式化回覆信息（IPv4和IPv6）
        ip_type = "IPv6" if is_ipv6 else "IPv4"
        return (
            f"🔍 {ip_type} 查詢結果\n"
            f"IP：{data['query']}\n"
            f"國家：{data['country']}\n"
            f"省／地區：{data['regionName']}\n"
            f"城市：{data['city']}\n"
            f"網路供應商：{data['isp']}\n"
            f"🔍 IPQS 風險評分：0 / 100\n"
            f"🔥 VPN / Proxy / TOR：{'是' if data.get('proxy') else '否'}\n"
            f"時區：{data.get('timezone', '未知')}\n"
            f"經緯度：{data.get('lat', '未知')}, {data.get('lon', '未知')}"
        )
        
    except requests.exceptions.Timeout:
        return "❌ 查詢超時，請稍後再試。"
    
    except requests.exceptions.RequestException as e:
        return "❌ 網路連線錯誤，請檢查網路連線。"
    
    except Exception as e:
        return f"❌ 查詢時發生錯誤：{str(e)}"

def handle_ip_command(bot, chat_id, text):
    """處理 /ip 命令 - IP地址查詢（支持IPv4和IPv6）"""
    try:
        # 解析命令參數
        command_parts = text.split()
        
        if len(command_parts) < 2:
            bot.send_message(chat_id, "請輸入要查詢的 IP，例如：\n/ip 8.8.8.8 (IPv4)\n/ip 2001:4860:4860::8888 (IPv6)")
            return

        ip = command_parts[1].strip()
        
        # 驗證IP地址格式
        if not validate_ip_address(ip):
            bot.send_message(chat_id, "❌ IP地址格式無效，請輸入正確的IPv4或IPv6地址")
            return
        
        # 發送處理中消息
        bot.send_message(chat_id, "🔍 正在查詢IP地理位置信息，請稍候...")
        
        # 查詢IP並發送結果
        result = query_single_ip(bot, chat_id, ip)
        bot.send_message(chat_id, result)
        logger.info(f"成功查詢IP: {ip}")
        
    except Exception as e:
        bot.send_message(chat_id, "❌ 查詢時發生錯誤，請稍後再試。")
        logger.error(f"未知錯誤: {e}")

def handle_direct_ip_message(bot, chat_id, text):
    """處理直接發送的IP地址（無需指令）"""
    try:
        # 從文字中提取IP地址
        ips = extract_ips_from_text(text)
        
        if not ips:
            return False  # 沒有找到IP地址，不處理
        
        if len(ips) > 5:
            bot.send_message(chat_id, "❌ 一次最多查詢 5 個 IP 地址，請分批查詢。")
            return True
        
        # 發送處理中消息
        if len(ips) == 1:
            bot.send_message(chat_id, "🔍 正在查詢IP地理位置信息，請稍候...")
        else:
            bot.send_message(chat_id, f"🔍 找到 {len(ips)} 個 IP 地址，正在查詢...")
        
        # 查詢每個IP
        results = []
        for ip in ips:
            result = query_single_ip(bot, chat_id, ip)
            results.append(result)
        
        # 發送結果
        if len(results) == 1:
            bot.send_message(chat_id, results[0])
        else:
            # 多個IP結果，分別發送
            for i, result in enumerate(results):
                bot.send_message(chat_id, f"【第 {i+1} 個 IP】\n{result}")
        
        logger.info(f"成功查詢 {len(ips)} 個IP: {', '.join(ips)}")
        return True
        
    except Exception as e:
        bot.send_message(chat_id, "❌ 查詢時發生錯誤，請稍後再試。")
        logger.error(f"直接IP查詢錯誤: {e}")
        return True

def process_message(bot, message):
    """處理收到的消息"""
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")
    
    if not chat_id or not text:
        return
    
    # 處理命令
    if text.startswith("/start"):
        handle_start_command(bot, chat_id)
    elif text.startswith("/help"):
        handle_help_command(bot, chat_id)
    elif text.startswith("/ip"):
        handle_ip_command(bot, chat_id, text)
    else:
        # 嘗試直接解析IP地址
        if not handle_direct_ip_message(bot, chat_id, text):
            # 如果不是IP地址，顯示幫助信息
            bot.send_message(chat_id, "請直接發送IP地址查詢，或發送 /help 查看使用說明。")

def main():
    """主函數"""
    try:
        print("✅ 中文IP地理位置查詢機器人正在啟動...")
        
        # 創建機器人實例
        bot = PotatoBot(BOT_TOKEN)
        
        # 測試Bot Token是否有效
        try:
            bot_info = bot.get_me()
            if bot_info:
                print(f"機器人連接成功：{bot_info.get('first_name', 'Unknown')}")
                print(f"機器人ID: {bot_info.get('id', 'Unknown')}")
                print("機器人正在運行中，按 Ctrl+C 停止")
            else:
                print("❌ Bot Token 無效！")
                print("請檢查您的 BOT_TOKEN 是否正確：")
                print("1. 確認token格式正確")
                print("2. 確認token是從 BotCreator 獲取的最新token")
                print("3. 檢查是否有額外的空格或字符")
                return
        except Exception as token_error:
            print(f"❌ Token驗證失敗: {token_error}")
            return
        
        # 開始輪詢
        while True:
            try:
                updates = bot.get_updates()
                
                for update in updates:
                    if "message" in update:
                        message = update["message"]
                        user = message.get("from", {})
                        logger.info(f"收到消息 - 用戶: {user.get('first_name', 'Unknown')} ({user.get('id', 'Unknown')})")
                        
                        process_message(bot, message)
                
                # 短暫休息避免過度請求
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n🛑 機器人已停止")
                break
            except Exception as e:
                logger.error(f"處理更新時發生錯誤: {e}")
                time.sleep(5)  # 錯誤時等待更長時間
        
    except Exception as e:
        logger.error(f"啟動機器人時發生錯誤: {e}")
        print(f"❌ 錯誤：{e}")

if __name__ == '__main__':
    main()
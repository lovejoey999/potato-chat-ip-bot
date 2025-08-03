#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文IP地理位置查詢機器人 - 增強版
支持多個API源，更詳細的IP信息查詢
"""

import os
import re
import requests
import telebot
from telebot import types
import time
import json

# 初始化機器人
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ 錯誤：請設置環境變數 BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

class IPLookupService:
    """IP查詢服務類 - 支持多個API源"""
    
    def __init__(self):
        self.apis = [
            {
                'name': 'IP-API (中文)',
                'url': 'http://ip-api.com/json/{ip}?lang=zh-CN&fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query,proxy,hosting',
                'parser': self._parse_ipapi
            },
            {
                'name': 'IPWhois.io',
                'url': 'https://ipwhois.app/json/{ip}',
                'parser': self._parse_ipwhois
            }
        ]
    
    def _parse_ipapi(self, data):
        """解析IP-API.com回應"""
        if data.get('status') != 'success':
            return None
            
        return {
            'ip': data.get('query', ''),
            'country': data.get('country', '未知'),
            'region': data.get('regionName', '未知'),
            'city': data.get('city', '未知'),
            'isp': data.get('isp', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone', '未知'),
            'latitude': data.get('lat', 0),
            'longitude': data.get('lon', 0),
            'zip_code': data.get('zip', '未知'),
            'as_info': data.get('as', '未知'),
            'proxy': '是' if data.get('proxy', False) else '否',
            'hosting': '是' if data.get('hosting', False) else '否',
            'api_source': 'IP-API.com'
        }
    
    def _parse_ipwhois(self, data):
        """解析IPWhois.io回應"""
        if not data.get('success', False):
            return None
            
        return {
            'ip': data.get('ip', ''),
            'country': data.get('country', '未知'),
            'region': data.get('region', '未知'),
            'city': data.get('city', '未知'),
            'isp': data.get('isp', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone_name', '未知'),
            'latitude': data.get('latitude', 0),
            'longitude': data.get('longitude', 0),
            'zip_code': '未知',
            'as_info': data.get('asn', '未知'),
            'currency': f"{data.get('currency', '未知')} ({data.get('currency_code', 'N/A')})",
            'flag_url': data.get('country_flag', ''),
            'api_source': 'IPWhois.io'
        }
    
    def lookup_ip(self, ip_address):
        """查詢IP地址信息"""
        for api in self.apis:
            try:
                url = api['url'].format(ip=ip_address)
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    result = api['parser'](data)
                    if result:
                        return result
                        
            except Exception as e:
                print(f"API {api['name']} 查詢失敗: {e}")
                continue
        
        return None

# 初始化IP查詢服務
ip_service = IPLookupService()

def is_valid_ip(ip):
    """驗證IP地址格式（IPv4和IPv6）"""
    # IPv4 正則
    ipv4_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    # IPv6 正則（簡化版）
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,7}:$|^([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}$|^([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}$|^([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}$|^([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}$|^[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})$|^:((:[0-9a-fA-F]{1,4}){1,7}|:)$'
    
    return bool(re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip))

def extract_ips_from_text(text):
    """從文字中提取IP地址"""
    # 支援IPv4和IPv6
    ipv4_pattern = r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    ipv6_pattern = r'\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b([0-9a-fA-F]{1,4}:){1,7}:\b'
    
    ipv4_matches = re.findall(ipv4_pattern, text)
    ipv6_matches = re.findall(ipv6_pattern, text)
    
    ips = []
    for match in ipv4_matches:
        if isinstance(match, tuple):
            ips.append(''.join(match))
        else:
            ips.append(match)
    
    for match in ipv6_matches:
        if isinstance(match, tuple):
            ip = ''.join(match)
        else:
            ip = match
        if ip not in ips:
            ips.append(ip)
    
    return ips[:5]  # 最多處理5個IP

def format_ip_info(ip_info):
    """格式化IP信息為中文輸出"""
    if not ip_info:
        return "❌ 無法獲取IP地址信息"
    
    # 基本信息
    result = f"🌍 **IP地址查詢結果**\n\n"
    result += f"🔍 **IP地址**: `{ip_info['ip']}`\n"
    result += f"🏴 **國家**: {ip_info['country']}\n"
    result += f"📍 **地區**: {ip_info['region']}\n"
    result += f"🏙️ **城市**: {ip_info['city']}\n"
    result += f"🌐 **ISP供應商**: {ip_info['isp']}\n"
    result += f"🏢 **組織**: {ip_info['org']}\n"
    result += f"🕐 **時區**: {ip_info['timezone']}\n"
    result += f"📍 **經緯度**: {ip_info['latitude']}, {ip_info['longitude']}\n"
    
    # 郵遞區號（如果有）
    if ip_info.get('zip_code') and ip_info['zip_code'] != '未知':
        result += f"📮 **郵遞區號**: {ip_info['zip_code']}\n"
    
    # AS信息
    if ip_info.get('as_info') and ip_info['as_info'] != '未知':
        result += f"🔗 **AS信息**: {ip_info['as_info']}\n"
    
    # 安全信息
    result += f"\n🛡️ **安全檢測**\n"
    if 'proxy' in ip_info:
        result += f"🔒 **代理服務器**: {ip_info['proxy']}\n"
    if 'hosting' in ip_info:
        result += f"☁️ **託管服務**: {ip_info['hosting']}\n"
    
    # 貨幣信息（IPWhois提供）
    if ip_info.get('currency'):
        result += f"💰 **當地貨幣**: {ip_info['currency']}\n"
    
    # API來源
    result += f"\n📊 **數據來源**: {ip_info['api_source']}"
    
    return result

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """歡迎訊息"""
    welcome_text = """
🤖 **中文IP地理位置查詢機器人** (增強版)

✨ **功能特色**:
• 🔍 自動識別IP地址 (IPv4/IPv6)
• 🌍 詳細地理位置信息
• 🛡️ 安全風險評估  
• 📊 多API數據源
• 🚀 快速回應

📝 **使用方法**:
直接發送IP地址即可，無需任何命令！

例如: `8.8.8.8` 或 `2001:4860:4860::8888`

支持批量查詢（最多5個IP）

輸入 /help 獲取更多說明
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    """幫助訊息"""
    help_text = """
📖 **詳細使用說明**

🔍 **IP查詢功能**:
• 支持IPv4: `192.168.1.1`
• 支持IPv6: `2001:4860:4860::8888`
• 批量查詢: 一條訊息可包含多個IP

📊 **查詢信息包括**:
• 🏴 國家、地區、城市
• 🌐 ISP供應商和組織信息
• 🕐 時區和經緯度
• 🛡️ 代理和託管檢測
• 💰 當地貨幣信息

🌟 **增強功能**:
• 多API數據源確保準確性
• 中文本地化顯示
• 智能文本IP提取
• 快速響應時間

如有問題請聯繫管理員
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """處理所有訊息，自動檢測IP地址"""
    text = message.text.strip()
    
    # 提取訊息中的IP地址
    ips = extract_ips_from_text(text)
    
    if not ips:
        bot.reply_to(message, 
                    "❌ 未檢測到有效的IP地址\n\n"
                    "請發送有效的IP地址，例如:\n"
                    "• `8.8.8.8`（IPv4）\n"
                    "• `2001:4860:4860::8888`（IPv6）\n\n"
                    "輸入 /help 獲取更多說明",
                    parse_mode='Markdown')
        return
    
    # 處理找到的IP地址
    bot.send_chat_action(message.chat.id, 'typing')
    
    for i, ip in enumerate(ips):
        try:
            ip_info = ip_service.lookup_ip(ip)
            
            if ip_info:
                response = format_ip_info(ip_info)
                bot.reply_to(message, response, parse_mode='Markdown')
            else:
                bot.reply_to(message, 
                           f"❌ 無法查詢IP地址 `{ip}` 的信息\n"
                           f"可能原因:\n"
                           f"• IP地址格式錯誤\n"
                           f"• 私有或保留IP地址\n"
                           f"• API服務暫時不可用",
                           parse_mode='Markdown')
            
            # 避免頻繁請求
            if i < len(ips) - 1:
                time.sleep(1)
                
        except Exception as e:
            print(f"處理IP {ip} 時發生錯誤: {e}")
            bot.reply_to(message, f"❌ 處理IP地址 `{ip}` 時發生錯誤", parse_mode='Markdown')

def main():
    """主程序"""
    try:
        print("✅ 中文IP地理位置查詢機器人正在啟動...")
        
        # 測試Bot Token
        bot_info = bot.get_me()
        print(f"機器人連接成功：{bot_info.first_name}")
        print(f"機器人ID: {bot_info.id}")
        
        print("機器人正在運行中，按 Ctrl+C 停止")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
        
    except Exception as e:
        if "401" in str(e) or "Unauthorized" in str(e):
            print("❌ Bot Token 無效！")
            print("請檢查您的 BOT_TOKEN 是否正確：")
            print("1. 確認token格式正確（例如：123456789:ABCdefGHIjklMNOpqrsTUVwxyz）")
            print("2. 確認token是從 @BotFather 獲取的最新token")
            print("3. 檢查是否有額外的空格或字符")
        else:
            print(f"❌ 機器人啟動失敗: {e}")

if __name__ == '__main__':
    main()
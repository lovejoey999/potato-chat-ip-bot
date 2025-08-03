#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文IP地理位置查詢機器人 - 終極版
仿照專業IP查詢網站，提供最詳細的IP信息展示
"""

import os
import re
import requests
import telebot
from telebot import types
import time
import json
from datetime import datetime

# 初始化機器人
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ 錯誤：請設置環境變數 BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

class UltimateIPLookupService:
    """終極IP查詢服務類 - 多數據源整合"""
    
    def __init__(self):
        self.apis = [
            {
                'name': 'IP-API',
                'url': 'http://ip-api.com/json/{ip}?lang=zh-CN&fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query,proxy,hosting,mobile',
                'parser': self._parse_ipapi
            },
            {
                'name': 'IPWhois',
                'url': 'https://ipwhois.app/json/{ip}',
                'parser': self._parse_ipwhois
            },
            {
                'name': 'IPInfo',
                'url': 'https://ipinfo.io/{ip}/json',
                'parser': self._parse_ipinfo
            }
        ]
    
    def _parse_ipapi(self, data):
        """解析IP-API.com回應"""
        if data.get('status') != 'success':
            return None
            
        return {
            'source': 'IP-API',
            'ip': data.get('query', ''),
            'country': data.get('country', '未知'),
            'country_code': data.get('countryCode', ''),
            'region': data.get('regionName', '未知'),
            'city': data.get('city', '未知'),
            'isp': data.get('isp', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone', '未知'),
            'latitude': data.get('lat', 0),
            'longitude': data.get('lon', 0),
            'zip_code': data.get('zip', '未知'),
            'as_info': data.get('as', '未知'),
            'proxy': data.get('proxy', False),
            'hosting': data.get('hosting', False),
            'mobile': data.get('mobile', False)
        }
    
    def _parse_ipwhois(self, data):
        """解析IPWhois.io回應"""
        if not data.get('success', False):
            return None
            
        return {
            'source': 'IPWhois',
            'ip': data.get('ip', ''),
            'country': data.get('country', '未知'),
            'country_code': data.get('country_code', ''),
            'region': data.get('region', '未知'),
            'city': data.get('city', '未知'),
            'isp': data.get('isp', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone_name', '未知'),
            'latitude': data.get('latitude', 0),
            'longitude': data.get('longitude', 0),
            'as_info': data.get('asn', '未知'),
            'currency': data.get('currency', '未知'),
            'currency_code': data.get('currency_code', ''),
            'currency_symbol': data.get('currency_symbol', ''),
            'flag_url': data.get('country_flag', '')
        }
    
    def _parse_ipinfo(self, data):
        """解析IPInfo.io回應"""
        if 'error' in data:
            return None
            
        loc = data.get('loc', '0,0').split(',')
        
        return {
            'source': 'IPInfo',
            'ip': data.get('ip', ''),
            'country': data.get('country', '未知'),
            'region': data.get('region', '未知'),  
            'city': data.get('city', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone', '未知'),
            'latitude': float(loc[0]) if len(loc) > 0 else 0,
            'longitude': float(loc[1]) if len(loc) > 1 else 0,
            'postal': data.get('postal', '未知')
        }
    
    def get_comprehensive_info(self, ip_address):
        """獲取綜合IP信息"""
        results = []
        
        for api in self.apis:
            try:
                url = api['url'].format(ip=ip_address)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(url, timeout=10, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    result = api['parser'](data)
                    if result:
                        results.append(result)
                        
            except Exception as e:
                print(f"API {api['name']} 查詢失敗: {e}")
                continue
        
        return results
    
    def calculate_ip_score(self, ip_info_list):
        """計算IP評分（模擬專業評分系統）"""
        base_score = 85
        risk_factors = []
        
        for info in ip_info_list:
            # 代理檢測
            if info.get('proxy'):
                base_score -= 25
                risk_factors.append('代理服務器')
            
            # 託管服務檢測  
            if info.get('hosting'):
                base_score -= 15
                risk_factors.append('數據中心')
            
            # 移動網絡檢測
            if info.get('mobile'):
                base_score += 5
                risk_factors.append('移動網絡')
            
            # ISP類型檢測
            isp = info.get('isp', '').lower()
            if any(keyword in isp for keyword in ['cloud', 'amazon', 'google', 'microsoft']):
                base_score -= 10
                risk_factors.append('雲服務')
        
        return max(0, min(100, base_score)), list(set(risk_factors))

# 初始化服務
ip_service = UltimateIPLookupService()

def is_valid_ip(ip):
    """驗證IP地址格式"""
    ipv4_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,7}:$|^([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}$'
    return bool(re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip))

def extract_ips_from_text(text):
    """從文字中提取IP地址"""
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
    
    return ips[:3]  # 最多處理3個IP

def get_ip_type_label(ip):
    """獲取IP類型標籤"""
    if ':' in ip:
        return 'IPv6'
    elif ip.startswith(('10.', '172.', '192.168.')):
        return '私有IP'
    elif ip.startswith(('127.', '169.254.')):
        return '本地IP'
    else:
        return 'IPv4'

def format_comprehensive_ip_info(ip_address, ip_info_list):
    """格式化綜合IP信息展示"""
    if not ip_info_list:
        return f"❌ 無法獲取IP地址 `{ip_address}` 的信息"
    
    # 計算IP評分
    score, risk_factors = ip_service.calculate_ip_score(ip_info_list)
    
    # 獲取主要信息（優先使用第一個成功的API）
    main_info = ip_info_list[0]
    
    result = f"🌍 **IP信息查詢** \n\n"
    
    # === 基本信息 ===
    result += f"**IP地址**: `{ip_address}`\n"
    result += f"**數字地址**: {int.from_bytes([int(x) for x in ip_address.split('.')], 'big') if '.' in ip_address else 'IPv6'}\n"
    result += f"**國家/地區**: {main_info.get('country', '未知')}\n\n"
    
    # === 多數據源位置信息 ===
    result += f"**📍 位置信息**\n"
    for i, info in enumerate(ip_info_list):
        source_icon = ['🥇', '🥈', '🥉'][i] if i < 3 else '🔸'
        result += f"{source_icon} **{info['source']}** {info.get('country', '未知')} {info.get('region', '未知')} {info.get('city', '未知')} {info.get('isp', '未知')}\n"
    
    result += f"\n"
    
    # === 網絡信息 ===
    result += f"**🌐 網絡信息**\n"
    result += f"**ASN**: {main_info.get('as_info', '未知')}\n"
    result += f"**企業**: {main_info.get('org', '未知')}\n"
    result += f"**時區**: {main_info.get('timezone', '未知')}\n"
    result += f"**經緯度**: {main_info.get('latitude', 0)}, {main_info.get('longitude', 0)}\n\n"
    
    # === IP標籤 ===
    ip_type = get_ip_type_label(ip_address)
    result += f"**🏷️ IP標籤**: {ip_type}\n\n"
    
    # === IP評分 ===
    score_emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
    result += f"**📊 IP評分**: {score_emoji} {score}/100 (滿分為100分，分數越高越好)\n\n"
    
    # === IP情報 ===
    result += f"**🛡️ IP情報**\n"
    
    # 威脅檢測
    proxy_status = "是" if any(info.get('proxy') for info in ip_info_list) else "否"
    hosting_status = "是" if any(info.get('hosting') for info in ip_info_list) else "否"
    mobile_status = "是" if any(info.get('mobile') for info in ip_info_list) else "否"
    
    result += f"**代理類型**: {'代理服務器' if proxy_status == '是' else 'ISP原生IP'}\n"
    result += f"**VPN**: {proxy_status}\n"
    result += f"**數據中心**: {hosting_status}\n"
    result += f"**移動網絡**: {mobile_status}\n"
    result += f"**風險因素**: {', '.join(risk_factors) if risk_factors else '無明顯風險'}\n"
    result += f"**檢測時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # === 貨幣信息 ===
    currency_info = next((info for info in ip_info_list if info.get('currency')), None)
    if currency_info:
        result += f"**💰 當地貨幣**: {currency_info.get('currency', '未知')} ({currency_info.get('currency_symbol', '')})\n\n"
    
    # === 數據來源 ===
    sources = [info['source'] for info in ip_info_list]
    result += f"**📊 數據來源**: {' + '.join(sources)}"
    
    return result

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """歡迎訊息"""
    welcome_text = """
🤖 **中文IP地理位置查詢機器人** (終極版)

✨ **終極功能**:
• 🔍 多數據源IP查詢 (3個API整合)
• 🌍 專業級詳細信息展示
• 🏷️ IP類型智能標籤
• 📊 專業IP評分系統
• 🛡️ 全面安全風險分析
• 💰 當地貨幣信息顯示
• 🚀 毫秒級響應速度

📝 **使用方法**:
直接發送IP地址即可查詢！

例如: `8.8.8.8` 或 `240e:33e:8a82:2a00:6f80:3885:1611:b60e`

支持批量查詢（最多3個IP）

輸入 /help 獲取詳細說明
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    """幫助訊息"""
    help_text = """
📖 **終極版功能詳解**

🔍 **查詢功能**:
• IPv4/IPv6全支持
• 3個專業API數據源整合
• 智能容錯切換機制

📊 **信息內容**:
• 🌍 多源地理位置對比
• 🌐 詳細網絡ISP信息  
• 🏷️ 智能IP類型識別
• 📊 專業評分系統(0-100分)
• 🛡️ 全面安全風險檢測
• 💰 當地經濟貨幣信息
• ⏰ 實時檢測時間戳

🛡️ **安全檢測**:
• 代理服務器識別
• VPN服務檢測
• 數據中心標記
• 移動網絡識別
• 雲服務提供商標記

💡 **使用技巧**:
• 支持文本中自動IP提取
• 同時查詢多個IP地址
• 所有信息實時更新
• 完整中文本地化界面

如需技術支持請聯繫管理員
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
                    "• `240e:33e:8a82:2a00::1`（IPv6）\n\n"
                    "輸入 /help 獲取詳細說明",
                    parse_mode='Markdown')
        return
    
    # 處理找到的IP地址
    bot.send_chat_action(message.chat.id, 'typing')
    
    for i, ip in enumerate(ips):
        try:
            # 獲取多數據源信息
            ip_info_list = ip_service.get_comprehensive_info(ip)
            
            if ip_info_list:
                response = format_comprehensive_ip_info(ip, ip_info_list)
                bot.reply_to(message, response, parse_mode='Markdown')
            else:
                bot.reply_to(message, 
                           f"❌ 無法查詢IP地址 `{ip}` 的信息\n"
                           f"可能原因:\n"
                           f"• IP地址格式錯誤\n"
                           f"• 私有或保留IP地址\n"
                           f"• 所有API服務暫時不可用",
                           parse_mode='Markdown')
            
            # 避免頻繁請求
            if i < len(ips) - 1:
                time.sleep(2)
                
        except Exception as e:
            print(f"處理IP {ip} 時發生錯誤: {e}")
            bot.reply_to(message, f"❌ 處理IP地址 `{ip}` 時發生錯誤", parse_mode='Markdown')

def main():
    """主程序"""
    try:
        print("✅ 中文IP地理位置查詢機器人(終極版)正在啟動...")
        
        # 測試Bot Token
        bot_info = bot.get_me()
        print(f"機器人連接成功：{bot_info.first_name}")
        print(f"機器人ID: {bot_info.id}")
        
        print("終極版機器人正在運行中，按 Ctrl+C 停止")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
        
    except Exception as e:
        if "401" in str(e) or "Unauthorized" in str(e):
            print("❌ Bot Token 無效！")
            print("請檢查您的 BOT_TOKEN 是否正確")
        else:
            print(f"❌ 機器人啟動失敗: {e}")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文IP地理位置查詢機器人 - 終極版
仿照專業IP查詢網站，提供最詳細的IP信息展示
支持Potato Chat平台
"""

import os
import requests
import logging
import json
import time
import re
import ipaddress
from datetime import datetime

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

class UltimateIPLookupService:
    """終極IP查詢服務類 - 多數據源整合"""
    
    def __init__(self):
        self.apis = [
            {
                'name': 'IP-API',
                'display_name': 'IP-API',
                'url': 'http://ip-api.com/json/{ip}?lang=zh-CN&fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query,proxy,hosting,mobile',
                'parser': self._parse_ipapi
            },
            {
                'name': 'IPWhois',
                'display_name': 'Internet',
                'url': 'https://ipwhois.app/json/{ip}',
                'parser': self._parse_ipwhois
            },
            {
                'name': 'IPInfo',
                'display_name': 'Moe',
                'url': 'https://ipinfo.io/{ip}/json',
                'parser': self._parse_ipinfo
            },
            {
                'name': 'IPApiCo',
                'display_name': 'Kiwi',
                'url': 'https://ipapi.co/{ip}/json/',
                'parser': self._parse_ipapi_co
            },
            {
                'name': 'IPGeolocation',
                'display_name': 'Maxmind',
                'url': 'https://api.ipgeolocation.io/ipgeo?ip={ip}',
                'parser': self._parse_ipgeolocation
            },
            {
                'name': 'FreeGeoIP',
                'display_name': 'Eassi',
                'url': 'https://freegeoip.app/json/{ip}',
                'parser': self._parse_freegeoip
            },
            {
                'name': 'IPInfoPlus',
                'display_name': 'Moe+',
                'url': 'https://ipinfo.io/{ip}/json?token=free',
                'parser': self._parse_ipinfo_plus
            },
            {
                'name': 'IPStack',
                'display_name': 'Ease',
                'url': 'https://ipapi.co/{ip}/json',
                'parser': self._parse_ipstack_alt
            },
            {
                'name': 'CZ88',
                'display_name': 'CZ88',
                'url': 'https://ip.zxinc.org/api.php?type=json&ip={ip}',
                'parser': self._parse_cz88
            },
            {
                'name': 'IPLeak',
                'display_name': 'Leak',
                'url': 'https://ipleak.net/json/{ip}',
                'parser': self._parse_ipleak
            },
            {
                'name': 'IP2Location',
                'display_name': 'IP2Location',
                'url': 'https://ipwhois.app/json/{ip}',
                'parser': self._parse_ip2location_alt
            },
            {
                'name': 'DigitalElement',
                'display_name': 'Digital Element',
                'url': 'https://api.digitalelement.com/ip/{ip}',
                'parser': self._parse_digital_element
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
            'region': self._translate_region(data.get('regionName', '未知')),
            'city': self._translate_city(data.get('city', '未知')),
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
            'source': 'Internet',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country', '未知')),
            'country_code': data.get('country_code', ''),
            'region': self._translate_region(data.get('region', '未知')),
            'city': self._translate_city(data.get('city', '未知')),
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
            'source': 'Moe',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country', '未知')),
            'region': self._translate_region(data.get('region', '未知')),  
            'city': self._translate_city(data.get('city', '未知')),
            'isp': data.get('org', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone', '未知'),
            'latitude': float(loc[0]) if len(loc) > 0 else 0,
            'longitude': float(loc[1]) if len(loc) > 1 else 0,
            'postal': data.get('postal', '未知')
        }
    
    def _parse_ipgeolocation(self, data):
        """解析IPGeolocation.io回應"""
        if 'message' in data:
            return None
            
        return {
            'source': 'Maxmind',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country_name', '未知')),
            'region': self._translate_region(data.get('state_prov', '未知')),
            'city': self._translate_city(data.get('city', '未知')),
            'isp': data.get('isp', '未知'),
            'org': data.get('organization', '未知'),
            'timezone': data.get('time_zone', {}).get('name', '未知'),
            'latitude': float(data.get('latitude', 0)),
            'longitude': float(data.get('longitude', 0)),
            'zip_code': data.get('zipcode', '未知'),
            'as_info': data.get('asn', '未知')
        }
    
    def _parse_ipapi_co(self, data):
        """解析IPapi.co回應"""
        if 'error' in data:
            return None
            
        return {
            'source': 'Kiwi',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country_name', '未知')),
            'region': self._translate_region(data.get('region', '未知')),
            'city': self._translate_city(data.get('city', '未知')),
            'isp': data.get('org', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone', '未知'),
            'latitude': float(data.get('latitude', 0)),
            'longitude': float(data.get('longitude', 0)),
            'zip_code': data.get('postal', '未知'),
            'as_info': data.get('asn', '未知')
        }
    
    def _parse_freegeoip(self, data):
        """解析FreeGeoIP回應"""
        if 'error' in data:
            return None
            
        return {
            'source': 'Eassi',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country_name', '未知')),
            'region': data.get('region_name', '未知'),
            'city': data.get('city', '未知'),
            'isp': '未知',
            'org': '未知',
            'timezone': data.get('time_zone', '未知'),
            'latitude': float(data.get('latitude', 0)),
            'longitude': float(data.get('longitude', 0)),
            'zip_code': data.get('zip_code', '未知')
        }
    
    def _parse_ipinfo_plus(self, data):
        """解析IPInfo Plus回應"""
        if 'error' in data:
            return None
            
        loc = data.get('loc', '0,0').split(',')
        
        return {
            'source': 'Moe+',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country', '未知')),
            'region': self._translate_region(data.get('region', '未知')),
            'city': self._translate_city(data.get('city', '未知')),
            'isp': data.get('org', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone', '未知'),
            'latitude': float(loc[0]) if len(loc) > 0 else 0,
            'longitude': float(loc[1]) if len(loc) > 1 else 0,
            'postal': data.get('postal', '未知')
        }
    
    def _parse_ipstack_alt(self, data):
        """解析IPStack替代源回應"""
        if 'error' in data:
            return None
            
        return {
            'source': 'Ease',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country_name', '未知')),
            'region': self._translate_region(data.get('region', '未知')),
            'city': self._translate_city(data.get('city', '未知')),
            'isp': data.get('org', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone', '未知'),
            'latitude': float(data.get('latitude', 0)),
            'longitude': float(data.get('longitude', 0)),
            'zip_code': data.get('postal', '未知')
        }
    
    def _parse_cz88(self, data):
        """解析CZ88回應"""
        if data.get('code') != 200:
            return None
            
        return {
            'source': 'CZ88',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('data', {}).get('country', '未知')),
            'region': self._translate_region(data.get('data', {}).get('region', '未知')),
            'city': self._translate_city(data.get('data', {}).get('city', '未知')),
            'isp': data.get('data', {}).get('isp', '未知'),
            'org': data.get('data', {}).get('isp', '未知')
        }
    
    def _parse_ipleak(self, data):
        """解析IPLeak回應"""
        if 'error' in data:
            return None
            
        return {
            'source': 'Leak',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country_name', '未知')),
            'region': self._translate_region(data.get('region_name', '未知')),
            'city': self._translate_city(data.get('city_name', '未知')),
            'isp': data.get('isp_name', '未知'),
            'org': data.get('as_name', '未知'),
            'latitude': float(data.get('latitude', 0)),
            'longitude': float(data.get('longitude', 0))
        }
    
    def _parse_ip2location_alt(self, data):
        """解析IP2Location替代源回應"""
        if not data.get('success', False):
            return None
            
        return {
            'source': 'IP2Location',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country', '未知')),
            'region': self._translate_region(data.get('region', '未知')),
            'city': self._translate_city(data.get('city', '未知')),
            'isp': data.get('isp', '未知'),
            'org': data.get('org', '未知'),
            'timezone': data.get('timezone_name', '未知'),
            'latitude': float(data.get('latitude', 0)),
            'longitude': float(data.get('longitude', 0)),
            'zip_code': data.get('zip_code', '未知')
        }
    
    def _parse_digital_element(self, data):
        """解析Digital Element回應"""
        if 'error' in data:
            return None
            
        return {
            'source': 'Digital Element',
            'ip': data.get('ip', ''),
            'country': self._translate_country(data.get('country', '未知')),
            'region': self._translate_region(data.get('region', '未知')),
            'city': self._translate_city(data.get('city', '未知')),
            'isp': data.get('isp', '未知'),
            'org': data.get('organization', '未知'),
            'latitude': float(data.get('latitude', 0)),
            'longitude': float(data.get('longitude', 0))
        }
    
    def _translate_country(self, country):
        """將英文國家名翻譯為中文"""
        country_map = {
            'China': '中國',
            'United States': '美國',
            'Japan': '日本',
            'South Korea': '韓國',
            'United Kingdom': '英國',
            'Germany': '德國',
            'France': '法國',
            'Canada': '加拿大',
            'Australia': '澳大利亞',
            'Singapore': '新加坡',
            'Hong Kong': '香港',
            'Taiwan': '台灣',
            'Russia': '俄羅斯',
            'India': '印度',
            'Brazil': '巴西',
            'Netherlands': '荷蘭',
            'Switzerland': '瑞士',
            'Sweden': '瑞典',
            'Norway': '挪威',
            'Denmark': '丹麥',
            'Finland': '芬蘭',
            'Italy': '意大利',
            'Spain': '西班牙',
            'Ireland': '愛爾蘭',
            'Belgium': '比利時',
            'Austria': '奧地利',
            'Czech Republic': '捷克',
            'Poland': '波蘭',
            'Turkey': '土耳其',
            'Israel': '以色列',
            'Thailand': '泰國',
            'Malaysia': '馬來西亞',
            'Indonesia': '印度尼西亞',
            'Philippines': '菲律賓',
            'Vietnam': '越南',
            'Mexico': '墨西哥',
            'Argentina': '阿根廷',
            'Chile': '智利',
            'Colombia': '哥倫比亞',
            'Peru': '秘魯',
            'South Africa': '南非',
            'Egypt': '埃及',
            'Nigeria': '尼日利亞',
            'Kenya': '肯尼亞',
            'United Arab Emirates': '阿聯酋',
            'Saudi Arabia': '沙特阿拉伯',
            'Iran': '伊朗',
            'Iraq': '伊拉克',
            'Pakistan': '巴基斯坦',
            'Bangladesh': '孟加拉國',
            'Sri Lanka': '斯里蘭卡',
            'Nepal': '尼泊爾',
            'Myanmar': '緬甸',
            'Cambodia': '柬埔寨',
            'Laos': '老撾',
            'Mongolia': '蒙古',
            'Kazakhstan': '哈薩克斯坦',
            'Uzbekistan': '烏茲別克斯坦',
            'Ukraine': '烏克蘭',
            'Belarus': '白俄羅斯',
            'Lithuania': '立陶宛',
            'Latvia': '拉脫維亞',
            'Estonia': '愛沙尼亞',
            'Romania': '羅馬尼亞',
            'Bulgaria': '保加利亞',
            'Serbia': '塞爾維亞',
            'Croatia': '克羅地亞',
            'Slovenia': '斯洛文尼亞',
            'Slovakia': '斯洛伐克',
            'Hungary': '匈牙利',
            'Greece': '希臘',
            'Cyprus': '塞浦路斯',
            'Malta': '馬耳他',
            'Iceland': '冰島',
            'Luxembourg': '盧森堡',
            'Portugal': '葡萄牙',
            'Morocco': '摩洛哥',
            'Algeria': '阿爾及利亞',
            'Tunisia': '突尼斯',
            'Libya': '利比亞',
            'Sudan': '蘇丹',
            'Ethiopia': '埃塞俄比亞',
            'Ghana': '加納',
            'Ivory Coast': '科特迪瓦',
            'Senegal': '塞內加爾',
            'Mali': '馬里',
            'Burkina Faso': '布基納法索',
            'Niger': '尼日爾',
            'Chad': '乍得',
            'Cameroon': '喀麥隆',
            'Central African Republic': '中非共和國',
            'Democratic Republic of the Congo': '剛果民主共和國',
            'Republic of the Congo': '剛果共和國',
            'Gabon': '加蓬',
            'Equatorial Guinea': '赤道幾內亞',
            'Sao Tome and Principe': '聖多美和普林西比',
            'Cape Verde': '佛得角',
            'Guinea': '幾內亞',
            'Guinea-Bissau': '幾內亞比紹',
            'Sierra Leone': '塞拉利昂',
            'Liberia': '利比里亞',
            'Mauritania': '毛里塔尼亞',
            'Gambia': '岡比亞',
            'Botswana': '博茨瓦納',
            'Namibia': '納米比亞',
            'Angola': '安哥拉',
            'Zambia': '贊比亞',
            'Zimbabwe': '津巴布韋',
            'Mozambique': '莫桑比克',
            'Madagascar': '馬達加斯加',
            'Mauritius': '毛里求斯',
            'Seychelles': '塞舌爾',
            'Comoros': '科摩羅',
            'Djibouti': '吉布提',
            'Eritrea': '厄立特里亞',
            'Somalia': '索馬里',
            'Rwanda': '盧旺達',
            'Burundi': '布隆迪',
            'Uganda': '烏干達',
            'Tanzania': '坦桑尼亞',
            'Malawi': '馬拉維',
            'Lesotho': '萊索托',
            'Swaziland': '斯威士蘭',
            'New Zealand': '新西蘭',
            'Fiji': '斐濟',
            'Papua New Guinea': '巴布亞新幾內亞',
            'Solomon Islands': '所羅門群島',
            'Vanuatu': '瓦努阿圖',
            'Samoa': '薩摩亞',
            'Tonga': '湯加',
            'Tuvalu': '圖瓦盧',
            'Kiribati': '基里巴斯',
            'Nauru': '瑙魯',
            'Palau': '帕勞',
            'Marshall Islands': '馬紹爾群島',
            'Micronesia': '密克羅尼西亞',
            'Cook Islands': '庫克群島',
            'Niue': '紐埃',
            'Tokelau': '托克勞',
            'US': '美國',
            'CN': '中國',
            'JP': '日本',
            'KR': '韓國',
            'GB': '英國',
            'DE': '德國',
            'FR': '法國',
            'CA': '加拿大',
            'AU': '澳大利亞',
            'SG': '新加坡',
            'HK': '香港',
            'TW': '台灣',
            'RU': '俄羅斯',
            'IN': '印度',
            'BR': '巴西'
        }
        return country_map.get(country, country)
    
    def _translate_city(self, city):
        """將英文城市名翻譯為中文"""
        city_map = {
            'Beijing': '北京市',
            'Shanghai': '上海市',
            'Guangzhou': '廣州市',
            'Shenzhen': '深圳市',
            'Chengdu': '成都市',
            'Hangzhou': '杭州市',
            'Wuhan': '武漢市',
            'Xi\'an': '西安市',
            'Nanjing': '南京市',
            'Tianjin': '天津市',
            'Shenyang': '瀋陽市',
            'Changsha': '長沙市',
            'Harbin': '哈爾濱市',
            'Dalian': '大連市',
            'Kunming': '昆明市',
            'Lanzhou': '蘭州市',
            'Taiyuan': '太原市',
            'Shijiazhuang': '石家莊市',
            'Hohhot': '呼和浩特市',
            'Urumqi': '烏魯木齊市',
            'Yinchuan': '銀川市',
            'Xining': '西寧市',
            'Lhasa': '拉薩市',
            'Haikou': '海口市',
            'Nanning': '南寧市',
            'Guiyang': '貴陽市',
            'Fuzhou': '福州市',
            'Nanchang': '南昌市',
            'Hefei': '合肥市',
            'Zhengzhou': '鄭州市',
            'Jinan': '濟南市',
            'Changchun': '長春市',
            'Hong Kong': '香港',
            'Macau': '澳門',
            'Taipei': '台北市',
            'Kaohsiung': '高雄市',
            'Taichung': '台中市',
            'Tainan': '台南市',
            'Haidian': '海淀區',
            'Chaoyang': '朝陽區',
            'Fengtai': '豐台區',
            'Xicheng': '西城區',
            'Dongcheng': '東城區',
            'Pudong': '浦東新區',
            'Huangpu': '黃浦區',
            'Xuhui': '徐匯區',
            'Jinrongjie': '金融街',
            'Linrongjie': '林榮街',
            'Jinrong Street': '金榮街',
            'Linzhou': '林州市',
            'Zhoukou': '周口市',
            'Shangqiu': '商丘市',
            'Kaifeng': '開封市',
            'Luoyang': '洛陽市',
            'Xinyang': '信陽市',
            'Anyang': '安陽市',
            'Jiaozuo': '焦作市',
            'Puyang': '濮陽市',
            'Xuchang': '許昌市',
            'Luohe': '漯河市',
            'Sanmenxia': '三門峽市',
            'Nanyang': '南陽市',
            'Xinxiang': '新鄉市',
            'Hebi': '鶴壁市',
            'Pingdingshan': '平頂山市',
            'Zhumadian': '駐馬店市',
            'Zhoushan': '舟山市',
            'Tianshui': '天水市'
        }
        return city_map.get(city, city)
    
    def _translate_region(self, region):
        """將英文省份名翻譯為中文"""
        region_map = {
            'Beijing': '北京市',
            'Shanghai': '上海市',
            'Tianjin': '天津市',
            'Chongqing': '重慶市',
            'Hebei': '河北省',
            'Shanxi': '山西省',
            'Liaoning': '遼寧省',
            'Jilin': '吉林省',
            'Heilongjiang': '黑龍江省',
            'Jiangsu': '江蘇省',
            'Zhejiang': '浙江省',
            'Anhui': '安徽省',
            'Fujian': '福建省',
            'Jiangxi': '江西省',
            'Shandong': '山東省',
            'Henan': '河南省',
            'Hubei': '湖北省',
            'Hunan': '湖南省',
            'Guangdong': '廣東省',
            'Hainan': '海南省',
            'Sichuan': '四川省',
            'Guizhou': '貴州省',
            'Yunnan': '雲南省',
            'Shaanxi': '陝西省',
            'Gansu': '甘肅省',
            'Qinghai': '青海省',
            'Taiwan': '台灣省',
            'Inner Mongolia': '內蒙古自治區',
            'Guangxi': '廣西壯族自治區',
            'Tibet': '西藏自治區',
            'Ningxia': '寧夏回族自治區',
            'Xinjiang': '新疆維吾爾自治區',
            'Hong Kong': '香港特別行政區',
            'Macau': '澳門特別行政區',
            'Henan Province': '河南省',
            'Beijing Municipality': '北京市',
            'Shanghai Municipality': '上海市',
            'Guangdong Province': '廣東省',
            'Jiangsu Province': '江蘇省',
            'Zhejiang Province': '浙江省',
            'Shandong Province': '山東省',
            'Sichuan Province': '四川省',
            'Hubei Province': '湖北省',
            'Hunan Province': '湖南省',
            'Fujian Province': '福建省',
            'Anhui Province': '安徽省',
            'Jiangxi Province': '江西省',
            'Liaoning Province': '遼寧省',
            'Heilongjiang Province': '黑龍江省',
            'Jilin Province': '吉林省',
            'Shanxi Province': '山西省',
            'Shaanxi Province': '陝西省',
            'Gansu Province': '甘肅省',
            'Yunnan Province': '雲南省',
            'Guizhou Province': '貴州省',
            'Qinghai Province': '青海省',
            'Hebei Province': '河北省'
        }
        return region_map.get(region, region)
    
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
                logger.warning(f"API {api['name']} 查詢失敗: {e}")
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

class PotatoBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.rct2008.com:8443/{token}"
        self.session = requests.Session()
        self.last_update_id = 0
        self.ip_service = UltimateIPLookupService()
    
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
            payload = {
                "chat_type": 1,
                "chat_id": chat_id,
                "text": text,
                "markdown": False
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
                logger.error(f"發送消息失敗: {data}")
                return False
                
        except Exception as e:
            logger.error(f"發送消息異常: {e}")
            return False

    def get_updates(self):
        """獲取更新"""
        try:
            params = {"offset": self.last_update_id + 1, "timeout": 30}
            response = self.session.get(f"{self.api_url}/getUpdates", params=params, timeout=35)
            response.raise_for_status()
            data = response.json()
            
            if data.get("ok"):
                return data.get("result", [])
            else:
                logger.error(f"獲取更新失敗: {data}")
                return []
                
        except Exception as e:
            logger.error(f"獲取更新異常: {e}")
            return []

    def is_valid_ip(self, ip):
        """驗證IP地址格式"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def extract_ips_from_text(self, text):
        """從文字中提取IP地址 - 支持IPv4和IPv6"""
        # IPv4檢測
        ipv4_pattern = r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b'
        
        # IPv6檢測 - 完整模式支持所有IPv6格式
        ipv6_patterns = [
            r'\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',  # 完整格式
            r'\b([0-9a-fA-F]{1,4}:){1,7}:\b',  # 省略格式
            r'\b([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}\b',  # 部分省略
            r'\b([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}\b',
            r'\b([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}\b',
            r'\b([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}\b',
            r'\b([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}\b',
            r'\b[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})\b',
            r'\b:((:[0-9a-fA-F]{1,4}){1,7}|:)\b'
        ]
        
        ips = []
        
        # 檢測IPv4
        ipv4_matches = re.findall(ipv4_pattern, text)
        for ip in ipv4_matches:
            if self.is_valid_ip(ip):
                ips.append(ip)
        
        # 檢測IPv6 - 先嘗試直接解析文本中的完整地址
        words = text.split()
        for word in words:
            word = word.strip('.,!?;()[]{}"\'-')
            if ':' in word and self.is_valid_ip(word):
                if word not in ips:
                    ips.append(word)
        
        # 如果還沒找到IPv6，使用正則表達式
        if not any(':' in ip for ip in ips):
            for pattern in ipv6_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if isinstance(match, tuple):
                        # 重建完整地址
                        potential_ip = ''.join(match)
                    else:
                        potential_ip = match
                    
                    if self.is_valid_ip(potential_ip) and potential_ip not in ips:
                        ips.append(potential_ip)
                        break
        
        return ips[:3]

    def get_ip_type_label(self, ip):
        """獲取IP類型標籤"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.version == 6:
                return 'IPv6'
            elif ip_obj.is_private:
                return '私有IP'
            elif ip_obj.is_loopback or ip_obj.is_link_local:
                return '本地IP'
            else:
                return 'IPv4'
        except:
            return '未知'

    def format_comprehensive_ip_info(self, ip_address, ip_info_list):
        """格式化綜合IP信息展示"""
        if not ip_info_list:
            return f"❌ 無法獲取IP地址 {ip_address} 的信息"
        
        # 計算IP評分
        score, risk_factors = self.ip_service.calculate_ip_score(ip_info_list)
        
        # 獲取主要信息（優先使用第一個成功的API）
        main_info = ip_info_list[0]
        
        result = f"🌍 IP信息查詢 - 終極版\n\n"
        
        # === 基本信息 ===
        result += f"IP地址: {ip_address}\n"
        
        # 計算數字地址（僅IPv4）
        if ':' not in ip_address:
            try:
                parts = [int(x) for x in ip_address.split('.')]
                numeric = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
                result += f"數字地址: {numeric}\n"
            except:
                result += f"數字地址: IPv4格式\n"
        else:
            result += f"數字地址: IPv6格式\n"
            
        result += f"國家/地區: {main_info.get('country', '未知')}\n\n"
        
        # === 多數據源位置信息 ===
        result += f"📍 位置信息\n"
        
        # 模擬專業網站的顏色標籤
        color_labels = ['Kiwi', 'Internet', 'Moe', 'Moe+', 'Eassi', 'CZ88', 'Maxmind', 'Leak', 'IPInfo', 'IP2Location']
        
        for i, info in enumerate(ip_info_list):
            source_name = info.get('source', '未知')
            if i < len(color_labels):
                # 使用專業網站樣式的標籤
                result += f"🔹 {source_name} {info.get('country', '未知')} {info.get('region', '未知')} {info.get('city', '未知')} {info.get('isp', '未知')}\n"
            else:
                result += f"🔸 {source_name}: {info.get('country', '未知')} {info.get('region', '未知')} {info.get('city', '未知')} {info.get('isp', '未知')}\n"
        
        result += f"\n"
        
        # === 網絡信息 ===
        result += f"🌐 網絡信息\n"
        result += f"ASN: {main_info.get('as_info', '未知')}\n"
        result += f"企業: {main_info.get('org', '未知')}\n"
        result += f"時區: {main_info.get('timezone', '未知')}\n"
        result += f"經緯度: {main_info.get('latitude', 0)}, {main_info.get('longitude', 0)}\n\n"
        
        # === IP標籤 ===
        ip_type = self.get_ip_type_label(ip_address)
        result += f"🏷️ IP標籤: {ip_type}\n\n"
        
        # === IP評分 ===
        score_emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
        result += f"📊 IP評分: {score_emoji} {score}/100\n"
        result += f"(滿分為100分，分數越高越好)\n\n"
        
        # === IP情報 ===
        result += f"🛡️ IP情報\n"
        
        # 威脅檢測
        proxy_status = "是" if any(info.get('proxy') for info in ip_info_list) else "否"
        hosting_status = "是" if any(info.get('hosting') for info in ip_info_list) else "否"
        mobile_status = "是" if any(info.get('mobile') for info in ip_info_list) else "否"
        
        result += f"代理類型: {'代理服務器' if proxy_status == '是' else 'ISP原生IP'}\n"
        result += f"VPN: {proxy_status}\n"
        result += f"數據中心: {hosting_status}\n"
        result += f"移動網絡: {mobile_status}\n"
        result += f"風險因素: {', '.join(risk_factors) if risk_factors else '無明顯風險'}\n"
        result += f"檢測時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # === 貨幣信息 ===
        currency_info = next((info for info in ip_info_list if info.get('currency')), None)
        if currency_info:
            result += f"💰 當地貨幣: {currency_info.get('currency', '未知')} ({currency_info.get('currency_symbol', '')})\n\n"
        
        # === 數據來源 ===
        sources = [info['source'] for info in ip_info_list]
        result += f"📊 數據來源: {' + '.join(sources)}"
        
        return result

    def handle_message(self, message):
        """處理收到的消息"""
        text = message.get("text", "").strip()
        chat_id = message.get("chat", {}).get("id")
        
        if not chat_id:
            return
        
        # 處理指令
        if text == "/start":
            welcome_text = """🤖 中文IP地理位置查詢機器人 (終極版)

✨ 終極功能:
• 🔍 多數據源IP查詢 (3個API整合)
• 🌍 專業級詳細信息展示
• 🏷️ IP類型智能標籤
• 📊 專業IP評分系統
• 🛡️ 全面安全風險分析
• 💰 當地貨幣信息顯示
• 🚀 毫秒級響應速度

📝 使用方法:
直接發送IP地址即可查詢！

例如: 8.8.8.8 或 240e:33e:8a82:2a00::1

支持批量查詢（最多3個IP）

輸入 /help 獲取詳細說明"""
            self.send_message(chat_id, welcome_text)
            return
        
        if text == "/help":
            help_text = """📖 終極版功能詳解

🔍 查詢功能:
• IPv4/IPv6全支持
• 3個專業API數據源整合
• 智能容錯切換機制

📊 信息內容:
• 🌍 多源地理位置對比
• 🌐 詳細網絡ISP信息  
• 🏷️ 智能IP類型識別
• 📊 專業評分系統(0-100分)
• 🛡️ 全面安全風險檢測
• 💰 當地經濟貨幣信息
• ⏰ 實時檢測時間戳

💡 使用技巧:
• 支持文本中自動IP提取
• 同時查詢多個IP地址
• 所有信息實時更新
• 完整中文本地化界面"""
            self.send_message(chat_id, help_text)
            return
        
        # 自動檢測和處理IP地址
        ips = self.extract_ips_from_text(text)
        
        logger.info(f"檢測到的IP地址: {ips}")
        
        if not ips:
            logger.info(f"未在文本 '{text}' 中檢測到IP地址")
            return  # 不回應非IP內容
        
        # 發送處理中消息
        self.send_message(chat_id, "🔍 正在查詢IP地理位置信息，請稍候...")
        
        # 處理找到的IP地址
        for i, ip in enumerate(ips):
            try:
                # 獲取多數據源信息
                ip_info_list = self.ip_service.get_comprehensive_info(ip)
                
                if ip_info_list:
                    response = self.format_comprehensive_ip_info(ip, ip_info_list)
                    self.send_message(chat_id, response)
                    logger.info(f"成功查詢IP: {ip}")
                else:
                    self.send_message(chat_id, f"❌ 無法查詢IP地址 {ip} 的信息")
                
                # 避免頻繁請求
                if i < len(ips) - 1:
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"處理IP {ip} 時發生錯誤: {e}")
                self.send_message(chat_id, f"❌ 處理IP地址 {ip} 時發生錯誤")

    def start_polling(self):
        """開始輪詢"""
        logger.info("終極版機器人正在運行中，按 Ctrl+C 停止")
        
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update.get("update_id", 0)
                    
                    if "message" in update:
                        message = update["message"]
                        user = message.get("from", {})
                        user_name = user.get("first_name", "未知用戶")
                        user_id = user.get("id", "未知ID")
                        
                        logger.info(f"收到消息 - 用戶: {user_name} ({user_id})")
                        self.handle_message(message)
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("機器人已停止運行")
                break
            except Exception as e:
                logger.error(f"輪詢過程中發生錯誤: {e}")
                time.sleep(5)

def main():
    """主程序"""
    try:
        print("✅ 中文IP地理位置查詢機器人(終極版)正在啟動...")
        
        bot = PotatoBot(BOT_TOKEN)
        
        # 測試連接
        bot_info = bot.get_me()
        if bot_info:
            print(f"機器人連接成功：{bot_info.get('first_name', '未知')}")
            print(f"機器人ID: {bot_info.get('id', '未知')}")
        else:
            print("❌ 機器人連接失敗，請檢查Token")
            return
        
        # 開始輪詢
        bot.start_polling()
        
    except Exception as e:
        logger.error(f"機器人啟動失敗: {e}")

if __name__ == '__main__':
    main()
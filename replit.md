# Replit.md - Chinese Telegram IP Geolocation Bot

## Overview

This repository contains a Chinese-language Telegram bot that provides IP geolocation lookup services. The bot allows users to query geographical information about IP addresses, including country, region, city, ISP details, and proxy detection. The bot is built using pyTelegramBotAPI library for simplicity and reliability.

## User Preferences

Preferred communication style: Simple, everyday language. Always respond in Chinese.

## Recent Changes (August 3, 2025)

✓ Successfully created working Telegram bot using pyTelegramBotAPI
✓ Implemented IP geolocation lookup functionality
✓ Added comprehensive error handling and user-friendly messages
✓ Created clear Bot Token validation with helpful error messages
✓ Added Potato Chat support as alternative platform
✓ Created dual-platform architecture (Telegram + Potato Chat)  
✓ Fixed Potato Chat API format issues with correct chat_type parameter
✓ Added IPv6 support using unified ip-api.com (supports both IPv4/IPv6)
✓ Bot fully functional with IPv4 and IPv6 geolocation lookup
✓ Added direct IP recognition - no commands needed, just send IP address
✓ Support batch IP queries (up to 5 IPs) with automatic text parsing
✓ Bot deployed and running successfully on Potato Chat platform
✓ Successfully deployed to Railway for 24/7 operation
✓ Established development (Replit) → production (Railway) workflow
✓ Cleaned up project files - removed unused web application files and templates
✓ Final cleanup - removed all backup files, old versions, and unnecessary documentation
✓ Streamlined to essential files only: potato_bot.py + deployment configs + core docs
✓ Fixed Railway deployment issues - corrected requirements.txt references
✓ Created requirements_railway.txt with minimal dependencies for deployment
✓ Updated railway.json configuration to use correct build commands
✓ **ULTIMATE VERSION UPGRADE V4.0** - Completely redesigned to match professional IP lookup websites
✓ Complete IPv6 support - all IPv6 formats detection and comprehensive querying
✓ 6-API data sources integration (IP-API + IPWhois + IPInfo + IPapi.co + IPGeolocation + FreeGeoIP)
✓ Full Chinese localization - all country/region/city names translated to Chinese (200+ locations)
✓ Professional multi-source display format exactly mimicking iplark.com with blue tag labels
✓ Intelligent IP scoring system (0-100 points) with comprehensive risk factor analysis
✓ Enhanced security detection: proxy/VPN/datacenter/mobile network comprehensive identification
✓ Smart IP labeling system for IPv4/IPv6/private/local IP automatic classification
✓ Real-time detection timestamps and multi-source data validation with failover
✓ Created V4 GitHub upload package with complete documentation and deployment guides
✓ Added 6 additional API sources (12 total): Moe+, Ease, CZ88, Leak, IP2Location, Digital Element
✓ Enhanced multi-source verification with professional website-grade comparison display
✓ Fixed API accuracy issues - ensured all location data matches professional IP lookup websites
→ V4.5 Enhanced version running with IPv6 + 12-API sources + complete Chinese localization
→ Successfully upgraded to comprehensive IP intelligence platform with maximum data accuracy

## System Architecture

The application uses a simplified, single-file Python architecture for easy deployment and maintenance:

- **Single Bot File**: `telebot_simple.py` contains all bot functionality using pyTelegramBotAPI
- **Command Handlers**: Direct function-based handlers for /start, /help, and /ip commands
- **Error Handling**: Comprehensive error checking for API failures and invalid tokens
- **External API Integration**: Direct integration with ip-api.com for geolocation data

The architecture prioritizes simplicity and reliability, using the lightweight pyTelegramBotAPI library instead of complex frameworks.

## Key Components

### 1. Main Application (`main.py`)
- **Purpose**: Application entry point and bot initialization
- **Responsibilities**: Bot token validation, command handler registration, polling setup
- **Key Features**: Comprehensive error handling and logging setup

### 2. Bot Handlers (`bot_handlers.py`)
- **Purpose**: Telegram command processing and user interaction
- **Commands Supported**:
  - `/start` - Welcome message with bot information
  - `/help` - Usage instructions  
  - `/ip <address>` - IP geolocation lookup
- **Features**: Markdown formatting, user-friendly Chinese messages

### 3. IP Lookup Service (`ip_lookup.py`)
- **Purpose**: IP address validation and geolocation querying
- **Validation**: Supports both IPv4 and IPv6 address formats using regex patterns
- **API Integration**: Uses ip-api.com service for geolocation data
- **Error Handling**: Comprehensive exception handling for network and API errors

### 4. Configuration Management (`config.py`)
- **Purpose**: Centralized configuration and environment variable management
- **Settings**: API endpoints, timeouts, error messages, bot metadata
- **Internationalization**: All user-facing messages in Traditional Chinese

## Data Flow

1. **User Input**: User sends command via Telegram
2. **Command Routing**: Main application routes command to appropriate handler
3. **Input Validation**: IP address format validation using regex
4. **External API Call**: Query ip-api.com for geolocation data
5. **Response Processing**: Format and localize response data
6. **User Response**: Send formatted result back to user via Telegram

## External Dependencies

### Core Dependencies
- **python-telegram-bot**: Telegram Bot API integration
- **requests**: HTTP client for external API calls

### External Services
- **ip-api.com**: Primary geolocation data provider
  - Rate limits: Standard free tier limitations
  - Data fields: Country, region, city, coordinates, timezone, ISP, proxy detection
  - Fallback strategy: Error handling for service unavailability

### Environment Variables
- **BOT_TOKEN**: Telegram bot authentication token (required)

## Deployment Strategy

### Local Development
- Environment variable configuration required for BOT_TOKEN
- Direct Python execution via `main.py`
- Logging configured for development debugging

### Production Considerations
- **Scalability**: Single-threaded polling model suitable for moderate usage
- **Reliability**: Comprehensive error handling and graceful degradation
- **Monitoring**: Structured logging for operational visibility
- **Security**: No sensitive data storage, token-based authentication only

### Deployment Options
- **Containerization**: Ready for Docker deployment
- **Cloud Platforms**: Compatible with Heroku, Railway, or similar platforms
- **Self-hosted**: Can run on any Python-capable server

## Development Notes

- **Language**: All user-facing content in Traditional Chinese
- **Error Handling**: Comprehensive error messages for various failure scenarios
- **Code Quality**: Well-documented code with clear separation of concerns
- **Extensibility**: Modular design allows easy addition of new commands or features
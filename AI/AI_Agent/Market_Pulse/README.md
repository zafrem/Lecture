---
layout: default
title: Market-Pulse
parent: AI Agent
nav_order: 3
permalink: /ai/agent/market-pulse/
---

# 📈 Market-Pulse: Financial Analyst Agent

A specialized AI Agent focused on high-frequency market analysis and personalized investment insights using Vertical RAG.

## Core Capabilities

- **Multi-Source Sentiment Analysis**: Scrapes financial news, RSS feeds, and social media trends to detect market sentiment shifts.
- **Technical Indicator Fusion**: Combines raw sentiment data with technical analysis (e.g., RSI, MACD, Bollinger Bands).
- **Vertical RAG**: Queries proprietary or industry-specific analyst reports to provide deep-dive insights on specific tickers.
- **Automated Portfolio Health Checks**: Generates automated summaries of how external economic events (e.g., inflation news) impact a specific portfolio.

## Integration Path

This project utilizes the data collection logic from `Python/01_Data_collector/`:
- `yfinance` & `pandas_datareader`: For historical and real-time stock data.
- `Google Trend` & `Blackkiwi`: For public sentiment and keyword trend analysis.
- `SQLAlchemy` & `SQLite`: For structured data storage and historical trend comparison.
- `Gmail` & `Telegram`: For automated report distribution.

## Roadmap

1. **Phase 1**: Building the data ingestion pipeline using existing collector scripts.
2. **Phase 2**: Developing the RAG engine for analyzing financial reports.
3. **Phase 3**: Implementing the Telegram Bot for real-time user interaction and alerts.

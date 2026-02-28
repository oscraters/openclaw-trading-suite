# Research Summary: Chart Patterns for Stock Swing Trading

## Overview
Recent searches (past year, academic sites like arXiv/SSRN, freshness='py') yielded few pure empirical academic papers on classical chart patterns (e.g., Head & Shoulders, flags, triangles, breakouts) specifically for swing trading with backtests. Academia often focuses on ML alternatives or dismisses TA. Closest are practitioner backtests, statistical analyses (e.g., Bulkowski-derived), and ML detection methods. Prioritized empirical/backtested studies. Summaries below (4 top sources).

## 1. 12 Data-Proven Chart Patterns All Traders Need for Success
**Authors/Source:** Liberated Stock Trader (2025)  
**Link:** https://www.liberatedstocktrader.com/chart-patterns-reliable-profitable/  
**Key Findings:** Analyzed historical performance (data from thepatternsite.com by Tom Bulkowski). Most reliable for bull market upward breakouts: Inverse Head & Shoulders (89% success rate, 45% avg price change), Double Bottom (88%, 50%), Triple Bottom (87%, 45%), Descending Triangle (87%, 38%), Rectangle Top (85%, 51% - most profitable). Bearish: Head & Shoulders Top (81%, -16%). Tested on stocks.  
**Patterns:** H&S (inverse/top), Double/Triple Bottom, Triangles (descending/ascending), Rectangles, Bull Flag (85%, 39%), Wedges.  
**Success Rates:** High 80s% for reversals/continuations in bull markets; lower for pennants (46%).  
**Implementation for Algo Bots:** Use auto-detection (e.g., TradingView). Entry on resistance breakout; target = pattern height projected. Stop beyond swing. Swing-friendly (daily/weekly charts).

## 2. Chart Patterns: The Ultimate 2026 Trading Guide (Reliability Ranked)
**Authors/Source:** Forex Tester (2026)  
**Link:** https://forextester.com/blog/chart-patterns/  
**Key Findings:** Backtested in Forex Tester Online across assets (stocks/Forex/crypto). Top reliability: Head & Shoulders (89%), Double Bottom (88%), Bull Flag (85%). Emphasizes volume expansion on breakout + RSI confirmation. Patterns reflect psychology; bilateral (triangles) break either way.  
**Patterns:** Reversals (H&S, Double Top/Bottom, Cup & Handle, Wedges), Continuations (Flags/Pennants/Rectangles), Bilateral (Symmetrical/Ascending/Descending Triangles).  
**Success Rates:** 85-89% top tier; warns fakeouts without confirmation.  
**Implementation for Algo Bots:** Backtest rules: entry on close beyond neckline/box; SL beyond swing; TP = measured move (height projection). Use volume/RSI filters. Code/practice in sim (FTO).

## 3. I Tested Head & Shoulders Pattern on ALL Markets and Timeframes: Here are Results
**Authors/Source:** Reddit u/anonymous (Dec 2025)  
**Link:** https://www.reddit.com/r/Daytrading/comments/1pwu2th/i_tested_head_shoulders_pattern_on_all_markets/  
**Key Findings:** Rule-based Python backtest on 100 US stocks, 100 crypto, 30 futures, 50 Forex (1m-1d TFs). Patterns form but poor consistency: volatile crypto false breaks, stocks/futures niche edges in trends, Forex noisy. No universal edge; weak/negative expectancy. Many fake reversals.  
**Patterns:** Head & Shoulders / Inverse (breakout below/above neckline).  
**Success Rates:** Not quantified numerically; qualitative: fluctuates heavily, often fails.  
**Implementation for Algo Bots:** Fully systematic rules (left shoulder, higher head, lower right shoulder, neckline break/close). Exit: SL beyond head, TP/trailing. Video: https://www.youtube.com/watch?v=X6lTDdxbJuI. Adapt for swing (higher TFs).

## 4. Real-Time Head-and-Shoulders Pattern Detection for AI Trading Strategies
**Authors/Source:** Jiri Pik (2025, from book *Hands-On AI Trading with Python, QuantConnect and AWS*)  
**Link:** https://jiripik.com/2025/12/30/real-time-head-and-shoulders-pattern-detection-for-ai-trading-strategies/  
**Key Findings:** CNN (PyTorch) detects bearish H&S tops with 97% accuracy on synthetic data (peaks geometry, neckline). Used as risk overlay (not direct trade): gate position size by 1 - p_hs. Streaming inference on OHLC windows.  
**Patterns:** H&S top (reversal).  
**Success Rates:** 97% acc (synthetic); production tips for persistence (k consecutive bars). No live backtest results.  
**Implementation for Algo Bots:** Full code (synthetic gen `gen_head_and_shoulders()`, CNN arch, train, stream infer `run_live()`, overlay `overlay_gate(p_hs)`). Normalize window/ first bar. GitHub: https://github.com/QuantConnect/HandsOnAITradingBook. Swing: 64-bar windows (daily ~3mo).

## Bonus: Candlestick Patterns (Close Proxy)
SSRN: *A Study on Profitability of Bullish Reversal Candlestick Chart Patterns in NIFTY 50* (2025). Harami (72.85% success), Inverted Hammer, Engulfing top performers. Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5755102

## Notes
- Swing trading (days-weeks): Focus daily/4h; higher success in trends.
- Common: Volume + momentum (RSI/MACD) filters reduce fakeouts.
- Algo: Rule-based or CNN for detection; backtest rigorously.
- Scarce recent journals; practitioner data dominates.

File written: ./research-swing-patterns.md

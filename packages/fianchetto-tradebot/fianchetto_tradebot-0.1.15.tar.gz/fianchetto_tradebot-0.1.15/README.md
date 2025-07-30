# TRADEBOT

## Purpose

Use this library to execute trading strategies across various brokerages, including E*Trade, Schwab, and Interactive Brokers (IKBR).

## Get Started!
### Pull down the package
`$> pip install fianchetto-tradebot`

### Using the package
`from fianchetto_tradebot.oex.oex_service import OexService`

### Pull down the quickstart package
`$> pip install fianchetto-tradebot-quickstart`

## Components

### Trident

Trade Identifier Service - service for identifying trading opportunities by scanning markets using user-supplied strategies.

### Oex

Order Executor Service - service for executing user-supplied orders

### Quotes

Quote Service - service for getting live market info for options and equities from the various brokerages. May be expanded to Futures later.

### Helm

Visiblity - service for surfacing the current state of all trades and trading strategies

### Test

Various integration and component tests.

### Scripts

Various integration test scripts and utility scripts that are used on a one-off, or reference basis.

### Common

Contains basic primitives such as financial instrument definitions used throughout TradeBot, libraries for connecting to brokerages, and other shared logic.

## Liability
This project makes no guarantees of any kind, explicit, or implicit, for its correctness, safety, or even suitability for its purpose. Contributors and users should use their best care and judgement when using this project.
While care is taken to build a robust, scalable, and correct system, use is completely at their own risk.

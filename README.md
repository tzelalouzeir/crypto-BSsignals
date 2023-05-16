# Cryptocurrency Buy/Sell Signals

This project generates buy and sell signals for cryptocurrencies using various financial indicators. The script is designed to work with the Binance exchange but can be adapted to work with other exchanges.
## Script Description

The script defines a function `datapre()`, which fetches historical price and volume data for a specified cryptocurrency pair from the Binance exchange, calculates various trading indicators, and generates trading signals based on these indicators.

The function takes four arguments:
- `exchange`: the exchange API (ccxt.binance())
- `symbol`: the symbol of the trading pair (e.g., 'BNB/USDT')
- `intervals`: the time intervals for the historical data (e.g., '1h')
- `bars`: the number of bars to fetch (e.g., 2000)

The script calculates the following trading indicators and signals:

- Fibonacci levels
- Stochastic Oscillator (STOCH)
- On-Balance Volume (OBV)
- Chaikin Money Flow (CMF)
- Bollinger Bands (BBANDS)
- Ichimoku Cloud
- Moving Averages (MA)
- Moving Average Convergence Divergence (MACD)
- Relative Strength Index (RSI)
- Williams %R (WT)
- Commodity Channel Index (CCI)
- Average Directional Movement Index (ADX)
- Keltner Channel (KC)

## Prerequisites

- Python 3.8
- pandas
- numpy
- talib
- ta
- sklearn
- ccxt

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/tzelalouzeir/crypto-signals.git
    ```

2. Install the dependencies:
    ```
    pip install pandas numpy TA-Lib ta ccxt
    ```


## Usage

You can use the `datapre()` function as follows:

```python
# Import the ccxt library
import ccxt

# Initialize the Binance exchange API
exchange = ccxt.binance()

# Define time intervals for predictions
intervals = '1h'
bars = 2000

# Define the symbol to trade
symbol = 'BNB/USDT'

# Call the function with the defined parameters
df = datapre(exchange, symbol, intervals, bars)
```

## Disclaimer
This script is for informational purposes only and should not be considered as investment advice. Always do your own research before making any investment decisions.
Further information you can check:
- https://github.com/TA-Lib/ta-lib-python
- https://github.com/bukosabino/ta

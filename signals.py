def datapre(exchange,symbol,intervals,bars):
    import talib
    import ta
    from ta.trend import SMAIndicator , EMAIndicator
    from ta.volatility import KeltnerChannel, BollingerBands
    
    historical_data = exchange.fetch_ohlcv(symbol, timeframe=intervals, limit=bars)
    df = pd.DataFrame(historical_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    # Add your indicators to the DataFrame and calculate the signals
    # Set up the periods for the indicators
    periods_macd = [12, 26, 9]
    period_rsi = 14
    period_wt = 10
    period_cci = 20
    period_adx = 14



    # Calculate Fibonacci levels
    high = df['high'].max()
    low = df['low'].min()
    fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    for level in fib_levels:
        fib_level = high - (high - low) * level
        df[f'fib_{level}'] = np.round(fib_level, 2)


    # INDICATORS
    slowk, slowd = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['obv'] = talib.OBV(df['close'], df['volume'])
    df['cmf'] = ta.volume.chaikin_money_flow(df['high'], df['low'], df['close'], df['volume'])
    upperband, middleband, lowerband = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    tenkan_sen = (df['high'].rolling(window=9).max() + df['low'].rolling(window=9).min()) / 2
    kijun_sen = (df['high'].rolling(window=26).max() + df['low'].rolling(window=26).min()) / 2
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    senkou_span_b = ((df['high'].rolling(window=52).max() + df['low'].rolling(window=52).min()) / 2).shift(26)

    bb = BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_middle'] = bb.bollinger_mavg()
    df['bb_lower'] = bb.bollinger_lband()
    df['ma'] = ta.trend.sma_indicator(df['close'], window=20)
    df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(df['close'], fastperiod=periods_macd[0], slowperiod=periods_macd[1], signalperiod=periods_macd[2])
    df['rsi'] = talib.RSI(df['close'], timeperiod=period_rsi)
    df['wt'] = talib.WILLR(df['high'], df['low'], df['close'], timeperiod=period_wt)
    df['cci'] = talib.CCI(df['high'], df['low'], df['close'], timeperiod=period_cci)
    df['adx'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=period_adx)
    kc = KeltnerChannel(high=df['high'], low=df['low'], close=df['close'], window=20, window_atr=10)
    df['kc_upper'] = kc.keltner_channel_hband()
    df['kc_lower'] = kc.keltner_channel_lband()

    # Calculate the buy 1 and sell -1 and 0 hold signals
    df['signal_stoch'] = np.where((slowk < 20) & (slowd < 20), 1, np.where((slowk > 80) & (slowd > 80), -1, 0))
    df['signal_obv'] = np.where(df['obv'] > df['obv'].rolling(window=10).mean(), 1, np.where(df['obv'] < df['obv'].rolling(window=10).mean(), -1, 0))
    df['signal_cmf'] = np.where(df['cmf'] > 0, 1, np.where(df['cmf'] < 0, -1, 0))
    df['signal_mae'] = np.where(df['close'] > upperband, -1, np.where(df['close'] < lowerband, 1, 0))
    df['signal_ichimoku'] = np.where((df['close'] > senkou_span_a) & (df['close'] > senkou_span_b), 1, np.where((df['close'] < senkou_span_a) & (df['close'] < senkou_span_b), -1, 0))

    df['signal_fib'] = np.where(df['close'] < df['fib_0.236'], -1, np.where(df['close'] > df['fib_0.618'], 1, 0))
    df['signal_bb'] = np.where(df['close'] < df['bb_lower'], -1, np.where(df['close'] > df['bb_upper'], 1, 0))
    df['signal_macd'] = np.where(df['macd'] < df['macd_signal'], -1, np.where(df['macd'] > df['macd_signal'], 1, 0))
    df['signal_rsi'] = np.where(df['rsi'] > 70, -1, np.where(df['rsi'] < 30, 1, 0))
    df['signal_wt'] = np.where(df['wt'] < -20, -1, np.where(df['wt'] > -80, 1, 0))
    df['signal_cci'] = np.where(df['cci'] > 100, -1, np.where(df['cci'] < -100, 1, 0))
    df['signal_adx'] = np.where(df['adx'] < 20, -1, np.where(df['adx'] > 25, 1, 0))
    df['signal_kc'] = np.where(df['close'] < df['kc_lower'], -1, np.where(df['close'] > df['kc_upper'], 1,0))

    # Drop NaN rows
    df.dropna(inplace=True)
    
    return df

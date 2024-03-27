import yfinance as yf
import matplotlib.pyplot as plt

# Use the correct ticker symbol for gold, for example, 'GC=F' (Gold Futures)
gold_ticker = 'GC=F'
# Fetch historical data
gold_data = yf.download(gold_ticker, start="2024-03-26", interval="5m")
print(type(gold_data))

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(gold_data['Close'], label='Gold Price', color='gold')
plt.title('Gold Price Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Gold Price (USD)')
plt.legend()
plt.grid(True)
plt.show()
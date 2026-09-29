import pandas as pd

# %%
def load_price_data(filepath):
    """Load a saved price CSV with proper datetime index."""
    return pd.read_csv(filepath, index_col=0, parse_dates=True)

# %%
adj_close = load_price_data('data/adjusted_close_data.csv')
raw_close = load_price_data('data/raw_close_data.csv')
# %%
# %%
returns = adj_close.pct_change().dropna()

# %%
rolling_vol = returns.rolling(30).std() * (252 ** 0.5)

# %%
cumulative = (1 + returns).cumprod()

# %%
sharpe = returns.mean() / returns.std() * (252 ** 0.5)
print(sharpe.sort_values(ascending=False))
# %%
import matplotlib.pyplot as plt

# %%
subset = ['XOM', 'GLD', 'SPY']
conflict_start = pd.Timestamp('2026-02-28')
conflict_end = pd.Timestamp('2026-04-08')  # ceasefire announced

fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Top: rolling volatility
for ticker in subset:
    axes[0].plot(rolling_vol.index, rolling_vol[ticker], label=ticker)
axes[0].axvspan(conflict_start, conflict_end, color='gray', alpha=0.2, label='Iran conflict / Hormuz closure')
axes[0].set_title('30-Day Rolling Annualized Volatility')
axes[0].set_ylabel('Annualized Volatility')
axes[0].legend()

# Bottom: cumulative returns
for ticker in subset:
    axes[1].plot(cumulative.index, cumulative[ticker], label=ticker)
axes[1].axvspan(conflict_start, conflict_end, color='gray', alpha=0.2)
axes[1].set_title('Cumulative Returns (Growth of $1)')
axes[1].set_ylabel('Growth Multiplier')
axes[1].legend()

plt.tight_layout()
plt.show()

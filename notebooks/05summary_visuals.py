# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_price_data(filepath):
    """Load a saved price CSV with proper datetime index."""
    return pd.read_csv(filepath, index_col=0, parse_dates=True)

os.makedirs('figures', exist_ok=True)

# %%
adj_close = load_price_data('data/adjusted_close_data.csv')
raw_close = load_price_data('data/raw_close_data.csv')
returns = adj_close.pct_change().dropna()
rolling_vol = returns.rolling(30).std() * (252 ** 0.5)
cumulative = (1 + returns).cumprod()

tariff_start, tariff_end = pd.Timestamp('2025-03-01'), pd.Timestamp('2025-04-30')
hormuz_start, hormuz_end = pd.Timestamp('2026-02-28'), pd.Timestamp('2026-04-08')

# %%
# FIGURE 1: Correlation heatmap, all 8 tickers
fig, ax = plt.subplots(figsize=(9, 7))
corr_matrix = returns.corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            vmin=-0.3, vmax=1.0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
ax.set_title('Daily Return Correlation Matrix (Full 5-Year Window)', fontsize=13, pad=12)
plt.tight_layout()
plt.savefig('figures/01_correlation_heatmap.png', dpi=200)
plt.show()

# %%
# FIGURE 2: Raw vs Adjusted Close, GLD (control) vs JNJ (dividend payer)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].plot(raw_close.index, raw_close['GLD'], label='Raw Close', linewidth=1.5)
axes[0].plot(adj_close.index, adj_close['GLD'], label='Adjusted Close', linewidth=1.5, linestyle='--')
axes[0].set_title('GLD: Raw vs. Adjusted Close\n(No dividend -> should overlap)')
axes[0].set_ylabel('Price ($)')
axes[0].legend()

axes[1].plot(raw_close.index, raw_close['JNJ'], label='Raw Close', linewidth=1.5)
axes[1].plot(adj_close.index, adj_close['JNJ'], label='Adjusted Close', linewidth=1.5, linestyle='--')
axes[1].set_title('JNJ: Raw vs. Adjusted Close\n(Dividend payer -> should diverge)')
axes[1].set_ylabel('Price ($)')
axes[1].legend()

plt.tight_layout()
plt.savefig('figures/02_adjustment_control_check.png', dpi=200)
plt.show()

# %%
# FIGURE 3: Rolling volatility + cumulative returns, both crisis windows shaded
subset = ['XOM', 'GLD', 'SPY']
fig, axes = plt.subplots(2, 1, figsize=(13, 9), sharex=True)

for ticker in subset:
    axes[0].plot(rolling_vol.index, rolling_vol[ticker], label=ticker)
axes[0].axvspan(tariff_start, tariff_end, color='orange', alpha=0.15, label='Liberation Day tariffs (2025)')
axes[0].axvspan(hormuz_start, hormuz_end, color='gray', alpha=0.2, label='Iran conflict / Hormuz closure (2026)')
axes[0].set_title('30-Day Rolling Annualized Volatility')
axes[0].set_ylabel('Annualized Volatility')
axes[0].legend(loc='upper left', fontsize=9)

for ticker in subset:
    axes[1].plot(cumulative.index, cumulative[ticker], label=ticker)
axes[1].axvspan(tariff_start, tariff_end, color='orange', alpha=0.15)
axes[1].axvspan(hormuz_start, hormuz_end, color='gray', alpha=0.2)
axes[1].set_title('Cumulative Returns (Growth of $1)')
axes[1].set_ylabel('Growth Multiplier')
axes[1].legend(loc='upper left', fontsize=9)

plt.tight_layout()
plt.savefig('figures/03_volatility_and_returns_both_events.png', dpi=200)
plt.show()

# %%
# FIGURE 4: Correlation breakdown - baseline vs crisis, grouped bar chart
baseline_xom = returns['SPY'].corr(returns['XOM'])
baseline_gld = returns['SPY'].corr(returns['GLD'])
crisis_xom = returns.loc[tariff_start:tariff_end, 'SPY'].corr(returns.loc[tariff_start:tariff_end, 'XOM'])
crisis_gld = returns.loc[hormuz_start:hormuz_end, 'SPY'].corr(returns.loc[hormuz_start:hormuz_end, 'GLD'])

fig, ax = plt.subplots(figsize=(8, 6))
pairs = ['SPY-XOM\n(Liberation Day)', 'SPY-GLD\n(Hormuz)']
baseline_vals = [baseline_xom, baseline_gld]
crisis_vals = [crisis_xom, crisis_gld]

x = np.arange(len(pairs))
width = 0.35
ax.bar(x - width/2, baseline_vals, width, label='Full-period baseline', color='#4c72b0')
ax.bar(x + width/2, crisis_vals, width, label='During crisis window', color='#c44e52')

ax.set_ylabel('Correlation')
ax.set_title('Correlation Breakdown: Baseline vs. Crisis Window')
ax.set_xticks(x)
ax.set_xticklabels(pairs)
ax.set_ylim(0, max(baseline_vals + crisis_vals) + 0.1)
ax.axhline(0, color='black', linewidth=0.8)
ax.legend()

for i, (b, c) in enumerate(zip(baseline_vals, crisis_vals)):
    ax.text(i - width/2, b + 0.02, f'{b:.2f}', ha='center', fontsize=10)
    ax.text(i + width/2, c + 0.02, f'{c:.2f}', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('figures/04_correlation_breakdown.png', dpi=200)
plt.show()

# %%
# FIGURE 5: Return distribution, SPY vs TLT (fat tails contrast)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

sns.histplot(returns['SPY'], kde=True, ax=axes[0], color='#4c72b0', bins=80)
axes[0].set_title(f"SPY Daily Returns\n(kurtosis={returns['SPY'].kurtosis():.2f}, skew={returns['SPY'].skew():.2f})")
axes[0].set_xlabel('Daily Return')

sns.histplot(returns['TLT'], kde=True, ax=axes[1], color='#55a868', bins=80)
axes[1].set_title(f"TLT Daily Returns\n(kurtosis={returns['TLT'].kurtosis():.2f}, skew={returns['TLT'].skew():.2f})")
axes[1].set_xlabel('Daily Return')

plt.tight_layout()
plt.savefig('figures/05_return_distributions_spy_vs_tlt.png', dpi=200)
plt.show()

print("All figures saved to figures/")

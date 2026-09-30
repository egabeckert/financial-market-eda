# %%
import pandas as pd
from scipy.stats import pearsonr

def load_price_data(filepath):
    """Load a saved price CSV with proper datetime index."""
    return pd.read_csv(filepath, index_col=0, parse_dates=True)

# %%
adj_close = load_price_data('data/adjusted_close_data.csv')
returns = adj_close.pct_change().dropna()

# %%
pairs = [('AAPL', 'QQQ'), ('AAPL', 'XOM'), ('SPY', 'TLT')]
for a, b in pairs:
    corr, p_val = pearsonr(returns[a], returns[b])
    print(f"{a} vs {b}: corr={corr:.3f}, p={p_val:.6f}")

# %%
corr_matrix = returns.corr()
print(corr_matrix)

# %%
rolling_corr_spy_xom = returns['SPY'].rolling(20).corr(returns['XOM'])
rolling_corr_spy_gld = returns['SPY'].rolling(20).corr(returns['GLD'])

# %%
tariff_start, tariff_end = '2025-03-01', '2025-04-30'
hormuz_start, hormuz_end = '2026-02-28', '2026-04-08'

crisis_corr_spy_xom = returns.loc[tariff_start:tariff_end, 'SPY'].corr(returns.loc[tariff_start:tariff_end, 'XOM'])
crisis_corr_spy_gld = returns.loc[hormuz_start:hormuz_end, 'SPY'].corr(returns.loc[hormuz_start:hormuz_end, 'GLD'])

baseline_corr_spy_xom = returns['SPY'].corr(returns['XOM'])
baseline_corr_spy_gld = returns['SPY'].corr(returns['GLD'])

print(f"SPY-XOM: crisis={crisis_corr_spy_xom:.3f}, full-period baseline={baseline_corr_spy_xom:.3f}")
print(f"SPY-GLD: crisis={crisis_corr_spy_gld:.3f}, full-period baseline={baseline_corr_spy_gld:.3f}")

# %%
corr_xom, p_xom = pearsonr(
    returns.loc[tariff_start:tariff_end, 'SPY'],
    returns.loc[tariff_start:tariff_end, 'XOM']
)
corr_gld, p_gld = pearsonr(
    returns.loc[hormuz_start:hormuz_end, 'SPY'],
    returns.loc[hormuz_start:hormuz_end, 'GLD']
)

n_tariff = len(returns.loc[tariff_start:tariff_end])
n_hormuz = len(returns.loc[hormuz_start:hormuz_end])

print(f"SPY-XOM crisis: corr={corr_xom:.3f}, p={p_xom:.6f}, n={n_tariff}")
print(f"SPY-GLD crisis: corr={corr_gld:.3f}, p={p_gld:.6f}, n={n_hormuz}")

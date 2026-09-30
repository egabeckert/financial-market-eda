# %%
import pandas as pd
from scipy import stats

def load_price_data(filepath):
    """Load a saved price CSV with proper datetime index."""
    return pd.read_csv(filepath, index_col=0, parse_dates=True)

# %%
adj_close = load_price_data('data/adjusted_close_data.csv')
returns = adj_close.pct_change().dropna()

# %%
for ticker in returns.columns:
    skew = returns[ticker].skew()
    kurt = returns[ticker].kurtosis()
    stat, p = stats.shapiro(returns[ticker])
    print(f"{ticker}: skew={skew:.3f}, kurtosis={kurt:.3f}, shapiro_p={p:.6f}")

# %%
for ticker in returns.columns:
    t_stat, p_val = stats.ttest_1samp(returns[ticker], 0)
    print(f"{ticker}: t={t_stat:.3f}, p={p_val:.4f}")

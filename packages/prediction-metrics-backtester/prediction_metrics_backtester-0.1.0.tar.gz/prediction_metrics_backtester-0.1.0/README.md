# Enhanced Prediction Metrics Backtester

A flexible backtesting framework for evaluating trading strategies based on prediction metrics. This Python package provides comprehensive tools to simulate trading activity using CSV files containing prediction data and analyze strategy performance with detailed metrics and visualizations.

## Features

- **Comprehensive Backtesting**: Simulate trading strategies using prediction metrics from CSV files
- **Configurable Parameters**: Highly customizable backtesting parameters for different strategies
- **Performance Analytics**: Calculate various performance metrics including Sharpe ratio, maximum drawdown, win rate, and CAGR
- **Rich Visualizations**: Generate detailed charts including equity curves, drawdown analysis, monthly returns heatmap, and trade distribution
- **Flexible Data Loading**: Support for custom data loading functions to work with various data sources
- **Multiple Model Support**: Analyze and compare performance across different prediction models
- **Risk Management**: Built-in stop-loss, take-profit, and position sizing controls

## Installation

### From PyPI (Recommended)

```bash
pip install prediction-metrics-backtester
```

### From Source

```bash
git clone https://github.com/nawihu/prediction-metrics-backtester.git
cd prediction-metrics-backtester
pip install -e .
```

### Dependencies

The package requires Python 3.7+ and the following dependencies:

```bash
pip install pandas numpy matplotlib seaborn
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from prediction_metrics_backtesting import Backtester

# Create backtester instance
backtester = Backtester(
    csv_path="your_data.csv",
    initial_capital=100000,
    position_size_pct=0.1,
    take_profit_pct=0.3,
    stop_loss_pct=0.2
)

# Run backtest and generate report
metrics = backtester.generate_report()
print(f"Total Return: {metrics['total_return']:.2f}%")
```

## Data Format

### Required Columns

Your CSV file must contain the following columns:

| Column | Type | Description | Required |
|--------|------|-------------|----------|
| `timestamp` | datetime | Timestamp of the prediction/signal | ✅ |
| `signal` | string | Trading signal ("buy" or "sell") | ✅ |
| `last_trade_price` | float | Asset price at signal time | ⚠️* |
| `actual_pct_change` | float | Actual percentage change after signal | ⚠️* |

*Either `last_trade_price` or `actual_pct_change` is required

### Optional Columns

| Column | Type | Description |
|--------|------|-------------|
| `model_name` | string | Name of the prediction model |
| `confidence_width` | float | Model confidence measure (lower = higher confidence) |
| `would_hit_tp` | bool | Whether take profit would be hit |
| `would_hit_sl` | bool | Whether stop loss would be hit |

### Example Data

```csv
timestamp,signal,last_trade_price,actual_pct_change,model_name,confidence_width,would_hit_tp,would_hit_sl
2024-04-12 09:30:00,buy,150.00,0.05,LSTM_model_1,0.04,True,False
2024-04-12 10:00:00,sell,150.75,-0.02,LSTM_model_1,0.03,False,False
2024-04-12 10:30:00,buy,149.50,0.08,LSTM_model_2,0.06,True,False
```

## Usage

### Command Line Interface

```bash
# Basic usage
python -m prediction_metrics_backtesting data.csv

# With custom parameters
python -m prediction_metrics_backtesting data.csv \
    --initial-capital 50000 \
    --take-profit 0.1 \
    --stop-loss 0.05 \
    --commission 0.25

# Filter by model
python -m prediction_metrics_backtesting data.csv \
    --model LSTM_model_1 \
    --output-dir model_1_results

# Use risk-reward ratio
python -m prediction_metrics_backtesting data.csv \
    --use-risk-reward \
    --risk-reward 3.0 \
    --stop-loss 0.1
```

### Python API

```python
from prediction_metrics_backtesting import Backtester

# Advanced configuration
backtester = Backtester(
    csv_path="data.csv",
    initial_capital=100000,
    position_size_pct=0.2,
    take_profit_pct=0.5,
    stop_loss_pct=0.3,
    risk_reward_ratio=2.0,
    use_risk_reward_for_tp_sl=True,
    commission_per_trade=1.0,
    slippage_pct=0.01,
    model_filter="LSTM_model_1",
    confidence_threshold=0.05,
    output_dir="my_backtest_results"
)

# Run backtest
metrics = backtester.generate_report()

# Access results
print(f"Win Rate: {metrics['win_rate']:.2f}%")
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `initial_capital` | float | 100000 | Starting capital for backtest |
| `position_size_pct` | float | 0.2 | Position size as fraction of capital (0-1) |
| `take_profit_pct` | float | 0.5 | Take profit target percentage |
| `stop_loss_pct` | float | 0.3 | Stop loss percentage |
| `risk_reward_ratio` | float | 2.0 | Target risk/reward ratio |
| `use_risk_reward_for_tp_sl` | bool | True | Calculate TP based on risk/reward ratio |
| `commission_per_trade` | float | 1.0 | Commission fee per trade |
| `slippage_pct` | float | 0.01 | Slippage percentage |
| `model_filter` | string | None | Filter for specific model name |
| `confidence_threshold` | float | None | Minimum confidence threshold |
| `output_dir` | string | "backtest_results" | Output directory for results |

## Custom Data Loading

For non-CSV data sources, create a custom data loading function:

```python
# my_data_loader.py
import pandas as pd
import sqlite3

def load_data(db_path):
    """Load data from SQLite database"""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    conn.close()
    return df
```

Then use it with the CLI:

```bash
python -m prediction_metrics_backtesting data.db --data-loader my_data_loader.py
```

Or in Python:

```python
from my_data_loader import load_data

backtester = Backtester(
    csv_path="data.db",
    fetch_data_function=load_data
)
```

## Output Files

The backtester generates the following outputs in the specified directory:

| File | Description |
|------|-------------|
| `backtest_report.txt` | Comprehensive performance summary |
| `trades.csv` | Detailed trade-by-trade results |
| `equity_curve.csv` | Equity progression over time |
| `equity_curve.png` | Equity curve visualization |
| `drawdown_chart.png` | Drawdown analysis chart |
| `monthly_returns.png` | Monthly returns heatmap |
| `trade_distribution.png` | Trade P&L distribution histogram |

## Performance Metrics

The backtester calculates comprehensive performance metrics:

### Return Metrics
- **Total Return**: Overall portfolio return percentage
- **CAGR**: Compound Annual Growth Rate
- **Benchmark Return**: Buy-and-hold comparison

### Risk Metrics
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return measure
- **Win Rate**: Percentage of profitable trades

### Trading Metrics
- **Total Trades**: Number of completed trades
- **Profit Factor**: Ratio of gross profit to gross loss
- **Average Trade**: Mean profit/loss per trade

## Examples

### Basic Momentum Strategy

```python
# Simple momentum strategy backtest
backtester = Backtester(
    csv_path="momentum_signals.csv",
    initial_capital=50000,
    position_size_pct=0.15,
    take_profit_pct=0.2,
    stop_loss_pct=0.1
)

results = backtester.generate_report()
```

### High-Frequency Strategy

```python
# High-frequency strategy with tight risk controls
backtester = Backtester(
    csv_path="hf_signals.csv",
    position_size_pct=0.05,
    take_profit_pct=0.05,
    stop_loss_pct=0.02,
    commission_per_trade=0.1,
    slippage_pct=0.001
)
```

### Model Comparison

```python
# Compare different models
models = ["LSTM_v1", "LSTM_v2", "CNN_v1"]
results = {}

for model in models:
    backtester = Backtester(
        csv_path="all_signals.csv",
        model_filter=model,
        output_dir=f"results_{model}"
    )
    results[model] = backtester.generate_report()

# Compare performance
for model, metrics in results.items():
    print(f"{model}: {metrics['total_return']:.2f}% return, "
          f"{metrics['sharpe_ratio']:.2f} Sharpe")
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this software in your research, please cite:

```bibtex
@software{huff2025backtester,
  author = {Huff, Nathaniel William},
  title = {Enhanced Prediction Metrics Backtester},
  year = {2025},
  url = {https://github.com/nawihu/prediction-metrics-backtester}
}
```

## Support

- **Documentation**: [Full documentation](https://github.com/nawihu/prediction-metrics-backtester/wiki)
- **Issues**: [GitHub Issues](https://github.com/nawihu/prediction-metrics-backtester/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nawihu/prediction-metrics-backtester/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

---

**Author**: Nathaniel William Huff  
**Email**: nathanielwilliam117@gmail.com  
**GitHub**: [@nawihu](https://github.com/nawihu)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os
from typing import Dict, List, Optional


class Backtester:
    """Backtest trading strategy using enhanced prediction metrics CSV"""

    def __init__(
            self,
            csv_path: str,
            fetch_data_function: callable = pd.read_csv,  # Default to pandas
            initial_capital: float = 100000,
            position_size_pct: float = 0.2,
            take_profit_pct: float = 0.5,
            stop_loss_pct: float = 0.3,
            risk_reward_ratio: float = 2.0,
            use_risk_reward_for_tp_sl: bool = True,
            commission_per_trade: float = 1.0,
            slippage_pct: float = 0.01,
            model_filter: Optional[str] = None,
            confidence_threshold: Optional[float] = None,
            output_dir: str = "backtest_results",
    ):
        """
        Initialize the backtester with configuration parameters

        Args:
            csv_path: Path to the data source (e.g., CSV file path, database connection string, etc.)
            fetch_data_function: Function to load the data.
                                 It must accept 'csv_path' as its first argument
                                 and return a pandas DataFrame.
            initial_capital: Starting capital for backtest
                       csv_path: Path to the enhanced prediction metrics CSV
            position_size_pct: Position size as percentage of capital (0-1)
            take_profit_pct: Take profit target percentage
            stop_loss_pct: Stop loss percentage
            risk_reward_ratio: Target risk/reward ratio (only used if use_risk_reward_for_tp_sl is True)
            use_risk_reward_for_tp_sl: Use risk/reward ratio to determine take profit based on stop loss
            commission_per_trade: Commission fee per trade
            slippage_pct: Slippage percentage
            model_filter: Filter for specific model name
            confidence_threshold: Minimum confidence threshold to take a trade
            output_dir: Directory to save output files
        """
        self.csv_path = csv_path
        self.fetch_data_function = fetch_data_function  # Store the function
        self.initial_capital = initial_capital
        self.csv_path = csv_path
        self.initial_capital = initial_capital
        self.position_size_pct = position_size_pct
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct
        self.risk_reward_ratio = risk_reward_ratio
        self.use_risk_reward_for_tp_sl = use_risk_reward_for_tp_sl
        self.commission_per_trade = commission_per_trade
        self.slippage_pct = slippage_pct
        self.model_filter = model_filter
        self.confidence_threshold = confidence_threshold
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Results storage
        self.trades = []
        self.equity_curve = []
        self.current_capital = initial_capital
        self.positions = {}

    def load_data(self):
        """Load and prepare data from the CSV file"""
        print(f"Loading data from {self.csv_path}")
        # df = pd.read_csv(self.csv_path)  # Original line

        # --- Replace with user-provided data loading ---
        df = self.fetch_data_function(self.csv_path)  # Call user's function
        # ---------------------------------------------

        # Convert date columns to datetime
        date_cols = ['timestamp', 'prediction_time', 'last_data_timestamp']
        for col in date_cols:
            if col in df.columns and col in df.columns:  # safety check
                df[col] = pd.to_datetime(df[col])

        # Sort by timestamp
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp')
        else:
            raise ValueError("timestamp column is missing")

        # Apply model filter if specified
        if self.model_filter and 'model_name' in df.columns:
            df = df[df['model_name'] == self.model_filter]
            if df.empty:
                raise ValueError(f"No data found for model {self.model_filter}")

        # Apply confidence threshold if specified
        if self.confidence_threshold is not None and 'confidence_width' in df.columns:
            # Lower confidence width means higher confidence
            df = df[df['confidence_width'] <= self.confidence_threshold]
            if df.empty:
                raise ValueError(f"No data meets confidence threshold {self.confidence_threshold}")

        print(f"Loaded {len(df)} prediction records")
        return df

    def run_backtest(self):
        """Execute the backtest simulation"""
        # Load data
        df = self.load_data()

        # Initialize tracking
        self.current_capital = self.initial_capital
        self.equity_curve = [(df.iloc[0]['timestamp'], self.current_capital)]
        self.trades = []
        self.positions = {}

        # Track benchmark (buy and hold from start)
        benchmark_start_price = None
        benchmark_shares = None
        benchmark_equity = []

        # Process each prediction in chronological order
        for idx, row in df.iterrows():
            timestamp = row['timestamp']
            model_name = row['model_name']
            signal = row['signal']

            # For benchmark tracking (if we have price data)
            if 'last_trade_price' in row and pd.notna(row['last_trade_price']):
                current_price = row['last_trade_price']

                # Initialize benchmark on first data point
                if benchmark_start_price is None:
                    benchmark_start_price = current_price
                    benchmark_shares = self.initial_capital / benchmark_start_price

                # Update benchmark value
                benchmark_value = benchmark_shares * current_price
                benchmark_equity.append((timestamp, benchmark_value))
            else:
                # If we don't have price data, we can simulate it from predicted/actual changes
                # This is less accurate but allows us to run without price data
                if idx > 0:
                    prev_row = df.iloc[idx - 1]
                    if 'actual_pct_change' in prev_row and pd.notna(prev_row['actual_pct_change']):
                        # Use the actual percentage change to adjust our simulated price
                        prev_price = self.positions.get('simulated_price', 100.0)  # Default starting price
                        current_price = prev_price * (1 + prev_row['actual_pct_change'] / 100)
                        self.positions['simulated_price'] = current_price
                    else:
                        # If we don't have actual change, use a placeholder
                        current_price = self.positions.get('simulated_price', 100.0)
                else:
                    # For the first data point
                    current_price = 100.0  # Arbitrary starting price
                    self.positions['simulated_price'] = current_price
                    benchmark_start_price = current_price
                    benchmark_shares = self.initial_capital / benchmark_start_price

                # Update benchmark
                benchmark_value = benchmark_shares * current_price
                benchmark_equity.append((timestamp, benchmark_value))

            # Update existing positions - check for stop loss/take profit
            self.update_positions(timestamp, current_price, row)

            # Check for new signal
            if signal in ['buy', 'sell'] and not self.positions.get('active_position'):
                self.process_signal(timestamp, current_price, row)

            # Update equity curve
            self.equity_curve.append((timestamp, self.current_capital))

        # Close any open positions at the end
        if self.positions.get('active_position'):
            self.close_position(
                df.iloc[-1]['timestamp'],
                self.positions.get('simulated_price', df.iloc[-1].get('last_trade_price', 100.0)),
                'backtest_end'
            )

        # Calculate performance metrics
        results = self.calculate_performance_metrics(benchmark_equity)

        # Generate visualizations
        self.generate_visualizations(benchmark_equity)

        return results

    def update_positions(self, timestamp, current_price, row):
        """Update open positions and check for exits"""
        if not self.positions.get('active_position'):
            return

        position = self.positions
        entry_price = position['entry_price']
        position_type = position['position_type']
        stop_loss = position['stop_loss']
        take_profit = position['take_profit']

        # Calculate current P&L
        if position_type == 'long':
            current_pnl_pct = (current_price / entry_price - 1) * 100
            hit_stop = current_price <= stop_loss
            hit_tp = current_price >= take_profit
        else:  # short
            current_pnl_pct = (entry_price / current_price - 1) * 100
            hit_stop = current_price >= stop_loss
            hit_tp = current_price <= take_profit

        # Update position metrics
        position['current_price'] = current_price
        position['current_pnl_pct'] = current_pnl_pct

        # Use data from CSV if available
        if 'would_hit_tp' in row and pd.notna(row['would_hit_tp']):
            hit_tp = row['would_hit_tp']

        if 'would_hit_sl' in row and pd.notna(row['would_hit_sl']):
            hit_stop = row['would_hit_sl']

        # Check exit conditions
        if hit_stop:
            self.close_position(timestamp, current_price, 'stop_loss')
        elif hit_tp:
            self.close_position(timestamp, current_price, 'take_profit')

    def process_signal(self, timestamp, current_price, row):
        """Process a trading signal"""
        signal = row['signal']

        # Skip if invalid signal or already in a position
        if signal not in ['buy', 'sell'] or self.positions.get('active_position'):
            return

        # Calculate position size
        position_size = self.calculate_position_size(row)

        # Skip if position size is too small
        if position_size <= 0:
            return

        # Get predicted change and confidence
        predicted_change = row.get('predicted_pct_change', 0)
        confidence = row.get('confidence_width', 1.0)

        # Open position based on signal
        if signal == 'buy':
            # Apply slippage to entry price
            entry_price = current_price * (1 + self.slippage_pct / 100)

            # Calculate stop loss and take profit levels
            if self.use_risk_reward_for_tp_sl:
                stop_loss = entry_price * (1 - self.stop_loss_pct / 100)
                take_profit = entry_price + (entry_price - stop_loss) * self.risk_reward_ratio
            else:
                stop_loss = entry_price * (1 - self.stop_loss_pct / 100)
                take_profit = entry_price * (1 + self.take_profit_pct / 100)

            # Calculate shares
            shares = position_size / entry_price

            # Record position
            self.positions = {
                'active_position': True,
                'timestamp': timestamp,
                'entry_price': entry_price,
                'position_type': 'long',
                'shares': shares,
                'position_size': position_size,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'current_price': entry_price,
                'current_pnl_pct': 0,
                'signal_data': {
                    'signal': signal,
                    'predicted_change': predicted_change,
                    'confidence': confidence,
                    'model': row.get('model_name')
                }
            }

            # Apply commission
            self.current_capital -= self.commission_per_trade

        elif signal == 'sell':
            # Apply slippage to entry price
            entry_price = current_price * (1 - self.slippage_pct / 100)

            # Calculate stop loss and take profit for short
            if self.use_risk_reward_for_tp_sl:
                stop_loss = entry_price * (1 + self.stop_loss_pct / 100)
                take_profit = entry_price - (stop_loss - entry_price) * self.risk_reward_ratio
            else:
                stop_loss = entry_price * (1 + self.stop_loss_pct / 100)
                take_profit = entry_price * (1 - self.take_profit_pct / 100)

            # Calculate shares
            shares = position_size / entry_price

            # Record position
            self.positions = {
                'active_position': True,
                'timestamp': timestamp,
                'entry_price': entry_price,
                'position_type': 'short',
                'shares': shares,
                'position_size': position_size,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'current_price': entry_price,
                'current_pnl_pct': 0,
                'signal_data': {
                    'signal': signal,
                    'predicted_change': predicted_change,
                    'confidence': confidence,
                    'model': row.get('model_name')
                }
            }

            # Apply commission
            self.current_capital -= self.commission_per_trade

        print(f"Opened {signal} position at {timestamp}: {shares:.2f} shares at ${entry_price:.2f}")

    def close_position(self, timestamp, current_price, reason):
        """Close an open position"""
        if not self.positions.get('active_position'):
            return

        position = self.positions
        position_type = position['position_type']
        entry_price = position['entry_price']
        shares = position['shares']

        # Apply slippage to exit price
        if position_type == 'long':
            exit_price = current_price * (1 - self.slippage_pct / 100)
        else:  # short
            exit_price = current_price * (1 + self.slippage_pct / 100)

        # Calculate profit/loss
        if position_type == 'long':
            profit_pct = (exit_price / entry_price - 1) * 100
        else:  # short
            profit_pct = (entry_price / exit_price - 1) * 100

        profit_amount = position['position_size'] * profit_pct / 100

        # Update capital
        self.current_capital += (position['position_size'] + profit_amount)

        # Apply commission
        self.current_capital -= self.commission_per_trade

        # Record trade
        trade = {
            'entry_time': position['timestamp'],
            'exit_time': timestamp,
            'position_type': position_type,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'shares': shares,
            'profit_pct': profit_pct,
            'profit_amount': profit_amount,
            'close_reason': reason,
            'signal_data': position.get('signal_data', {})
        }

        # Add trade to results
        self.trades.append(trade)

        # Clear position
        self.positions = {
            'active_position': False,
            'simulated_price': current_price  # Keep tracking price for simulation
        }

        print(
            f"Closed {position_type} position at {timestamp}: {shares:.2f} shares at ${exit_price:.2f} for {profit_pct:.2f}% profit")

    def calculate_position_size(self, row):
        """Calculate position size based on available capital and signal confidence"""
        # Base position size
        base_size = self.current_capital * self.position_size_pct

        # Adjust based on confidence if available
        confidence = row.get('confidence_width')
        pred_change = row.get('predicted_pct_change')

        if confidence is not None and pred_change is not None:
            # For confidence width, lower values indicate higher confidence
            # Scale position size inversely with confidence width
            confidence_scalar = 1.0 + (1.0 / (confidence + 0.1))

            # Scale position size with predicted magnitude (larger predicted moves get larger positions)
            magnitude_scalar = 1.0 + (abs(pred_change) / 5.0)

            # Combine factors (can adjust weights as needed)
            position_scalar = (confidence_scalar * 0.3) + (magnitude_scalar * 0.7)

            # Cap at 50% of capital for safety
            return min(base_size * position_scalar, self.current_capital * 0.5)

        return base_size

    def calculate_performance_metrics(self, benchmark_equity):
        """Calculate performance metrics from backtest results"""
        if not self.trades:
            print("No trades executed in backtest")
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'net_profit_pct': 0,
                'final_equity': self.current_capital,
                'max_drawdown': 0,
                'sharpe_ratio': 0
            }

        # Convert trades to DataFrame for analysis
        trades_df = pd.DataFrame(self.trades)

        # Convert equity curve to DataFrame
        equity_df = pd.DataFrame(self.equity_curve, columns=['timestamp', 'equity'])
        equity_df.set_index('timestamp', inplace=True)

        # Calculate daily returns for Sharpe ratio
        equity_df['daily_return'] = equity_df['equity'].pct_change()

        # Basic trade metrics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['profit_pct'] > 0])
        losing_trades = total_trades - winning_trades
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        # Profit metrics
        gross_profit = trades_df[trades_df['profit_pct'] > 0]['profit_pct'].sum() if winning_trades > 0 else 0
        gross_loss = trades_df[trades_df['profit_pct'] <= 0]['profit_pct'].sum() if losing_trades > 0 else 0
        net_profit = gross_profit + gross_loss

        # Calculate profit factor
        profit_factor = abs(gross_profit / gross_loss) if gross_loss < 0 else float('inf')

        # Calculate max drawdown
        equity_df['peak'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['equity'] / equity_df['peak'] - 1) * 100
        max_drawdown = equity_df['drawdown'].min()

        # Calculate Sharpe ratio (annualized, assuming 252 trading days)
        excess_returns = equity_df['daily_return'].dropna() - 0.01 / 252  # Assuming 1% risk-free rate
        sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252) if len(excess_returns) > 0 else 0

        # Calculate CAGR (Compound Annual Growth Rate)
        start_date = equity_df.index[0]
        end_date = equity_df.index[-1]
        years = (end_date - start_date).days / 365.25
        cagr = (self.current_capital / self.initial_capital) ** (1 / years) - 1 if years > 0 else 0

        # Return dictionary of metrics
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate * 100,  # Convert to percentage
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'net_profit': net_profit,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'cagr': cagr * 100,  # Convert to percentage
            'final_equity': self.current_capital,
            'total_return': (self.current_capital / self.initial_capital - 1) * 100,  # Convert to percentage
            'benchmark_return': (benchmark_equity[-1][1] / benchmark_equity[0][1] - 1) * 100 if benchmark_equity else 0
        }

    def generate_visualizations(self, benchmark_equity):
        """Generate visualization charts from backtest results"""
        # 1. Equity Curve
        self.plot_equity_curve(benchmark_equity)

        # 2. Drawdown Chart
        self.plot_drawdown_chart()

        # 3. Monthly Returns
        self.plot_monthly_returns()

        # 4. Trade Distribution
        self.plot_trade_distribution()

    def plot_equity_curve(self, benchmark_equity):
        """Plot equity curve with benchmark comparison"""
        if not self.equity_curve:
            print("No equity data to plot")
            return

        # Convert to DataFrame
        equity_df = pd.DataFrame(self.equity_curve, columns=['timestamp', 'equity'])
        equity_df.set_index('timestamp', inplace=True)

        # Plot equity curve
        plt.figure(figsize=(12, 6))
        plt.plot(equity_df.index, equity_df['equity'], label='Strategy')

        # Add benchmark if available
        if benchmark_equity:
            benchmark_df = pd.DataFrame(benchmark_equity, columns=['timestamp', 'equity'])
            benchmark_df.set_index('timestamp', inplace=True)
            plt.plot(benchmark_df.index, benchmark_df['equity'], linestyle='--', label='Benchmark (Buy & Hold)')

        plt.title('Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Equity ($)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save figure
        plt.savefig(f"{self.output_dir}/equity_curve.png")

    def plot_drawdown_chart(self):
        """Plot drawdown chart"""
        if not self.equity_curve:
            return

        # Convert to DataFrame
        equity_df = pd.DataFrame(self.equity_curve, columns=['timestamp', 'equity'])
        equity_df.set_index('timestamp', inplace=True)

        # Calculate drawdown
        equity_df['peak'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['equity'] / equity_df['peak'] - 1) * 100

        # Plot drawdown
        plt.figure(figsize=(12, 6))
        plt.plot(equity_df.index, equity_df['drawdown'])
        plt.fill_between(equity_df.index, equity_df['drawdown'], 0, alpha=0.3, color='red')
        plt.title('Drawdown Chart')
        plt.xlabel('Date')
        plt.ylabel('Drawdown (%)')
        plt.grid(True)
        plt.tight_layout()

        # Save figure
        plt.savefig(f"{self.output_dir}/drawdown_chart.png")

    def plot_monthly_returns(self):
        """Plot monthly returns heatmap"""
        if not self.equity_curve:
            return

        # Convert to DataFrame
        equity_df = pd.DataFrame(self.equity_curve, columns=['timestamp', 'equity'])
        equity_df.set_index('timestamp', inplace=True)

        # Calculate daily returns
        equity_df['daily_return'] = equity_df['equity'].pct_change()

        # Resample to get monthly returns
        monthly_returns = equity_df['daily_return'].resample('M').apply(
            lambda x: (1 + x).prod() - 1
        ) * 100  # Convert to percentage

        # Reshape for heatmap (year x month)
        monthly_returns_table = monthly_returns.to_frame()
        monthly_returns_table['year'] = monthly_returns_table.index.year
        monthly_returns_table['month'] = monthly_returns_table.index.month
        monthly_returns_pivot = monthly_returns_table.pivot_table(
            index='year',
            columns='month',
            values='daily_return',
            aggfunc='sum'
        )

        # Plot heatmap if we have enough data
        if not monthly_returns_pivot.empty and monthly_returns_pivot.size > 1:
            plt.figure(figsize=(12, 6))
            sns.heatmap(monthly_returns_pivot, annot=True, fmt=".2f", cmap="RdYlGn",
                        center=0, linewidths=1, cbar_kws={"label": "Return %"})
            plt.title('Monthly Returns (%)')
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/monthly_returns.png")

    def plot_trade_distribution(self):
        """Plot trade distribution (profit/loss histogram)"""
        if not self.trades:
            return

        # Convert to DataFrame
        trades_df = pd.DataFrame(self.trades)

        # Plot profit distribution
        plt.figure(figsize=(12, 6))

        # Plot histogram
        sns.histplot(trades_df['profit_pct'], bins=20, kde=True)

        # Add vertical line at zero
        plt.axvline(x=0, color='r', linestyle='--')

        plt.title('Trade Profit/Loss Distribution')
        plt.xlabel('Profit/Loss (%)')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.tight_layout()

        # Save figure
        plt.savefig(f"{self.output_dir}/trade_distribution.png")

    def generate_report(self):
        """Generate a comprehensive performance report"""
        # Run backtest to get results
        metrics = self.run_backtest()

        # Create report content
        report = [
            f"Backtest Performance Report",
            f"=========================",
            f"",
            f"Configuration:",
            f"  Initial Capital: ${self.initial_capital:,.2f}",
            f"  Position Size: {self.position_size_pct:.1%} of capital",
            f"  Take Profit: {self.take_profit_pct:.2f}%",
            f"  Stop Loss: {self.stop_loss_pct:.2f}%",
            f"  Risk/Reward Ratio: {self.risk_reward_ratio:.1f}",
            f"  Commission: ${self.commission_per_trade:.2f} per trade",
            f"  Slippage: {self.slippage_pct:.2f}%",
            f"",
            f"Performance Summary:",
            f"  Total Trades: {metrics['total_trades']}",
            f"  Win Rate: {metrics['win_rate']:.2f}%",
            f"  Profit Factor: {metrics['profit_factor']:.2f}",
            f"  Net Profit: {metrics['net_profit']:.2f}%",
            f"  Total Return: {metrics['total_return']:.2f}%",
            f"  Benchmark Return: {metrics['benchmark_return']:.2f}%",
            f"  CAGR: {metrics['cagr']:.2f}%",
            f"  Max Drawdown: {metrics['max_drawdown']:.2f}%",
            f"  Sharpe Ratio: {metrics['sharpe_ratio']:.2f}",
            f"  Final Equity: ${metrics['final_equity']:,.2f}",
            f"",
            f"Trade Statistics:",
            f"  Winning Trades: {metrics['winning_trades']}",
            f"  Losing Trades: {metrics['losing_trades']}",
            f"  Gross Profit: {metrics['gross_profit']:.2f}%",
            f"  Gross Loss: {metrics['gross_loss']:.2f}%",
        ]

        # Save report to file
        report_path = f"{self.output_dir}/backtest_report.txt"
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))

        print(f"Report saved to {report_path}")

        # Export trade details to CSV
        if self.trades:
            trades_df = pd.DataFrame(self.trades)
            trades_df.to_csv(f"{self.output_dir}/trades.csv", index=False)
            print(f"Trade details saved to {self.output_dir}/trades.csv")

        # Export equity curve to CSV
        if self.equity_curve:
            equity_df = pd.DataFrame(self.equity_curve, columns=['timestamp', 'equity'])
            equity_df.to_csv(f"{self.output_dir}/equity_curve.csv", index=False)
            print(f"Equity curve saved to {self.output_dir}/equity_curve.csv")

        return metrics


def main():
    """Main function to run enhanced backtester"""
    parser = argparse.ArgumentParser(
        description="Enhanced Prediction Metrics Backtesting"
    )

    parser.add_argument(
        "csv_path", type=str, help="Path to enhanced prediction metrics CSV file"
    )
    parser.add_argument(
        "--initial-capital", type=float, default=100000, help="Initial capital"
    )
    parser.add_argument(
        "--position-size",
        type=float,
        default=0.2,
        help="Position size as fraction of capital",
    )
    parser.add_argument(
        "--take-profit", type=float, default=0.5, help="Take profit percentage"
    )
    parser.add_argument(
        "--stop-loss", type=float, default=0.25, help="Stop loss percentage"
    )
    parser.add_argument(
        "--risk-reward", type=float, default=2.0, help="Risk/reward ratio"
    )
    parser.add_argument(
        "--use-risk-reward",
        action="store_true",
        help="Use risk/reward ratio for take profit calculation",
    )
    parser.add_argument(
        "--commission", type=float, default=1.0, help="Commission per trade"
    )
    parser.add_argument(
        "--slippage", type=float, default=0.01, help="Slippage percentage"
    )
    parser.add_argument(
        "--model", type=str, help="Filter for specific model name"
    )
    parser.add_argument(
        "--confidence",
        type=float,
        help="Confidence threshold (lower is more confident)",
    )
    parser.add_argument(
        "--output-dir", type=str, default="backtest_results", help="Output directory"
    )
    # Add an argument for the custom data loading function
    parser.add_argument(
        "--data-loader",
        type=str,
        help="Path to a Python file containing a function to load data",
    )

    args = parser.parse_args()

    # Custom data loading function (if provided)
    data_loader_func = pd.read_csv  # Default to pandas
    if args.data_loader:
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "data_loader", args.data_loader
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            data_loader_func = module.load_data  # User's function
            print(f"Using custom data loading function from {args.data_loader}")
        except ImportError as e:
            print(f"Error importing data loading function: {e}. Using default pandas read_csv")
        except AttributeError as e:
            print(f"Error: load_data function not found in {args.data_loader}. Using default pandas read_csv")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Using default pandas read_csv")

    # Create and run backtester
    backtester = Backtester(
        csv_path=args.csv_path,
        fetch_data_function=data_loader_func,  # Pass the function
        initial_capital=args.initial_capital,
        position_size_pct=args.position_size,
        take_profit_pct=args.take_profit,
        stop_loss_pct=args.stop_loss,
        risk_reward_ratio=args.risk_reward,
        use_risk_reward_for_tp_sl=args.use_risk_reward,
        commission_per_trade=args.commission,
        slippage_pct=args.slippage,
        model_filter=args.model,
        confidence_threshold=args.confidence,
        output_dir=args.output_dir,
    )

    # Generate report (this also runs the backtest)
    metrics = backtester.generate_report()

    # Print summary
    print("\nBacktest Summary:")
    print(f"Total Trades: {metrics['total_trades']}")
    print(f"Win Rate: {metrics['win_rate']:.2f}%")
    print(f"Net Profit: {metrics['net_profit']:.2f}%")
    print(f"Total Return: {metrics['total_return']:.2f}%")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")

if __name__ == "__main__":
    main()

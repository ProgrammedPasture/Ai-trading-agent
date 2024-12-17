import pandas as pd
import matplotlib.pyplot as plt
import os


def visualize_indicators(file_path):
    """
    Visualize Positive Volatility, Volume Gauge, and Momentum Oscillator.

    :param file_path: Path to the CSV file containing calculated indicators.
    """
    # Load the indicators from CSV
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)


    # Plot 1: Positive Volatility and Upper Signal Line
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['positive_volatility'], label="Positive Volatility", color='blue')
    plt.plot(data.index, data['upper_signal'], label="Upper Signal", color='orange', linestyle='--')
    plt.title("Positive Volatility vs. Upper Signal Line")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.legend()
    plt.grid()
    plt.show()


    # Plot 2: Volume Gauge (Bar Plot with Threshold Colors)
    volume_colors = data['volume_color'].map({
        'High': 'green',
        'Low': 'red',
        'Medium': 'yellow'
    })
    plt.figure(figsize=(12, 6))
    plt.bar(data.index, data['volume_gauge'], color=volume_colors)
    plt.title("Volume Gauge with Dynamic Threshold Colors")
    plt.xlabel("Date")
    plt.ylabel("Volume Gauge")
    plt.grid()
    plt.show()


    # Plot 3: Momentum Oscillator with Oversold and Overbought Levels
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['momentum'], label="Momentum Oscillator", color='green')
    plt.axhline(data['mom_oversold'].iloc[0], color='red', linestyle='--', label="Oversold Level")
    plt.axhline(data['mom_overbought'].iloc[0], color='green', linestyle='--', label="Overbought Level")
    plt.title("Momentum Oscillator")
    plt.xlabel("Date")
    plt.ylabel("Momentum")
    plt.legend()
    plt.grid()
    plt.show()


# Example usage
if __name__ == "__main__":
    file_path = "../../data/calculated_indicators_AAPL.csv"  # Adjust path if needed
    visualize_indicators(file_path)

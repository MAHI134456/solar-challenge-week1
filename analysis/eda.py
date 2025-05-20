import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import numpy as np

def perform_eda(csv_file, country, output_dir='scripts'):
    # Loading the data
    df = pd.read_csv(csv_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Summary statistics and missing values
    print(f"\nSummary statistics for {country}:")
    print(df.describe())
    print(f"\nMissing value for {country}:")
    missing = df.isnull().sum()
    print(missing)
    missing_pct = ((missing / len(df)) * 100)
    print(f"\nColumns with >5% missing values:")
    print(missing_pct[missing_pct > 5])

    # Outlier detection and cleaning
    numeric_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
    z_scores = df[numeric_cols].apply(stats.zscore)
    outliers = (z_scores.abs() > 3).any(axis=1)
    print(f"\nOutliers (|z|>3) for {country}: {outliers.sum()} rows")

    # Impute missing values with median for key columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    
    # Export cleaned data
    cleaned_csv = f'data/{country}_clean.csv'
    df.to_csv(cleaned_csv, index=False)
    print(f"Cleaned data saved to {cleaned_csv}")

    # Time series analysis
    z_scores_ghi = stats.zscore(df['GHI'], nan_policy='omit')
    anomalies = df[z_scores_ghi.abs() > 3]
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df['Timestamp'], df['GHI'], label='GHI', color='blue')
    ax1.plot(df['Timestamp'], df['DNI'], label='DNI', color='green')
    ax1.plot(df['Timestamp'], df['DHI'], label='DHI', color='red')
    if not anomalies.empty:
        ax1.scatter(anomalies['Timestamp'], anomalies['GHI'], color='black', label='GHI Anomalies (|Z|>3)', marker='x')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Irradiance (W/m²)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True)
    ax1.legend(loc='upper left')
    plt.xticks(rotation=45)
    ax2 = ax1.twinx()
    ax2.plot(df['Timestamp'], df['Tamb'], label='Tamb', color='orange', linestyle='--')
    ax2.set_ylabel('Temperature (°C)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.legend(loc='upper right')
    plt.title(f'Solar Irradiance and Temperature Over Time ({country})')
    fig.tight_layout()
    time_plot = f'{output_dir}/{country}_ghi_time.png'
    plt.savefig(time_plot)
    plt.show()
    print(f"\nGHI Anomalies (|Z|>3) for {country}: {len(anomalies)} rows")

    # Bar chart of monthly pattern 
    df['Month'] = df['Timestamp'].dt.month
    monthly_avg = df.groupby('Month')[['GHI', 'DNI', 'DHI', 'Tamb']].mean()
    monthly_avg.plot(kind='bar', figsize=(12, 6))
    plt.title(f'Monthly Average Irradiance and Temperature ({country})')
    plt.xlabel('Month')
    plt.ylabel('Average Irradiance (W/m²) and Temperature (°C)')
    plt.legend()
    plt.tight_layout()
    monthly_plot = f'{output_dir}/{country}_monthly.png'
    plt.savefig(monthly_plot)
    plt.show()
    print(f"\nMonthly Averages for {country}:")
    print(monthly_avg)
    
    # Daily trends 
    df['Hour'] = df['Timestamp'].dt.hour
    hourly_avg = df.groupby('Hour')[['GHI', 'DNI', 'DHI']].mean()
    hourly_avg.plot(kind='line', figsize=(12, 6))
    plt.title(f'Hourly Average Irradiance ({country})')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Irradiance (W/m²)')
    plt.grid(True)
    plt.tight_layout()
    hourly_plot = f'{output_dir}/{country}_hourly.png'
    plt.savefig(hourly_plot)
    plt.show()
    print(f"\nHourly Averages for {country}:")
    print(hourly_avg)

    # Cleaning Impact
    cleaning_impact = df.groupby('Cleaning')[['ModA', 'ModB']].mean()
    print(f"\nCleaning Impact for {country}:")
    print(cleaning_impact)
    cleaning_impact.plot(kind='bar', title=f'ModA & ModB Pre/Post Cleaning ({country})')
    plt.ylabel('Mean Value (W/m²)')
    plt.tight_layout()
    cleaning_plot = f'{output_dir}/{country}_cleaning.png'
    plt.savefig(cleaning_plot)
    plt.show()

    # Correlation Analysis
    corr_cols = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB']
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[corr_cols].corr(), annot=True, cmap='coolwarm')
    plt.title(f'Correlation Heatmap ({country})')
    corr_plot = f'{output_dir}/{country}_corr.png'
    plt.savefig(corr_plot)
    plt.show()

    # Scatter Plots
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.scatter(df['WS'], df['GHI'], alpha=0.5)
    plt.title(f'WS vs GHI ({country})')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('GHI (W/m²)')
    
    plt.subplot(1, 3, 2)
    plt.scatter(df['RH'], df['GHI'], alpha=0.5)
    plt.title(f'RH vs GHI ({country})')
    plt.xlabel('Relative Humidity (%)')
    
    plt.subplot(1, 3, 3)
    plt.scatter(df['RH'], df['Tamb'], alpha=0.5)
    plt.title(f'RH vs Tamb ({country})')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Tamb (°C)')
    plt.tight_layout()
    scatter_plot = f'{output_dir}/{country}_scatter.png'
    plt.savefig(scatter_plot)
    plt.show()

    # Wind Analysis
    # Radial bar plot for wind speed and direction
    bins = np.arange(0, 360 + 45, 45)
    labels = [f'{int(b)}-{int(b+45)}' for b in bins[:-1]]
    wd_binned = pd.cut(df['WD'], bins=bins, labels=labels, include_lowest=True)
    ws_mean = df['WS'].groupby(wd_binned).mean()
    angles = np.linspace(0, 2 * np.pi, len(ws_mean), endpoint=False)
    widths = np.pi / 4  # 45 degrees per bar
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.bar(angles, ws_mean, width=widths, edgecolor='white', alpha=0.7)
    ax.set_xticks(angles)
    ax.set_xticklabels(ws_mean.index)
    ax.set_title(f'Wind Direction and Speed ({country})')
    wind_plot = f'{output_dir}/{country}_wind_radial.png'
    plt.savefig(wind_plot)
    plt.show()

    # Histogram
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.hist(df['GHI'], bins=20)
    plt.title(f'GHI Distribution ({country})')
    plt.xlabel('GHI (W/m²)')
    
    plt.subplot(1, 3, 2)
    plt.hist(df['WS'], bins=20)
    plt.title(f'Wind Speed Distribution ({country})')
    plt.xlabel('Wind Speed (m/s)')

    plt.subplot(1, 3, 3)
    plt.hist(df['RH'], bins=20)
    plt.title(f'Relative Humidity Distribution ({country})')
    plt.xlabel('Relative Humidity (%)')
    plt.tight_layout()
    hist_plot = f'{output_dir}/{country}_hist.png'
    plt.savefig(hist_plot)
    plt.show()

    # Bubble Chart
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Tamb'], df['GHI'], s=df['RH']*10, alpha=0.5)
    plt.title(f'GHI vs Tamb, Bubble Size = RH ({country})')
    plt.xlabel('Tamb (°C)')
    plt.ylabel('GHI (W/m²)')
    plt.grid(True)
    bubble_plot = f'{output_dir}/{country}_bubble.png'
    plt.savefig(bubble_plot)
    plt.show()

    return df
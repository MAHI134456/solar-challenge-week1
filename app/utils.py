import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_process_data(benin_file, togo_file, sierra_file):
    """Load and combine cleaned CSV files with a Country column."""
    benin = pd.read_csv(benin_file)
    togo = pd.read_csv(togo_file)
    sierra = pd.read_csv(sierra_file)
    
    benin['Country'] = 'Benin'
    togo['Country'] = 'Togo'
    sierra['Country'] = 'Sierra Leone'
    
    return pd.concat([benin, togo, sierra], ignore_index=True)

def create_boxplot(data, metric):
    """Create a boxplot for the specified metric."""
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Country', y=metric, data=data, palette='Set2')
    plt.title(f'{metric} Distribution by Country')
    plt.xlabel('Country')
    plt.ylabel(f'{metric} (W/m²)')
    plt.tight_layout()
    return plt

def create_ghi_ranking(data):
    """Create a bar chart ranking countries by average GHI."""
    avg_ghi = data.groupby('Country')['GHI'].mean().sort_values(ascending=False)
    plt.figure(figsize=(8, 6))
    sns.barplot(x=avg_ghi.values, y=avg_ghi.index, palette='Set2')
    plt.title('Average GHI Ranking by Country')
    plt.xlabel('Mean GHI (W/m²)')
    plt.ylabel('Country')
    plt.tight_layout()
    return plt
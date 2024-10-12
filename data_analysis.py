import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
restaurant_data = pd.read_csv('C:/Users/juanc/OneDrive/Documents/icwucn_projects/icwucn2025k/restaurant_orders_cleaned.csv')
tattoo_data = pd.read_csv('C:/Users/juanc/OneDrive/Documents/icwucn_projects/icwucn2025k/tattoo_shop_orders_cleaned.csv')

# Convert 'date' to datetime format
restaurant_data['date'] = pd.to_datetime(restaurant_data['date'])
tattoo_data['date'] = pd.to_datetime(tattoo_data['date'])

# Set 'date' as index
restaurant_data.set_index('date', inplace=True)
tattoo_data.set_index('date', inplace=True)

# Descriptive statistics
print("Restaurant Data Description:")
print(restaurant_data.describe())
print("\nTattoo Shop Data Description:")
print(tattoo_data.describe())

# Combine data for correlation analysis
combined_data = pd.DataFrame({
    'restaurant_orders': restaurant_data['orders'],
    'tattoo_orders': tattoo_data['orders']
})

# Drop any rows with NaN values for correlation
combined_data.dropna(inplace=True)

# Calculate correlation matrix
correlation_matrix = combined_data.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Plot heatmap for correlations
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap')
plt.show()

# Time Series Analysis
plt.figure(figsize=(14, 7))
plt.plot(restaurant_data.index, restaurant_data['orders'], label='Restaurant Orders', color='blue')
plt.plot(tattoo_data.index, tattoo_data['orders'], label='Tattoo Shop Orders', color='orange')
plt.title('Orders Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

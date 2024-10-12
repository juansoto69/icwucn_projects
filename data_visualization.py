import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
restaurant_data = pd.read_csv('C:\\Users\\juanc\\OneDrive\\Documents\\icwucn_projects\\icwucn2025k\\restaurant_orders_cleaned.csv')
tattoo_data = pd.read_csv('C:\\Users\\juanc\\OneDrive\\Documents\\icwucn_projects\\icwucn2025k\\tattoo_shop_orders_cleaned.csv')

# Convert 'date' column to datetime
restaurant_data['date'] = pd.to_datetime(restaurant_data['date'])
tattoo_data['date'] = pd.to_datetime(tattoo_data['date'])

# Set the date as the index
restaurant_data.set_index('date', inplace=True)
tattoo_data.set_index('date', inplace=True)

# Plotting Restaurant Orders
plt.figure(figsize=(14, 6))
plt.plot(restaurant_data.index, restaurant_data['orders'], marker='o', label='Restaurant Orders')
plt.title('Restaurant Orders Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('restaurant_orders_trend.png')
plt.show()

# Plotting Tattoo Shop Orders
plt.figure(figsize=(14, 6))
plt.plot(tattoo_data.index, tattoo_data['orders'], marker='o', color='orange', label='Tattoo Shop Orders')
plt.title('Tattoo Shop Orders Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('tattoo_shop_orders_trend.png')
plt.show()

# Seaborn Visualization
plt.figure(figsize=(14, 6))
sns.lineplot(data=restaurant_data.reset_index(), x='date', y='orders', marker='o', label='Restaurant Orders')
sns.lineplot(data=tattoo_data.reset_index(), x='date', y='orders', marker='o', color='orange', label='Tattoo Shop Orders')
plt.title('Comparison of Orders Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('comparison_orders_trend.png')
plt.show()

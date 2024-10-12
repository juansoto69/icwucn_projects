import pandas as pd
from prophet import Prophet

# Load your data
restaurant_data = pd.read_csv('C:/Users/juanc/OneDrive/Documents/icwucn_projects/icwucn2025k/restaurant_orders.csv')
tattoo_data = pd.read_csv('C:/Users/juanc/OneDrive/Documents/icwucn_projects/icwucn2025k/tattoo_shop_orders.csv')

# Prepare the dataset for Prophet
restaurant_prophet_data = restaurant_data[['date', 'orders']].rename(columns={'date': 'ds', 'orders': 'y'})
tattoo_prophet_data = tattoo_data[['date', 'orders']].rename(columns={'date': 'ds', 'orders': 'y'})

# Create and train the restaurant model
restaurant_model = Prophet()
restaurant_model.fit(restaurant_prophet_data)

# Create and train the tattoo shop model
tattoo_model = Prophet()
tattoo_model.fit(tattoo_prophet_data)

# Make future predictions for the restaurant
restaurant_future = restaurant_model.make_future_dataframe(periods=30)
restaurant_forecast = restaurant_model.predict(restaurant_future)

# Make future predictions for the tattoo shop
tattoo_future = tattoo_model.make_future_dataframe(periods=30)
tattoo_forecast = tattoo_model.predict(tattoo_future)

# Output the forecasts
print("Restaurant Forecast:")
print(restaurant_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

print("\nTattoo Shop Forecast:")
print(tattoo_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
import pandas as pd
from prophet import Prophet
import plotly.graph_objs as go

# Load your data
restaurant_data = pd.read_csv('C:/Users/juanc/OneDrive/Documents/icwucn_projects/icwucn2025k/restaurant_orders.csv')
tattoo_data = pd.read_csv('C:/Users/juanc/OneDrive/Documents/icwucn_projects/icwucn2025k/tattoo_shop_orders.csv')

# Prepare the dataset for Prophet
restaurant_prophet_data = restaurant_data[['date', 'orders']].rename(columns={'date': 'ds', 'orders': 'y'})
tattoo_prophet_data = tattoo_data[['date', 'orders']].rename(columns={'date': 'ds', 'orders': 'y'})

# Create and train the restaurant model
restaurant_model = Prophet()
restaurant_model.fit(restaurant_prophet_data)

# Create and train the tattoo shop model
tattoo_model = Prophet()
tattoo_model.fit(tattoo_prophet_data)

# Make future predictions for the restaurant
restaurant_future = restaurant_model.make_future_dataframe(periods=30)
restaurant_forecast = restaurant_model.predict(restaurant_future)

# Make future predictions for the tattoo shop
tattoo_future = tattoo_model.make_future_dataframe(periods=30)
tattoo_forecast = tattoo_model.predict(tattoo_future)

# Output the forecasts
print("Restaurant Forecast:")
print(restaurant_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

print("\nTattoo Shop Forecast:")
print(tattoo_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

# Plot Restaurant Forecast
fig_restaurant = go.Figure()
fig_restaurant.add_trace(go.Scatter(x=restaurant_forecast['ds'], y=restaurant_forecast['yhat'],
                                     mode='lines', name='Predicted Orders'))
fig_restaurant.add_trace(go.Scatter(x=restaurant_forecast['ds'], y=restaurant_forecast['yhat_lower'],
                                     mode='lines', name='Lower Bound', line=dict(dash='dash')))
fig_restaurant.add_trace(go.Scatter(x=restaurant_forecast['ds'], y=restaurant_forecast['yhat_upper'],
                                     mode='lines', name='Upper Bound', line=dict(dash='dash')))
fig_restaurant.update_layout(title='Restaurant Order Forecast',
                              xaxis_title='Date',
                              yaxis_title='Number of Orders',
                              legend=dict(x=0, y=1))

# Show the Restaurant Forecast
fig_restaurant.show()

# Plot Tattoo Shop Forecast
fig_tattoo = go.Figure()
fig_tattoo.add_trace(go.Scatter(x=tattoo_forecast['ds'], y=tattoo_forecast['yhat'],
                                 mode='lines', name='Predicted Orders'))
fig_tattoo.add_trace(go.Scatter(x=tattoo_forecast['ds'], y=tattoo_forecast['yhat_lower'],
                                 mode='lines', name='Lower Bound', line=dict(dash='dash')))
fig_tattoo.add_trace(go.Scatter(x=tattoo_forecast['ds'], y=tattoo_forecast['yhat_upper'],
                                 mode='lines', name='Upper Bound', line=dict(dash='dash')))
fig_tattoo.update_layout(title='Tattoo Shop Order Forecast',
                          xaxis_title='Date',
                          yaxis_title='Number of Orders',
                          legend=dict(x=0, y=1))

# Show the Tattoo Shop Forecast
fig_tattoo.show()

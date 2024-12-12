# Fermata Energy

Day-Ahead Building Load Forecasting 

Challenge Summary: 
- Train a timeseries forecasting model for building energy demand. The model will predict the next 24 hours of building demand at an interval of 15 minutes. The model should be able to generate predictions for buildings not explicitly included in the training set. 
- Context Impact: Forecasted building energy load is a key input into Fermata's optimization models, which are responsible for charging and discharging V2X-enabled EV batteries. The accuracy of a load forecast has a direct and measurable impact on the economics of Fermata's V2X deployments.
- Approach: Modeling approaches include statistical autoregressive models (SARIMAX), Random Forest, Gradient Boosted Decision Trees, classic ML-based linear regression, and Persistence model which uses the previous 24 hours to predict the next 24 hours.

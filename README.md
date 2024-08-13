# Fermata Energy

Day-Ahead Building Load Forecasting 

Challenge Summary: 
- Train a timeseries forecasting model for building energy demand. The model will predict the next 24 hours of building demand at an interval of 15 minutes. The model should be able to generate predictions for buildings not explicitly included in the training set. 
- Context Impact: Forecasted building energy load is a key input into Fermata's optimization models, which are responsible for charging and discharging V2X-enabled EV batteries. The accuracy of a load forecast has a direct and measurable impact on the economics of Fermata's V2X deployments.
- Suggested Approach: Modeling approaches may include statistical autoregressive models (ie: ARIMA, SARIMAX), classic ML-based regression (ie: random or gradient-boosted trees) or deep learning. In addition to leveraging autoregressive features, consider how you would incorporate exogenous information such as weather dat

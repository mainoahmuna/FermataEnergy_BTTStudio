# Fermata Energy Building Demand Forecasting ✨

[![Contributors](https://contrib.rocks/image?repo=mainoahmuna/FermataEnergy_BTTStudio)](https://github.com/mainoahmuna/FermataEnergy_BTTStudio/graphs/contributors)

[![Contributors](https://img.shields.io/badge/contributors-5-brightgreen)](#credits-and-acknowledgments)

[View Final Presentation](https://docs.google.com/presentation/d/1hNWK2RBWMXfDfkOpyrGVRlA4LNeisJycWgmE_2mB8h0/edit?usp=sharing)

## Project Overview, Objectives, and Goals 🎮
This project aims to develop a time series forecasting model to predict building energy demand for the next 24 hours at 15-minute intervals. The model must generalize to buildings not explicitly included in the training dataset. The ultimate goal is to enhance the accuracy of load forecasts, which directly impacts the efficiency and economics of Fermata’s V2X-enabled EV battery deployments.

### Objectives:
- Predict 24-hour building energy demand with 15-minute granularity.
- Ensure the model performs well on unseen buildings.
- Support Fermata’s optimization models by providing precise load forecasts to maximize the economic benefits of V2X technology.

### Problem Significance ⚡️:
Forecasting building energy load is critical for optimizing the charging and discharging cycles of V2X-enabled EV batteries. Accurate forecasts improve decision-making, reduce costs, and enhance the sustainability of energy systems.

## Methodology 🔢

### Data Collection and Preprocessing:
- Utilized the [ComStock Dataset](https://comstock.nrel.gov/), an open-source simulated dataset for U.S. commercial buildings.
  - Metadata.csv: Building characteristics (building_id, location, type).
  - Load.csv: 15-minute intervals, one-year time series.
  - Weather.csv: Hourly temperature & humidity, one-year time series.
- Addressed challenges such as seasonality, trends, and class imbalance in time-series data.
- One-hot encoded metadata and added engineered features, including heat index, weekday/weekend indicators, and max/min temperature/load per hour.

### Modeling Approaches:

| Model Name                       | Description                                                                 | Train SMAPE | Test SMAPE | Pros                                            | Cons                                     |
|----------------------------------|-----------------------------------------------------------------------------|-------------|------------|------------------------------------------------|------------------------------------------|
| **Persistence Model**            | Use the prior 24 hours to predict the next 24 hours                        | ~19.05      | ~18.95     | Simple prediction method, computationally inexpensive | SMAPE score can be improved by using different models |
|                                  | Accounting for Workday                                                     | ~14.64      | ~18.97     |                                                |                                          |
| **Linear Regression**            | Classic linear regression using weather and building metadata to predict load |             | ~87.8      | Simple, easy to implement                      | SMAPE score is not great                 |
| **Random Forest**                | An ensemble method combining decision trees to improve accuracy and reduce overfitting | ~11.7       | ~29.0      | Handles high-dimensional data                 | Slow training time and memory consumption, some overfitting |
| **CatBoostRegressor**            | Builds trees sequentially to correct previous errors for better predictions | ~37.7       | ~39.8      | Handles categorical features well, minimal overfitting | Computationally expensive (CPU and RAM) |
| **XGBoost Gradient-Boosted Tree**| An ensemble gradient-boosted decision tree utilizing parallel processing   | ~33.7       | ~33.2      | Handles categorical and numerical features, minimal overfitting | High memory usage                        |
| **SARIMAX**                      | A time series model accounting for seasonality, trends, and external factors | ~30.2       | ~54.7      | Captures seasonality, trends, and external influences effectively | Requires careful parameter tuning, some overfitting |

### Tools and Resources ⚙️:
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/-Scikit%20Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-11557C?style=flat&logo=python&logoColor=white)
![Google Colab](https://img.shields.io/badge/-Google%20Colab-F9AB00?style=flat&logo=google-colab&logoColor=white)
![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github&logoColor=white)
![Jira](https://img.shields.io/badge/-Jira-0052CC?style=flat&logo=jira&logoColor=white)
![Slack](https://img.shields.io/badge/-Slack-4A154B?style=flat&logo=slack&logoColor=white)

## Results and Key Findings 🔄
- Persistence model outperformed advanced models, emphasizing the importance of simplicity in certain scenarios.
- Cold climates exhibited higher electricity use, even in warm seasons, while hot climates depended on electric cooling.
- Daily and weekly patterns strongly correlated with building schedules.
- Feature engineering (e.g., adding heat index) improved model interpretability and performance.

## Potential Next Steps 🔼
- Conduct deeper hyperparameter tuning to enhance model performance.
- Explore additional features, such as lagged values and seasonal indicators.
- Investigate cutting-edge models, including transformers and ensemble methods.
- Scale computational resources using cloud solutions for better scalability.

## License 🔒
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits and Acknowledgments ❤️
- **Contributors**: Riley Denn, Victoria Worthington, Veronica Hangsan, Ananya Hota, Mainoah Muna
- **Advisors**: Cindy Deng, Christian Brown, Erik Hasse
- **Libraries and Tools**: scikit-learn, TensorFlow, XGBoost, Pandas, Matplotlib, Google Colab, Jira, Slack

For more information, visit the project repository: [Fermata Energy BTTStudio](https://github.com/mainoahmuna/FermataEnergy_BTTStudio/tree/main/src).

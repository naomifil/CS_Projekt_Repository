## Concept
### Business Case: Personal Air Quality Health Advisor
AirSense is a personalized air-quality health advisor that helps users assess whether outdoor conditions are safe for
physical activity when travelling.
By combining live pollution data, weather forecasts, and machine learning, the app generates personalized daily risk 
scores for people with asthma or other respiratory conditions.

### Architecture
OpenAQ API ─┐
            ├── SQLite Database ──> ML Forecast Model ──> Risk Engine ──> Streamlit UI
OpenMeteo ──┘

* Run application: streamlit run AirSense.py
* Update API and database data: python api_and_db.py

## Features
### API Data
Our app uses air quality data from preselected location via OpenAQ and weather data from Openmeteo. Specifically, we 
are querying PM2.5, PM10 and O₃ in µg/m³ and mean daily temperature in °C and mean daily relative humidity in %. 
Air quality is fetched for current timestamp and weather is fetched for past 28 days and forecast for 14 days. 
For public deployment of the app the file `api_and_db.py` should be run daily to collect the latest data for all
locations (e.g. with task scheduler). 
Limitations regarding data: 
- focus on selected air quality and weather data, further factors such as pollen were not available for free 
- timestamps used for air particles are current rather than measurement timestamp due to inconsistent measurement 
intervals across stations This choice was made to avoid large gaps in dataset.

### Machine Learning
A Decision Tree Regressor was trained to predict PM2.5, PM10, and O₃ levels using temperature and relative humidity as 
input features. Historical pollution and weather data were merged by date and location after preprocessing and 
aggregation into daily averages and standardizing timestamps.
Model performance was evaluated using Mean Absolute Error (MAE).
After training, the model generates future pollution forecasts using weather predictions from OpenMeteo.
The model currently uses only temperature and humidity as features. As the model is limited to these two input 
features affecting air pollution, it may restrict predictive performance and does not allow exploration of 
higher-dimensional feature spaces.

### Risk calculation and UI
User inputs include destination, age, asthma level, planned activity levels, start of trip and end date which 
are used to calculate the risk score together with the data from our db and our ml
forecast. The process is explained on our `about_page.py`. App returns daily risk scores graphically and tabular as
well as air quality adn weather data for the duration of the trip for user to better comprehend results. 


  
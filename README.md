# BIOSTAT823-Final-Project
This is the final project of BIOSTAT823: Statistical Programming for Big Data in 2020 Fall Semester at Duke. Our team name is "Doctor Covid". This project is finished by Yiping Song (https://github.com/ys279), Xiangwen Mo (https://github.com/xiangwenmo), Bingruo Wu (https://github.com/Bingruo-Wu) and Fan Yang (https://github.com/FanYang44/).

## Data Collection and processing
For our project, the main data source we use is JHU CSSE Covid-19 repository: https://github.com/CSSEGISandData/COVID-19  
We acquire all data through url and cleaned the data.   
More details are in the folder [data](https://github.com/ys279/BIOSTAT823-Final-Project/tree/master/data)

## Interactive dashboard and visualization  
We used streamlit to build our dashboard for visualizing data analysis. 
Links to our dashboard: https://final-covid19-dashboard.herokuapp.com/ and you can check our [source codes](https://github.com/ys279/BIOSTAT823-Final-Project/tree/master/streamlit/final-covid19-dashboard) for deployment.  


There are three main sections included in the dashboard:  

#### Map  
* Daily updated active cases map for the world and for the United States. For global, we included active cases bubble map and case-fatalty ratio bubble map.  For US, we included active cases bubble map and death cases Choropleth map.    
* Global spread of covid-19 maps, in which users can select their intrested time range and see the animated spread of COVID-19 across the world.  

#### General Trend  
* plot of top 10 highest max infection cases/rate countries
* plots of infection rate vs. incidence rate for each countries  

#### Covid19 in US 
* plot of death rates vs. survive rates in US  
* plot for confirm cases, death cases, and recover cases in US  
  


## Model Development  
We have tried three time-series model to predict the number of new cases in a next given period.   
Models included:  
* [SARIMAX](https://github.com/ys279/BIOSTAT823-Final-Project/blob/master/model/SARIMAX%2BProphet.ipynb) 
* [SVR](https://github.com/ys279/BIOSTAT823-Final-Project/blob/master/model/SVR%20Model.ipynb)  
* [Prophet](https://github.com/ys279/BIOSTAT823-Final-Project/blob/master/prophet_model.ipynb)  

Each model has its advantage in prediction accuracy, but also has some limitations.   
In particular, we have tried to use SARIMAX model and Prophet model to predict death increase rate, and Prophet performs better. However, as Prophet model basically works like a black box, that we may lack of knowledge about what exactly happens there.  
SVR models is accurate for predicting global confirmed cases and recover cases in next 10 days. Yet not so accurate on predicting death cases.  
We also apply prophet model on predicting confirm and death cases. Prediction is only accurate for short-term, yet for long-term the outcome is out of our expectations.  

## Related Skills  
* Time series models  
* Functional programming  
* Data collection and preprocessing  
* Visualization with interactive plots (`plotly`, `altair`)  
* `streamlit` Dashboard   

## References  
https://github.com/CSSEGISandData/COVID-19  
https://plotly.com/python/scattermapbox/  
https://www.statsmodels.org/dev/examples/notebooks/generated/statespace_sarimax_stata.html  
https://www.sciencedirect.com/science/article/pii/S0960077920302538  
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7390340/  
https://machinelearningmastery.com/time-series-forecasting-with-prophet-in-python/  
https://www.streamlit.io/  

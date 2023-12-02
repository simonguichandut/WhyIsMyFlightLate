# Will My Flight Be Late?

This is our data science project for the Erdos Institute data science bootcamp 2023. We will be using machine learning to answer the question, Will My Flight Be Late?

## Team
- Ketan Sand
- Simon Guichandut
- Tim Hallatt

PhD students at McGill University and the Trottier Space Institute.

Here is a plot showing 11 years data of departure delay (in mins) from the busiest airport in US - Hartsfield-Jackson Atlanta International Airport Atlanta, GA. We see quite a lot of day to day variation, having an estimate on how much delay we expect and what might be the reason will not only help passengers but also save overhead costs for airports and airlines.

![Atlanta_all](https://github.com/simonguichandut/WhyIsMyFlightLate/assets/55292615/5a75b47d-84a3-4f7e-aeb3-db2d8b5cda09)


## The Format of this Repo
Stage one of our analysis is to clean and prepare the data for training. 

In [data](data/) we include our download and cleaning scripts (see the readme there).

In [notebooks](notebooks/) we include the following:
- Exploratory.ipynb contains our preliminary analysis tracking the fraction of delayed flights as functions of origin, destinations, time of year, time of day.
- Classification-final.ipynb contains the classification script using logistic regression, random forest, and XGBoost.
- Get_delay_range_final.ipynb contains the script for estimating how delayed your flight is going to be.
- Hyperparameter_tuning_future.ipynb contains preliminary hyperparameter tuning.
- We also have the plots directory in here which contains all the relevant plots generated by various script. 
 The important ones are the two pdfs that show the performance of our models on different time range of data. We ultimately used these curves to get our best results.
 [metrics_plot_validation.pdf](https://github.com/simonguichandut/WhyIsMyFlightLate/files/13532685/metrics_plot_validation.pdf)

In [models](models) we include the final trained models from our analysis.
- We have our Random forest model trained on 2022-2023 data here. This model gave us the best results.

Finally is the streamlit code to host our web-app. Which make all this a more user-friendly experience. Have a look at https://willmyflightbelate.streamlit.app/ !

(You may get a "This app has gone over its resource limits." if too many requests are made to it. We're sorry, we are trying to optimize its memory use!)

Hackathon with NBIM: Case 1
===========================

Our solution consists of multiple parts. The source code is found inside the `src/helpers/`
directory, where the file-names are a description of the contents. The `src/` directory also
consists of the streamlit-website we have built.

1. Fetching data
----------------
In the `src/helpers/weather.py` file, we have created an object that fetches weather data from
the met.no-API. The code has been extremely generalized, allowing the user to specify multiple
weather stations, sensor data-types to fetch and time-periods to fetch data from. The object
automatically divides the time-periods such that the requests are within the API's limits. The
fetched data is then stored to a file if wanted. (We also found the spot price for all the price
areas in Norway online and downloaded this directly – from www.forbrukerrådet.no/strompris/
spotpriser.) An example can be found in the jupyter notebook `src/helpers/fetching.ipynb`.

2. Data cleaning
----------------
In the `src/helpers/cleaning.py` file, we have created an object that cleans the data fetched such
that it is representable. The object then combines the weather- and spot-data into a single table
and either returns or saves this (whichever is specified by the user).

3. Modelling
------------
In the `src/helpers/model.py` file, we have created an object that models the data. The object takes
the data as input along with the wanted price area, and combines preprocessing and training. The
model that is being created is an XGBoost regressor, along with a few time-series features. The
model used in the streamlit-website is trained on the full dataset (excepting the last X hours)
which the model then predicts. (See method "predict" in the file.)

4. Visualizing
--------------
In the `src/helpers/integral.py` file, we have created functions to handle the visualization. The
first method in the file calculates the time periods within the predicted time period that are
optimal for selling electricity to the grid based on how much you have stored. The second method
plots the spot- and predicted prices for the given time period, and highlights the optimal selling
periods.

5. Streamlit
------------
In the `src/website.py` file, we have created a streamlit-website that allows the user to specify
the stored energy as well as the export capacity. This information is then used to find the optimal
time-periods within the next 24 hours to sell electricity to the grid. The website also shows the
previously mentioned plot (see 4. Visualizing), and incorporates the modelling of the fetched data
(see steps 1., 2. and 3.).

To open the website
-------------------
Navigate to the `src/` directory and run the following command in the terminal:
`streamlit run website.py`.

Made by:
--------
* Hallvard H. Lavik
* Leo Q. T. Bækholt
* Karen Eide
* Isabelle Damhaug
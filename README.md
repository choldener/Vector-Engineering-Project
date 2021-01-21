# COVID-19 Sequencing Dashboard

Project can be found at the following url [vector-project.herokuapp.com](https://vector-project.herokuapp.com/)

## Table of Contents

- [COVID-19 Sequencing Dashboard](#covid-19-sequencing-dashboard)
- [Requirements](#requirements)
- [Setup and Running](#setup-and-running)
- [Project Outline](#project-outline)
  - [Data Pipeline and Transformation](#data-pipeline-and-transformation)
  - [Data Dictionary](#data-dictionary)
  - [Dashboard](#dashboard)
  - [Data visualization](#data-visualization)
- [About the Project](#about-the-project)
  - [Features to add / TO-DO](#TO-DO)


## Requirements

  Project was wrote on Python 3.7 and requires a handful of python packages. Install them using:
  ```bash
  pip install -r requirements.txt
  ```
  Project also requires connection to the internet in order to pull the data from online sources.
  A Mapbox token is required for the application to run locally.
  
## Setup and Running

  Once the required packages are installed, setup is minimal. Clone this repository to get all the required files. 
  Take the mapbox token you aquired and paste it into the mapbox_key.txt file. 
  Run app.py to start the local server.
  
  
  A local server should run and you should now be able to nagivate to the application locally.


## Project Outline

* ### Data Pipeline and Transformation
  Data is gathered from the following sources:
    * Case Data: [https://storage.googleapis.com/ve-public/covid_case_counts2.csv](https://storage.googleapis.com/ve-public/covid_case_counts2.csv)
    * Sequence Data: [https://storage.googleapis.com/ve-public/covid_new_sequences.csv](https://storage.googleapis.com/ve-public/covid_new_sequences.csv)
    * Country Data: [https://storage.googleapis.com/ve-public/country_iso.csv](https://storage.googleapis.com/ve-public/country_iso.csv)
    * continent Data: [https://pkgstore.datahub.io/JohnSnowLabs/country-and-continent-codes-list/country-and-continent-codes-list-csv_csv/data/b7876b7f496677669644f3d1069d3121/country-and-continent-codes-list-csv_csv.csv](https://pkgstore.datahub.io/JohnSnowLabs/country-and-continent-codes-list/country-and-continent-codes-list-csv_csv/data/b7876b7f496677669644f3d1069d3121/country-and-continent-codes-list-csv_csv.csv)


  Data was transformed and combined utilizing pandas in three parts.
  
  1) Case data is called and merged with country and continent, then melted with variable as the number of cases
  2) Sequence data is called, date is converted from a string to pd.DateTime, and column names are changed for easier merging.
  3) Case data and sequence is merged using a left join on Country and Date columns. new_sequences and Cases columns had null data filled by zeros, while new_sequences was also      grouped and a cumulative sum calculated for each country on each date. This alowed for all further tests and calculations to be done on the data.
  
  
* ### Data Dictionary
  Data Dictionary can be found [here](https://github.com/choldener/Vector-Engineering-Project/blob/main/Data%20Dictonary.xlsx).


* ### Dashboard

  Dashboard was wrote utilizing [Dash Plotly](https://plotly.com/dash/) which is a Python framework for building web apps.
  Dash was chosen due to it's ease of use and the ability to quickly prototype usable interactive dashboards.
  

* ### Data Visualization

  Visualization was done utilizing a combination of Plotly Express and Plotly's baceline Graph Objects. 
  
  
  Refreshing the page should restart the visualizations and reveret settings back to baseline.


## About the Project

Project was developed with the [COVID CG global sequencing coverage map]( https://covidcg.org/?tab=global_sequencing) as inspiration. Special thanks goes out to their team.


#### TO-DO
* Add Feature: Clicking on the selected country (deslecting it) will enable orignal graph
* Improvement: Overall Documentation improvement
* Improvement: Further clean and refine Data
  * Clean Case Sequence Line data to not include countries with 0 sequences at time of latest data
* Improvement MAJOR: Chart feedback is slow due to expensive data cleaning/transforming happening on each callback

# sqlalchemy-challenge
- Module 10 Challenge
- Steph Abegg

## Files

In the SurfsUp folder, I have included:

(1) [climate.ipynb](SurfsUp/climate.ipynb). This contains the Part 1: Analyze and Explore the Climate Data analysis. In this section, I used Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, I used SQLAlchemy ORM queries, Pandas, and Matplotlib. 

(2) Images/Precipitation_Plot and Images/Station_Plot_USC00519281. These are two output images from the Part 1 analysis. 

(3) [app.py](SurfsUp/app.py). This contains the code for Part 2: Design Your Climate App. In this section, I designed a Flask API based on the queries developed in Part 1. When run, the app.py file creates the app at http://127.0.0.1:5000. 

## Part 1: Analyze and Explore the Climate Data

In the Part 1 analysis, we plotted precipitation over time for the last 12 months of data. Two versions of the plot are shown below, in different format (the second matches that in the Module Challenge description, but the first was my own formatting).

![Precipitation_Plot.png](SurfsUp/Images/Precipitation_Plot.png?raw=true)
![Precipitation_Plot_2.png](SurfsUp/Images/Precipitation_Plot_2.png?raw=true)

In the Part 1 analysis, we also looked at the temperature data at the most active station, which was Station USC00519281, with 2772 measurements over the timeframe of the data.  According to the analysis, the lowest, highest, and average temperature, respectively, at Station USC00519281 are: 54.0, 85.0, 71.7 degrees Fahrenheit. The histogram below shows the temperatures at Station USC00519281 (the station with the most data) for the last 12 months of data.

![Station_Plot_USC00519281.png](SurfsUp/Images/Station_Plot_USC00519281.png?raw=true)

## Part 2: Design Your Climate App

In this section, I designed a Flask API based on the queries developed in Part 1. When run, the app.py file creates the app at http://127.0.0.1:5000. Here's an image of the main page of the working app:

![app.png](SurfsUp/Images/app.png?raw=true)

## External Resources

For me, sqlalchemy has been the most challenging concept of the course so far. I watched several lectures/tutorials on youtuble and googled the web for other tutorials. I wrote all of my own code using techniques from class and help of the XPert Learning Assistant.

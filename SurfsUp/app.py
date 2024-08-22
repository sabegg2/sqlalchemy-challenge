# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine)

# Save references to each table
measurement_table = Base.classes.measurement
station_table = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# List the stations and their counts in descending order
stations_by_measurement_count = session.query(station_table.station, func.count(measurement_table.station)).\
        filter(station_table.station == measurement_table.station).\
                group_by(station_table.station).\
                        order_by(func.count(measurement_table.station).desc()).\
                                all()
# Most active station is the first one in the stations_by_measurement_count list
most_active_station = stations_by_measurement_count[0][0]

# Find the most recent date in the data set
# Calculate the date one year from the last date in data set
date_oldest = session.query(func.min(measurement_table.date)).scalar()
date_most_recent = session.query(func.max(measurement_table.date)).scalar()
date_one_yr_before_dt = dt.datetime.strptime(date_most_recent, '%Y-%m-%d') - dt.timedelta(days=365)
date_one_yr_before = date_one_yr_before_dt.strftime('%Y-%m-%d')

# Close session
session.close()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Start at the homepage.
# List all the available routes.
@app.route("/")
def homepage():
    return (
        "<h1>Welcome to the Climate App!</h1>"
        "This is a Flask API for Climate Analysis for Honolulu, Hawaii.<br/><br/><br/>"
        "<img width='600' src='https://content.r9cdn.net/rimg/dimg/29/40/3f4ec996-city-28070-16c96b74d6d.jpg?width=1366&height=768&xhint=3379&yhint=2867&crop=true'>"
        
        #f"<h2>Here are the available routes:</h2>"
        #f"/api/v1.0/precipitation<br/>"
        #f"/api/v1.0/stations<br/>"
        #f"/api/v1.0/tobs<br/>"
        #"/api/v1.0/<start><br/>"
        #f"/api/v1.0/<start>/<end><br/>"

        "<h2>Here are the available routes with hyperlinks:</h2>"

        "/api/v1.0/precipitation<br/>"
        "<a href=http://127.0.0.1:5000/api/v1.0/precipitation> \
            JSON list of precipitation (inches) by date for the most recent year of data available.</a><br/><br/>"

        "/api/v1.0/stations<br/>"
        "<a href=http://127.0.0.1:5000/api/v1.0/stations> \
            JSON list of stations.</a><br/><br/>"

        "/api/v1.0/tobs<br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/tobs> \
            JSON list of temperature (Fahrenheit) observations for the previous year at the most active station (Station {most_active_station}).</a><br/><br/>"

        "/api/v1.0/start_date<br/>"
        "<a href=http://127.0.0.1:5000/api/v1.0/2016-08-23> \
            Change the start date (YYYY-MM-DD) in the url to show the minimum, average, and maximum temperature for all dates greater than and equal to the start date.</a><br/><br/>"

        "/api/v1.0/start_date/end_date<br/>"
        "<a href=http://127.0.0.1:5000/api/v1.0/2016-08-23/2017-08-23> \
            Change the start date and end date (YYYY-MM-DD) in the url to show the minimum, average, and maximum temperature for dates from the start date to the end date, inclusive.</a><br/>" 
    )

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
# to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    data_precip_last_year = session.query(measurement_table.date, measurement_table.prcp).filter(measurement_table.date >= date_one_yr_before).all()
    
    # Close session
    session.close()

    # Dictionary using date as the key and prcp as the value
    data_precip_last_year_dict = {date: prcp for date, prcp in data_precip_last_year}

    # Return the JSON representation of your dictionary
    return jsonify(data_precip_last_year_dict)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    # Query to get stations
    station_list = session.query(station_table.station).all()
    
    # Close session
    session.close()

    # Unravel results into a 1D array and convert to a list
    station_list = list(np.ravel(station_list))

    # Return a JSON list of stations from the dataset
    return jsonify(station_list)


# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def temp_most_active_station():
    session = Session(engine)

    # Query the last 12 months of temperature observation data for this station
    data_temp_last_year = session.query(measurement_table.date, measurement_table.tobs).\
            filter(measurement_table.date.between(date_one_yr_before,date_most_recent),\
                   measurement_table.station == most_active_station).all()
    
    # Close session
    session.close()
    
    # Dictionary using date as the key and tobs as the value
    data_temp_last_year_dict = {date: tobs for date, tobs in data_temp_last_year}

    # Return the JSON representation of your dictionary
    return jsonify(data_temp_last_year_dict)


# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route('/api/v1.0/<start>', defaults={'end': None})
@app.route('/api/v1.0/<start>/<end>')
def temp_stats_date_range(start, end):
    session = Session(engine)

    # Select statement, query(*[]) will unpack list
    sel_statement = [func.min(measurement_table.tobs), func.avg(measurement_table.tobs), func.max(measurement_table.tobs)]

    # If end date given, calculate TMIN, TAVG, TMAX for the dates from the start date to the end date, inclusive
    if end != None:
        temp_stats = session.query(*sel_statement).\
            filter(measurement_table.date >= start).filter(measurement_table.date <= end).all()
    # If no end date given, calculate TMIN, TAVG, TMAX for dates greater than or equal to the start date.
    else:
        temp_stats = session.query(*sel_statement).\
            filter(measurement_table.date >= start).all()
    
    # Close session
    session.close()

    # Convert the query results to a list, and return error message if no temperature data found.
    temp_stats_list = []
    no_temperature_data = False
    for min_temp, avg_temp, max_temp in temp_stats:
        if min_temp == None or avg_temp == None or max_temp == None:
            no_temperature_data = True
        temp_stats_list.append(min_temp)
        temp_stats_list.append(avg_temp)
        temp_stats_list.append(max_temp)
    # Return a JSON list of the temperatures
    if no_temperature_data == True:
        return (
            "No temperature data found for the given date range.<br/>"
            f"Data from {date_oldest} to {date_most_recent}.<br/>"
            "Try another date range."
        )
    else:
        return jsonify(temp_stats_list)


if __name__ == '__main__':
    app.run()
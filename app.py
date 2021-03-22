import numpy as np
import datetime as dt
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
session = Session(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start_date <br/>"
        f"/api/v1.0/start_end <br/>"
     
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    one_year = dt.date(2016, 8, 23)

    Precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).all()

    session.close()
    # Dict with date as the key and prcp as the value
    # prcp_dict = {date: prcp for date, prcp in Precipitation}
    # return jsonify(prcp_dict)
    return {date: prcp for date, prcp in Precipitation}


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_results = session.query(Station.station, Station.name).all()

    session.close()

    #create dictionary from the query"/api/v1.0/<start>
    stations = []

    for station, name in station_results:
        stns= {}
        stns["station"] = station
        stns["name"] = name
        stations.append(stns)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    Year_Temp = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= one_year)\
    .filter(Measurement.station =="USC00519281")\
    .order_by(Measurement.tobs).all()

    session.close()

    return jsonify(Year_Temp)


@app.route("/api/v1.0/start_date")

def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    #create dictionary from the query
    start_date = []

    for min, avg, max in start_results:
        start= {}
        start["avg"] = avg
        start["min"] = min
        start["max"] = max
        start_date.append(start)

    return jsonify(start_date)


if __name__ == '__main__':
    app.run(debug=True)
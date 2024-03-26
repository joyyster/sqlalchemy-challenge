# Import the dependencies.
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    precipitation_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-24').\
        filter(Measurement.date <= '2017-08-23').\
        order_by(Measurement.date).all()
    
    precipitation_dict = {}
    for date, prcp in precipitation_year:
        precipitation_dict[date] = prcp
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""

    stations_data = session.query(Station.station).all()
    station_list = [station[0] for station in stations_data]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == 'USC00519281').\
                filter(Measurement.date >= '2016-08-23').all()
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                       filter(Measurement.date >= start).all()
    temperature_list = []
    for result in temperature_data:
        temperature_dict = {}
        temperature_dict["TMIN"] = result[0]
        temperature_dict["TAVG"] = result[1]
        temperature_dict["TMAX"] = result[2]
        temperature_list.append(temperature_dict)

    return jsonify(temperature_list)
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                       filter(Measurement.date >= start).\
                       filter(Measurement.date <= end).all()
    temperature_list = []
    for result in temperature_data:
        temperature_dict = {}
        temperature_dict["TMIN"] = result[0]
        temperature_dict["TAVG"] = result[1]
        temperature_dict["TMAX"] = result[2]
        temperature_list.append(temperature_dict)
    
    return jsonify(temperature_list)

if __name__ == '__main__':
    app.run(debug=True)
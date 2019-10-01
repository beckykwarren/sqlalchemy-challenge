# 
import numpy as np
import statistics
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station




# Create an app
app = Flask(__name__)


# Define static routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    prcp_observations = []
    for date, prcp in results:
        prcp_dict = {date: prcp}
        prcp_observations.append(prcp_dict)


    return jsonify(prcp_observations)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()
    session.close()
    # Convert list of tuples into normal list
    weather_stations = list(np.ravel(results))

    return jsonify(weather_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter_by(station='USC00519281' ).filter(and_(func.date(Measurement.date) >= '2016-08-23'),func.date(Measurement.date) <= '2017-08-23')
    session.close()
    
    temp_observations = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"]= date
        temp_dict["temp observation"]= tobs
        temp_observations.append(temp_dict)


    return jsonify(temp_observations)

# Define variable routes
@app.route("/api/v1.0/<start>/<end>")
def dates_closed(start,end):
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(and_(func.date(Measurement.date) >= start),func.date(Measurement.date) <= end)
    session.close()

    temp_list = []
    for tobs in results:
        temp_list.append(tobs)
    
    tmax = max(temp_list)
    tmin = min(temp_list)
    #tavg = statistics.mean(temp_list)
    
    range_dict = {"TMAX":tmax, "TMIN":tmin }
    # "TAVG":tavg,

    return jsonify(range_dict)


@app.route("/api/v1.0/<start>")
def dates_open(start):
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(and_(func.date(Measurement.date) >= start),func.date(Measurement.date) <= '2017-08-23')
    session.close()

    temp_list = []
    for tobs in results:
        temp_list.append(tobs)
    
    tmax = max(temp_list)
    tmin = min(temp_list)
    #tavg = statistics.mean(temp_list)
    
    range_dict = {"TMAX":tmax, "TMIN":tmin }
    # "TAVG":tavg,

    return jsonify(range_dict)



# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect Base = automap_base()the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of precipitation scores by date for 12 month period"""
    # Query all measurements and filter by last 12 months
    prev_year = '2016-08-23'
    sel = [Measurement.date, Measurement.prcp]
    prcp_results = session.query(*sel).filter(Measurement.date >= prev_year).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    precip = []
    for date, prcp in prcp_results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip.append(precip_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of stations and observation counts in descending order and find the most active station"""
    # Query all stations
    sel = [Measurement.station, func.count(Measurement.date)]
    results = session.query(*sel).\
    group_by(Measurement.station).order_by(func.count(Measurement.date).desc()).all()

    session.close()

    # Convert list of tuples into normal list
    station_activity = list(np.ravel(results))
    
    return jsonify(station_activity)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of temperatures for the most active station for the last year"""
    # Query all stations
    start_date = '2016-08-18'
    sel = [Measurement.station, Measurement.date, Measurement.tobs]
    tobs_results = session.query(*sel).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    temps = []
    for station, date, tobs in tobs_results:
        temps_dict = {}
        temps_dict[date] = tobs
        temps.append(temps_dict)

    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Fetch the min, max and avg temps for specified start date."""
    # Query all temps
    start_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date == start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    start_temps = []
    for min, max, avg in start_results:
        start_dict = {}
        start_dict["Min Temp"] = min
        start_dict["Max Temp"] = max
        start_dict["Avg Temp"] = avg
        start_temps.append(start_dict)

    return jsonify(start_temps)

                                 
@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Fetch the min, max and avg temps for specified start and end date."""
    # Query all temps
    range_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs).filter(Measurement.date >= start_date)).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    range_temps = []
    for min, max, avg in range_results:
        range_dict = {}
        range_dict["Min Temp"] = min
        range_dict["Max Temp"] = max
        range_dict["Avg Temp"] = avg
        range_temps.append(range_dict)

    return jsonify(range_temps)
    
if __name__ == '__main__':
    app.run(debug=True)
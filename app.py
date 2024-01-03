# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import app

#################################################
# Database Setup
#################################################

# Create session from Python to the DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
measurement_table = Base.classes.measurement
station_table = Base.classes.station

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
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>" 
        f"/api/v1.0/stations<br/>" 
        f"/api/v1.0/tobs<br/>" 
        f"/api/v1.0/start<br/>" 
        f"/api/v1.0/start/end<br/>" 
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(measurement_table.date, measurement_table.prcp).\
        filter(measurement_table.date >= previous_year).all()

    
    precip = {date: prcp for date, prcp in precipitation}
    session.close()

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    results = session.query(station_table.station).all()
    
    stations = list(np.ravel(results))
    #ssession.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():     
    # Create our session (link) from Python to the DB
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement_table.tobs).\
        filter(measurement_table.station == 'USC00519281').\
        filter(measurement_table.date >= previous_year).all()
    
    temps = list(np.ravel(results))
    session.close()

    return jsonify(temps)

app.route("/api/v1.0/<start>")  
app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):
    # Create our session (link) from Python to the DB
    operation = [func.min(measurement_table.tobs), func.avg(measurement_table.tobs), func.max(measurement_table.tobs)]
    
    if not end:
        results = session.query(*operation).\
            filter(measurement_table.date >= start).all()
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)

    results = session.query(*operation).\
        filter(measurement_table.date >= start).\
        filter(measurement_table.date <= end).all()
    
    temps = list(np.ravel(results))
    session.close()

    return jsonify(temps)   

if __name__ == '__main__':
    app.run(debug=True)
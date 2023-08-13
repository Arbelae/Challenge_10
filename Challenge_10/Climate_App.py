import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect an existing database into new model
Base = automap_base()
#reflect tables
Base.prepare(autoload_with=engine)

#ref to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# flask setup
app = Flask(__name__)



@app.route("/")
def home():
    #list available api routes
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
    #creating our session(link)
    session = Session(engine)

    #return a list
    last_year = session.query(func.max(Measurement.date)).scalar()
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

    Session.close()
    #convert list 
    prcp_data = {date: prcp for date, prcp in results}
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #return a list
    results = session.query(Station.station, Station.name).all()
    Session.close()
    #convert list 
    stations_data = {station: name for station, name in results}
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #return a list
    active_station = "USC00519281"
    last_year = session.query(func.max(Measurement.date)).scalar()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == active_station, Measurement.date >= last_year).all()
    Session.close()
    #convert list 
    tobs_data = {date: tobs for date, tobs in results}
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    session = Session(engine)
    #return a list
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    Session.close()
    #convert list 
    temp_data = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end):
    session = Session(engine)
    #return a list
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    Session.close()
    #convert list 
    temp_data = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)
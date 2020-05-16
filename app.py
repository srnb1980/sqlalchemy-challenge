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

# # reflect an existing database into a new model
Base = automap_base()
# # reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# ip_address = flask.request.remote_addr
# print(ip_address)
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
        f"/api/v1.0/start"<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    
#     # Create our session (link) from Python to the DB
    session = Session(engine)
    
    One_year_data = session.query(Measurement).all()

    from pandas import DataFrame
    prcp_df = pd.DataFrame([(d.date, d.prcp) for d in One_year_data], 
                   columns=['Date', 'Precipitation']).sort_values('Date')
    new_prcp_df = prcp_df.set_index('Date')
#    Sort the dataframe by date
    final_prcp_df=new_prcp_df.sort_index(axis = 0)
    final_prcp_df.dropna(inplace=True)
    session.close()

    prcp_dict = final_prcp_df.to_dict()
#     # Create a dictionary from the row data and append to a list of all_passengers
# #    all_precipitation=[{"Date":"20001102","Prcp":"6.5"},{"Date":"20001102","Prcp":"6.5"}]
#     all_precipitation = []
#     for row in prcp_df.iterrows():
#         Date=row["Date"]
#         Prcp=row["Precipitation"]
#         precipitation_dict = {Date:Prcp}
# #          precipitation_dict["D"] = d.date
# #          precipitation_dict["P"] = d.prcp
# # #        passenger_dict["P"] = prcp
#         all_precipitation.append(precipitation_dict)
    return jsonify(prcp_dict)
    print("Server received request for 'About' page...")
#    return "Welcome to my 'About' page!"

@app.route("/api/v1.0/stations")
def stations():
    
    
#     # Create our session (link) from Python to the DB
    session = Session(engine)
    
    station_data = session.query(Station).all()

    from pandas import DataFrame
    station_df = pd.DataFrame([(d.station, d.name) for d in station_data], 
                   columns=['Station', 'Station_Name']).sort_values('Station')
    new_station_df = station_df.set_index('Station')
#    Sort the dataframe by date
    final_station_df=new_station_df.sort_index(axis = 0)
    final_station_df.dropna(inplace=True)
    session.close()

    station_dict = final_station_df.to_dict()
#     # Create a dictionary from the row data and append to a list of all_passengers
# #    all_precipitation=[{"Date":"20001102","Prcp":"6.5"},{"Date":"20001102","Prcp":"6.5"}]
#     all_precipitation = []
#     for row in prcp_df.iterrows():
#         Date=row["Date"]
#         Prcp=row["Precipitation"]
#         precipitation_dict = {Date:Prcp}
# #          precipitation_dict["D"] = d.date
# #          precipitation_dict["P"] = d.prcp
# # #        passenger_dict["P"] = prcp
#         all_precipitation.append(precipitation_dict)
    return jsonify(station_dict)
    print("Server received request for 'About' page...")
#    return "Welcome to my 'About' page!"

@app.route("/api/v1.0/tobs")
def tobs():
    
    
#     # Create our session (link) from Python to the DB
    session=Session(engine)
    
    
    last_row = session.query(Measurement).order_by(Measurement.id.desc()).first()
    # Calculate the date 1 year ago from the last data point in the database
    from datetime import datetime
    current_date=last_row.date
    current_date_dt = datetime.strptime(current_date, '%Y-%m-%d').date()

    from dateutil.relativedelta import relativedelta
    #import datetime
    Date_One_Year_Ago= current_date_dt - relativedelta(years=1)

    from pandas import DataFrame
    Most_Active_Station=session.query(Measurement.station,func.count(Measurement.station).label("Count")).group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc()).first()
    Most_Act_Station_Name=Most_Active_Station.station

    One_year_data_Act_Stn = session.query(Measurement.date,Measurement.tobs)\
    .filter(Measurement.date >=Date_One_Year_Ago).filter(Measurement.station==Most_Act_Station_Name)


    tobs_df=pd.DataFrame([(d.date, d.tobs) for d in One_year_data_Act_Stn], 
                  columns=['Date','TOBS']).sort_values('Date')

    new_tobs_df = tobs_df.set_index('Date')
#    Sort the dataframe by date
    final_tobs_df=new_tobs_df.sort_index(axis = 0)
    final_tobs_df.dropna(inplace=True)
    session.close()

    tobs_dict = final_tobs_df.to_dict()
#     # Create a dictionary from the row data and append to a list of all_passengers
# #    all_precipitation=[{"Date":"20001102","Prcp":"6.5"},{"Date":"20001102","Prcp":"6.5"}]
# #     all_precipitation = []
#     all_tobs = []
#     for Date, TOBS in tobs_dict:
#         tmp_tobs_dict = {}
#         tmp_tobs_dict["Date"] = Date
#         tmp_tobs_dict["TOBS"] = TOBS
#         all_tobs.append(tmp_tobs_dict)
    return jsonify(tobs_dict)
    print("Server received request for 'About' page...")
#    return "Welcome to my 'About' page!"


@app.route("/api/v1.0/<start>")
def startdt(start):
    
    
    from datetime import datetime
    current_date_dt = datetime.strptime(start, '%Y%m%d').date()
    str_current_date_dt = str(current_date_dt)
    # Create our session (link) from Python to the DB
    session=Session(engine)
    
    
#     start_row = session.query(Measurement).order_by(Measurement.id.desc()).first()
    
#    LT=session.query(func.min(Measurement.tobs).label('low_temp')).filter(or_(Measurement.date>=current_date_dt,Measurement.tobs!=None))

    LT=session.query(func.min(Measurement.tobs).label('low_temp')).filter(Measurement.date>=current_date_dt)
    
    HT=session.query(func.max(Measurement.tobs).label('max_temp')).filter(Measurement.date>=current_date_dt)
    
    AT=session.query(func.avg(Measurement.tobs).label('avg_temp')).filter(Measurement.date>=current_date_dt) 
    
    for temp in LT:
        low_temp=temp.low_temp
    for temp in HT:
        max_temp=temp.max_temp
    for temp in AT:
        avg_temp=temp.avg_temp

    tmp_start_dict={ "Start Date": str_current_date_dt,"TMIN":low_temp,"TMAX":max_temp,"TAVG":avg_temp}
    session.close()
    
#    tmp_start_dict={"Name":current_date_dt,"Date":"12/12/2019"}
    
    return jsonify(tmp_start_dict)
#    return current_date_dt


@app.route("/api/v1.0/<start>/<end>")
def startenddt(start,end):
    
    
    from datetime import datetime
    current_st_dt = datetime.strptime(start, '%Y%m%d').date()
    current_end_dt = datetime.strptime(end, '%Y%m%d').date()
    str_current_st_dt = str(current_st_dt)
    str_current_end_dt = str(current_end_dt)
    # Create our session (link) from Python to the DB
    session=Session(engine)
    
    
#     start_row = session.query(Measurement).order_by(Measurement.id.desc()).first()
    
#    LT=session.query(func.min(Measurement.tobs).label('low_temp')).filter(or_(Measurement.date>=current_date_dt,Measurement.tobs!=None))

    LT=session.query(func.min(Measurement.tobs).label('low_temp')).filter(Measurement.date>=current_st_dt).filter(Measurement.date<=current_end_dt)
    
    HT=session.query(func.max(Measurement.tobs).label('max_temp')).filter(Measurement.date>=current_st_dt).filter(Measurement.date<=current_end_dt)
    
    AT=session.query(func.avg(Measurement.tobs).label('avg_temp')).filter(Measurement.date>=current_st_dt).filter(Measurement.date<=current_end_dt)
    
    for temp in LT:
        low_temp=temp.low_temp
    for temp in HT:
        max_temp=temp.max_temp
    for temp in AT:
        avg_temp=temp.avg_temp

    tmp_start_dict={ "Start Date": str_current_st_dt, "End Date": str_current_end_dt, "TMIN":low_temp,"TMAX":max_temp,"TAVG":avg_temp}
    session.close()
    
#    tmp_start_dict={"Name":current_date_dt,"Date":"12/12/2019"}
    
    return jsonify(tmp_start_dict)
#    return current_date_dt


if __name__ == '__main__':
     app.run(debug=True)
        
       
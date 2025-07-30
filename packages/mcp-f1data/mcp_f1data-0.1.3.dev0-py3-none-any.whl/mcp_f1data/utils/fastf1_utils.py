import fastf1
import pandas as pd
from pandas import DataFrame

def get_session(type_event:str, year:int, event:int, session:str) -> object:
    try:
        if type_event == "official":
            session = fastf1.get_session(year, event, session)
        elif type_event == "pretest":
            session = fastf1.get_testing_session(year, event, session)
        session.load()
    except:
        raise ValueError("The session does not exist or is not available now!")
    return session

def get_laps(type_event:str, year:int, event:int, session:str, driver:str=None) -> DataFrame:
    session = get_session(type_event, year, event, session)
    laps = session.laps
    laps["LapTime"] = pd.to_timedelta(laps["LapTime"])
    if driver: laps = laps.pick_drivers(driver)
    return laps

def get_specific_lap(laps:DataFrame, lap_number:int = -1, get_personal_fastest_lap: bool = False, get_general_fastest_lap:bool = False) -> DataFrame:
    if (get_general_fastest_lap or get_personal_fastest_lap) and (lap_number == -1):
        lap = laps.pick_fastest()
    else:
        lap = laps.pick_laps(lap_number)
    return lap
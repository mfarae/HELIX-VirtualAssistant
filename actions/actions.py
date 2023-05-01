# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#

'''Better intent examples
More stories and rules
Config.yml
Training stories more'''


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, VARCHAR, text, Float, select
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import result

engine = create_engine('postgresql://postgres:sys@localhost/helix')
connection = engine.connect()
meta = MetaData(bind=engine)
MetaData.reflect(meta)
db = scoped_session(sessionmaker(bind=engine))

user = Table(
    'user', meta,
    Column('u_id', Integer, primary_key=True),
    Column('u_name', VARCHAR),
    extend_existing=True
)


device = Table(
    'device', meta,
    Column('d_id', Integer, primary_key=True),
    Column('d_type', VARCHAR),
    Column('d_value', Integer),
    extend_existing=True
)

smart_tv = Table(
    'smart_tv', meta,
    Column('s_app', VARCHAR),
    Column('s_search', VARCHAR),
    Column('s_running', Integer),
    extend_existing=True
)

thermostat = Table(
    'thermostat', meta,
    Column('t_temp', Float),
    extend_existing=True
)

alarm = Table(
    'alarm', meta,
    Column('a_time', VARCHAR),
    extend_existing=True
)

air_quality = Table(
    'air_quality', meta,
    Column("purity_index", Float),
    extend_existing=True
)

boiler = Table(
    'boiler', meta,
    Column('start_time', VARCHAR),
    Column('end_time', VARCHAR),
    extend_existing=True
)

meta.create_all(engine)

u1 = user.insert().values(u_id=1, u_name='Farae')
u2 = user.insert().values(u_id=2, u_name='Hamza')
u3 = user.insert().values(u_id=3, u_name='Umair')

d1 = device.insert().values(d_id=1, d_type='Light', d_value=0)
d2 = device.insert().values(d_id=2, d_type='Door', d_value=0)

#engine.execute(u1)
#engine.execute(u2)
#engine.execute(u3)
#engine.execute(d1)
#engine.execute(d2)

tv = smart_tv.insert().values(s_app="None", s_search="None", s_running=0)
#engine.execute(tv)

therm = thermostat.insert().values(t_temp='25.0')
#engine.execute(therm)

air = air_quality.insert().values(purity_index=50)
#engine.execute(air)

boil = boiler.insert().values(start_time="None", end_time="None")
#engine.execute(boil)


class ActLockDoor(Action):
    def name(self) -> Text:
        return "action_lock_door"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DEVICE = meta.tables['device']

        u = update(DEVICE)
        u = u.values({"d_value" : 1})
        u = u.where(DEVICE.c.d_type == "Door")
        engine.execute(u)

        return []
    
class ActUnlockDoor(Action):
    def name(self) -> Text:
        return "action_unlock_door"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DEVICE = meta.tables['device']

        u = update(DEVICE)
        u = u.values({"d_value" : 0})
        u = u.where(DEVICE.c.d_type == "Door")
        engine.execute(u)

        return []
    
class ActLightOn(Action):
    def name(self) -> Text:
        return "action_light_on"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        DEVICE = meta.tables['device']
        u = update(DEVICE)
        u = u.values({"d_value" : 1})
        u = u.where(DEVICE.c.d_type == "Light")
        engine.execute(u)

        return []
    
class ActLightOff(Action):
    def name(self) -> Text:
        return "action_light_off"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        DEVICE = meta.tables['device']
        u = update(DEVICE)
        u = u.values({"d_value" : 0})
        u = u.where(DEVICE.c.d_type == "Light")
        engine.execute(u)

        return []
    
class ActOpenEntertainment(Action):
    def name(self) -> Text:
        return "action_open_entertainment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entertainment = tracker.get_slot("entertainment")
        source = tracker.get_slot("source")
        msg = ""
        ent = ["netflix", "hulu", "youtube", "spotify", "disneyplus"]
        if source.lower() in ent:
            update_tv = smart_tv.update().values(s_app=source, s_search=entertainment, s_running=1)
            engine.execute(update_tv)
            msg = f"sure, opening {source} with {entertainment}"
        else:
            msg = f"the platform {source} is not registered with the system. please try again"
        dispatcher.utter_message(text=msg)

        return []
    
class ActCloseEntertainment(Action):
    def name(self) -> Text:
        return "action_close_entertainment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        update_tv = smart_tv.update().values(s_running=0)
        engine.execute(update_tv)
        msg = f"sure, closing the smart tv"
        dispatcher.utter_message(text=msg)

        return []
    
class ActSetThermostat(Action):
    def name(self) -> Text:
        return "action_set_thermostat"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        temperature = tracker.get_slot("temperature")

        if temperature is None:
            dispatcher.utter_message(text="Sorry I encountered an issue. Please try again later")
            return []
        #query = select([thermostat])
        #ResultProxy = connection.execute(query)
        #ResultSet = ResultProxy.fetchone()
        update_therm = thermostat.update().values(t_temp=temperature)
        engine.execute(update_therm)
        msg = f"Updated the temperature of the thermostat to {temperature}"
        dispatcher.utter_message(text=msg)

        return []
    
class ActDecreaseThermostat(Action):
    def name(self) -> Text:
        return "action_decrease_thermostat"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dec = tracker.get_slot("decrement")
        if dec is None:
            dispatcher.utter_message(text="Sorry I encountered an issue. Please try again later")
            return []
        query = select([thermostat])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchone()
        current_temp = ResultSet["t_temp"]
        new_temp = float(current_temp) - float(dec)
        update_temp = thermostat.update().values(t_temp=new_temp)
        engine.execute(update_temp)

        msg = f"Updated the temperature of the thermostat to {new_temp}"
        dispatcher.utter_message(text=msg)

        return [SlotSet("temperature", new_temp)]

class ActIncreaseThermostat(Action):
    def name(self) -> Text:
        return "action_increase_thermostat"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        inc = tracker.get_slot("increment")
        if inc is None:
            dispatcher.utter_message(text="Sorry I encountered an issue. Please try again later")
            return []
        query = select([thermostat])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchone()
        current_temp = ResultSet["t_temp"]
        new_temp = float(current_temp) + float(inc)
        update_temp = thermostat.update().values(t_temp=new_temp)
        engine.execute(update_temp)

        msg = f"Updated the temperature of the thermostat to {new_temp}"
        dispatcher.utter_message(text=msg)

        return [SlotSet("temperature", new_temp)]

class ActSetAlarm(Action):
    def name(self) -> Text:
        return "action_set_alarm"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        time = tracker.get_slot("time")
        if time is None:
            dispatcher.utter_message(text="Sorry I encountered an issue. Please try again later")
            return []
        query = alarm.insert().values(a_time=time) 
        engine.execute(query)
        msg = f"alarm has been set for {time}"
        dispatcher.utter_message(text=msg)

        return []
    

class ActCheckAirPurification(Action):
    def name(self) -> Text:
        return "action_check_air_purification"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = select([air_quality])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchone()
        purity = ResultSet["purity_index"]
        msg = f"The current air purity level is {purity}"
        dispatcher.utter_message(text=msg)

        return []
    
class ActTurnOnBoiler(Action):
    def name(self) -> Text:
        return "action_turn_on_boiler"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        start = tracker.get_slot("start_time")
        end = tracker.get_slot("end_time")

        if start is None or end is None:
            dispatcher.utter_message(text="Sorry I encountered an issue. Please try again later")
            return []
        update_boiler = boiler.update().values(start_time=start, end_time=end)
        engine.execute(update_boiler)
        msg = f"The boiler will run from {start} to {end}"
        dispatcher.utter_message(text=msg)

        return[]
        
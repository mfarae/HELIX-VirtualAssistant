# coding: utf-8
from sqlalchemy import Column, Float, Integer, String, Table, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_air_quality = Table(
    'air_quality', metadata,
    Column('purity_index', Float(53))
)


t_alarm = Table(
    'alarm', metadata,
    Column('a_time', String)
)


t_boiler = Table(
    'boiler', metadata,
    Column('start_time', String),
    Column('end_time', String)
)


class Device(Base):
    __tablename__ = 'device'

    d_id = Column(Integer, primary_key=True, server_default=text("nextval('device_d_id_seq'::regclass)"))
    d_type = Column(String)
    d_value = Column(Integer)


t_smart_tv = Table(
    'smart_tv', metadata,
    Column('s_app', String),
    Column('s_search', String),
    Column('s_running', Integer)
)


t_thermostat = Table(
    'thermostat', metadata,
    Column('t_temp', Float(53))
)


class User(Base):
    __tablename__ = 'user'

    u_id = Column(Integer, primary_key=True, server_default=text("nextval('user_u_id_seq'::regclass)"))
    u_name = Column(String)

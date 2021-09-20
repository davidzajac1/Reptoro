from sqlalchemy import Column, String, Float, create_engine, Date, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import cast, select
from sqlalchemy.orm import Session
import pandas as pd
import os


def get_df():

    engine = create_engine(os.environ['CONNECTIONSTRING'])

    Base = declarative_base()
    session = Session(engine)

    class Animal(Base):
        __tablename__ = 'master'
        __table_args__ = {'schema': 'morphmarket'}

        url = Column('url', String)
        breeder_url = Column('breeder_url', String, primary_key=True)
        id_num = Column('id_num', String)
        status = Column('status', String)
        first_posted = Column('first_posted', String)
        last_updated = Column('last_updated', String)
        last_renewed = Column('last_renewed', String)
        date_scraped = Column('date_scraped', Date)
        currency = Column('currency', String)
        price = Column('price', Float)
        title = Column('title', String)
        store = Column('store', String)
        traits = Column('traits', String)
        type_ = Column('type', String)
        sex = Column('sex', String)
        maturity = Column('maturity', String)
        birthday = Column('birthday', String)
        shipping = Column('shipping', String)
        trades = Column('trades', String)
        likes = Column('likes', Float)
        offers = Column('offers', String)
        origin = Column('origin', String)
        proven_breeder = Column('proven_breeder', Float)
        clutch = Column('clutch', String)
        diet = Column('diet', String)
        images = Column('images', String)
        weight = Column('weight', String)
        quantity = Column('quantity', String)
        description = Column('description', String)

    stmt = select([Animal.url, Animal.breeder_url, Animal.price
                    , Animal.maturity, Animal.first_posted
                    , Animal.last_updated, Animal.type_, Animal.traits
                    , Animal.sex, Animal.proven_breeder
                    , (cast(Animal.last_updated, Date) - cast(Animal.first_posted, Date)).label('Days on Market')
                        ,]).where(and_(Animal.status == 'sold'
                    , Animal.price.between(5,30000)))


    return pd.read_sql(stmt, session.connection())






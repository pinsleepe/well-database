from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import dautil as dl
from tabulate import tabulate
import sqlite3
import os
from joblib import Memory

Base = declarative_base()
# memory = Memory(cachedir='.')


class DimUser(Base):
    __tablename__ = 'dim_user'

    id = Column(Integer, primary_key=True)
    # demographic info
    # start of intervention
    gender = Column(String)
    sexual_orientation = Column(String)
    partnership_status = Column(String)
    mental_health = Column(String)
    # end of intervention
    age = Column(Integer)
    socioeconomic_status = Column(String)
    household_composition = Column(String)
    children = Column(Integer)
    city = Column(String)


class DimArm(Base):
    __tablename__ = 'dim_arm'
    id = Column(Integer, primary_key=True)
    # BAU, T1, T2 or PC
    name = Column(String, nullable=False, unique=True)


class DimQuiz(Base):
    __tablename__ = 'dim_channel'
    id = Column(Integer, primary_key=True)
    channel = Column(String)


class FactQuiz(Base):
    __tablename__ = 'fact_quiz'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('dim_user.id'),
                     primary_key=True)
    arm_id = Column(Integer,
                    ForeignKey('dim_arm.id'),
                    primary_key=True)
    # channel_id = Column(Integer, ForeignKey('dim_channel.id'),
    #                     primary_key=True)
    # Storing amount as seconds
    duration = Column(Integer)
    score = Column(Integer)
    #
    # def __repr__(self):
    #     return "zip_code_id={0} channel_id={1} segment_id={2}".format(self.zip_code_id,
    #                                                                   self.channel_id,
    #                                                                   self.segment_id)


# def create_session(dbname):
#     engine = create_engine('sqlite:///{}'.format(dbname))
#     DBSession = sessionmaker(bind=engine)
#     Base.metadata.create_all(engine)
#     return DBSession()
#
#
# def populate_dim_segment(session):
#     options = ['Mens E-Mail', 'Womens E-Mail', 'No E-Mail']
#     for option in options:
#         if not dl.db.count_where(session, DimSegment.segment, option):
#             session.add(DimSegment(segment=option))
#     session.commit()
#
#
# def populate_dim_zip_code(session):
#     # Note the interesting spelling
#     options = ['Urban', 'Surburban', 'Rural']
#     for option in options:
#         if not dl.db.count_where(session, DimZipCode.zip_code, option):
#             session.add(DimZipCode(zip_code=option))
#     session.commit()
#
#
# def populate_dim_channels(session):
#     options = ['Phone', 'Web', 'Multichannel']
#     for option in options:
#         if not dl.db.count_where(session, DimChannel.channel, option):
#             session.add(DimChannel(channel=option))
#     session.commit()
#
#
# def load(csv_rows, session, dbname):
#     channels = dl.db.map_to_id(session, DimChannel.channel)
#     segments = dl.db.map_to_id(session, DimSegment.segment)
#     zip_codes = dl.db.map_to_id(session, DimZipCode.zip_code)
#     conn = sqlite3.connect(dbname)
#     c = conn.cursor()
#     logger = dl.log_api.conf_logger(__name__)
#     for i, row in enumerate(csv_rows):
#         channel_id = channels[row['channel']]
#         segment_id = segments[row['segment']]
#         zip_code_id = zip_codes[row['zip_code']]
#         spend = dl.data.centify(row['spend'])
#         insert = "INSERT INTO fact_sales (id, segment_id,\
#         zip_code_id, channel_id, spend) VALUES({id}, \
#         {sid}, {zid}, {cid}, {spend})"
#         c.execute(insert.format(id=i, sid=segment_id,
#                                 zid=zip_code_id, cid=channel_id,
#                                 spend=spend))
#         if i % 1000 == 0:
#             logger.info("Progress %s/64000", i)
#     conn.commit()
#     conn.commit()
#     c.close()
#     conn.close()
#
#
# @memory.cache
# def get_and_parse():
#     out = dl.data.get_direct_marketing_csv()
#     return dl.data.read_csv(out)
#
#
# if __name__ == "__main__":
#     dbname = os.path.join(dl.data.get_data_dir(), 'marketing.db')
#     session = create_session(dbname)
#     populate_dim_segment(session)
#     populate_dim_zip_code(session)
#     populate_dim_channels(session)
#     if session.query(FactSales).count() < 64000:
#         load(get_and_parse(), session, dbname)
#     fsum = func.sum(FactSales.spend)
#     query = session.query(DimSegment.segment, DimChannel.channel,
#                           DimZipCode.zip_code, fsum)
#     dim_cols = (DimSegment.segment, DimChannel.channel,
#                 DimZipCode.zip_code)
#     dim_entities = [dl.db.entity_from_column(col) for col in dim_cols]
#     spend_totals = query.join(FactSales,
#                               *dim_entities) \
#         .group_by(*dim_cols).order_by(fsum.
#                                       desc()).all()
#     print(tabulate(spend_totals, tablefmt='psql',
#                    headers=['Segment', 'Channel', 'Zip Code',
#                             'Spend']))

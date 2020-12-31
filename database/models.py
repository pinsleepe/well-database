from sqlalchemy import (Column, Integer, String, ForeignKey, Boolean, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from database import db

engine = db.engine

Base = declarative_base()
Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True))

    arm_id = Column(Integer, ForeignKey('arm.id'))
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


class Arm(Base):
    __tablename__ = 'arm'

    id = Column(Integer, primary_key=True)

    # BAU, T1, T2 or PC
    name = Column(String, nullable=False, unique=True)


class Module(Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)
    # need a dummy module for Control Arm with no modules
    name = Column(String, nullable=False)
    arm_id = Column(Integer, ForeignKey('arm.id'))


class ModuleFlow(Base):
    __tablename__ = 'module_flow'
    id = Column(Integer, primary_key=True)
    flow_id = Column(Integer, ForeignKey('flow.id'))
    module_id = Column(Integer, ForeignKey('module.id'))


class Flow(Base):
    __tablename__ = 'flow'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Quiz(Base):
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    quiz_id = Column(Integer, ForeignKey('quiz.id'))


class Option(Base):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey('question.id'))


class Answer(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    # user answer
    option_id = Column(Integer, ForeignKey('option.id'))
    user_id = Column(Integer, ForeignKey('user.id'))


class ModuleEvent(Base):
    __tablename__ = 'module_event'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True))

    user_id = Column(Integer, ForeignKey('user.id'))
    module_id = Column(Integer, ForeignKey('module.id'))
    flow_id = Column(Integer, ForeignKey('flow.id'))
    arm_id = Column(Integer, ForeignKey('arm.id'))

    completed = Column(Boolean)
    # Storing amount as seconds
    duration = Column(Integer)
    # module before this, relates to module_event.id
    penult_module = Column(Integer, ForeignKey('module_event.id'))


class QuizEvent(Base):
    __tablename__ = 'quiz_event'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True))

    user_id = Column(Integer, ForeignKey('user.id'))
    quiz_id = Column(Integer, ForeignKey('quiz.id'))
    arm_id = Column(Integer, ForeignKey('arm.id'))

    score = Column(Integer)
    # Storing amount as seconds
    duration = Column(Integer)
    completed = Column(Boolean)
    # module before this, relates to module_event.id
    penult_module = Column(Integer, ForeignKey('module_event.id'))


def populate_quiz_table(session,
                        flows_flow,
                        flows_flow_labels,
                        flows_flowlabel):
    s = select([
        flows_flow.c.name.label('name'),
        flows_flow.c.id.label('id')
    ]).select_from(flows_flow_labels.join(
        flows_flow,
        flows_flow_labels.c.flow_id == flows_flow.c.id
    ).join(flows_flowlabel,
           flows_flow_labels.c.flowlabel_id == flows_flowlabel.c.id)
                   ).where(flows_flowlabel.c.name == 'Trial Quiz'
                           ).group_by(
        flows_flow.c.name,
        flows_flow.c.id
    )
    rp = connection.execute(s)  # result proxy
    results = rp.fetchall()
    q = [Quiz(id=r['id'], name=r['name']) for r in results]
    session.add_all(q)
    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine,
                             Base.metadata.tables.values(),
                             checkfirst=True)
    connection = engine.connect()
    metadata = MetaData()
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()

    # read raw tables
    flows_flow_labels = Table('flows_flow_labels',
                              metadata,
                              autoload=True,
                              autoload_with=engine)
    flows_flowlabel = Table('flows_flowlabel',
                            metadata,
                            autoload=True,
                            autoload_with=engine)
    flows_flow = Table('flows_flow',
                       metadata,
                       autoload=True,
                       autoload_with=engine)

    populate_quiz_table(session,
                        flows_flow,
                        flows_flow_labels,
                        flows_flowlabel)

    session.close()

from sqlalchemy import (Column, Integer, String, ForeignKey, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import db

engine = db.engine

Base = declarative_base()
Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

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
    name = Column(String)
    users = relationship("user")


class Module(Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)
    version = Column(String)
    flows = relationship("Flow")


class Flow(Base):
    __tablename__ = 'flow'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = relationship("FlowQuestion")
    # this relates specifically to quizzes at the end of a module
    is_quiz = Column(Boolean)
    # TODO PC group will not complete any module so we can add a dummy one
    # so that the database don't brake, like version PC?
    module_id = Column(Integer, ForeignKey('module.id'))


class FlowQuestion(Base):
    __tablename__ = 'flow_question'

    id = Column(Integer, primary_key=True)
    flow_id = Column(Integer, ForeignKey('flow.id'))
    text = Column(String)
    options = relationship("FlowQuestionOption")


class FlowQuestionOption(Base):
    __tablename__ = 'flow_question_option'

    id = Column(Integer, primary_key=True)
    flow_question_id = Column(Integer, ForeignKey('flow_question.id'))
    text = Column(String)


class FlowUserAnswer(Base):
    __tablename__ = 'flow_user_answer'

    id = Column(Integer, primary_key=True)
    flow_question_id = Column(Integer, ForeignKey('flow_question.id'))
    # user answer
    flow_question_option_id = Column(Integer, ForeignKey('flow_question_option.id'))
    user_id = Column(Integer, ForeignKey('user.id'))


if __name__ == "__main__":
    Base.metadata.create_all(engine,
                             Base.metadata.tables.values(),
                             checkfirst=True)

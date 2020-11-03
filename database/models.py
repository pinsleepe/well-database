from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload

engine = create_engine('sqlite:///:memory:', echo=True)

# The base class which our objects will be defined on.
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    # Every SQLAlchemy table should have a primary key named 'id'
    id = Column(Integer, primary_key=True)

    # contact fields
    arm_id = Column(Integer, ForeignKey('arm.id'))

    # demographic info
    # start
    gender = Column(String)
    sexual_orientation = Column(String)
    partnership_status = Column(String)
    mental_health = Column(String)
    # end
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


class Quiz(Base):
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = relationship("QuizQuestion")


class QuizQuestion(Base):
    __tablename__ = 'quiz_question'

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id'))
    text = Column(String)
    options = relationship("QuizQuestionOption")


class QuizQuestionOption(Base):
    __tablename__ = 'quiz_question_option'

    id = Column(Integer, primary_key=True)
    quiz_question_id = Column(Integer, ForeignKey('quiz_question.id'))
    text = Column(String)


class QuizUserAnswer(Base):
    __tablename__ = 'quiz_user_answer'

    id = Column(Integer, primary_key=True)
    quiz_question_id = Column(Integer, ForeignKey('quiz_question.id'))
    quiz_question_option_id = Column(Integer, ForeignKey('quiz_question_option.id'))
    user_id = Column(Integer, ForeignKey('user.id'))


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
    flow_question_option_id = Column(Integer, ForeignKey('flow_question_option.id'))
    user_id = Column(Integer, ForeignKey('user.id'))


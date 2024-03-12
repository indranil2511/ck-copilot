from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


# Create a base class for our ORM models
Base = declarative_base()
class Chat_history(Base):
    """
    Model for chat history
    """
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    user_id = Column(String)
    question = Column(String)
    answer = Column(String)
    timestamp = Column(DateTime)
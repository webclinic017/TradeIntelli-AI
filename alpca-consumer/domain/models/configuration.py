from sqlalchemy import Column, Integer, Boolean, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json


Base = declarative_base()


class Configuration(Base):
    __tablename__ = 'configuration'

    id = Column(Integer, primary_key=True)
    run_check = Column(Boolean, default=False)
    subscribers = Column(String, default='[]')  # Store emails as a JSON string

    # To handle subscribers as a list
    @property
    def subscriber_list(self):
        return json.loads(self.subscribers)

    @subscriber_list.setter
    def subscriber_list(self, email_list):
        self.subscribers = json.dumps(email_list)


# Create an SQLite engine and a session
engine = create_engine('sqlite:///yourdatabase.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

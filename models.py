from sqlalchemy import Column, Integer, String, DECIMAL
from database import Base, engine
from sqlalchemy.orm import sessionmaker, relationship

# example only
class Teams(Base):
    __tablename__ = 'teams'

    owner = Column(String(50), primary_key=True)
    name = Column(String(50))

class Scoreboard(Base):
    __tablename__ = 'scoreboard'

    owner = Column(String(50))
    team = Column(String(50))
    week = Column(Integer)
    points = Column(Integer)
    total = Column(Integer)
    pointsScored = Column(DECIMAL(6,2))

class ScoreLog(Base):
    __tablename__ = 'scoreLog'

    owner = Column(String(50))
    team = Column(String(50))
    week = Column(String(50))
    position = Column(String(50))
    slotPosition = Column(String(50))
    projectedPoints = Column(DECIMAL(4,2))
    points = Column(DECIMAL(4,2))

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()

results = session.execute('SELECT * FROM teams').fetchall()

session.close()

print(results)
    
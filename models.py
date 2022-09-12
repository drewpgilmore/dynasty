from sqlalchemy import Column, Integer, String
from database import Base


# example only
class Season(Base):
    __tablename__ = 'season'

    owner = Column(String(50), primary_key=True)
    team = Column(String(50), unique=True)
    
    week1 = Column(Integer)
    # ...
    week14 = Column(Integer)
    playoffs = Column(Integer)
    cumulative = Column(Integer)

    
    def __init__(self, owner=None, team=None):
        self.name = name
        self.email = email
    
    def __repr__(self):
        return f'<User {self.name!r}>'
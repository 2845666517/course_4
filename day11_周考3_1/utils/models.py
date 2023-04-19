from sqlalchemy import Column, Integer, String
from utils.databases import Base

class College(Base):
    # 'id', 'school', 'address', 'sum_score', 'score'
    __tablename__ = 'college'
    id = Column(Integer, primary_key=True)
    rank=Column(Integer)
    school = Column(String(50))
    address = Column(String(120))
    sum_score = Column(Integer)
    score= Column(Integer)

    def __init__(self, rank=None,school=None, address=None, sum_score=None, score=None):
        self.rank=rank
        self.school = school
        self.address = address
        self.sum_score = sum_score
        self.score = score
    def to_json(self):
        dict=self.__dict__
        if '_sa_instance_state' in dict:
            del dict['_sa_instance_state']
        return dict
    def __repr__(self):
        return f'<College {self.name!r}>'



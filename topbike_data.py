from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Date
from dateutil import parser
from datetime import date

Base = declarative_base()


class Team(Base):
    __tablename__ = "Team"
    id = Column(Integer, primary_key=True)
    skill_level = Column(Integer)
    team_size = Column(Integer)

    def __repr__(self):
        return f"Team(id:{self.id}    skill level:{self.skill_level}    team size: {self.team_size})"

    def convert_to_tuple(self):
        return self.id, self.skill_level, self.team_size

    def valid(self):
        try:
            value = int(self.team_size)
        except ValueError:
            return False
        return value >= 0

    @staticmethod
    def convert_from_tuple(tuple_):
        team = Team(id=tuple_[0], skill_level=tuple_[1], team_size=tuple_[2])
        return team


class Lane(Base):
    __tablename__ = "Lane"
    id = Column(Integer, primary_key=True)
    max_capacity = Column(Integer)
    difficulty = Column(Integer)

    def __repr__(self):
        return f"Lane(id:{self.id}    max_capacity:{self.max_capacity}    difficulty:{self.difficulty})"

    def convert_to_tuple(self):
        return self.id, self.max_capacity, self.difficulty

    def valid(self):
        try:
            value = int(self.max_capacity)
        except ValueError:
            return False
        return value >= 0

    @staticmethod
    def convert_from_tuple(tuple_):
        try:
            max_capacity = int(tuple_[1])
            if max_capacity < 0:
                print(f"max capacity is negative! ({max_capacity})")
            else:
                lane = Lane(id=tuple_[0], max_capacity=max_capacity, difficulty=tuple_[2])
                return lane
        except:
            print("Entries could not be converted to lane!")


class Booking(Base):
    __tablename__ = "Booking"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    team_id = Column(Integer, ForeignKey("Team.id"), nullable=False)
    lane_id = Column(Integer, ForeignKey("Lane.id"), nullable=False)

    def __repr__(self):
        return f"Booking(id:{self.id}    date:{self.date}    team:{self.team_id}    lane:{self.lane_id})"

    def convert_to_tuple(self):
        return self.id, self.date, self.team_id, self.lane_id

    def valid(self):

        value = self.date.year
        return value >= 2001

    @staticmethod
    def convert_from_tuple(tuple_):
        try:
            if tuple_[0] != '':
                id_ = int(tuple_[0])
            else:
                id_ = 0
            date = parser.parse(tuple_[1])
            team_id = int(tuple_[2])
            lane_id = int(tuple_[3])

            booking = Booking(id=id_, date=date, team_id=team_id, lane_id=lane_id)
            return booking
        except:
            print("Entries could not be converted to booking")

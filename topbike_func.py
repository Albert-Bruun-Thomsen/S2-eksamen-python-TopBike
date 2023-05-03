from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import extract

import topbike_data as tbd
import topbike_sql as tbsql

def booked_lane(lane, date_):
    with Session(tbsql.engine) as session:
        records = session.scalars(select(tbd.Booking).where(tbd.Booking.lane_id == lane.id).where(extract("day", tbd.Booking.date) == date_.day).where(extract("month", tbd.Booking.date) == date_.month).where(extract("year", tbd.Booking.date) == date_.year))
        weight = 0
        for record in records:
            weight += tbsql.get_record(tbd.Team, record.id).team_size

    print(weight)
    return weight


def capacity_available(lane, date_, new_team):
    booked = booked_lane(lane, date_)

    return lane.max_capacity >= booked + new_team.team_size

def lane_available(lane, date_):
    print(lane)
    print(date_)
    with Session(tbsql.engine) as session:
        records = session.scalars(select(tbd.Lane).where(tbd.Lane.id == lane.id).where(extract("day", tbd.Booking.date) == date_.day).where(extract("month", tbd.Booking.date) == date_.month).where(extract("year", tbd.Booking.date) == date_.year))
        print("records = ", records)
        if records == None:
            print("records = ", records)
            return True
        return False

# read all Bane-records from the database, where bane.dato == date_
# if zero records were found return True
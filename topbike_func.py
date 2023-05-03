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
    # read all Lane-records from the database, where bane.dato == date_
    # if zero records were found return True
    # else check if lane is the same on both dates if not return True else False
    # print(lane)
    # print(date_)
    with Session(tbsql.engine) as session:
        # records = session.scalars(select(tbd.Lane).where(tbd.Lane.id == lane.id).where(extract("day", tbd.Booking.date) == date_.day).where(extract("month", tbd.Booking.date) == date_.month).where(extract("year", tbd.Booking.date) == date_.year))

        records = session.scalars(select(tbd.Lane).where(extract("day", tbd.Booking.date) == date_.day).where(extract("month", tbd.Booking.date) == date_.month).where(extract("year", tbd.Booking.date) == date_.year))
        for record in records:
            # print("record = ", record)
            # print("lane = ", lane)
            if record.id == lane.id:
                return False
            elif record.id != lane.id:
                # print("record.id is not equal to lane.id", record.id, lane.id)
                return True
            # else:
        #         print("no conditions met!", record) # unnecessary precaution
        # print("No records found!")
        return True


def capacity_ok(lane, team):
    # checks if capacity is okay returns bool
    # print(lane)
    # print(team)
    result = lane.max_capacity - team.team_size
    if result < 0:
        return False
    return True

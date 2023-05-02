from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update, delete
from datetime import date
from topbike_data import Team, Lane, Booking, Base

# add the following 7 lines to make foreign key constraints work  https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#sqlite-foreign-keys
from sqlalchemy.engine import Engine
from sqlalchemy import event
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


Database = "sqlite:///topbike.db"

def create_test_data():  # Optional. Used to test data base functions before gui is ready.
    with Session(engine) as session:
        new_items = []
        # new_items.append(Container(weight=1200, destination="Oslo"))
        # new_items.append(Container(weight=700, destination="Helsinki"))
        # new_items.append(Container(weight=1800, destination="Helsinki"))
        # new_items.append(Container(weight=1000, destination="Helsinki"))
        new_items.append(Team(skill_level=1, team_size=6))
        new_items.append(Team(skill_level=2, team_size=4))
        new_items.append(Lane(max_capacity=8, difficulty=0))
        new_items.append(Lane(max_capacity=10, difficulty=1))
        new_items.append(Lane(max_capacity=6, difficulty=2))

        a_date = date(day=10, month=12, year=2022)  # comment out if first run
        new_items.append(Booking(date=a_date, team_id=1, lane_id=2))  # comment out if first run
        a_date = date(day=30, month=4, year=2023)  # comment out if first run
        new_items.append(Booking(date=a_date, team_id=2, lane_id=1))  # comment out if first run
        session.add_all(new_items)
        session.commit()

def select_all(classparam):
    # return a list of all records in classparams table
    with Session(engine) as session:
        records = session.scalars(select(classparam))
        result = []
        for record in records:
            # print(record)
            result.append(record)
    return result


def get_record(classparam, record_id):  # https://docs.sqlalchemy.org/en/14/tutorial/data_select.html
    # return the record in classparams table with a certain id
    with Session(engine) as session:
        record = session.scalars(select(classparam).where(classparam.id_label == record_id)).first()
    return record


def create_record(record):
    # Create a record in the database
    with Session(engine) as session:
        record.id = None
        session.add(record)
        session.commit()


def update_team(team):
    #  updates a team in the database
    with Session(engine) as session:
        session.execute(update(Team).where(Team.id == team.id).values(skill_level=team.skill_level, team_size=team.team_size))
        session.commit()


def soft_delete_team(team):
    #  soft deletes a team by invalidating their team_size
    with Session(engine) as session:
        session.execute(update(Team).where(Team.id == team.id).values(skill_level=team.skill_level, team_size=-1))
        session.commit()


if __name__ == "__main__":  #executed when file is executed directly
    engine = create_engine(Database, echo=False, future=True)
    Base.metadata.create_all(engine)
    create_test_data()

else:
    engine = create_engine(Database, echo=False, future=True)
    Base.metadata.create_all(engine)
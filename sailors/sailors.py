'''
Sailors and Boats lecture script
@eugsokolov
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL

# Adjust the connection string to your SQLite database
engine = create_engine('sqlite:///C:/Users/malek/Desktop/eceProj1/sqlite-tools-win-x64-3450100/sailors.db', echo=True)

Base = declarative_base()

class Sailor(Base):
    __tablename__ = 'sailors'
    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return f"<Sailor(id={self.sid}, name='{self.sname}', rating={self.rating}, age={self.age})>"

class Boat(Base):
    __tablename__ = 'boats'
    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation', back_populates='boat')

    def __repr__(self):
        return f"<Boat(id={self.bid}, name='{self.bname}', color={self.color})>"

class Reservation(Base):
    __tablename__ = 'reserves'
    sid = Column(Integer, ForeignKey('sailors.sid'), primary_key=True)
    bid = Column(Integer, ForeignKey('boats.bid'), primary_key=True)
    day = Column(DateTime)

    sailor = relationship('Sailor', back_populates='reservations')
    boat = relationship('Boat', back_populates='reservations')

    def __repr__(self):
        return f"<Reservation(sailor_id={self.sid}, boat_id={self.bid}, day={self.day})>"
    
class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    ename = Column(String(100))
    position = Column(String(100))
    hourly_rate = Column(DECIMAL(10, 2))
    work_logs = relationship('WorkLog', back_populates='employee')
    def __repr__(self):
        return f"<Employee(id={self.employee_id}, name='{self.ename}', position='{self.position}', hourly_rate={self.hourly_rate})>"

class WorkLog(Base):
    __tablename__ = 'work_logs'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    work_date = Column(DateTime)
    hours_worked = Column(DECIMAL(5, 2))
    employee = relationship('Employee', back_populates='work_logs')
    def __repr__(self):
        return f"<WorkLog(log_id={self.log_id}, employee_id={self.employee_id}, work_date='{self.work_date}', hours_worked={self.hours_worked})>"

# Establish relationship in the Sailor class to complete the bidirectional relationship
Sailor.reservations = relationship('Reservation', back_populates='sailor')

# Create tables in the database (this is idempotent)
Base.metadata.create_all(engine)

# Create a new session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Example query: Fetch all sailors
sailors = session.query(Sailor).all()
for sailor in sailors:
    print(sailor)

# Remember to close the session when you're done
session.close()

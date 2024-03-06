# Simple program to assist employees with common tasks (Part 3)

from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from sailors import Base, Sailor, Boat, Reservation, session, Employee, WorkLog # Adjust this import to match your model definitions
from datetime import datetime

# Adjust the connection string to your SQLite database
DATABASE_URI = 'sqlite:///path/to/your/database.db'

def setup_database_session():
    # Create the database engine and session factory
    engine = create_engine(DATABASE_URI, echo=True)
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    return scoped_session(Session)

def suggest_boats_for_sailor(session, sailor_id):
    # Identify the sailor's most commonly rented boat color
    most_common_color = session.query(
        Boat.color, func.count(Boat.color).label('color_count')
    ).join(Reservation, Boat.bid == Reservation.bid
    ).filter(Reservation.sid == sailor_id
    ).group_by(Boat.color
    ).order_by(func.count(Boat.color).desc()
    ).limit(1).first()

    # Identify the sailor's most commonly rented boat length
    most_common_length = session.query(
        Boat.length, func.count(Boat.length).label('length_count')
    ).join(Reservation, Boat.bid == Reservation.bid
    ).filter(Reservation.sid == sailor_id
    ).group_by(Boat.length
    ).order_by(func.count(Boat.length).desc()
    ).limit(1).first()

    if not most_common_color or not most_common_length:
        print("No rental history found for sailor.")
        return []

    color, _ = most_common_color
    length, _ = most_common_length

    print(f"Sailor's most common color: {color}, length: {length}")

    # Suggest boats with the same color or length.
    suggested_boats = session.query(
        Boat.bid, Boat.bname, Boat.color, Boat.length
    ).filter(
        or_(Boat.color == color, Boat.length == length)
    ).all()

    return suggested_boats

def find_available_boats(session, date_str):
    # Attempt to parse the input date string
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Perform the query to find available boats
    available_boats = session.query(
        Boat
    ).filter(
        Boat.bid.notin_(
            session.query(Reservation.bid
            ).filter(Reservation.day == date)
        )
    ).all()

    if not available_boats:
        print("No boats available for rent on this date.")
        return []

    return available_boats

def calculate_biweekly_salary(session, start_date_str, end_date_str):
    # Attempt to parse the input date strings
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    # Perform the query to calculate biweekly salaries
    biweekly_salaries = session.query(
        Employee.employee_id,
        Employee.ename,
        func.sum(WorkLog.hours_worked).label('total_hours'),
        (func.sum(WorkLog.hours_worked) * Employee.hourly_rate).label('total_pay')
    ).join(
        WorkLog, Employee.employee_id == WorkLog.employee_id
    ).filter(
        WorkLog.work_date.between(start_date, end_date)
    ).group_by(
        Employee.employee_id
    ).all()
    
    # for some reason printing the results in main didn't work correctly, so I moved the print statement here
    for employee in biweekly_salaries:
        print(f"Employee ID: {employee.employee_id}, Name: {employee.ename}, Total Hours: {employee.total_hours}, Total Pay: ${employee.total_pay:.2f}")

# Rudamentary main function to simulate the employee assistance portal. A real version would likely be a web application and have more features/safeguards.
def main():
    session = setup_database_session()

    print("Welcome to the BOATY BOAT employee assistance portal")
    while True:
        print("\nWhat would you like to do:")
        print("1. Suggest boats based on a sailor's rental history")
        print("2. Find available boats for a given date")
        print("3. Calculate the Biweekly salary of employees")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            while True:
                sailor_id = input("Enter sailor's ID or 'back' to return to the main menu: ")
                if sailor_id.lower() == 'back':
                    break
                suggested_boats = suggest_boats_for_sailor(session, sailor_id)
                print("Suggested boats based on your rental history:")
                for boat in suggested_boats:
                    print(f"Boat ID: {boat.bid}, Name: {boat.bname}, Color: {boat.color}, Length: {boat.length}")

        elif choice == "2":
            while True:
                date_input = input("Enter a date (YYYY-MM-DD) to find available boats or 'back' to return to the main menu: ")
                if date_input.lower() == 'back':
                    break
                available_boats = find_available_boats(session, date_input)
                print("Available boats for rent on this date:")
                for boat in available_boats:
                    print(f"Boat ID: {boat.bid}, Name: {boat.bname}, Color: {boat.color}, Length: {boat.length}")

        elif choice == "3":
            while True:
                period_start = input("Enter the start date of the 2-week period (YYYY-MM-DD) or 'back' to return to the main menu: ")
                if period_start.lower() == 'back':
                    break
                period_end = input("Enter the end date of the 2-week period (YYYY-MM-DD) or 'back' to return to the main menu: ")
                if period_end.lower() == 'back':
                    break
                else:
                    calculate_biweekly_salary(session, period_start, period_end)

        elif choice == "4":
            print("Exiting the employee assistance portal.")
            break
        else:
            print("Invalid choice. Please try again.")

    session.remove()

if __name__ == "__main__":
    main()

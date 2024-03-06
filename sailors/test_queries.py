# tests/test_queries.py
import pytest
from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker, scoped_session, aliased
from sqlalchemy import not_, exists, and_, select
from sqlalchemy.sql.expression import over
from sailors import Base, Sailor, Boat, Reservation, session  # Ensure this import matches your setup in sailors.py

DATABASE_URI = 'sqlite:///C:/Users/malek/Desktop/eceProj1/sqlite-tools-win-x64-3450100/sailors.db'

@pytest.fixture(scope="module")
def test_session():
    # Setup for an in-memory SQLite database for testing. Adjust if using a persistent database
    engine = create_engine(DATABASE_URI, echo=True)
    # Correctly pass engine to create_all()
    Base.metadata.create_all(engine)
    _session = sessionmaker(bind=engine)
    session = scoped_session(_session)
    yield session  # This is where the testing happens
    session.remove()


# Prompt 1

def test_list_boats_with_reservations(test_session):
    from sqlalchemy import func
    # Query to replicate the SQL
    query = test_session.query(
        Boat.bid, 
        Boat.bname, 
        func.count(Reservation.sid).label('reservation_count')
    ).join(Reservation, Boat.bid == Reservation.bid
    ).group_by(Boat.bid, Boat.bname
    ).having(func.count(Reservation.sid) > 0
    ).order_by(Boat.bid).all()  # Ordering by bid for consistent results

    # Expected results based on your database state
    expected_results = [
        (101, "Interlake", 2),
        (102, "Interlake", 3),
        (103, "Clipper", 3),
        (104, "Clipper", 5),
        (105, "Marine", 3),
        (106, "Marine", 3),
        (107, "Marine", 1),
        (108, "Driftwood", 1),
        (109, "Driftwood", 4),
        (110, "Klapser", 3),
        (111, "Sooney", 1),
        (112, "Sooney", 1),
    ]

    # Convert query results to a list of tuples for easy comparison
    query_results = [(bid, bname, count) for bid, bname, count in query]

    # Assert that the query results match the expected results
    assert query_results == expected_results

# Prompt 2:
    
def test_sailors_who_reserved_every_red_boat(test_session):
    # First, identify all red boats.
    red_boats = session.query(Boat.bid).filter(Boat.color == 'red').subquery()

    # Then, for each sailor, count the number of unique red boats they've reserved.
    sailor_reservations_for_red_boats = session.query(
        Reservation.sid,
        func.count(distinct(Reservation.bid)).label('reserved_red_boats_count')
    ).join(
        red_boats, Reservation.bid == red_boats.c.bid
    ).group_by(
        Reservation.sid
    ).subquery()

    # Now, get the total number of red boats to establish a baseline for "every" red boat.
    total_red_boats = session.query(func.count()).select_from(red_boats).scalar()

    # Finally, select sailors whose count of reserved red boats matches the total count of red boats.
    sailors_who_reserved_every_red_boat = session.query(
        Sailor.sid, 
        Sailor.sname
    ).join(
        sailor_reservations_for_red_boats, 
        Sailor.sid == sailor_reservations_for_red_boats.c.sid
    ).filter(
        sailor_reservations_for_red_boats.c.reserved_red_boats_count == total_red_boats
    ).all()

    # Assuming the prompt implies there are such sailors, adjust this assertion accordingly.
    # For an exact match with the provided output indicating no sailors meet this criterion, you'd expect an empty result:
    assert len(sailors_who_reserved_every_red_boat) == 0

# Prompt 3:
    
def test_sailors_who_reserved_only_red_boats(test_session):
    # Subquery for sailors who have reserved non-red boats
    sailors_with_non_red_reservations_subq = select(Reservation.sid).join(
        Boat, Reservation.bid == Boat.bid
    ).where(
        Boat.color != 'red'
    ).distinct().alias('non_red_reservations')

    # Main query using an explicit select() to find sailors who have not reserved non-red boats
    sailors_exclusively_reserved_red = test_session.query(Sailor.sid, Sailor.sname).filter(
        Sailor.sid.notin_(
            select(sailors_with_non_red_reservations_subq.c.sid)
        ),
        exists().where(and_(
            Reservation.sid == Sailor.sid,
            Reservation.bid == Boat.bid,
            Boat.color == 'red'
        ))
    ).group_by(Sailor.sid, Sailor.sname).all()

    # Expected result based on the provided output
    expected_sailors = [
        (23, 'emilio'),
        (24, 'scruntus'),
        (35, 'figaro'),
        (62, 'shaun'),
        (61, 'ossola')
    ]

    # Convert query results to a list of tuples for easy comparison
    query_results = sorted([(sid, sname) for sid, sname in sailors_exclusively_reserved_red])

    # Sort the expected list for comparison
    expected_sailors_sorted = sorted(expected_sailors)

    # Assert that the query results match the expected results
    assert query_results == expected_sailors_sorted

# Prompt 4:

def test_boat_with_most_reservations(test_session):
    # Query to find the boat with the highest number of reservations
    most_reserved_boat = session.query(
        Boat.bid, 
        Boat.bname, 
        func.count(Reservation.bid).label('reservation_count')
    ).join(
        Reservation, Boat.bid == Reservation.bid
    ).group_by(
        Boat.bid, Boat.bname
    ).order_by(
        func.count(Reservation.bid).desc()
    ).limit(1).all()

    # Expected result based on the provided output
    expected_result = [(104, 'Clipper', 5)]

    # Assert that the query result matches the expected result
    assert most_reserved_boat == expected_result

# Prompt 5:
    
def test_sailors_never_reserved_red_boat(test_session):
    # Define the subquery for sailors who have reserved red boats, using the SQL Expression Language
    sailors_with_red_reservations_subq = select(Reservation.sid).\
        join(Boat, Boat.bid == Reservation.bid).\
        where(Boat.color == 'red').\
        distinct().\
        scalar_subquery()

    # Main query to find sailors who have never reserved a red boat, correctly using the subquery
    sailors_never_reserved_red = test_session.query(
        Sailor.sid, 
        Sailor.sname
    ).filter(
        ~Sailor.sid.in_(sailors_with_red_reservations_subq)
    ).order_by(Sailor.sid).all()

    # Expected result based on the provided output
    expected_sailors = [
        (29, 'brutus'),
        (32, 'andy'),
        (58, 'rusty'),
        (60, 'jit'),
        (71, 'zorba'),
        (74, 'horatio'),
        (85, 'art'),
        (90, 'vin'),
        (95, 'bob'),
        (99, 'joe'),
    ]

    # Convert query results to a list of tuples for easy comparison
    query_results = sorted([(sid, sname) for sid, sname in sailors_never_reserved_red])

    # Assert that the query results match the expected results
    assert query_results == expected_sailors

# Prompt 6:

def test_average_age_of_sailors_with_rating_10(test_session):
    # Query to calculate the average age of sailors with a rating of 10
    average_age = test_session.query(
        func.avg(Sailor.age).label('average_age')
    ).filter(
        Sailor.rating == 10
    ).scalar()  # Use .scalar() to get the first column of the first row

    # Since the database might return a Decimal or float, we round the result for comparison
    average_age_rounded = round(average_age, 2)

    # Expected result based on the provided output
    expected_average_age = 35.00

    # Assert that the calculated average age matches the expected average age
    assert average_age_rounded == expected_average_age

# Prompt 7:
    
def test_youngest_sailor_by_rating(test_session):
    # Define an alias for sailors to use for window function
    SailorAlias = aliased(Sailor)

    # Use the window function to assign ranks based on age within each rating
    ranked_sailors = select(
        SailorAlias.sid,
        SailorAlias.sname,
        SailorAlias.rating,
        SailorAlias.age,
        func.row_number().over(
            partition_by=SailorAlias.rating,
            order_by=SailorAlias.age.asc()
        ).label('rank')
    ).alias('ranked_sailors')

    # Select sailors where rank is 1, meaning the youngest sailor per rating
    youngest_sailors_query = select(
        ranked_sailors.c.sid,
        ranked_sailors.c.sname,
        ranked_sailors.c.rating,
        ranked_sailors.c.age
    ).where(
        ranked_sailors.c.rank == 1
    )

    youngest_sailors = test_session.execute(youngest_sailors_query).fetchall()

    # Expected results
    expected_results = [
        (24, 'scruntus', 1, 33.0),
        (85, 'art', 3, 25.0),
        (61, 'ossola', 7, 16.0),
        (32, 'andy', 8, 25.0),
        (74, 'horatio', 9, 25.0),
        (58, 'rusty', 10, 35.0),
    ]

    # Convert query results to a list of tuples for comparison
    query_results = sorted([(sid, sname, rating, age) for sid, sname, rating, age in youngest_sailors])

    # Sort the expected list for comparison
    expected_results_sorted = sorted(expected_results)

    # Assert that the query results match the expected results
    assert query_results == expected_results_sorted

# Prompt 8:
    
def test_sailor_with_most_reservations_per_boat(test_session):
    # Assuming Reservation, Sailor, and Boat are your ORM models and they're properly imported

    # Alias for easier subquery referencing
    R = aliased(Reservation)
    S = aliased(Sailor)
    B = aliased(Boat)

    # First, create a subquery to count reservations per sailor per boat
    reservation_counts = select(
        R.bid,
        R.sid,
        func.count().label('reservation_count')
    ).group_by(
        R.bid,
        R.sid
    ).alias('reservation_counts')

    # Next, create another subquery to find the maximum reservation count for each boat
    max_reservation_counts = select(
        reservation_counts.c.bid,
        func.max(reservation_counts.c.reservation_count).label('max_reservation_count')
    ).group_by(
        reservation_counts.c.bid
    ).alias('max_reservation_counts')

    # Final query joining with the Boat and Sailor tables
    most_reservations_query = select(
        B.bid,
        B.bname,
        S.sid,
        S.sname,
        reservation_counts.c.reservation_count
    ).select_from(
        reservation_counts.join(B, reservation_counts.c.bid == B.bid)
                           .join(S, reservation_counts.c.sid == S.sid)
                           .join(max_reservation_counts, and_(
                               reservation_counts.c.bid == max_reservation_counts.c.bid,
                               reservation_counts.c.reservation_count == max_reservation_counts.c.max_reservation_count
                           ))
    ).order_by(
        B.bid,
        reservation_counts.c.reservation_count.desc()
    )

    results = test_session.execute(most_reservations_query).fetchall()

    expected_results = [
        # (bid, bname, sid, sname, reservation_count),
        (101,'Interlake',22,'dusting',1),
        (101,'Interlake',64,'horatio',1),
        (102,'Interlake',22,'dusting',1),
        (102,'Interlake',31,'lubber',1),
        (102,'Interlake',64,'horatio',1),
        (103,'Clipper',22,'dusting',1),
        (103,'Clipper',31,'lubber',1),
        (103,'Clipper',74,'horatio',1),
        (104,'Clipper',22,'dusting',1),
        (104,'Clipper',23,'emilio',1),
        (104,'Clipper',24,'scruntus',1),
        (104,'Clipper',31,'lubber',1),
        (104,'Clipper',35,'figaro',1),
        (105,'Marine',23,'emilio',1),
        (105,'Marine',35,'figaro',1),
        (105,'Marine',59,'stum',1),
        (106,'Marine',60,'jit',2),
        (107,'Marine',88,'dan',1),
        (108,'Driftwood',89,'dye',1),
        (109,'Driftwood',59,'stum',1),
        (109,'Driftwood',60,'jit',1),
        (109,'Driftwood',89,'dye',1),
        (109,'Driftwood',90,'vin',1),
        (110,'Klapser',88,'dan',2),
        (111,'Sooney',88,'dan',1),
        (112,'Sooney',61,'ossola',1),
    ]

    assert [(row[0], row[1], row[2], row[3], row[4]) for row in results] == expected_results

# results of tests: https://prnt.sc/zR-kM54UMLPV
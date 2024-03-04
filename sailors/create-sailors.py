'''
Create a Sailors and Boats dataset in Python
@eugsokolov
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///C:/Users/malek/Desktop/eceProj1/sqlite-tools-win-x64-3450100/sailors.db', echo=True)


Session = sessionmaker(bind = engine)
session = Session()

sailors = [
INSERT INTO sailors VALUES	(22,"dusting",7,45.0);
INSERT INTO sailors VALUES	(23,"emilio",7,45.0);
INSERT INTO sailors VALUES	(24,"scruntus",1,33.0);
INSERT INTO sailors VALUES	(29,"brutus",1,33.0);
INSERT INTO sailors VALUES	(31,"lubber",8,55.5);
INSERT INTO sailors VALUES	(32,"andy",8,25.5);
INSERT INTO sailors VALUES	(35,"figaro",8,55.5);
INSERT INTO sailors VALUES	(58,"rusty",10,35);
INSERT INTO sailors VALUES	(59,"stum",8,25.5);
INSERT INTO sailors VALUES	(60,"jit",10,35);
INSERT INTO sailors VALUES	(61,"ossola",7,16);
INSERT INTO sailors VALUES	(62,"shaun",10,35);
INSERT INTO sailors VALUES	(64,"horatio",7,16);
INSERT INTO sailors VALUES	(71,"zorba",10,35);
INSERT INTO sailors VALUES	(74,"horatio",9,25.5);
INSERT INTO sailors VALUES	(85,"art",3,25.5);
INSERT INTO sailors VALUES	(88,"kevin",3,25.5);
INSERT INTO sailors VALUES	(89,"will",3,25.5);
INSERT INTO sailors VALUES	(90,"josh",3,25.5);
INSERT INTO sailors VALUES	(95,"bob",3,63.5);
]

boats = [
	(101,"Interlake","blue",45),
	(102,"Interlake","red",45),
	(103,"Clipper","green",40),
	(104,"Clipper","red",40),
	(105,"Marine","red",35),
	(106,"Marine","green",35),
	(107,"Marine","blue",35),
	(108,"Driftwood","red",35),
	(109,"Driftwood","blue",35),
	(110,"Klapser","red",30),
	(111,"Sooney","green",28),
	(112,"Sooney","red",28),
]

reserves = [
	(22,101,"1998-10-10"),
	(22,102,"1998-10-10"),
	(22,103,"1998-08-10"),
	(22,104,"1998-07-10"),
	(23,104,"1998-10-10"),
	(23,105,"1998-11-10"),
	(24,104,"1998-10-10"),
	(31,102,"1998-11-10"),
	(31,103,"1998-11-06"),
	(31,104,"1998-11-12"),
	(35,104,"1998-08-10"),
	(35,105,"1998-11-06"),
	(59,105,"1998-07-10"),
	(59,106,"1998-11-12"),
	(59,109,"1998-11-10"),
	(60,106,"1998-09-05"),
	(60,106,"1998-09-08"),
	(60,109,"1998-07-10"),
	(61,112,"1998-09-08"),
	(62,110,"1998-11-06"),
	(64,101,"1998-09-05"),
	(64,102,"1998-09-08"),
	(74,103,"1998-09-08"),
	(88,107,"1998-09-08"),
	(88,110,"1998-09-05"),
	(88,110,"1998-11-12"),
	(88,111,"1998-09-08"),
	(89,108,"1998-10-10"),
	(89,109,"1998-08-10"),
	(90,109,"1998-10-10"),
]


#TODO

session.commit()



from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine("sqlite:///chinook.sqlite")

# reflect the tables
Base.prepare(engine, reflect=True)

session = Session(engine)

print (Base.classes.keys())

Album = Base.classes.Album
Artist = Base.classes.Artist
Track = Base.classes.Track

print (Artist.__table__.foreign_keys)
print (Album.__table__.foreign_keys)
print (Track.__table__.foreign_keys)
#print (Album.__table__.columns)
#print (Album.__table__.constraints)
#print (Album.__table__.indexes)
#print (Album.__table__.primary_key)

u1 = session.query(Album).select_from(Artist)
u2 = session.query(Album).join(Artist).filter(Artist.ArtistId==1)

print (u1)
print (u2)

for cols in u2:
  print (cols.__dict__)

#u1 = session.query(Album).join("Artist", aliased=True).filter(Artist.ArtistId==1)

#for x in u1:
#  print (x.__dict__)

print(u2)

# /Artists

s = "Artists".split('/')

if len(s) % 2 == 0:
  print (s)
else:
  s.append("")
  print (s)

# /Artists/1
# /Artists/1/Albums
# /Artists/1/Albums/3
# /Artists/1/Albums/3/Tracks

def query(table, rest):
  print (table, rest)
  
  q = session.query(table)

  for t in rest.keys():
    print(q, t)
    print(q.join(t))

  print (q)

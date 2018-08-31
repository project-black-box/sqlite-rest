from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#u1 = session.query(Album).select_from(Artist)
#u2 = session.query(Album).join(Artist).filter(Artist.ArtistId==1)

# /Artists/1
# /Artists/1/Albums
# /Artists/1/Albums/3
# /Artists/1/Albums/3/Tracks

def query(joins):
  Base = automap_base()

  # engine, suppose it has two tables 'user' and 'address' set up
  engine = create_engine("sqlite:///chinook.sqlite")

  # reflect the tables
  Base.prepare(engine, reflect=True)

  session = Session(engine)

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
  print (Base.classes.keys())

  hashmap = {
    "Artist": Artist,
    "Album": Album,
    "Track": Track
  }

  obj = hashmap[joins[0]['table']]
  q = session.query(obj)

  for j in joins[1::]:
    obj = hashmap[j['table']]
    q = q.join(obj)

  return str(q)

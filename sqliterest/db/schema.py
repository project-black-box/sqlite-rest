from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()
engine = create_engine("sqlite:///chinook.sqlite")
Base.prepare(engine, reflect=True)

#u1 = session.query(Album).select_from(Artist)
#u2 = session.query(Album).join(Artist).filter(Artist.ArtistId==1)

#Base = automap_base()
#engine = create_engine("sqlite:///chinook.sqlite")
#Base.prepare(engine, reflect=True)
#Album = Base.classes.Album
#print (Album.__table__.foreign_keys)
#print (Album.__table__.columns)
#print (Album.__table__.constraints)
#print (Album.__table__.indexes)
#print (Album.__table__.primary_key)
#print (Base.classes.keys())

# /Artist/1
# /Artist/1/Album
# /Artist/1/Album/3
# /Artist/1/Album/3/Track

def row2dict(row):
  d = {}
  for column in row.__table__.columns:
    d[column.name] = str(getattr(row, column.name))
  return d

def get_mapping(table):
  return Base.classes[table['name']]

def get_primary_key(table):
  obj = get_mapping(table)
  cols = obj.__table__.primary_key.columns
  keys = cols.keys()
  # can we have multiple primary keys?
  key = keys[0]
  return cols[key]

def join(query, table, first=False):
  obj = get_mapping(table)

  if first:
    query = query.query(obj)
  else:
    query = query.join(obj)

  if table['key'] != None:
    pk = get_primary_key(table)
    query = query.filter(pk == table['key'])
  
  return query

def query(tables):
  q = join(Session(engine), tables[0], True)

  for t in tables[1::]:
    q = join(q, t)

  rest = [row2dict(x) for x in q.all()]

  return rest
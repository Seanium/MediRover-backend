from database import db

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mapname = db.Column(db.String(20), unique=True)
    mappath = db.Column(db.String(128))
    waypointpath = db.Column(db.String(128))
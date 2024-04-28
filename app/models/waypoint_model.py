from database import db


class Waypoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waypointname = db.Column(db.String(20), unique=True)
    pos_x = db.Column(db.Float)
    pos_y = db.Column(db.Float)
    pos_z = db.Column(db.Float)
    ori_x = db.Column(db.Float)
    ori_y = db.Column(db.Float)
    ori_z = db.Column(db.Float)
    ori_w = db.Column(db.Float)
    table_height = db.Column(db.Float)

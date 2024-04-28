from database import db


# 患者表
class Pt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    # 病床航点ID是外码
    waypoint_id = db.Column(db.Integer, db.ForeignKey("waypoint.id"))

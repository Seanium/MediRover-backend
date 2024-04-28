from database import db


class Robot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    robot_status = db.Column(db.String(64))
    robot_ip = db.Column(db.String(64))
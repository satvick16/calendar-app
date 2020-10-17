from datetime import datetime
from flaskblog import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.String(4), nullable=False)
    end_time = db.Column(db.String(4), nullable=False)
    repeat = db.Column(db.String(1), nullable=False, default=False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.date}')"

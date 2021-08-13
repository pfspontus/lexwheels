"""
SQLAlchemy Owner model class
"""


def init(db):
    class Owner(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True, nullable=False)

        def __repr__(self):
            return f'<Owner {self.name}>'
    return Owner

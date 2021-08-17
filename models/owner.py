"""
SQLAlchemy Owner model class
"""


def init(db):
    class Owner(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True, nullable=False)

        def __repr__(self):
            return f'<Owner {self.name}>'

        def as_dict(self):
            d = {
                'id': self.id,
                'name': self.name,
                'cars': [c.as_dict() for c in self.cars]
            }
            return d

    return Owner

"""
SQLAlchemy Car model class
"""


def init(db):
    class Car(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        owner_id = db.Column(db.Integer,
                             db.ForeignKey('owner.id'),
                             nullable=False)
        owner = db.relationship('Owner',
                                backref=db.backref('cars', lazy=True))
        make = db.Column(db.String(100),
                         unique=False, nullable=False)
        model = db.Column(db.String(100),
                          unique=False, nullable=False)
        year = db.Column(db.Integer,
                         unique=False, nullable=False)

        def __repr__(self):
            year = self.year or '<unknown year>'
            make = self.make or '<unknown make>'
            model = self.model or '<unknown model>'
            return f'<Car {year}, {make} {model}>'
    return Car

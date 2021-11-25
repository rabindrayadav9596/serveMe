from datetime import datetime
from . import db
from flask_login import UserMixin

db.metadata.clear()

class User (UserMixin, db.Model):
    def get_id(self):
        return (self.userID)
    userID         = db.Column(db.String(50), primary_key=True)
    email           = db.Column(db.String(50), nullable=False)
    name            = db.Column(db.String(30), nullable=False)
    password        = db.Column(db.String(100))
    gender          = db.Column(db.String(20))
    age             = db.Column(db.Integer, nullable=False)
    phoneNum    = db.Column(db.String(10), nullable=False)
    points     = db.Column(db.Integer, nullable=False)
    #reviews         = db.relationship('Review', backref='author', lazy=True)
    
    def __repr__(self):
        return 'String representation of user'
    

class Order (db.Model):
    order_id        = db.Column(db.Integer, primary_key=True)
    provider_id     = db.Column(db.Integer, nullable=False)
    service_id      = db.Column(db.Integer, nullable=False)
    userID         = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    cost            = db.Column(db.Float(precision=2), nullable=False)
    review_id       = db.Column(db.Integer)
    description     = db.Column(db.String(255))
    date            = db.Column(db.DateTime())
    
    def __repr__(self):
        return f'{self.order_id}-{self.provider_id}-{self.service_id}-{self.userID} - {self.cost} - {self.review_id} - {self.description} - {self.date} '
    
class Review (db.Model):
    review_id       = db.Column(db.Integer, primary_key=True)
    userID         = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    provider_id     = db.Column(db.Integer, nullable=False)
    review_text     = db.Column(db.String(255), nullable=False)
    date_posted     = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    number_stars    = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return 'String representation of Reviews'


class Provider (db.Model):
    provider_id     = db.Column(db.Integer, primary_key=True)
    provider_name   = db.Column(db.String(50), nullable=False)
    rating_avg      = db.Column(db.Float)
    phone_number    = db.Column(db.String(10), nullable=False)
    address         = db.Column(db.String(25), nullable=False)
    email           = db.Column(db.String(20), nullable=False)
    ssn             = db.Column(db.String(9), nullable=False)
    services        = db.relationship('Service', backref='service_provider', lazy=True)
    
    def __repr__(self):
        return f'{self.provider_id}-{self.provider_name}-{self.rating_avg}-{self.phone_number} - {self.address} - {self.email} - {self.ssn} - {self.services} '
    

# Different services that a provider has
class Service (db.Model):
    __searchable__  = ['description']
    provider_id     = db.Column(db.Integer, db.ForeignKey('provider.provider_id'), nullable=False)
    service_id      = db.Column(db.Integer, nullable=False, primary_key=True)
    rating_avg      = db.Column(db.Float(precision=2), nullable=False)
    service_name    = db.Column(db.String(20), nullable=False)
    cost            = db.Column(db.Float(precision=2), nullable=False)
    description     = db.Column(db.String(255), nullable=False)
    category        = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'{self.provider_id}-{self.service_id}-{self.rating_avg}-{self.service_name} - {self.cost} - {self.description} - {self.category} '
        # return [{self.service_name,self.cost,self.description,self.category}]
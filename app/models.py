from app.main import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.BigInteger)
    message = db.Column(db.String())
    timestamp = db.Column(db.BigInteger) 

    def __init__(self, phone, message, timestamp):
        self.phone = phone
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return '<phone: {} timestamp: {}>'.format(self.id, self.timestamp)

    def serialize(self):
        return {
            'phone': self.phone, 
            'message': self.message,
            'timestamp': self.timestamp,
        }
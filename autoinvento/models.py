from autoinvento import db, login_manager
from datetime import datetime
from flask_login import UserMixin



# A user loader function that Flask-Login will use to load users from the database
@login_manager.user_loader
def load_user(mechanic_id):
    return Mechanics.query.get(int(mechanic_id))


class Mechanics(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    requests = db.relationship('InventoryRequest', back_populates='requester')
    usage_logs = db.relationship('UsageLog', back_populates='mechanic')
    notifications = db.relationship('Notification', back_populates='owner')
    
    def __repr__(self):
        return f"Mechanics('{self.username}', '{self.email}', '{self.image_file}')"


class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    low_stock_threshold = db.Column(db.Integer, default=10)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    supplier = db.relationship('Supplier', back_populates='items')
    usage_logs = db.relationship('UsageLog', back_populates='items', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', back_populates='items', cascade='all, delete-orphan')
    requests = db.relationship('InventoryRequest', back_populates='requested_item')

    def __repr__(self):
        return f"Item('{self.name}', '{self.quantity}', '{self.date_added}')"


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=True)
    contact = db.Column(db.String(125), nullable=True)
    items = db.relationship('InventoryItem', back_populates='supplier')

    def __repr__(self):
        return f"Item('{self.name}', '{self.email}', '{self.contact}')"


class UsageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    quantity_used = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    mechanic = db.relationship('Mechanics', back_populates='usage_logs', foreign_keys=[mechanic_id])
    items = db.relationship('InventoryItem', back_populates='usage_logs', foreign_keys=[item_id])

    def __repr__(self):
        return f"Item('{self.item_id}', '{self.quantity_used}', '{self.timestamp}')"
    

class InventoryRequest(db.Model):
    __tablename__ = 'inventory_request'
    
    id = db.Column(db.Integer, primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)  # User who made the request
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)  # Requested item
    quantity_requested = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # Status can be 'pending', 'approved' or 'rejected'
    request_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    requester = db.relationship('Mechanics', back_populates='requests', lazy=True)
    requested_item = db.relationship('InventoryItem', back_populates='requests')

    def __init__(self, mechanic_id, item_id, quantity_requested, status):
        self.mechanic_id = mechanic_id
        self.item_id = item_id
        self.quantity_requested = quantity_requested
        self.status = status
    
    def __repr__(self):
        return f"InventoryRequest('{self.item_id}', '{self.mechanic_id}', '{self.quantity_requested}', '{self.status}', '{self.request_timestamp}')"


class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    item_id =db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)
    quantity_requested = db.Column(db.Integer)
    message = db.Column(db.String(256), nullable=False)
    inventory_request_id = db.Column(db.Integer, db.ForeignKey('inventory_request.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    owner = db.relationship('Mechanics', back_populates='notifications')
    items = db.relationship('InventoryItem', back_populates='notifications')
   
    def __init__(self, request_id, item_id, quantity):
        self.request_id = request_id
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self):
        return f"Notification('{self.item_id}', '{self.message}', {self.timestamp})"



from flask import (
    url_for,
)
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from datetime import datetime
from .utilities.constants import (
    USER_TYPES,
    EXPIRY_TYPES
)
from datetime import datetime

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


class Users(db.Model):
    __tablename__ = "users_profile"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(250), nullable=False)
    user_type = db.Column(db.Integer, nullable=False, default=USER_TYPES["USER"])
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password():
        raise ValueError("Invalid Request")

    @password.setter
    def password(self, pass_):
        self.password_hash = generate_password_hash(pass_)

    def valid_passkey(self, pass_):
        return check_password_hash(self.password_hash, pass_)

    def to_dict(self):
        data = {
            "id": self.id,
            "user_type": self.user_type,
            "username": self.username,
            "email": self.email,
            "join_date": self.join_date,

        }
        return data


    def __repr__(self):
        return f"User<ID: {self.id}, USERNAME: {self.username}>"


class Links(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    original_link = db.Column(db.String(250), nullable=False)
    short_link = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey(
        "users_profile.id",
        ondelete="CASCADE",
        onupdate="CASCADE"))

    created_by = db.relationship("Users", backref=db.backref(
        'links', lazy="dynamic", passive_deletes=True), uselist=False)


    def to_dict(self):
        data = {
            "id": self.id,
            "original_link": self.original_link,
            "short_link": self.short_link,
            "created_at": self.created_at,
            "created_by": self.created_by.to_dict(),
        }

        return data

    def __repr__(self):
        return f"Link<ID: {self.id}, OL: {self.original_link}, SL: {self.short_link}"


class Clicks(db.Model):
    __tablename__ = "clicks"
    id = db.Column(db.Integer, primary_key=True)
    time_click = db.Column(db.DateTime, default=datetime.utcnow)
    counter = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    link_id = db.Column(db.Integer, db.ForeignKey("links.id", ondelete="CASCADE",
        onupdate="CASCADE"))

    link = db.relationship("Links", backref=db.backref(
        "clicks", lazy="dynamic", passive_deletes=True), uselist=False)

    def to_dict(self):
        data = {
            "id": self.id,
            "time_click": self.time_click,
            "counter": self.counter,
            "created_at": self.created_at,
            "link": self.link.to_dict(),
        }
        return data

    def __repr__(self):
        return f"Click<ID: {self.id}, CTR: {self.counter}>"


class Subscriptions(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_type = db.Column(db.String(15), nullable=False, default=EXPIRY_TYPES["YEARLY"])
    expiry_offset = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "created_at": self.created_at,
            "expiry_type": self.type,
            "expiry_offset": self.expiry_offset,
        }
        return data


    def __repr__(self):
        return f"Subscription<ID: {self.id}, TITLE: {self.title}, PRICE: {self.price}"


class UsersSubscriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    added_by_id = db.Column(db.Integer, db.ForeignKey(
        "users_profile.id",
        ondelete="CASCADE",
        onupdate="CASCADE"))
    status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subscription_id = db.Column(db.Integer, db.ForeignKey(
        "subscriptions.id",
        ondelete="CASCADE",
        onupdate="CASCADE"))

    added_by = db.relationship("Users", backref=db.backref(
        'mysubs', lazy="dynamic", passive_deletes=True), uselist=False)
    subscription = db.relationship("Subscriptions", backref=db.backref(
        'sub_list', lazy="dynamic", passive_deletes=True), uselist=False)

    def to_dict(self):
        data = {
            "id": self.id,
            "added_by": self.added_by.to_dict(),
            "status": self.status,
            "created_at": self.created_at,
            "subscription": self.subscription.to_dict(),
        }
        return data


    def __repr__(self):
        return f"UserSubscription<ID: {self.id}, BY: {self.added_by.to_dict().get('username')}, STATUS: {self.satus}>"
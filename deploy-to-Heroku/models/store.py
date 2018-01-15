from db import db

class StoreModel(db.Model):
    # specify table name and columns
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80)) # 80 character maximum to limit the size

    # back reference: look items to see which items are in this store. we do this because prevent it looking into database to create items everytime when we create store model, and only create when we call json()
    # but it will look in database everytime when we call json(), so it's a trade-off between creation and calling json()
    items = db.relationship('ItemModel', lazy = 'dynamic') # when we do lazy = 'dynamic, the self.items in json(self) became a query builder

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    # keep this as class method since it will return a dictionary other than a model object
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

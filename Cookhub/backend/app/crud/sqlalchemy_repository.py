class SqlAlchemyRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get(self, id):
        return self.session.query(self.model).get(id)
    # modern version: return self.session.get(self.model, id)

    def list(self):
        return self.session.query(self.model).all()

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()

    def save(self):
        self.session.commit()

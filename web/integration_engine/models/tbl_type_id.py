from integration_engine import db


class TypeId(db.Model):

    __tablename__ = "tbl_type_id"
    ccn_type_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.String(2), nullable=False)
    description_type_id = db.Column(db.String(40), nullable=False)

    # Relationships
    rel_employee = db.relationship("Employee", backref="TypeId", lazy=True)

    def __init__(self, type_id, description_type_id):

        self.type_id = type_id
        self.description_type_id = description_type_id

    def choice_query():
        return TypeId.query

    def __repr__(self):
        return f"TypeID: {self.description_type_id}"

    def save(self):
        if not self.description_type_id:
            db.session.add(self)
            db.session.commit()

    def delete_type(type_id):
        q = TypeId.query.filter(TypeId.type_id == type_id).first()

        db.session.delete(q)
        db.session.commit()

        return print(q)

    @staticmethod
    def get_by_id(id_fixed_asset):
        return TypeId.query.get(id_fixed_asset)

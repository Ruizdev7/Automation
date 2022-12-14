from werkzeug.security import generate_password_hash, check_password_hash

from integration_engine import db


class Employee(db.Model):

    __tablename__ = "tbl_employee"
    ccn_employee = db.Column(db.Integer, primary_key=True)
    ccn_type_id = db.Column(db.Integer, db.ForeignKey("tbl_type_id.ccn_type_id"))
    number_id_employee = db.Column(db.Integer, nullable=False)
    first_name_employee = db.Column(db.String(30), nullable=False)
    middle_name_employee = db.Column(db.String(30), nullable=True)
    first_last_name_employee = db.Column(db.String(30), nullable=False)
    second_last_name_employee = db.Column(db.String(30), nullable=True)
    full_name_employee = db.Column(db.String(200), nullable=False)
    date_birth_employee = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    employee_personal_email = db.Column(db.String(100), nullable=False)
    employee_personal_cellphone = db.Column(db.String(40), nullable=False)
    informed_consent_law_1581 = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    employee_password = db.Column(db.String(300), nullable=False)

    def __init__(
        self,
        ccn_type_id,
        number_id_employee,
        first_name_employee,
        middle_name_employee,
        first_last_name_employee,
        second_last_name_employee,
        full_name_employee,
        date_birth_employee,
        age,
        employee_personal_email,
        employee_personal_cellphone,
        informed_consent_law_1581,
        image,
        employee_password,
    ):
        self.ccn_type_id = ccn_type_id
        self.number_id_employee = number_id_employee
        self.first_name_employee = first_name_employee
        self.middle_name_employee = middle_name_employee
        self.first_last_name_employee = first_last_name_employee
        self.second_last_name_employee = second_last_name_employee
        self.full_name_employee = full_name_employee
        self.date_birth_employee = date_birth_employee
        self.age = age
        self.employee_personal_email = employee_personal_email
        self.employee_personal_cellphone = employee_personal_cellphone
        self.informed_consent_law_1581 = informed_consent_law_1581
        self.image = image
        self.employee_password = employee_password

    def __repr__(self):
        return f"Employee: {self.full_name_employee}"

    def set_employee_password(self, employee_password):
        self.employee_password = generate_password_hash(employee_password)
        return self.employee_password

    def check_employee_password(self, employee_password):
        return check_password_hash(self.password, employee_password)

    def choice_query():
        return Employee.query

    def save(self):
        if not self.number_id_employee:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(number_id_employee):
        return Employee.query.get(number_id_employee)

    @staticmethod
    def get_by_email(employee_email):
        return Employee.query.filter_by(employee_email=employee_email).first()

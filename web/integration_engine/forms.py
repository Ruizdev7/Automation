from wtforms import FileField
from wtforms import SubmitField
from wtforms import StringField
from wtforms import SelectField
from wtforms import IntegerField
from wtforms import DecimalField
from wtforms import PasswordField
from wtforms import TextAreaField

from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import Email, Length
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from integration_engine import db
from integration_engine.models.tbl_roles import Role
from integration_engine.models.tbl_type_id import TypeId
from integration_engine.models.tbl_employee import Employee


class RegisterEmployee(FlaskForm):

    ccn_type_id = QuerySelectField(
        "Type ID",
        query_factory=TypeId.choice_query,
        get_label="description_type_id",
    )

    number_id_employee = IntegerField(
        "Number of Identification",
        validators=[
            DataRequired(message="This field is mandatory *"),
            Length(
                max=10, min=6, message="The field must have between 6 to 10 characters"
            ),
        ],
    )

    first_name_employee = StringField(
        "First Name",
        validators=[
            DataRequired(message="This field is mandatory"),
            Length(
                max=30, min=2, message="The field must have between 2 to 30 characters"
            ),
        ],
    )

    middle_name_employee = StringField(
        "Middle Name",
        validators=[
            Length(
                max=30, min=2, message="The field must have between 2 to 30 characters"
            )
        ],
    )

    first_last_name_employee = StringField(
        "Firts Last Name",
        validators=[
            DataRequired(message="This field is mandatory"),
            Length(
                max=30, min=2, message="The field must have between 3 to 12 characters"
            ),
        ],
    )

    second_last_name_employee = StringField(
        "Second Last Name",
        validators=[
            # DataRequired(message="This field is mandatory"),
            Length(
                max=30, min=2, message="The field must have between 3 to 12 characters"
            ),
        ],
    )

    date_birth_employee = DateField("Date Birth Employee")

    employee_personal_email = StringField(
        "Personal Email",
        validators=[DataRequired(message="This field is mandatory"), Email()],
    )

    employee_personal_cellphone = StringField(
        "Personal Cell-phone",
        validators=[DataRequired(message="This field is mandatory"), Email()],
    )

    img_employee = FileField("Employee Photo")

    employee_password = PasswordField("Password")

    submit = SubmitField("SUBMIT")


class LoginEmployee(FlaskForm):

    employee_personal_email = StringField(
        "Email address",
        validators=[DataRequired(message="This field is mandatory"), Email()],
    )

    employee_password = PasswordField("Password")

    submit = SubmitField("Submit")


class CreateTypeOfDocument(FlaskForm):
    type_id = StringField(
        "ID Tipo de mantenimiento",
        validators=[
            DataRequired(message="This field is mandatory"),
            Length(
                max=20,
                min=1,
                message="The field must have between 3 to 200 characters",
            ),
        ],
    )

    description_type_id = StringField(
        "description type",
        validators=[
            DataRequired(message="This field is mandatory"),
            Length(
                max=20,
                min=1,
                message="The field must have between 3 to 200 characters",
            ),
        ],
    )

    submit = SubmitField("Submit")


class ResetPassword(FlaskForm):
    usermail = StringField(
        "Usermail",
        validators=[
            DataRequired(message="This field is mandatory"),
            Length(
                max=20,
                min=1,
                message="The field must have between 3 to 20 characters",
            ),
        ],
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(message="This field is mandatory"),
            Length(
                max=20,
                min=1,
                message="The field must have between 3 to 20 characters",
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="This field is mandatory"),
            Length(
                max=20,
                min=1,
                message="The field must have between 3 to 20 characters",
            ),
        ],
    )

    submit = SubmitField("Submit")


class CreateRole(FlaskForm):

    area = StringField(
        "Area",
        validators=[
            DataRequired(message="Este campo es obligatorio(*)"),
            Length(
                max=50, min=1, message="El campo debera tener entre 1 y 50 caracteres"
            ),
        ],
    )

    role = StringField(
        "Role -> Cargo",
        validators=[
            DataRequired(message="Este campo es obligatorio(*)"),
            Length(
                max=50, min=1, message="El campo debera tener entre 1 y 50 caracteres"
            ),
        ],
    )

    associated_process = StringField(
        "Proceso Asociado",
        validators=[
            DataRequired(message="Este campo es obligatorio(*)"),
            Length(
                max=50, min=1, message="El campo debera tener entre 1 y 50 caracteres"
            ),
        ],
    )

    submit = SubmitField("CREAR")


class CreateTypeId(FlaskForm):

    type_id = StringField(
        "Tipo ID",
        validators=[
            DataRequired(message="Este campo es obligatorio(*)"),
            Length(
                max=40, min=1, message="El campo debera tener entre 1 y 40 caracteres"
            ),
        ],
    )

    description_type_id = StringField(
        "Tipo de identificacion",
        validators=[
            DataRequired(message="Este campo es obligatorio(*)"),
            Length(
                max=40, min=1, message="El campo debera tener entre 1 y 40 caracteres"
            ),
        ],
    )

    submit = SubmitField("CREAR")

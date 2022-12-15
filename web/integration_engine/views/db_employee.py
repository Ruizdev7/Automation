import os
import datetime
from email import message
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from integration_engine import db
from integration_engine import forms
from integration_engine.models.tbl_roles import Role
from integration_engine.models.tbl_type_id import TypeId
from integration_engine.models.tbl_employee import Employee


blueprint_db_employee = Blueprint("db_employee", __name__, url_prefix="")

# CREATE READ UPDATE DELETE BASIC DATA EMPLOYEE
@blueprint_db_employee.route("/registerEmployee", methods=["GET", "POST"])
def registerEmployee():
    form = forms.RegisterEmployee(request.form)
    if request.method == "GET":
        return render_template("login/signup.html", form=form)
    else:

        ccn_type_id = request.form["ccn_type_id"]
        number_id_employee = request.form["number_id_employee"]
        first_name_employee = request.form["first_name_employee"].upper()
        middle_name_employee = request.form["middle_name_employee"].upper()
        first_last_name_employee = request.form["first_last_name_employee"].upper()
        second_last_name_employee = request.form["second_last_name_employee"].upper()
        full_name_employee = (
            first_name_employee
            + " "
            + middle_name_employee
            + " "
            + first_last_name_employee
            + " "
            + second_last_name_employee
        )
        date_birth_employee = request.form["date_birth_employee"]
        pre_age = date_birth_employee.split("-")
        year = datetime.datetime.now()
        age = int(year.year) - int(pre_age[0])
        employee_personal_email = request.form["employee_personal_email"]
        employee_personal_cellphone = request.form["employee_personal_cellphone"]
        informed_consent_law_1581 = "yes"

        if request.files["img_employee"]:
            employee_photo = request.files["img_employee"]
            filename = secure_filename(employee_photo.filename)
            image = filename
            employee_photo.save(
                os.path.join(
                    "integration_engine/static/images/employee_photos", filename
                )
            )

        else:
            image = "not_registered.jpg"

        employee_password = generate_password_hash(request.form["employee_password"])

        new_employee = Employee(
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
        )

        db.session.add(new_employee)
        db.session.commit()

        return redirect(url_for("db_employee.list_employee"))


@blueprint_db_employee.route("/list_employee", methods=["GET", "POST"])
@blueprint_db_employee.route("/list_employee/<message>", methods=["GET", "POST"])
def list_employee(message=None):
    title = "List Employees"
    form = forms.RegisterEmployee()
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        user_html = query_logged_user.full_name_employee
        if request.method == "GET":
            query_list_employee = Employee.query.all()
            return render_template(
                "database_employees/basic_data_employee.html",
                query_logged_user=query_logged_user,
                query_list_employee=query_list_employee,
                title=title,
                user=user_name,
                form=form,
                user_html=user_html,
                message=message,
            )
        else:
            return render_template(
                "database_employees/basic_data_employee.html",
                query_logged_user=query_logged_user,
                query_list_employee=query_list_employee,
                title=title,
                user=user_name,
                form=form,
                user_html=user_html,
                message=message,
            )
    else:
        mensajeErrorSesion = "There is no active session please enter the platform"
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))


@blueprint_db_employee.route(
    "/update_employee/<int:ccn_employee>", methods=["GET", "POST"]
)
def update_employee(ccn_employee):
    if request.method == "GET":

        query_employee = Employee.query.filter_by(ccn_employee=ccn_employee).first()
        query_type_id = TypeId.query.filter_by(
            ccn_type_id=query_employee.ccn_type_id
        ).first()

        form = forms.RegisterEmployee(
            ccn_type_id=query_type_id,
            number_id_employee=query_employee.number_id_employee,
            first_name_employee=query_employee.first_name_employee,
            middle_name_employee=query_employee.middle_name_employee,
            first_last_name_employee=query_employee.first_last_name_employee,
            second_last_name_employee=query_employee.second_last_name_employee,
            full_name_employee=query_employee.full_name_employee,
            date_birth_employee=query_employee.date_birth_employee,
            employee_personal_email=query_employee.employee_personal_email,
            employee_personal_cellphone=query_employee.employee_personal_cellphone,
            image=query_employee.image,
            employee_password=query_employee.employee_password,
        )
        return render_template(
            "database_employees/update_data_employee.html",
            form=form,
            query_employee=query_employee,
            ccn_employee=ccn_employee,
        )
    elif request.method == "POST":

        query_employee = Employee.query.filter_by(ccn_employee=ccn_employee).first()

        query_employee.ccn_type_id = request.form["ccn_type_id"]
        query_employee.number_id_employee = request.form["number_id_employee"]
        query_employee.first_name_employee = request.form["first_name_employee"].upper()
        query_employee.middle_name_employee = request.form[
            "middle_name_employee"
        ].upper()
        query_employee.first_last_name_employee = request.form[
            "first_last_name_employee"
        ].upper()
        query_employee.second_last_name_employee = request.form[
            "second_last_name_employee"
        ].upper()
        query_employee.full_name_employee = (
            request.form["first_name_employee"].upper()
            + " "
            + request.form["middle_name_employee"].upper()
            + " "
            + request.form["first_last_name_employee"].upper()
            + " "
            + request.form["second_last_name_employee"].upper()
        )
        query_employee.date_birth_employee = request.form["date_birth_employee"]
        pre_age = request.form["date_birth_employee"].split("-")
        year = datetime.datetime.now()
        query_employee.age = int(year.year) - int(pre_age[0])
        query_employee.employee_personal_email = request.form["employee_personal_email"]
        query_employee.employee_personal_cellphone = request.form[
            "employee_personal_cellphone"
        ]
        query_employee.informed_consent_law_1581 = "yes"

        if request.files["img_employee"]:
            employee_photo = request.files["img_employee"]
            filename = secure_filename(employee_photo.filename)
            query_employee.image = filename
            employee_photo.save(
                os.path.join("hhrr_app/static/images/employee_photos", filename)
            )

        if request.form["employee_password"]:
            query_employee.employee_password = generate_password_hash(
                request.form["employee_password"]
            )
        else:
            query_employee.employee_password = query_employee.employee_password

        form = forms.RegisterEmployee(request.form)
        db.session.commit()

        type_message = "update"
        flash(f"{query_employee.full_name_employee} has been updated correctly")
        return redirect(
            url_for("db_employee.list_employee", flash=flash, message=type_message)
        )

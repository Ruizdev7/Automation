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
        query_auto_perceived_gender = AutoPerceivedGender.query.filter_by(
            ccn_auto_perceived_gender=query_employee.auto_perceived_gender
        ).first()
        query_age_range = AgeRange.query.filter_by(
            ccn_age_range=query_employee.age_range
        ).first()
        query_rh = RH.query.filter_by(ccn_rh=query_employee.rh).first()
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
            age_range=query_age_range,
            auto_perceived_gender=query_auto_perceived_gender,
            rh=query_rh,
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
        query_employee.age_range = request.form["age_range"]
        query_employee.auto_perceived_gender = request.form["auto_perceived_gender"]
        query_employee.rh = request.form["rh"]
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


# CREATE READ UPDATE DELETE Social Security Affiliation Form
@blueprint_db_employee.route(
    "/list_employee_social_security_affiliation", methods=["GET", "POST"]
)
@blueprint_db_employee.route(
    "/list_employee_social_security_affiliation/<message>", methods=["GET", "POST"]
)
def list_employee_social_security_affiliation(message=None):
    title = "List Employees Social Security Affiliation"
    form = forms.CreateSSEmployee()
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_ss_employee = SSEmployee.query.all()
            return render_template(
                "database_employees/employee_social_security_affiliation.html",
                query_logged_user=query_logged_user,
                query_list_ss_employee=query_list_ss_employee,
                title=title,
                user=user_name,
                form=form,
                message=message,
            )
        else:

            query_list_ss_employee = SSEmployee.query.all()

            return render_template(
                "database_employees/employee_social_security_affiliation.html",
                query_logged_user=query_logged_user,
                query_list_ss_employee=query_list_ss_employee,
                title=title,
                user=user_name,
                form=form,
                message=message,
            )
    else:
        mensajeErrorSesion = "There is no active session please enter the platform"
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))


@blueprint_db_employee.route("/create_ss_employee", methods=["GET", "POST"])
def create_ss_employee():
    form = forms.CreateSSEmployee(request.form)
    title = "New SS Employee"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateSSEmployee(request.form)
        if request.method == "GET":
            return render_template(
                "database_employees/employee_social_security_affiliation.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:
            ccn_employee = request.form["ccn_employee"]
            ccn_type_affiliation = request.form["ccn_type_affiliation"]
            ccn_type_contributor = request.form["ccn_type_contributor"]
            ccn_eps = request.form["ccn_eps"]
            ccn_afp = request.form["ccn_afp"]
            ccn_arl = request.form["ccn_arl"]
            ccn_ccf = request.form["ccn_ccf"]
            ccn_aap = request.form["ccn_aap"]

            new_ss_employee = SSEmployee(
                ccn_employee,
                ccn_type_affiliation,
                ccn_type_contributor,
                ccn_eps,
                ccn_afp,
                ccn_arl,
                ccn_ccf,
                ccn_aap,
            )

            db.session.add(new_ss_employee)
            db.session.commit()
            type_message = "create"
            flash(f"{ccn_employee} has been created correctly")
            return redirect(
                url_for(
                    "db_employee.list_employee_social_security_affiliation",
                    flash=flash,
                    message=type_message,
                )
            )
    else:
        mensajeErrorSesion = "There is no active session please enter the platform"
        flash(mensajeErrorSesion)
        return redirect(url_for("index.index"))


@blueprint_db_employee.route(
    "/update_ss_employee/<int:ccn_ss_employee>", methods=["GET", "POST"]
)
def update_ss_employee(ccn_ss_employee):
    if request.method == "GET":

        query_ss_employee = SSEmployee.query.filter_by(
            ccn_ss_employee=ccn_ss_employee
        ).first()

        query_ccn_employee = Employee.query.filter_by(
            ccn_employee=query_ss_employee.ccn_employee
        ).first()

        form = forms.CreateSSEmployee(
            ccn_employee=query_ccn_employee,
            ccn_type_affiliation=query_ss_employee.ccn_type_affiliation,
            ccn_type_contributor=query_ss_employee.ccn_type_contributor,
            ccn_eps=query_ss_employee.ccn_eps,
            ccn_afp=query_ss_employee.ccn_afp,
            ccn_arl=query_ss_employee.ccn_arl,
            ccn_ccf=query_ss_employee.ccn_ccf,
            ccn_aap=query_ss_employee.ccn_aap,
        )
        return render_template(
            "database_employees/update_ss_employee.html",
            form=form,
            query_ss_employee=query_ss_employee,
            ccn_ss_employee=ccn_ss_employee,
        )
    elif request.method == "POST":

        query_ss_employee = SSEmployee.query.filter_by(
            ccn_ss_employee=ccn_ss_employee
        ).first()

        query_ss_employee.ccn_employee = request.form["ccn_employee"]
        query_ss_employee.ccn_type_affiliation = request.form["ccn_type_affiliation"]
        query_ss_employee.ccn_type_contributor = request.form["ccn_type_contributor"]
        query_ss_employee.ccn_eps = request.form["ccn_eps"]
        query_ss_employee.ccn_afp = request.form["ccn_afp"]
        query_ss_employee.ccn_alr = request.form["ccn_arl"]
        query_ss_employee.ccn_ccf = request.form["ccn_ccf"]
        query_ss_employee.ccn_aap = request.form["ccn_aap"]

        form = forms.CreateSSEmployee(request.form)
        db.session.commit()

        type_message = "update"
        flash(f"El registro se ha actualizado correctamente")
        return redirect(
            url_for(
                "db_employee.list_employee_social_security_affiliation",
                flash=flash,
                message=type_message,
            )
        )


# CREATE READ UPDATE DELETE EMPLOYMENT RELATIONSHIP
@blueprint_db_employee.route("/list_employment_relationship", methods=["GET", "POST"])
@blueprint_db_employee.route(
    "/list_employment_relationship/<message>", methods=["GET", "POST"]
)
def list_employment_relationship(message=None):
    title = "Lista Vinculacion Laboral"
    form = forms.CreateEmploymentRelationship()
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_employment_relationship = EmploymentRelationship.query.all()
            return render_template(
                "database_employees/employment_relationship.html",
                query_logged_user=query_logged_user,
                query_list_employment_relationship=query_list_employment_relationship,
                title=title,
                user=user_name,
                form=form,
                message=message,
            )
        else:
            query_list_employment_relationship = EmploymentRelationship.query.all()

            return render_template(
                "database_employees/employment_relationship.html",
                query_logged_user=query_logged_user,
                query_list_employment_relationship=query_list_employment_relationship,
                title=title,
                user=user_name,
                form=form,
                message=message,
            )
    else:
        mensajeErrorSesion = "There is no active session please enter the platform"
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))


@blueprint_db_employee.route("/create_employment_relationship", methods=["GET", "POST"])
def create_employment_relationship():
    form = forms.CreateEmploymentRelationship(request.form)
    title = "Registrar Vinculacion Laboral"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateEmploymentRelationship(request.form)
        if request.method == "GET":
            return render_template(
                "database_employees/employment_relationship.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:

            ccn_employee = request.form["employee"]
            ccn_role = request.form["role"]
            ccn_work_shift = request.form["work_shift"]
            binding_date = request.form["binding_date"]
            # termination_date = request.form["termination_date"]
            termination_date = "2000-01-01 11:11:11"
            time_worked = 0.0
            pending_days_to_enjoy_for_holidays = 0.0
            ccn_type_relationship = request.form["type_relationship"]
            employee_corporate_email = request.form["employee_corporate_email"].upper()
            employee_corporate_cellphone = request.form["employee_corporate_cellphone"]

            new_employment_relationship = EmploymentRelationship(
                ccn_employee,
                ccn_role,
                ccn_work_shift,
                binding_date,
                termination_date,
                time_worked,
                pending_days_to_enjoy_for_holidays,
                ccn_type_relationship,
                employee_corporate_email,
                employee_corporate_cellphone,
            )

            db.session.add(new_employment_relationship)
            db.session.commit()
            type_message = "create"
            flash(
                f"La vinculacion laboral para el empleado con ccn {ccn_employee} ha sido creada correctamente"
            )
            return redirect(
                url_for(
                    "db_employee.list_employment_relationship",
                    flash=flash,
                    message=type_message,
                )
            )
    else:
        mensajeErrorSesion = "No hay una sesion activa porfavor ingrese a la plataforma"
        flash(mensajeErrorSesion)
        return redirect(url_for("index.index"))


@blueprint_db_employee.route(
    "/update_employment_relationship/<int:ccn_employment_relationship>",
    methods=["GET", "POST"],
)
def update_employment_relationship(ccn_employment_relationship):
    if request.method == "GET":
        query_employment_relationship = EmploymentRelationship.query.filter_by(
            ccn_employment_relationship=ccn_employment_relationship
        ).first()

        query_employee = Employee.query.filter_by(
            ccn_employee=query_employment_relationship.ccn_employee
        ).first()

        query_role = Role.query.filter_by(
            ccn_role=query_employment_relationship.ccn_role
        ).first()

        query_work_shift = WorkShift.query.filter_by(
            ccn_work_shift=query_employment_relationship.ccn_work_shift
        ).first()

        query_type_relationship = TypeRelationship.query.filter_by(
            ccn_type_relationship=query_employment_relationship.ccn_type_relationship
        ).first()

        form = forms.CreateEmploymentRelationship(
            employee=query_employee,
            role=query_role,
            work_shift=query_work_shift,
            binding_date=query_employment_relationship.binding_date,
            type_relationship=query_type_relationship,
            employee_corporate_email=query_employment_relationship.employee_corporate_email,
            employee_corporate_cellphone=query_employment_relationship.employee_corporate_cellphone,
        )
        return render_template(
            "database_employees/update_employment_relationship.html",
            form=form,
            query_employment_relationship=query_employment_relationship,
            ccn_employment_relationship=ccn_employment_relationship,
        )
    elif request.method == "POST":

        query_employment_relationship = EmploymentRelationship.query.filter_by(
            ccn_employment_relationship=ccn_employment_relationship
        ).first()

        query_employment_relationship.ccn_employee = request.form["employee"]
        query_employment_relationship.ccn_role = request.form["role"]
        query_employment_relationship.ccn_work_shift = request.form["work_shift"]
        query_employment_relationship.binding_date = request.form["binding_date"]
        query_employment_relationship.ccn_type_relationship = request.form[
            "type_relationship"
        ]
        query_employment_relationship.employee_corporate_email = request.form[
            "employee_corporate_email"
        ].upper()
        query_employment_relationship.employee_corporate_cellphone = request.form[
            "employee_corporate_cellphone"
        ]

        form = forms.CreateEmploymentRelationship(request.form)
        db.session.commit()
        type_message = "update"
        flash(
            f"{query_employment_relationship.ccn_employment_relationship} ha sido actualizado correctamente"
        )
        return redirect(
            url_for(
                "db_employee.list_employment_relationship",
                flash=flash,
                message=type_message,
            )
        )


@blueprint_db_employee.route(
    "/delete_employment_relationship/<int:ccn_employment_relationship>",
    methods=["GET", "POST"],
)
def delete_employment_relationship(ccn_employment_relationship):
    form = forms.CreateEmploymentRelationship(request.form)
    if "user_name" in session:
        EmploymentRelationship.delete_employment_relationship(
            ccn_employment_relationship
        )
        type_message = "delete"
        flash(f"El tipo de vinculacion ha sido eliminado correctamente")
        return redirect(
            url_for(
                "db_employee.list_employment_relationship",
                flash=flash,
                message=type_message,
            )
        )


# CREATE READ UPDATE DELETE DEMOGRAPHIC DATA
@blueprint_db_employee.route("/list_demographic_data", methods=["GET", "POST"])
@blueprint_db_employee.route(
    "/list_demographic_data/<message>", methods=["GET", "POST"]
)
def list_demographic_data(message=None):
    title = "Lista Datos Demograficos"
    form = forms.CreateDemographicData()
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_demographic_data = DemographicData.query.all()
            return render_template(
                "database_employees/demographic_data.html",
                query_logged_user=query_logged_user,
                query_list_demographic_data=query_list_demographic_data,
                title=title,
                user=user_name,
                form=form,
                message=message,
            )
        else:
            query_list_demographic_data = DemographicData.query.all()

            return render_template(
                "database_employees/demographic_data.html",
                query_logged_user=query_logged_user,
                query_list_demographic_data=query_list_demographic_data,
                title=title,
                user=user_name,
                form=form,
                message=message,
            )
    else:
        mensajeErrorSesion = "There is no active session please enter the platform"
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))


@blueprint_db_employee.route("/create_demographic_data", methods=["GET", "POST"])
def create_demographic_data():
    form = forms.CreateDemographicData(request.form)
    title = "Registrar Datos Demograficos"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateDemographicData(request.form)
        if request.method == "GET":
            return render_template(
                "database_employees/demographic_data.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:
            ccn_employee = request.form["employee"]

            birth_department = request.form["birth_department"]
            birth_city = request.form["birth_city"]
            department_residence = request.form["department_residence"]
            city_residence = request.form["city_residence"]
            ccn_schooling_level = request.form["ccn_schooling_level"]
            ccn_race = request.form["ccn_race"]

            if "on" in request.form.getlist("switch_is_head_of_household"):
                is_head_of_household = 1
            elif not request.form.getlist("switch_is_head_of_household"):
                is_head_of_household = 0

            new_demographic_data = DemographicData(
                ccn_employee,
                birth_department,
                birth_city,
                department_residence,
                city_residence,
                ccn_schooling_level,
                ccn_race,
                is_head_of_household,
            )

            db.session.add(new_demographic_data)
            db.session.commit()
            type_message = "create"
            flash(
                f"La creacion de datos demograficos para el empleado con ccn {ccn_employee} ha sido creada correctamente"
            )
            return redirect(
                url_for(
                    "db_employee.list_demographic_data",
                    flash=flash,
                    message=type_message,
                )
            )
    else:
        mensajeErrorSesion = "No hay una sesion activa porfavor ingrese a la plataforma"
        flash(mensajeErrorSesion)
        return redirect(url_for("index.index"))


# CREATE READ UPDATE DELETE EMERGENCY CONTACT DATA
@blueprint_db_employee.route(
    "/create_emergency_contact_details", methods=["GET", "POST"]
)
def create_emergency_contact_details():
    title = "Detalles Contacto de Emergencia"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateEmergencyContactDetails(request.form)
        if request.method == "GET":
            return render_template(
                "db_employee/emergency_contact_details.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:
            ccn_employee = request.form["employee"]
            emergency_contact = request.form["emergency_contact"]
            relationship = request.form["relationship"]
            cellphone = request.form["cellphone"]

            new_emergency_contact_details = EmergencyContactDetails(
                ccn_employee=ccn_employee,
                emergency_contact=emergency_contact,
                ccn_relationship=relationship,
                cellphone=cellphone,
            )

            db.session.add(new_emergency_contact_details)
            db.session.commit()
            type_message = "create"
            flash(
                f"El contacto de emergencia para el empleado {ccn_employee} ha sido creado correctamente!!!"
            )
            return redirect(
                url_for(
                    "db_employee.emergency_contact_details",
                    flash=flash,
                    message=type_message,
                )
            )
    else:
        mensajeErrorSesion = (
            "No hay una sesion activa porfavor inicia sesion en la plataforma"
        )
        flash(mensajeErrorSesion)
        return redirect(url_for("index.index"))


@blueprint_db_employee.route("/emergency_contact_details", methods=["GET", "POST"])
@blueprint_db_employee.route(
    "/emergency_contact_details/<message>", methods=["GET", "POST"]
)
def emergency_contact_details(message=None):
    message = message
    title = "Lista Contactos de Emergencia"
    form = forms.CreateEmergencyContactDetails(request.form)
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_emergency_contact_details = EmergencyContactDetails.query.all()
            return render_template(
                "database_employees/emergency_contact_details.html",
                query_list_emergency_contact_details=query_list_emergency_contact_details,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
        else:
            query_list_emergency_contact_details = EmergencyContactDetails.query.all()
            return render_template(
                "database_employees/emergency_contact_details.html",
                query_list_emergency_contact_details=query_list_emergency_contact_details,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
    else:
        mensajeErrorSesion = (
            "No hay una sesion activa porfavor inicia sesion en la plataforma"
        )
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))


@blueprint_db_employee.route(
    "/update_emergency_contact_details/<int:ccn_emergency_contact_details>",
    methods=["GET", "POST"],
)
def update_emergency_contact_details(ccn_emergency_contact_details):
    if request.method == "GET":

        query_emergency_contact_details = EmergencyContactDetails.query.filter_by(
            ccn_emergency_contact_details=ccn_emergency_contact_details
        ).first()

        query_relationship = Relationship.query.filter_by(
            ccn_relationship=query_emergency_contact_details.ccn_relationship
        ).first()

        query_employee = Employee.query.filter_by(
            ccn_employee=query_emergency_contact_details.ccn_employee
        ).first()

        form = forms.CreateEmergencyContactDetails(
            ccn_employee=query_employee,
            emergency_contact=query_emergency_contact_details.emergency_contact,
            relationship=query_relationship,
            cellphone=query_emergency_contact_details.cellphone,
        )
        return render_template(
            "database_employees/update_emergency_contact_details.html",
            form=form,
            query_emergency_contact_details=query_emergency_contact_details,
            ccn_emergency_contact_details=ccn_emergency_contact_details,
        )
    elif request.method == "POST":

        query_emergency_contact_details = EmergencyContactDetails.query.filter_by(
            ccn_emergency_contact_details=ccn_emergency_contact_details
        ).first()

        query_emergency_contact_details.ccn_employee = request.form["employee"]
        query_emergency_contact_details.emergency_contact = request.form[
            "emergency_contact"
        ]
        query_emergency_contact_details.relationship = request.form["relationship"]
        query_emergency_contact_details.cellphone = request.form["cellphone"]

        form = forms.CreateEmergencyContactDetails(request.form)
        db.session.commit()
        type_message = "update"
        flash(
            f"El contacto de emergencia del empleado {query_emergency_contact_details.Employee.full_name_employee} ha sido actualizada correctamente"
        )
        return redirect(
            url_for(
                "db_employee.emergency_contact_details",
                flash=flash,
                message=type_message,
            )
        )


@blueprint_db_employee.route(
    "/delete_emergency_contact_details/<int:ccn_emergency_contact_details>",
    methods=["GET", "POST"],
)
def delete_emergency_contact_details(ccn_emergency_contact_details):
    form = forms.CreateEmergencyContactDetails(request.form)
    if "user_name" in session:
        EmergencyContactDetails.delete_emergency_contact_details(
            ccn_emergency_contact_details
        )
        type_message = "delete"
        flash(f"Los datos de contacto de emergencia ha sido eliminados correctamente")
        return redirect(
            url_for(
                "db_employee.emergency_contact_details",
                flash=flash,
                message=type_message,
            )
        )


# CREATE READ UPDATE DELETE FAMILY NUCLEUS
@blueprint_db_employee.route("/create_family_nucleus", methods=["GET", "POST"])
def create_family_nucleus():
    title = "Detalle del nucleo familiar"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateFamilyNucleus(request.form)
        if request.method == "GET":
            return render_template(
                "db_employee/family_nucleus_detail.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:
            ccn_employee = request.form["ccn_employee"]
            ccn_marital_status = request.form["ccn_marital_status"]
            number_of_children = request.form["number_of_children"]
            ccn_type_id = request.form["ccn_type_id"]
            number_id = request.form["number_id"]
            ccn_auto_perceived_gender = request.form["ccn_auto_perceived_gender"]
            first_name = request.form["first_name"]
            middle_name = request.form["middle_name"]
            first_last_name = request.form["first_last_name"]
            second_last_name = request.form["second_last_name"]
            date_of_birth = request.form["date_of_birth"]
            age = request.form["age"]
            age_range = request.form["age_range"]
            ccn_schooling_level = request.form["ccn_schooling_level"]

            new_family_nucleus = FamilyNucleus(
                ccn_employee,
                ccn_marital_status,
                number_of_children,
                ccn_type_id,
                number_id,
                ccn_auto_perceived_gender,
                first_name,
                middle_name,
                first_last_name,
                second_last_name,
                date_of_birth,
                age,
                age_range,
                ccn_schooling_level,
            )

            db.session.add(new_family_nucleus)
            db.session.commit()
            type_message = "create"
            flash(
                f"Los datos del nucleo familiar para el empleado {ccn_employee} ha sido creado correctamente!!!"
            )
            return redirect(
                url_for(
                    "db_employee.family_nucleus_details",
                    flash=flash,
                    message=type_message,
                )
            )
    else:
        mensajeErrorSesion = (
            "No hay una sesion activa porfavor inicia sesion en la plataforma"
        )
        flash(mensajeErrorSesion)
        return redirect(url_for("index.index"))


@blueprint_db_employee.route("/family_nucleus_details", methods=["GET", "POST"])
@blueprint_db_employee.route(
    "/family_nucleus_details/<message>", methods=["GET", "POST"]
)
def family_nucleus_details(message=None):
    message = message
    title = "Lista de datos del nucleo familiar"
    form = forms.CreateFamilyNucleus(request.form)
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_family_nucleus = FamilyNucleus.query.all()
            return render_template(
                "database_employees/family_nucleus_detail.html",
                query_list_family_nucleus=query_list_family_nucleus,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
        else:
            query_list_family_nucleus = FamilyNucleus.query.all()
            return render_template(
                "database_employees/family_nucleus_detail.html",
                query_list_family_nucleus=query_list_family_nucleus,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
    else:
        mensajeErrorSesion = (
            "No hay una sesion activa porfavor inicia sesion en la plataforma"
        )
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))


@blueprint_db_employee.route(
    "/update_family_nucleus/<int:ccn_family_nucleus>",
    methods=["GET", "POST"],
)
def update_family_nucleus(ccn_family_nucleus):
    if request.method == "GET":

        query_family_nucleus = FamilyNucleus.query.filter_by(
            ccn_family_nucleus=ccn_family_nucleus
        ).first()

        query_martial_status = MaritalStatus.query.filter_by(
            ccn_marital_status=query_family_nucleus.ccn_marital_status
        ).first()
        query_employee = Employee.query.filter_by(
            ccn_employee=query_family_nucleus.ccn_employee
        ).first()
        query_auto_perceived_gender = AutoPerceivedGender.query.filter_by(
            ccn_auto_perceived_gender=query_family_nucleus.ccn_auto_perceived_gender
        ).first()
        query_type_id = TypeId.query.filter_by(
            ccn_type_id=query_family_nucleus.ccn_type_id
        ).first()

        form = forms.CreateFamilyNucleus(
            ccn_employee=query_employee,
            ccn_marital_status=query_martial_status,
            number_of_children=query_family_nucleus.number_of_children,
            ccn_type_id=query_type_id,
            number_id=query_family_nucleus.number_id,
            ccn_auto_perceived_gender=query_auto_perceived_gender,
            first_name=query_family_nucleus.first_name,
            middle_name=query_family_nucleus.middle_name,
            first_last_name=query_family_nucleus.first_last_name,
            second_last_name=query_family_nucleus.second_last_name,
            date_of_birth=query_family_nucleus.date_of_birth,
            age=query_family_nucleus.age,
            age_range=query_family_nucleus.age_range,
            ccn_schooling_level=query_family_nucleus.ccn_schooling_level,
        )
        return render_template(
            "database_employees/update_family_nucleus_detail.html",
            form=form,
            query_family_nucleus=query_family_nucleus,
            ccn_family_nucleus=ccn_family_nucleus,
        )
    elif request.method == "POST":

        query_family_nucleus = FamilyNucleus.query.filter_by(
            ccn_family_nucleus=ccn_family_nucleus
        ).first()

        query_family_nucleus.ccn_employee = request.form["ccn_employee"]
        query_family_nucleus.ccn_marital_status = request.form["ccn_marital_status"]
        query_family_nucleus.number_of_children = request.form["number_of_children"]
        query_family_nucleus.ccn_type_id = request.form["ccn_type_id"]
        query_family_nucleus.number_id = request.form["number_id"]
        query_family_nucleus.ccn_auto_perceived_gender = request.form[
            "ccn_auto_perceived_gender"
        ]
        query_family_nucleus.first_name = request.form["first_name"]
        query_family_nucleus.middle_name = request.form["middle_name"]
        query_family_nucleus.first_last_name = request.form["first_last_name"]
        query_family_nucleus.second_last_name = request.form["second_last_name"]
        query_family_nucleus.date_of_birth = request.form["date_of_birth"]
        query_family_nucleus.age = request.form["age"]
        query_family_nucleus.age_range = request.form["age_range"]
        query_family_nucleus.ccn_schooling_level = request.form["ccn_schooling_level"]

        form = forms.CreateFamilyNucleus(request.form)
        db.session.commit()
        type_message = "update"
        flash(
            f"El nucleo familiar del empleado {query_family_nucleus.Employee.ccn_employee} ha sido actualizada correctamente"
        )
        return redirect(
            url_for(
                "db_employee.family_nucleus_details",
                flash=flash,
                message=type_message,
            )
        )


@blueprint_db_employee.route(
    "/delete_family_nucleus/<int:ccn_family_nucleus>",
    methods=["GET", "POST"],
)
def delete_family_nucleus(ccn_family_nucleus):
    form = forms.CreateFamilyNucleus(request.form)
    if "user_name" in session:
        FamilyNucleus.delete_family_nuclus(ccn_family_nucleus)
        type_message = "delete"
        flash(f"Los datos del nucleo familiar han sido eliminados correctamente")
        return redirect(
            url_for(
                "db_employee.family_nucleus_details",
                flash=flash,
                message=type_message,
            )
        )


# CREATE READ UPDATE DELETE SOCIODEMOGRAPHICDATA
@blueprint_db_employee.route("/create_sociodemographic_data", methods=["GET", "POST"])
def create_sociodemographic_data():
    title = "Detalle de los datos sociodemograficos"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateSociodemographicData(request.form)
        if request.method == "GET":
            return render_template(
                "db_employee/sociodemographic_data_detail.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:

            ccn_employee = request.form["ccn_employee"]
            other_dependents = request.form["other_dependents"]
            relatives = request.form["relatives"]
            people_with_disabilities = request.form["people_with_disabilities"]
            monthly_income = request.form["monthly_income"]
            is_income_enougth = request.form["is_income_enougth"]
            ccn_sub_house_type = request.form["ccn_sub_house_type"]
            ccn_house_type = request.form["ccn_house_type"]
            where_its_located = request.form["where_its_located"]
            residence_address = request.form["residence_address"]
            type_transportation = request.form["type_transportation"]
            social_stratum = request.form["social_stratum"]
            electric_power = request.form["electric_power"]
            sewerage = request.form["sewerage"]
            aqueduct = request.form["aqueduct"]
            natural_gas = request.form["natural_gas"]
            garbage_collection = request.form["garbage_collection"]
            landline = request.form["landline"]
            debts = request.form["debts"]
            debt_refinancing = request.form["debt_refinancing"]
            computer_at_home = request.form["computer_at_home"]
            have_internet_access = request.form["have_internet_access"]

            new_sociodemographic_data = SociodemographicData(
                ccn_employee,
                other_dependents,
                relatives,
                people_with_disabilities,
                monthly_income,
                is_income_enougth,
                ccn_sub_house_type,
                ccn_house_type,
                where_its_located,
                residence_address,
                type_transportation,
                social_stratum,
                electric_power,
                sewerage,
                aqueduct,
                natural_gas,
                garbage_collection,
                landline,
                debts,
                debt_refinancing,
                computer_at_home,
                have_internet_access,
            )

            db.session.add(new_sociodemographic_data)
            db.session.commit()
            type_message = "create"
            flash(
                f"Los datos sociodemograficos para el empleado {ccn_employee} ha sido creado correctamente!!!"
            )
            return redirect(
                url_for(
                    "db_employee.sociodemographic_data_details",
                    flash=flash,
                    message=type_message,
                )
            )
    else:
        mensajeErrorSesion = (
            "No hay una sesion activa porfavor inicia sesion en la plataforma"
        )
        flash(mensajeErrorSesion)
        return redirect(url_for("index.index"))


@blueprint_db_employee.route("/sociodemographic_data_details", methods=["GET", "POST"])
@blueprint_db_employee.route(
    "/sociodemographic_data_details/<message>", methods=["GET", "POST"]
)
def sociodemographic_data_details(message=None):
    message = message
    title = "Lista de datos sociodemograficos"
    form = forms.CreateSociodemographicData(request.form)
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_sociodemographic_data = SociodemographicData.query.all()
            return render_template(
                "database_employees/sociodemographic_data_detail.html",
                query_list_sociodemographic_data=query_list_sociodemographic_data,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
        else:
            query_list_sociodemographic_data = SociodemographicData.query.all()
            return render_template(
                "database_employees/sociodemographic_data_detail.html",
                query_list_sociodemographic_data=query_list_sociodemographic_data,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
    else:
        mensajeErrorSesion = (
            "No hay una sesion activa porfavor inicia sesion en la plataforma"
        )
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))


@blueprint_db_employee.route(
    "/update_sociodemographic_data/<int:ccn_sociodemographic_data>",
    methods=["GET", "POST"],
)
def update_sociodemographic_data(ccn_sociodemographic_data):
    if request.method == "GET":

        query_sociodemographic_data = SociodemographicData.query.filter_by(
            ccn_sociodemographic_data=ccn_sociodemographic_data
        ).first()

        query_employee = Employee.query.filter_by(
            ccn_employee=query_sociodemographic_data.ccn_employee
        ).first()

        query_subhouse_type = SubHouseType.query.filter_by(
            ccn_sub_house_type=query_sociodemographic_data.ccn_sub_house_type
        ).first()

        ccn_house_type = HouseType.query.filter_by(
            ccn_house_type=query_sociodemographic_data.ccn_house_type
        ).first()

        form = forms.CreateSociodemographicData(
            ccn_employee=query_employee,
            other_dependents=query_sociodemographic_data.other_dependents,
            relatives=query_sociodemographic_data.relatives,
            people_with_disabilities=query_sociodemographic_data.people_with_disabilities,
            monthly_income=query_sociodemographic_data.monthly_income,
            is_income_enougth=query_sociodemographic_data.is_income_enougth,
            ccn_sub_house_type=query_subhouse_type,
            ccn_house_type=ccn_house_type,
            where_its_located=query_sociodemographic_data.where_its_located,
            residence_address=query_sociodemographic_data.residence_address,
            type_transportation=query_sociodemographic_data.type_transportation,
            social_stratum=query_sociodemographic_data.social_stratum,
            electric_power=query_sociodemographic_data.electric_power,
            sewerage=query_sociodemographic_data.sewerage,
            aqueduct=query_sociodemographic_data.aqueduct,
            natural_gas=query_sociodemographic_data.natural_gas,
            garbage_collection=query_sociodemographic_data.garbage_collection,
            landline=query_sociodemographic_data.landline,
            debts=query_sociodemographic_data.debts,
            debt_refinancing=query_sociodemographic_data.debt_refinancing,
            computer_at_home=query_sociodemographic_data.computer_at_home,
            have_internet_access=query_sociodemographic_data.have_internet_access,
        )
        return render_template(
            "database_employees/update_sociodemographic_data_detail.html",
            form=form,
            query_sociodemographic_data=query_sociodemographic_data,
            ccn_sociodemographic_data=ccn_sociodemographic_data,
        )
    elif request.method == "POST":

        query_sociodemographic_data = SociodemographicData.query.filter_by(
            ccn_sociodemographic_data=ccn_sociodemographic_data
        ).first()

        query_sociodemographic_data.ccn_employee = request.form["ccn_employee"]
        query_sociodemographic_data.other_dependents = request.form["other_dependents"]
        query_sociodemographic_data.relatives = request.form["relatives"]
        query_sociodemographic_data.people_with_disabilities = request.form[
            "people_with_disabilities"
        ]
        query_sociodemographic_data.monthly_income = request.form["monthly_income"]
        query_sociodemographic_data.is_income_enougth = request.form[
            "is_income_enougth"
        ]
        query_sociodemographic_data.ccn_sub_house_type = request.form[
            "ccn_sub_house_type"
        ]
        query_sociodemographic_data.ccn_house_type = request.form["ccn_house_type"]
        query_sociodemographic_data.where_its_located = request.form[
            "where_its_located"
        ]
        query_sociodemographic_data.residence_address = request.form[
            "residence_address"
        ]
        query_sociodemographic_data.type_transportation = request.form[
            "type_transportation"
        ]
        query_sociodemographic_data.social_stratum = request.form["social_stratum"]
        query_sociodemographic_data.electric_power = request.form["electric_power"]
        query_sociodemographic_data.sewerage = request.form["sewerage"]
        query_sociodemographic_data.aqueduct = request.form["aqueduct"]
        query_sociodemographic_data.natural_gas = request.form["natural_gas"]
        query_sociodemographic_data.garbage_collection = request.form[
            "garbage_collection"
        ]
        query_sociodemographic_data.landline = request.form["landline"]
        query_sociodemographic_data.debts = request.form["debts"]
        query_sociodemographic_data.debt_refinancing = request.form["debt_refinancing"]
        query_sociodemographic_data.computer_at_home = request.form["computer_at_home"]
        query_sociodemographic_data.have_internet_access = request.form[
            "have_internet_access"
        ]

        form = forms.CreateFamilyNucleus(request.form)
        db.session.commit()
        type_message = "update"
        flash(
            f"Los datos sociodemograficos del empleado {query_sociodemographic_data.Employee.ccn_employee} ha sido actualizada correctamente"
        )
        return redirect(
            url_for(
                "db_employee.sociodemographic_data_details",
                flash=flash,
                message=type_message,
            )
        )


@blueprint_db_employee.route(
    "/delete_sociodemographic_data/<int:ccn_sociodemographic_data>",
    methods=["GET", "POST"],
)
def delete_sociodemographic_data(ccn_sociodemographic_data):
    form = forms.CreateSociodemographicData(request.form)
    if "user_name" in session:
        SociodemographicData.delete_sociodemographic_data(ccn_sociodemographic_data)
        type_message = "delete"
        flash(f"Los datos del nucleo familiar han sido eliminados correctamente")
        return redirect(
            url_for(
                "db_employee.sociodemographic_data_details",
                flash=flash,
                message=type_message,
            )
        )


# CREATE READ UPDATE DELETE SOCIODEMOGRAPHICDATA
@blueprint_db_employee.route("/create_health_condition", methods=["GET", "POST"])
def create_health_condition():
    title = "Detalle del estado de salud"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateHealthCondition(request.form)
        if request.method == "GET":
            return render_template(
                "db_employee/health_condition_detail.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:
            ccn_employee = request.form["ccn_employee"]
            consume_alcoholic_beverages = request.form["consume_alcoholic_beverages"]
            diseases = request.form["diseases"]
            allergies = request.form["allergies"]
            what_allergy = request.form["what_allergy"]
            medicines = request.form["medicines"]
            what_medicin = request.form["what_medicin"]
            last_medical_consultation = request.form["last_medical_consultation"]
            plan_to_drink_less_alcoholic_beverages = request.form[
                "plan_to_drink_less_alcoholic_beverages"
            ]
            discomfort_due_to_criticism_when_ingesting_alcohol = request.form[
                "discomfort_due_to_criticism_when_ingesting_alcohol"
            ]
            need_to_drink_alcohol_in_the_morning = request.form[
                "need_to_drink_alcohol_in_the_morning"
            ]
            physical_activity_3_times_a_week_30_minutes = request.form[
                "physical_activity_3_times_a_week_30_minutes"
            ]
            he_is_a_smoker = request.form["he_is_a_smoker"]
            how_many_cigarettes_a_day = request.form["how_many_cigarettes_a_day"]
            he_is_ex_smoker = request.form["he_is_ex_smoker"]
            consume_psychoactive_substances = request.form[
                "consume_psychoactive_substances"
            ]
            used_psychoactive_substances_before = request.form[
                "used_psychoactive_substances_before"
            ]
            what_psychoactive_substances = request.form["what_psychoactive_substances"]

            new_health_condition = HealthCondition(
                ccn_employee,
                consume_alcoholic_beverages,
                diseases,
                allergies,
                what_allergy,
                medicines,
                what_medicin,
                last_medical_consultation,
                plan_to_drink_less_alcoholic_beverages,
                discomfort_due_to_criticism_when_ingesting_alcohol,
                need_to_drink_alcohol_in_the_morning,
                physical_activity_3_times_a_week_30_minutes,
                he_is_a_smoker,
                how_many_cigarettes_a_day,
                he_is_ex_smoker,
                consume_psychoactive_substances,
                used_psychoactive_substances_before,
                what_psychoactive_substances,
            )

            db.session.add(new_health_condition)
            db.session.commit()
            type_message = "create"
            flash(
                f"Los datos del estado de salud para el empleado {ccn_employee} ha sido creado correctamente!!!"
            )
            return redirect(
                url_for(
                    "db_employee.health_condition_detail",
                    flash=flash,
                    message=type_message,
                )
            )
    else:
        mensajeErrorSesion = (
            "No hay una sesion activa porfavor inicia sesion en la plataforma"
        )
        flash(mensajeErrorSesion)
        return redirect(url_for("index.index"))


@blueprint_db_employee.route("/health_condition_detail", methods=["GET", "POST"])
@blueprint_db_employee.route(
    "/health_condition_detail/<message>", methods=["GET", "POST"]
)
def health_condition_detail(message=None):
    message = message
    title = "Lista de datos sociodemograficos"
    form = forms.CreateHealthCondition(request.form)
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_health_condition = HealthCondition.query.all()
            return render_template(
                "database_employees/health_condition_detail.html",
                query_list_health_condition=query_list_health_condition,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
        else:
            query_list_health_condition = HealthCondition.query.all()
            return render_template(
                "database_employees/health_condition_detail.html",
                query_list_health_condition=query_list_health_condition,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
    else:
        mensajeErrorSesion = (
            "No hay una sesion activa porfavor inicia sesion en la plataforma"
        )
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))


@blueprint_db_employee.route(
    "/update_health_condition/<int:ccn_health_condition>",
    methods=["GET", "POST"],
)
def update_health_condition(ccn_health_condition):
    if request.method == "GET":

        query_health_condition = HealthCondition.query.filter_by(
            ccn_health_condition=ccn_health_condition
        ).first()

        query_employee = Employee.query.filter_by(
            ccn_employee=query_health_condition.ccn_employee
        ).first()

        form = forms.CreateHealthCondition(
            ccn_employee=query_employee,
            consume_alcoholic_beverages=query_health_condition.consume_alcoholic_beverages,
            diseases=query_health_condition.diseases,
            allergies=query_health_condition.allergies,
            what_allergy=query_health_condition.what_allergy,
            medicines=query_health_condition.medicines,
            what_medicin=query_health_condition.what_medicin,
            last_medical_consultation=query_health_condition.last_medical_consultation,
            plan_to_drink_less_alcoholic_beverages=query_health_condition.plan_to_drink_less_alcoholic_beverages,
            discomfort_due_to_criticism_when_ingesting_alcohol=query_health_condition.discomfort_due_to_criticism_when_ingesting_alcohol,
            need_to_drink_alcohol_in_the_morning=query_health_condition.need_to_drink_alcohol_in_the_morning,
            physical_activity_3_times_a_week_30_minutes=query_health_condition.physical_activity_3_times_a_week_30_minutes,
            he_is_a_smoker=query_health_condition.he_is_a_smoker,
            how_many_cigarettes_a_day=query_health_condition.how_many_cigarettes_a_day,
            he_is_ex_smoker=query_health_condition.he_is_ex_smoker,
            consume_psychoactive_substances=query_health_condition.consume_psychoactive_substances,
            used_psychoactive_substances_before=query_health_condition.used_psychoactive_substances_before,
            what_psychoactive_substances=query_health_condition.what_psychoactive_substances,
        )
        return render_template(
            "database_employees/update_health_condition_detail.html",
            form=form,
            query_health_condition=query_health_condition,
            ccn_health_condition=ccn_health_condition,
        )
    elif request.method == "POST":

        query_health_condition = HealthCondition.query.filter_by(
            ccn_health_condition=ccn_health_condition
        ).first()

        query_health_condition.ccn_employee = request.form["ccn_employee"]
        query_health_condition.consume_alcoholic_beverages = request.form[
            "consume_alcoholic_beverages"
        ]
        query_health_condition.diseases = request.form["diseases"]
        query_health_condition.allergies = request.form["allergies"]
        query_health_condition.what_allergy = request.form["what_allergy"]
        query_health_condition.medicines = request.form["medicines"]
        query_health_condition.what_medicin = request.form["what_medicin"]
        query_health_condition.last_medical_consultation = request.form[
            "last_medical_consultation"
        ]
        query_health_condition.plan_to_drink_less_alcoholic_beverages = request.form[
            "plan_to_drink_less_alcoholic_beverages"
        ]
        query_health_condition.discomfort_due_to_criticism_when_ingesting_alcohol = (
            request.form["discomfort_due_to_criticism_when_ingesting_alcohol"]
        )
        query_health_condition.need_to_drink_alcohol_in_the_morning = request.form[
            "need_to_drink_alcohol_in_the_morning"
        ]
        query_health_condition.physical_activity_3_times_a_week_30_minutes = (
            request.form["physical_activity_3_times_a_week_30_minutes"]
        )
        query_health_condition.he_is_a_smoker = request.form["he_is_a_smoker"]
        query_health_condition.how_many_cigarettes_a_day = request.form[
            "how_many_cigarettes_a_day"
        ]
        query_health_condition.he_is_ex_smoker = request.form["he_is_ex_smoker"]
        query_health_condition.consume_psychoactive_substances = request.form[
            "consume_psychoactive_substances"
        ]
        query_health_condition.used_psychoactive_substances_before = request.form[
            "used_psychoactive_substances_before"
        ]
        query_health_condition.what_psychoactive_substances = request.form[
            "what_psychoactive_substances"
        ]

        form = forms.CreateHealthCondition(request.form)
        db.session.commit()
        type_message = "update"
        flash(
            f"Los datos de la condicion de salud  del empleado {query_health_condition.Employee.ccn_employee} ha sido actualizada correctamente"
        )
        return redirect(
            url_for(
                "db_employee.health_condition_detail",
                flash=flash,
                message=type_message,
            )
        )


@blueprint_db_employee.route(
    "/delete_health_condition/<int:ccn_health_condition>",
    methods=["GET", "POST"],
)
def delete_health_condition(ccn_health_condition):
    form = forms.CreateHealthCondition(request.form)
    if "user_name" in session:
        HealthCondition.delete_health_condition(ccn_health_condition)
        type_message = "delete"
        flash(f"Los datos dela condicion de salud han sido eliminados correctamente")
        return redirect(
            url_for(
                "db_employee.health_condition_detail",
                flash=flash,
                message=type_message,
            )
        )

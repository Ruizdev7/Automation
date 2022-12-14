from integration_engine import forms
from integration_engine.models.tbl_employee import Employee
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from flask_wtf import CSRFProtect

from integration_engine import db

blueprint_home = Blueprint("home", __name__, url_prefix="")


# @blueprint_home.context_processor
# def user_roll():
#    if "user_name" in session:
#        user_name = session["user_name"]
#        q = Employee.query.filter(Employee.employee_email == user_name).first()
#        roll = Roles.query.filter(Roles.ccn_roles == q.ccn_roles).first()
#    return dict(roll=roll.description_roles)


@blueprint_home.route("/home", methods=["GET", "POST"])
def home():
    title = "Home"
    if "user_name" in session:
        user_name = session["user_name"]
        q_employe = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        user_html = (
            q_employe.first_name_employee + " " + q_employe.first_last_name_employee
        )

        if request.method == "GET":
            return render_template(
                "home/home.html",
                title=title,
                user=user_name,
                user_html=user_html,
            )
        else:
            return render_template(
                "home/home.html", title=title, user=user_name, user_html=user_html
            )
    else:
        mensajeErrorSesion = (
            "No existe una sesion activa porfavor ingrese a la plataforma"
        )
        flash(mensajeErrorSesion)

        return redirect(url_for("index.index"))


@blueprint_home.route("/log_out", methods=["GET", "POST"])
def log_out():
    session.pop("user_name")
    return redirect(url_for("landingPage.index"))

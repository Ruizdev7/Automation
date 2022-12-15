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


blueprint_xlsx_processing = Blueprint("xlsx_processing", __name__, url_prefix="")

# Muestra los servicios que pueden ser procesados atravez de la carga y procesamiento de archivos csv o xlsx
@blueprint_xlsx_processing.route("/list_xlsx_services", methods=["GET", "POST"])
@blueprint_xlsx_processing.route(
    "/list_xlsx_services/<message>", methods=["GET", "POST"]
)
def list_xlsx_services(message=None):
    title = "Listado de Servicios xlsx"
    # form = forms.RegisterEmployee()
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_employee = Employee.query.all()
            return render_template(
                "xlsx_services/xlsx_services.html",
                query_logged_user=query_logged_user,
                query_list_employee=query_list_employee,
                title=title,
                user=user_name,
                # form=form,
                message=message,
            )
        else:
            return render_template(
                "xlsx_services/xlsx_services.html",
                query_logged_user=query_logged_user,
                query_list_employee=query_list_employee,
                title=title,
                user=user_name,
                # form=form,
                message=message,
            )
    else:
        mensajeErrorSesion = "There is no active session please enter the platform"
        flash(mensajeErrorSesion)
        return redirect(url_for("landingPage.index"))

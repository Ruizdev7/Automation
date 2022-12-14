from flask import flash
from email import message
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import Blueprint
from flask_wtf import CSRFProtect
from flask import render_template

from integration_engine import db
from integration_engine import forms
from integration_engine.models.tbl_roles import Role
from integration_engine.models.tbl_type_id import TypeId
from integration_engine.models.tbl_employee import Employee


blueprint_defined_codes = Blueprint("defined_codes", __name__, url_prefix="")


# CREATE READ UPDATE DELETE ROLES
@blueprint_defined_codes.route("/create_role", methods=["GET", "POST"])
def create_role():
    title = "Roles"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateRole(request.form)
        if request.method == "GET":
            return render_template(
                "defined_codes/defined_codes_role.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:
            area = request.form["area"].upper()
            role = request.form["role"].upper()
            associated_process = request.form["associated_process"].upper()

            new_role = Role(
                area=area,
                role=role,
                process=associated_process,
            )

            db.session.add(new_role)
            db.session.commit()
            type_message = "create"
            flash(f"{role} ha sido creado correctamente!!!")
            return redirect(
                url_for(
                    "defined_codes.defined_code_roles",
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


@blueprint_defined_codes.route("/defined_code_roles", methods=["GET", "POST"])
@blueprint_defined_codes.route("/defined_code_roles/<message>", methods=["GET", "POST"])
def defined_code_roles(message=None):
    message = message
    title = "Roles"
    form = forms.CreateRole(request.form)
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_roles = Role.query.all()
            return render_template(
                "defined_codes/defined_codes_role.html",
                query_list_roles=query_list_roles,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
        else:
            query_list_roles = Role.query.all()
            return render_template(
                "defined_codes/defined_codes_role.html",
                query_list_roles=query_list_roles,
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


@blueprint_defined_codes.route("/update_role/<int:ccn_role>", methods=["GET", "POST"])
def update_role(ccn_role):
    if request.method == "GET":
        query_role = Role.query.filter_by(ccn_role=ccn_role).first()
        form = forms.CreateRole(
            area=query_role.area,
            role=query_role.role,
            associated_process=query_role.process,
        )
        return render_template(
            "defined_codes/update_role.html",
            form=form,
            query_role=query_role,
            ccn_role=ccn_role,
        )
    elif request.method == "POST":

        query_role = Role.query.filter_by(ccn_role=ccn_role).first()

        query_role.area = request.form["area"].upper()
        query_role.role = request.form["role"].upper()
        query_role.process = request.form["associated_process"].upper()
        query_role.full_role = (
            request.form["role"].upper()
            + " - "
            + request.form["associated_process"].upper()
        )
        form = forms.CreateRole(request.form)
        db.session.commit()
        type_message = "update"
        flash(f"{query_role.process} ha sido actualizado correctamente")
        return redirect(
            url_for(
                "defined_codes.defined_code_roles",
                flash=flash,
                message=type_message,
            )
        )


@blueprint_defined_codes.route("/delete_role/<int:ccn_role>", methods=["GET", "POST"])
def delete_role(ccn_role):
    form = forms.CreateRole(request.form)
    if "user_name" in session:
        Role.delete_role(ccn_role)
        type_message = "delete"
        flash(f"El Role ha sido eliminado correctamente")
        return redirect(
            url_for(
                "defined_codes.defined_code_roles",
                flash=flash,
                message=type_message,
            )
        )


# CREATE READ UPDATE DELETE TYPE IDENTIFICATION
@blueprint_defined_codes.route("/create_type_id", methods=["GET", "POST"])
def create_type_id():
    title = "Raza"
    if "user_name" in session:
        user_name = session["user_name"]
        form = forms.CreateTypeId(request.form)
        if request.method == "GET":
            return render_template(
                "defined_codes/defined_codes_type_id.html",
                title=title,
                user=user_name,
                form=form,
            )
        else:

            type_id = request.form["type_id"].upper()
            description_type_id = request.form["description_type_id"].upper()

            new_type_id = TypeId(
                type_id=type_id,
                description_type_id=description_type_id,
            )

            db.session.add(new_type_id)
            db.session.commit()
            type_message = "create"
            flash(
                f"Tipo de Identificacion {description_type_id} ha sido creado correctamente!!!"
            )
            return redirect(
                url_for(
                    "defined_codes.defined_code_type_id",
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


@blueprint_defined_codes.route("/defined_code_type_id", methods=["GET", "POST"])
@blueprint_defined_codes.route(
    "/defined_code_type_id/<message>", methods=["GET", "POST"]
)
def defined_code_type_id(message=None):
    message = message
    title = "Tipo de Identificacion"
    form = forms.CreateTypeId(request.form)
    if "user_name" in session:
        user_name = session["user_name"]
        query_logged_user = Employee.query.filter(
            Employee.employee_personal_email == user_name
        ).first()
        if request.method == "GET":
            query_list_type_id = TypeId.query.all()
            return render_template(
                "defined_codes/defined_codes_type_id.html",
                query_list_type_id=query_list_type_id,
                title=title,
                user=user_name,
                form=form,
                query_logged_user=query_logged_user,
                message=message,
            )
        else:
            query_list_type_id = TypeId.query.all()
            return render_template(
                "defined_codes/defined_codes_type_id.html",
                query_list_type_id=query_list_type_id,
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


@blueprint_defined_codes.route(
    "/update_type_id/<int:ccn_type_id>", methods=["GET", "POST"]
)
def update_type_id(ccn_type_id):
    if request.method == "GET":
        query_type_id = TypeId.query.filter_by(ccn_type_id=ccn_type_id).first()
        form = forms.CreateTypeId(
            type_id=query_type_id.type_id,
            description_type_id=query_type_id.description_type_id,
        )
        return render_template(
            "defined_codes/update_type_id.html",
            form=form,
            query_type_id=query_type_id,
            ccn_type_id=ccn_type_id,
        )
    elif request.method == "POST":

        query_type_id = TypeId.query.filter_by(ccn_type_id=ccn_type_id).first()

        query_type_id.type_id = request.form["type_id"].upper()
        query_type_id.description_type_id = request.form["description_type_id"].upper()

        form = forms.CreateTypeId(request.form)
        db.session.commit()
        type_message = "update"
        flash(f"{query_type_id.description_type_id} ha sido actualizada correctamente")
        return redirect(
            url_for(
                "defined_codes.defined_code_type_id",
                flash=flash,
                message=type_message,
            )
        )


@blueprint_defined_codes.route(
    "/delete_type_id/<int:ccn_type_id>", methods=["GET", "POST"]
)
def delete_type_id(ccn_type_id):
    form = forms.CreateTypeId(request.form)
    if "user_name" in session:
        TypeId.delete_type_id(ccn_type_id)
        type_message = "delete"
        flash(f"El tipo de Identificacion se ha sido eliminada correctamente")
        return redirect(
            url_for(
                "defined_codes.defined_code_type_id",
                flash=flash,
                message=type_message,
            )
        )

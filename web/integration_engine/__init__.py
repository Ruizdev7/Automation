import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.DevelopmentConfig")
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    csfr = CSRFProtect(app)

    from integration_engine.models import (
        tbl_employee,
        tbl_roles,
        tbl_type_id,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping("test_config")
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register BluePrints

    from integration_engine.views.home import blueprint_home
    from integration_engine.views.index import blueprint_landing_page
    from integration_engine.views.db_employee import blueprint_db_employee
    from integration_engine.views.defined_codes import blueprint_defined_codes
    from integration_engine.views.xlsx_processing import blueprint_xlsx_processing

    app.register_blueprint(blueprint_home, url_prefix="")
    app.register_blueprint(blueprint_db_employee, url_prefix="")
    app.register_blueprint(blueprint_landing_page, url_prefix="")
    app.register_blueprint(blueprint_defined_codes, url_prefix="")
    app.register_blueprint(blueprint_xlsx_processing, url_prefix="")

    return app

from flask import redirect, render_template, Blueprint, request, flash, \
    url_for
from flask_user import roles_accepted, current_user
from proxyweb.views.forms import OrganizationForm
from database.models import Organization
from proxyweb import app
import database as db
from sqlalchemy.exc import IntegrityError
from flask import Blueprint
from typing import Any

blueprint = Blueprint('organizations', __name__, url_prefix='/organizations/')

@blueprint.route('organizations')
@roles_accepted('system_admin')
def organizations() -> Any:
    organizations = Organization.query.all()
    return render_template('organizations/organizations.html',
                           organizations=organizations)


@blueprint.route('organization/<organization_id>')
@roles_accepted('system_admin')
def organization(organization_id: str) -> Any:
    organization = Organization.query. \
        filter(Organization.id == organization_id).first()
    return render_template('organizations/organization.html',
                           organization=organization)


@blueprint.route('organizations/create', methods=['GET', 'POST'])
@roles_accepted('system_admin')
def create_organization() -> Any:
    form = OrganizationForm(request.form)
    if request.method == 'POST' and form.validate():
        organization = Organization()
        form.populate_obj(organization)
        try:
            db.session.add(organization)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append('Company name is already in use')
            return render_template('organizations/new.html',
                                   form=form)
        except:
            db.session.rollback()
            flash('Error creating organization')
            return render_template('organizations/new.html',
                                   form=form)

        return redirect(url_for('organizations.organization',
                                organization_id=organization.id))

    return render_template('organizations/new.html', form=form)



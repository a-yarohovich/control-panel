import datetime
from flask import render_template, redirect, url_for, flash, session
from flask_paginate import Pagination, get_page_parameter
from flask import request
from logger import logger
from .forms import ProvHandleForm, ProvWizard
from . import provider_bl
from .. models import Provider


LOG = logger.LOG


@provider_bl.route("/", methods=["POST", "GET"])
def provider():
    form = ProvHandleForm()
    prov_lst = Provider.dump()
    if form.validate_on_submit():
        selected_prov = request.form.getlist("selected_prov")
        if form.submit_add.data:
            return redirect(url_for("provider.save"))
        if form.submit_edit.data:
            if len(selected_prov) != 1:
                flash("Invalid edited providers. Allowed only one selected item")
            else:
                for prov in prov_lst:
                    if prov.fiprovider_id == int(selected_prov[0]):
                        to_edit = {
                            "fiprovider_id": prov.fiprovider_id,
                            "fiprov_status": prov.fiprov_status,
                            "fdstart_date": prov.fdstart_date.strftime("%Y-%m-%d"),
                            "fdend_date": prov.fdend_date.strftime("%Y-%m-%d") if prov.fdend_date else "",
                            "fsprovider_code": prov.fsprovider_code,
                            "fsdesc": prov.fsdesc
                        }
                        session["to_edit"] = to_edit
                        return redirect(url_for("provider.update"))
        elif form.submit_delete.data:
            Provider.delete(tuple(selected_prov))
            return redirect(url_for("provider.provider"))
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(
        page=page,
        css_framework="foundation",
        per_page=25,
        total=len(prov_lst),
        search=search
    )
    return render_template(
        "tmprovider/tmprovider.html",
        prov_lst=prov_lst,
        pagination=pagination,
        form=form
    )


@provider_bl.route("/save", methods=["GET", "POST"])
def save():
    form = ProvWizard()
    form.status_selector.choices = [(200, "Active"), (300, "Not active")]
    try:
        if form.validate_on_submit():
            if not Provider.write(
                fiprov_status=form.status_selector.data,
                fdstart_date=form.from_date.data.strftime("%Y-%m-%d"),
                fdend_date=form.to_date.data.strftime("%Y-%m-%d"),
                fsprovider_code=form.prov_code.data,
                fsdesc=form.desc.data
            ):
                raise ValueError("Failed to update: {}".format(form.prov_code.data))
            return redirect(url_for("provider.provider"))
    except Exception as ex:
        LOG.error(LOG.exmsg(ex))
        flash("Something went wrong!")
        return render_template("errors/500.html")
    return render_template("tmprovider/tmprovider_save.html", form=form)


@provider_bl.route("/update", methods=["GET", "POST"])
def update():
    form = ProvWizard()
    form.status_selector.choices = [(200, "Active"), (300, "Not active")]
    try:
        to_edit = Provider.from_dict(session["to_edit"])
        if form.validate_on_submit():
            if Provider.write(
                fiprov_status=form.status_selector.data,
                fdstart_date=form.from_date.data.strftime("%Y-%m-%d"),
                fdend_date=form.to_date.data.strftime("%Y-%m-%d"),
                fsprovider_code=form.prov_code.data,
                fsdesc=form.desc.data,
                fiprovider_id=to_edit.fiprovider_id
            ):
                del session["to_edit"]
                return redirect(url_for("provider.provider"))
            else:
                raise ValueError("Failed to update: {}".format(form.serv_code))
        form.status_selector.default = to_edit.fiprov_status
        form.process()
        form.desc.data = to_edit.fsdesc
        form.prov_code.data = to_edit.fsprovider_code
        if to_edit.fdstart_date:
            form.from_date.data = datetime.datetime.strptime(to_edit.fdstart_date, "%Y-%m-%d").date()
        if to_edit.fdend_date:
            form.to_date.data = datetime.datetime.strptime(to_edit.fdend_date, "%Y-%m-%d").date()
    except Exception as ex:
        LOG.error(LOG.exmsg(ex))
        flash("Something went wrong!")
        return render_template("errors/500.html")
    return render_template("tmprovider/tmprovider_save.html", form=form)

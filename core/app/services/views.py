from flask import render_template, redirect, url_for, flash, session
from flask_paginate import Pagination, get_page_parameter
from flask import request
from logger import logger
from .forms import ServHandleForm, ServWizard
from . import serv_bl
from .. models import Service

LOG = logger.LOG


@serv_bl.route("/", methods=["POST", "GET"])
def services():
    form = ServHandleForm()
    serv_lst = Service.dump()
    if form.validate_on_submit():
        selected_serv = request.form.getlist("selected_serv")
        if form.submit_add.data:
            return redirect(url_for("services.save"))
        if form.submit_edit.data:
            if len(selected_serv) != 1:
                flash("Invalid edited services. Allowed only one selected service")
            else:
                for serv in serv_lst:
                    if serv.fiservice_id == int(selected_serv[0]):
                        session["editserv"] = {
                            "fiservice_id": serv.fiservice_id,
                            "fiservice_status": serv.fiservice_status,
                            "fsserv_desc": serv.fsserv_desc,
                            "fsserv_code": serv.fsserv_code
                        }
                        return redirect(url_for("services.update"))
        elif form.submit_delete.data:
            Service.delete(tuple(selected_serv))
            return redirect(url_for("services.services"))
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(
        page=page,
        css_framework="foundation",
        per_page=20,
        total=len(serv_lst),
        search=search
    )
    return render_template(
        "services/serv_view.html",
        serv_lst=serv_lst,
        pagination=pagination,
        form=form
    )


@serv_bl.route("/update", methods=["GET", "POST"])
def update():
    form = ServWizard()
    form.status_selector.choices = [(200, "Active"), (300, "Not active")]
    try:
        editserv = Service.from_dict(session["editserv"])
        if form.validate_on_submit():
            if Service.write(
                fiservice_status=form.status_selector.data,
                fsserv_desc=form.desc.data,
                fsserv_code=form.serv_code.data,
                fiservice_id=editserv.fiservice_id
            ):
                del session["editserv"]
                return redirect(url_for("services.services"))
            else:
                raise ValueError("Failed to update service: {}".format(form.serv_code))
        form.status_selector.default = editserv.fiservice_status
        form.process()
        form.desc.data = editserv.fsserv_desc
        form.serv_code.data = editserv.fsserv_code
    except Exception as ex:
        LOG.error(LOG.exmsg(ex))
        flash("Something went wrong!")
        return render_template("errors/500.html")
    return render_template("services/serv_save.html", form=form)


@serv_bl.route("/save", methods=["GET", "POST"])
def save():
    form = ServWizard()
    form.status_selector.choices = [(200, "Active"), (300, "Not active")]
    try:
        if form.validate_on_submit():
                if not Service.write(
                    fiservice_status=form.status_selector.data,
                    fsserv_desc=form.desc.data,
                    fsserv_code=form.serv_code.data
                ):
                    raise ValueError("Failed to update service: {}".format(form.serv_code))
                return redirect(url_for("services.services"))
    except Exception as ex:
        LOG.error(LOG.exmsg(ex))
        flash("Something went wrong!")
        return render_template("errors/500.html")
    return render_template("services/serv_save.html", form=form)

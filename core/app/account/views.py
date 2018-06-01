from flask import render_template, redirect, url_for, flash, session
from flask_paginate import Pagination, get_page_parameter
from flask import request
from logger import logger
from .forms import AccHandleForm, AccWizard
from . import lang_bl
from .. models import Language

LOG = logger.LOG


@lang_bl.route("/", methods=["POST", "GET"])
def lang():
    form = LangHandleForm()
    dump = Language.dump()
    if form.validate_on_submit():
        selected = request.form.getlist("selected_lang")
        if form.submit_add.data:
            return redirect(url_for("lang.save"))
        if form.submit_edit.data:
            if len(selected) != 1:
                flash("Invalid edited items. Allowed only one selected item")
            else:
                for lng in dump:
                    if lng.filang_id == int(selected[0]):
                        session["to_edit"] = {
                            "filang_id": lng.filang_id,
                            "fslang_iso639_1": lng.fslang_iso639_1,
                            "fslang_desc": lng.fslang_desc,
                        }
                        return redirect(url_for("lang.update"))
        elif form.submit_delete.data:
            Language.delete(tuple(selected))
            return redirect(url_for("lang.lang"))
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(
        page=page,
        css_framework="foundation",
        per_page=25,
        total=len(dump),
        search=search
    )
    return render_template(
        "lang/overview.html",
        render_lst=dump,
        pagination=pagination,
        form=form
    )


@lang_bl.route("/update", methods=["GET", "POST"])
def update():
    form = LangWizard()
    try:
        to_edit = Language.from_dict(session["to_edit"])
        if form.validate_on_submit():
            if Language.update(
                fslang_iso639_1=form.lang_iso639_1.data,
                fslang_desc=form.desc.data,
                filang_id=to_edit.filang_id
            ):
                del session["to_edit"]
                return redirect(url_for("lang.lang"))
            else:
                raise ValueError("Failed to update: {}".format(form.lang_iso639_1.data))
        form.desc.data = to_edit.fslang_desc
        form.lang_iso639_1.data = to_edit.fslang_iso639_1
    except Exception as ex:
        LOG.error(LOG.exmsg(ex))
        flash("Something went wrong!")
        return render_template("errors/500.html")
    return render_template("lang/save.html", form=form)


@lang_bl.route("/save", methods=["GET", "POST"])
def save():
    form = LangWizard()
    try:
        if form.validate_on_submit():
                if not Language.insert(
                    fslang_iso639_1=form.lang_iso639_1.data,
                    fslang_desc=form.desc.data
                ):
                    raise ValueError("Failed to insert: {}".format(form.serv_code))
                return redirect(url_for("lang.lang"))
    except Exception as ex:
        LOG.error(LOG.exmsg(ex))
        flash("Something went wrong!")
        return render_template("errors/500.html")
    return render_template("lang/save.html", form=form)

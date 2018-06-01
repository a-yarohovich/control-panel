from flask import render_template
from logger import logger
from .forms import CdrFilterForm
from . import cdr
from flask_paginate import Pagination, get_page_parameter
from flask import request
from .. models import CDR

LOG = logger.LOG


@cdr.route("/", methods=["POST", "GET"])
def cdr_view():
    form = CdrFilterForm()
    try:
        if form.validate_on_submit():
            if request.args.get('q'):
                search = True
            else:
                search = False
            page = request.args.get(get_page_parameter(), type=int, default=1)
            from_date = form.from_date.data.strftime("%Y-%m-%d %H:%M:%S")
            to_date = form.to_date.data.strftime("%Y-%m-%d %H:%M:%S")
            cdrs = CDR.dump(from_date, to_date)
            pagination = Pagination(
                page=page,
                css_framework="foundation",
                per_page=25,
                total=len(cdrs),
                search=search,
                record_name="cdr"
            )
            return render_template(
                "cdr/cdr_view.html",
                cdrs=cdrs,
                pagination=pagination,
                form=form
            )
    except Exception as ex:
        LOG.error(LOG.exmsg(ex))
    return render_template("cdr/cdr_view.html", form=form)

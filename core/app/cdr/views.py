from flask import render_template
from logger import logger
from .forms import CdrFilterForm
from . import cdr
from flask_paginate import Pagination, get_page_parameter
from flask import request
from .. import MyPgConnection


LOG = logger.LOG


# return list of tuples cdrs
def get_cdr_list(from_date=None, to_date=None) -> list:
    where_clause: str = ''
    if from_date is not None and to_date is not None:
        where_clause = "WHERE facreate_time BETWEEN '{}' AND '{}'".format(from_date, to_date)
    cursor = MyPgConnection.cursor()
    cursor.execute("SELECT "
                   "fiplatform_cdr_id, "    # cdr[0]
                   "fscontext_id, "         # cdr[1]
                   "fscall_id, "            # cdr[2]
                   "fscalling_number, "     # cdr[3]
                   "fscalled_number, "      # cdr[4]
                   "faanswer_time, "        # cdr[5]
                   "fadestroy_time, "       # cdr[6]
                   "facreate_time, "        # cdr[7]
                   "fiend_reason "          # cdr[8]
                   "FROM mycapp.platform_cdr {};".format(where_clause))
    return [(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8]) for line in cursor.fetchall()]


@cdr.route('/cdr_view', methods=['POST','GET'])
def cdr_view():
    form = CdrFilterForm()
    if form.validate_on_submit():
        search = False
        q = request.args.get('q')
        if q:
            search = True
        page = request.args.get(get_page_parameter(), type=int, default=1)
        from_date = form.from_date.data.strftime('%Y-%m-%d %H:%M:%S')
        to_date = form.to_date.data.strftime('%Y-%m-%d %H:%M:%S')
        cdrs = get_cdr_list(from_date, to_date)
        pagination = Pagination(page=page, css_framework='foundation', per_page=15, total=len(cdrs), search=search,
                                record_name='cdr')
        return render_template('cdr/cdr_view.html',
                               cdrs=cdrs,
                               pagination=pagination,
                               form=form)
    return render_template('cdr/cdr_view.html', form=form)

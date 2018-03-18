from flask import render_template
from flask_paginate import Pagination, get_page_parameter
from flask import request
from logger import logger
from .forms import CountryForm
from . import blcountry_dict
from .. import db_conn

LOG = logger.LOG


# return list of tuples cdrs
def get_country_list() -> list:
    cursor = db_conn.cursor

    cursor.execute(
        "SELECT "
        "ficountry_id, "             # cdr[0]
        "fsiso_3166_alpha2, "        # cdr[1]
        "fscountry_full "            # cdr[2]
        "FROM mycapp.country;"
    )
    return [(line[0], line[1], line[2]) for line in cursor.fetchall()]


@blcountry_dict.route('/country_dict', methods=['POST', 'GET'])
def country_dict():
    form = CountryForm()
    if form.validate_on_submit():
        search = False
        q = request.args.get('q')
        if q:
            search = True
        page = request.args.get(get_page_parameter(), type=int, default=1)
        countries = get_country_list()
        pagination = Pagination(
            page=page,
            css_framework='foundation',
            per_page=25,
            total=len(countries),
            search=search,
            record_name='cdr'
        )
        return render_template(
            "country_dict/country_dict.html",
            countries=countries,
            pagination=pagination,
            form=form
        )
    return render_template('cdr/cdr_view.html', form=form)

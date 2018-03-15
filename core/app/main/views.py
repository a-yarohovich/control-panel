from flask import render_template, session
import random
from logger import logger
from . import main
from .. import models

LOG = logger.LOG


@main.route('/', methods=['GET', 'POST'])
def index():
    user_id = session.get('user_id')
    spend = random.randint(1, 100)
    if not user_id:
        return render_template("main/main_view.html", spend=spend)
    return render_template("main/main_view.html", spend=0)

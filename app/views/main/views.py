from flask import render_template, request, session

import config
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html')


@main.before_app_request
def check_request():
    """
    此处会拦截所有app请求
    :return:
    """
    pass
    # print('sidebar_collapsed:', request.cookies.get('sbc'))


@main.app_context_processor
def handle_dict_in_context():
    return {
        'sys_nick': config.SYS_NAME_SHORT
    }

#!/usr/local/bin/python2.7
#coding:utf-8

from flask import Blueprint
from utils.helper import make_view
from views.gists.gists import Create, View, Raw

MODULE_NAME = 'gists'
view_func = make_view(MODULE_NAME)

gists = Blueprint(MODULE_NAME, __name__)

raw = view_func(Raw)
view = view_func(View)
create = view_func(Create)

gists.add_url_rule('/<git>/gist/create', view_func=create, methods=['GET', 'POST'])
gists.add_url_rule('/<git>/gist/<int:gid>', view_func=view, methods=['GET', 'POST'])
gists.add_url_rule('/<git>/gist/<int:gid>/raw/<path:path>', view_func=raw, methods=['GET'])

#!/usr/local/bin/python2.7
#coding:utf-8

from flask import Blueprint
from utils.helper import make_view
from views.repos.explore import Explore
from views.repos.commits import Commits, Commit
from views.repos.watchers import Watch, Unwatch, Watchers
from views.repos.commiters import Commiters, RemoveCommiter
from views.repos.modify import DeleteFile, NewFile, EditFile
from views.repos.view import View, Blob, Raw, Activities, Forks
from views.repos.repos import Create, Transport, Delete, Setting, Fork

MODULE_NAME = 'repos'
view_func = make_view(MODULE_NAME)

repos = Blueprint(MODULE_NAME, __name__)

fork = view_func(Fork)
forks = view_func(Forks)

create = view_func(Create)
setting = view_func(Setting)
transport = view_func(Transport)
delete = view_func(Delete)
explore = view_func(Explore)
activities = view_func(Activities)

commit = view_func(Commit)
commits = view_func(Commits)
commiters = view_func(Commiters)
remove_commiter = view_func(RemoveCommiter, name='remove_commiter')
watch = view_func(Watch)
unwatch = view_func(Unwatch)
watchers = view_func(Watchers)

raw = view_func(Raw)
view = view_func(View)
blob = view_func(Blob)

delete_file = view_func(DeleteFile, name='delete_file')
edit_file = view_func(EditFile, name='edit_file', tmpl='edit.file')
new_file = view_func(NewFile, name='new_file', tmpl='new.file')

repos.add_url_rule('/<git>/new', view_func=create, methods=['GET', 'POST'])

repos.add_url_rule('/<git>/<rname>/settings', view_func=setting, methods=['GET', 'POST'])
repos.add_url_rule('/<git>/<tname>/<rname>/settings', view_func=setting, methods=['GET', 'POST'])

repos.add_url_rule('/<git>/<rname>/commiters', view_func=commiters, methods=['GET', 'POST'])
repos.add_url_rule('/<git>/<tname>/<rname>/commiters', view_func=commiters, methods=['GET', 'POST'])

repos.add_url_rule('/<git>/<rname>/commiters/remove', view_func=remove_commiter, methods=['POST'])
repos.add_url_rule('/<git>/<tname>/<rname>/commiters/remove', view_func=remove_commiter, methods=['POST'])

repos.add_url_rule('/<git>/<rname>/transport', view_func=transport, methods=['GET', 'POST'])
repos.add_url_rule('/<git>/<tname>/<rname>/transport', view_func=transport, methods=['GET', 'POST'])

repos.add_url_rule('/<git>/<rname>/delete', view_func=delete, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/delete', view_func=delete, methods=['GET'])

repos.add_url_rule('/<git>/explore', view_func=explore, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/explore', view_func=explore, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/forks', view_func=forks, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/forks', view_func=forks, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/fork', view_func=fork, methods=['GET', 'POST'])
repos.add_url_rule('/<git>/<tname>/<rname>/fork', view_func=fork, methods=['GET', 'POST'])

repos.add_url_rule('/<git>/<rname>/activity', view_func=activities, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/activity', view_func=activities, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/watch', view_func=watch, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/watch', view_func=watch, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/unwatch', view_func=unwatch, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/unwatch', view_func=unwatch, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/watchers', view_func=watchers, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/watchers', view_func=watchers, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/commit/<version>', view_func=commit, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/commit/<version>', view_func=commit, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/commits/<version>', view_func=commits, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/commits/<version>', view_func=commits, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/commits/<version>/<path:path>', view_func=commits, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/commits/<version>/<path:path>', view_func=commits, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/delete/<version>/<path:path>', view_func=delete_file, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/delete/<version>/<path:path>', view_func=delete_file, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/edit/<version>/<path:path>', view_func=edit_file, methods=['GET', 'POST'])
repos.add_url_rule('/<git>/<tname>/<rname>/edit/<version>/<path:path>', view_func=edit_file, methods=['GET', 'POST'])

repos.add_url_rule('/<git>/<rname>/new/<version>', view_func=new_file, methods=['GET', 'POST'])
repos.add_url_rule('/<git>/<tname>/<rname>/new/<version>', view_func=new_file, methods=['GET', 'POST'])

repos.add_url_rule('/<git>/<rname>/new/<version>/<path:path>', view_func=new_file, methods=['GET', 'POST'])
repos.add_url_rule('/<git>/<tname>/<rname>/new/<version>/<path:path>', view_func=new_file, methods=['GET', 'POST'])

repos.add_url_rule('/<git>/<rname>', view_func=view, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>', view_func=view, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/tree/', view_func=view, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/tree/', view_func=view, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/tree/<version>/', view_func=view, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/tree/<version>/', view_func=view, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/tree/<version>/<path:path>', view_func=view, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/tree/<version>/<path:path>', view_func=view, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/blob/<version>/<path:path>', view_func=blob, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/blob/<version>/<path:path>', view_func=blob, methods=['GET'])

repos.add_url_rule('/<git>/<rname>/raw/<version>/<path:path>', view_func=raw, methods=['GET'])
repos.add_url_rule('/<git>/<tname>/<rname>/raw/<version>/<path:path>', view_func=raw, methods=['GET'])


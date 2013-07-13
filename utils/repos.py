#!/usr/local/bin/python2.7
#coding:utf-8

import os
import re
import time
import logging
import HTMLParser
from flask import g, abort, url_for, redirect

import misaka
import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename

from functools import wraps
from query.repos import get_repo_by_path, get_repo_commiter
from query.organization import get_team_member, get_team_by_name, \
        get_team

logger = logging.getLogger(__name__)

# USE login_required first
def repo_required(admin=False, need_write=False):
    def _repo_required(f):
        @wraps(f)
        def _(organization, member, *args, **kwargs):
            teamname = kwargs.pop('tname', '')
            reponame = kwargs.pop('rname', '')
            path = os.path.join(teamname, '%s.git' % reponame)
            if not reponame:
                raise abort(404)
            repo = get_repo_by_path(organization.id, path)
            if not repo:
                raise abort(404)
            team = team_member = None
            if teamname:
                team = get_team_by_name(organization.id, teamname)
                team_member = get_team_member(repo.tid, g.current_user.id)
                kwargs['team'] = team
                kwargs['team_member'] = team_member
            role = check_admin(g.current_user, repo, member, team_member)
            kwargs['admin'] = role
            if admin and not role:
                url = url_for('repos.view', git=organization.git, rname=repo.name, tname=teamname)
                return redirect(url)
            read, write = check_permits(g.current_user, repo, member, team, team_member, role)
            if not read:
                raise abort(403)
            if need_write and not write:
                raise abort(403)
            return f(organization, member, repo, *args, **kwargs)
        return _
    return _repo_required

def check_admin(user, repo, member, team_member):
    if repo.uid == user.id:
        return True
    elif member.admin:
        return True
    elif team_member and team_member.admin:
        return True
    else:
        return False

def check_permits(user, repo, member, team=None, team_member=None, role=None):
    if role is None and check_admin(user, repo, member, team_member):
            return True, True
    elif role:
        return True, True
    commiter = get_repo_commiter(user.id, repo.id)
    if commiter:
        return True, True
    if team:
        if team_member or not team.private:
            return True, False
        elif not team_member and team.private:
            return False, False
    else:
        return True, False

def format_time(ts):
    try:
        ts = float(ts)
        now = time.time()
        dur = now - ts
        if dur < 60:
            return '%d seconds ago' % dur
        elif dur < 60 * 60:
            return '%d minutes ago' % (dur / 60)
        elif dur < 60 * 60 * 24:
            return '%d hours ago' % (dur / 3600)
        elif dur < 86400 * 30:
            return '%d days ago' % (dur / 86400)
        elif dur < 31536000:
            return '%d months ago' % (dur / 2592000)
        else:
            return '%d years ago' % (dur / 31536000)
    except Exception, e:
        logger.exception(e)
        return '0'

def format_branch(branch):
    if branch.startswith('refs/heads/'):
        return branch.split('refs/heads/')[1]
    return branch

def get_url(view, organization, repo, kw={}, **kwargs):
    if repo.tid == 0:
        return url_for(view, git=organization.git, rname=repo.name, **kwargs)
    else:
        team = kw.get('team', None)
        if not team:
            team = get_team(repo.tid)
        return url_for(view, git=organization.git, rname=repo.name, tname=team.name, **kwargs)

def render_code(path, content):
    if path.rsplit('.', 1)[-1] in ['md', 'markdown', 'mkd']:
        html = misaka.html(content, extensions=\
                misaka.EXT_AUTOLINK|misaka.EXT_LAX_HTML_BLOCKS|misaka.EXT_SPACE_HEADERS|\
                misaka.EXT_SUPERSCRIPT|misaka.EXT_FENCED_CODE|misaka.EXT_NO_INTRA_EMPHASIS|\
                misaka.EXT_STRIKETHROUGH|misaka.EXT_TABLES)
        def _r(m):
            try:
                lexer_name = m.group(1)
                code = m.group(2)
                lexer = get_lexer_by_name(lexer_name)
                code = HTMLParser.HTMLParser().unescape(code)
                return highlight(code, lexer, HtmlFormatter())
            except pygments.util.ClassNotFound:
                return m.group()

        p = re.compile(r'''<pre><code class="([0-9a-zA-Z._-]+)">(.+?)</code></pre>''', re.DOTALL)
        html = r'''<div class="markdown">%s</div>''' % p.sub(lambda m: _r(m), html)

    else:
        try:
            lexer = guess_lexer_for_filename(path, content)
        except pygments.util.ClassNotFound:
            lexer = get_lexer_by_name("python")
        html = highlight(content, lexer,  HtmlFormatter(linenos=True, lineanchors='L', anchorlinenos=True))

    return html


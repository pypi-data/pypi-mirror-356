import json
from jinja2.environment import copy_cache
from flask import Blueprint, current_app, render_template, request, redirect, url_for

edits = Blueprint('edits', __name__, template_folder='templates', static_folder='assets')

@edits.route('/')
@edits.route('/<path:page>')
def index(page=None):
    _db = current_app.jinja_env.edits
    if _db:
        if not page or page not in _db:
            page = next(iter(_db.keys())) if _db else None
    else:
        page = None
    return render_template('edits-admin.html',
                            edits=_db,
                            page=page,
                            summernote=current_app.config['EDITS_SUMMERNOTE'],
                            preview=current_app.jinja_env.edits_preview)
                            
@edits.route('/preview', methods=['POST'])
def preview():
    if request.form.get('state') == 'true':
        preview = True
        cache = None
    else:
        preview = False
        cache = copy_cache(current_app.jinja_env.edits_cache)

    current_app.jinja_env.edits_preview = preview
    current_app.jinja_env.cache = cache

    if current_app.jinja_env.cache:
        current_app.jinja_env.cache.clear()

    return ''

@edits.route('/save', methods=['POST'])
def save():
    _db = current_app.jinja_env.edits
    page = request.form.get('page')
    for field in request.form:
        if field != 'page' and field != 'files':  # Skip 'files' field
            value = request.form.get(field)
            if value == '':
                value = None
            _db[page][field]['edited'] = value
    if current_app.jinja_env.cache:
        current_app.jinja_env.cache.clear()
    with open(current_app.config['FILE_PATH']+'edits.json', 'w') as f:
        f.write(json.dumps(_db, indent=4))
    return redirect(url_for('edits.index', page=page))

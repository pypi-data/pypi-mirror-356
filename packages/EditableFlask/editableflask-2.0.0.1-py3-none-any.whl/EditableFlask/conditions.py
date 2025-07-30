def CONDITIONS(app, edits):

    app.config.setdefault('ENABLE_ANALYTICS', True)
    app.config.setdefault('ENABLE_STATIC', True)
    app.config.setdefault('EDITABLE_STATIC', True)
    app.config.setdefault('ENABLE_RESOURCE_MONITER', True)
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///users.db')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    
    from flask import current_app
    
    if app.config.get("ENABLE_ANALYTICS") or app.config.get("ENABLE_STATIC") or app.config.get("EDITABLE_STATIC") or app.config.get('EDITS_LOCKED') == "SQL":
        @app.template_filter('retrive_edits')
        def retrive_edits(value):
            _db = current_app.jinja_env.edits
            return _db
        
    if app.config.get('EDITS_LOCKED') == "SQL":
        from .pyfiles.edits_locked_sql import EDITS_LOCKED
        EDITS_LOCKED(app, edits)
    elif app.config.get('EDITS_LOCKED'):
        from .pyfiles.edits_locked import EDITS_LOCKED
        EDITS_LOCKED(app, edits)
    if not app.config.get('EDITS_LOCKED') or app.config.get('EDITS_LOCKED') != "SQL":
        @app.template_filter('editsnavbar')
        def editsnavbar(value):
            from flask import render_template, request
            render_NAVBAR = render_template('navbar.htm', permitted_links="/", path=request.path)
            return render_NAVBAR

    if app.config.get("ENABLE_ANALYTICS"):
        from .pyfiles.analytics import ENABLE_ANALYTICS
        ENABLE_ANALYTICS(app, edits)

    if app.config.get("ENABLE_RESOURCE_MONITER"):
        from .pyfiles.resource_monitor import ENABLE_RESOURCE_MONITER
        ENABLE_RESOURCE_MONITER(app, edits)

    if app.config.get("ENABLE_STATIC"):
        from .pyfiles.static import ENABLE_STATIC
        ENABLE_STATIC(app, edits)
    if app.config.get("EDITABLE_STATIC"):
        from .pyfiles.static import EDITABLE_STATIC
        EDITABLE_STATIC(app, edits)

# THIS CAN BE DELETED BY NULL B
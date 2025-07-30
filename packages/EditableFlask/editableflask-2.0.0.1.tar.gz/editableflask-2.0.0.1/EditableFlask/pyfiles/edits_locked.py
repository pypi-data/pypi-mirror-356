import json
from flask import redirect, url_for, render_template, request
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin

def EDITS_LOCKED(app, edits):
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.config.setdefault('LOGIN_ROUTE', '/login')
    login_manager.login_view = app.config.get('EDITS_URL') + app.config.get('LOGIN_ROUTE')

    class User(UserMixin):
        def __init__(self, id):
            self.id = id

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == app.config.get('EDITS_USERNAME'):
            return User(user_id)
        return None
    
    @edits.before_request
    def require_login_role():
        if not current_user.is_authenticated and not request.path.startswith(app.config.get('EDITS_URL') + app.config.get('LOGIN_ROUTE')):
            return redirect(url_for('edits.login'))
        
    @edits.route(app.config.get('LOGIN_ROUTE'), methods=['POST', 'GET'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('edits.index'))
        if request.form.get('username') and request.form.get('password'):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == app.config.get('EDITS_USERNAME') and password == app.config.get('EDITS_PASSWORD'):
                user = User(username)
                login_user(user)
                return redirect(url_for('edits.index'))
        return render_template("login.html")
    
    @edits.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('edits.login'))
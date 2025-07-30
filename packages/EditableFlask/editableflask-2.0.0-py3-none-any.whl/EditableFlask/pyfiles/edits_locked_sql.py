import os, json
from datetime import datetime, timedelta
from flask import redirect, url_for, render_template, request
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

def EDITS_LOCKED(app, edits):
    
    @app.template_filter('fromjsonremoveprefix')
    def fromjsonremoveprefix_forusers(value):
        json_value = json.loads(value)
        OUTPUT = ""
        for index, link in enumerate(json_value):
            if not link.startswith("/"): 
                link = link.removeprefix("/")
            OUTPUT += link
            if index != len(json_value)-1: OUTPUT += ", "
        return OUTPUT
    
    @app.template_filter('editsnavbar')
    def editsnavbar(value):
        permitted_links = [link for link in json.loads(current_user.roles)]
        render_NAVBAR = render_template('navbar.htm', permitted_links=permitted_links, path=request.path)
        return render_NAVBAR
    
    @app.template_filter('currentuser_roles')
    def currentuser_roles(value):
        permitted_links = [link for link in json.loads(current_user.roles)]
        return permitted_links
    
    from .database import db

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, unique=True)
        password_hash = db.Column(db.String)
        password_retry_attemts = db.Column(db.Integer)
        password_retry_time = db.Column(db.Integer)
        roles = db.Column(db.String)
        
        def verify_password(self, password):
            return check_password_hash(self.password_hash, password)
        def __repr__(self):
            return '<User %r>' % self.username
    app.config.setdefault('PERMANENT_SESSION_LIFETIME', timedelta(minutes=60))
    database_uri = app.instance_path+'/'+app.config.get('SQLALCHEMY_DATABASE_URI').split('///')[-1]
    try: db.engine
    except: db.init_app(app)

    with app.app_context():
        if not os.path.exists(database_uri):
            User.__table__.create(db.engine, checkfirst=True)
            if 'EDITS_PASSWORD' not in app.config or 'EDITS_USERNAME' not in app.config:
                raise Exception("Please provide EDITS_USERNAME and EDITS_PASSWORD in app.config.")

        if 'EDITS_PASSWORD' in app.config or 'EDITS_USERNAME' in app.config: 
            Username = app.config.get('EDITS_USERNAME')
            Password = app.config.get('EDITS_PASSWORD')
            app.config.setdefault('EDITS_PASSWORD_RETRY_ATTEMPTS', 5)
            app.config.setdefault('EDITS_PASSWORD_RETRY_TIME', 5*60*60)
            password_retry_attemts = app.config.get('EDITS_PASSWORD_RETRY_ATTEMPTS')
            password_retry_time = app.config.get('EDITS_PASSWORD_RETRY_TIME')
            existing_user = User.query.filter_by(username=Username).first()
            if existing_user:
                existing_user.password_hash = generate_password_hash(Password)
            else:
                Roles = json.dumps(['/'])
                user = User(username=Username, password_hash=generate_password_hash(Password), password_retry_attemts=password_retry_attemts, password_retry_time=password_retry_time,roles=Roles)
                db.session.add(user)
            db.session.commit()

    login_manager = LoginManager()
    login_manager.init_app(app)
    app.config.setdefault('LOGIN_ROUTE', '/login')
    login_manager.login_view = app.config.get('EDITS_URL') + app.config.get('LOGIN_ROUTE')
    
    @login_manager.user_loader
    def load_user(user_id):
        """Flask-Login callback to load a user from the database by ID."""
        try:
            return User.query.get(int(user_id))
        except ValueError:
            return None
        
    @edits.before_request
    def require_login_role():
        path = request.path.removeprefix(app.config.get('EDITS_URL'))
        if not path.startswith("/assets") and path != "/logout" and path != app.config.get('LOGIN_ROUTE') and path != "/": 
            if current_user.is_authenticated:
                permitted_links = [link if link == "/" else "/" + link for link in json.loads(current_user.roles)]
                if not path.startswith(tuple(permitted_links)) and not "/" in permitted_links:
                    return redirect(app.config.get('EDITS_URL')+permitted_links[0])
            else:
                return redirect(url_for('edits.login'))
        
    if 'user_timeout' not in globals():
        global user_timeout
        user_timeout = {}

    @edits.route('/login', methods=['POST', 'GET'])
    def login():
        global user_timeout
        if current_user.is_authenticated:
            return redirect(url_for('edits.index'))
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username and password:
                got_user = User.query.filter_by(username=username).first()
                if got_user and got_user.username == username:
                    # Ensure username is in `user_timeout`
                    if username in user_timeout:
                        attempts, last_attempt_time = user_timeout[username]
                        # Check if the user exceeded retry attempts
                        print(got_user.password_retry_time)
                        if attempts >= got_user.password_retry_attemts and datetime.now() - last_attempt_time < timedelta(seconds=got_user.password_retry_time):
                            return render_template("login.html", ERROR="You have exceeded the maximum number of password retry attempts. Try again later.")
                    if got_user.verify_password(password):
                        user_timeout[username] = [0, datetime.now()]  # Reset on successful login
                        login_user(got_user)
                        return redirect(url_for('edits.index'))
                    # Increase attempt count on failure
                    if username not in user_timeout:
                        user_timeout[username] = [0, datetime.now()]
                    user_timeout[username][0] += 1
                    user_timeout[username][1] = datetime.now()
        return render_template("login.html")

    
    @edits.route('/users')
    @edits.route('/users/<string:action>', methods=['GET','POST'])
    def users(action=None):
        if action == 'add':
            username = request.form.get('username')
            password = request.form.get('password')
            password_retry_attemts = request.form.get('password_retry_attemts')
            password_retry_time = request.form.get('password_retry_time')
            roles = request.form.get('roles')
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                user = User(username=username, password_hash=generate_password_hash(password), password_retry_attemts=password_retry_attemts, password_retry_time=password_retry_time,roles=json.dumps(roles.split(',')))
                db.session.add(user)
                db.session.commit()
            else:
                users = User.query.all()
                user = [username, password, password_retry_attemts, password_retry_time, roles] 
                return render_template('users.html', users=users, user=user, ERROR="User already exists in the database with the same username.")
        elif action == 'edit':
            username = request.form.get('username')
            password = request.form.get('password')
            password_retry_attemts = request.form.get('password_retry_attemts')
            password_retry_time = request.form.get('password_retry_time')
            roles = request.form.get('roles')
            user = User.query.filter_by(username=username).first()
            if user:
                if user.username != username: user.Username = username
                if password: user.password_hash = generate_password_hash(password)
                dumped_roles = json.dumps(roles.split(','))
                if user.roles != dumped_roles: user.roles = dumped_roles
                if user.password_retry_attemts != password_retry_attemts: user.password_retry_attemts = password_retry_attemts
                if user.password_retry_time != password_retry_time: user.password_retry_time = password_retry_time
                db.session.commit()
        elif action == 'delete':
            username = request.form.get('username')
            user = User.query.filter_by(username=username).first()
            if user:
                db.session.delete(user)
                db.session.commit()
        users = User.query.all()
        return render_template('users.html', users=users)
    
    @edits.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('edits.login'))
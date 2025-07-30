import requests
from flask import render_template, request
import os, json, ipaddress
from datetime import datetime, timedelta
def ENABLE_ANALYTICS(app, edits):
    @app.template_filter('fromjson')
    def fromjson(value):
        json_value = json.loads(value)
        return json_value

    from .database import db

    class LoggedIP(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        ip = db.Column(db.String, nullable=False)
        coordinates = db.Column(db.String, nullable=True)
        datetime = db.Column(db.String, nullable=False)

    database_uri = app.instance_path+'/'+app.config.get('SQLALCHEMY_DATABASE_URI').split('///')[-1]

    with app.app_context():
        try: db.engine
        except: db.init_app(app)
        LoggedIP.__table__.create(db.engine, checkfirst=True)
    
    timeout_ip = {}

    @app.before_request
    def edits_before_request():
        if not request.path.startswith(app.config['EDITS_URL']):
            # Check if 'X-Forwarded-For' header is present (commonly used in proxies)
            if 'X-Forwarded-For' in request.headers:
                # The real client IP will be the first in the comma-separated list of IPs
                client_ip = request.headers['X-Forwarded-For'].split(',')[0]
            else:
                # If not behind a proxy, use request.remote_addr
                client_ip = request.remote_addr
            if not ipaddress.ip_address(client_ip).is_private:
                if client_ip not in timeout_ip or datetime.now() - timeout_ip[client_ip] > timedelta(seconds=580) and not client_ip.startswith("127.0.0.1"):
                    new_entry = LoggedIP(ip=client_ip, datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    db.session.add(new_entry)
                    db.session.commit()
                timeout_ip[client_ip] = datetime.now()
    
    @edits.route('/analytics', methods=['GET', 'POST'])
    def analytics():
        ips_without_coordinates = LoggedIP.query.filter_by(coordinates=None).all()
        if ips_without_coordinates:
            for logs in ips_without_coordinates:
                response = requests.get(f"http://ip-api.com/json/{logs.ip}").json()
                location_data = [response.get("lat"), response.get("lon")]
                logs.coordinates = json.dumps(location_data)
                db.session.commit()
        logged_ips = LoggedIP.query.all()
        for logs in logged_ips:
            print(logs.coordinates)
        return render_template('analytics.html', logged_ips=logged_ips)
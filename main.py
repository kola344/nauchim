from flask import Flask, render_template, request, jsonify, abort, make_response
import config
import db

application = Flask(__name__)

'''API'''
@application.route('/')
def index_page():
    return 'Hello World'

@application.route('/api/get_calendar_events')
def get_calendar_events_apipage():
    try:
        calendar_events_base = db.calendar_events_db()
        data = calendar_events_base.get_events_json()
        return jsonify({"status": True, "data": data})
    except:
        return jsonify({"status": False})

@application.route('/api/add_calendar_event', methods=["POST"])
def add_calendar_event_apipage():
    data = request.json
    if data['token'] == config.token:
        try:
            calendar_events_base = db.calendar_events_db()
            calendar_events_base.add_event(data['event_name'], data['description'], data['organizer'], data['region'], data['format'], data['direction'], data['person'], data['phone_number'], data['email'], data['date_start'], data['dates'])
            return jsonify({"status": True})
        except:
            return jsonify({"status": False})
    abort(401)

@application.route('/api/delete_calendar_event')
def delete_calendar_event_apipage():
    data = request.json
    if data['token'] == config.token:
        try:
            calendar_events_base = db.calendar_events_db()
            calendar_events_base.delete_event(data['event_name'])
            return jsonify({"status": True})
        except:
            return jsonify({"status": False})
    abort(401)

'''ADMIN'''
@application.route('/admin')
def admin_auth_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        return render_template('admin_main.html')
    else:
        return render_template('admin_auth.html')

if __name__ == '__main__':
    application.run(debug=True)

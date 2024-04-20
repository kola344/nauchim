from flask import Flask, render_template, request, jsonify, abort
import config
import db

application = Flask(__name__)

@application.route('/')
def index_page():
    return 'Hello World'

@application.route('/add_calendar_event', methods=["POST"])
def add_calendar_event_page():
    data = request.form
    if data['token'] == config.token:
        try:
            calendar_events_base = db.calendar_events_db()
            calendar_events_base.add_event(data['event_name'], data['description'], data['organizer'], data['region'], data['format'], data['direction'], data['person'], data['phone_number'], data['email'], data['date_start'], data['dates'])
            return jsonify({"status": True})
        except:
            return jsonify({"status": False})
    abort(401)

@application.route('/get_calendar_events')
def get_calendar_events_page():
    try:
        calendar_events_base = db.calendar_events_db()
        data = calendar_events_base.get_events_json()
        return jsonify({"status": True, "data": data})
    except:
        return jsonify({"status": False})

@application.route('/delete_calendar_event')
def delete_calendar_event_page():
    data = request.form
    if data['token'] == config.token:
        try:
            calendar_events_base = db.calendar_events_db()
            calendar_events_base.delete_event(data['event_name'])
            return jsonify({"status": True})
        except:
            return jsonify({"status": False})
    abort(401)


if __name__ == '__main__':
    application.run(debug=True)

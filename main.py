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
def admin_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        return render_template('admin_main.html', url_calendar_events=f'{config.main_url}admin/calendar_events')
    return render_template('admin_auth.html', url=f'{config.main_url}admin/auth', error='')

@application.route('/admin/auth', methods=["POST"])
def admin_auth_page():
    data = request.form
    print(data)
    password = data['password']
    if password == config.token:
        resp = make_response(render_template('admin_main.html'))
        resp.set_cookie('token', config.token, 30*24*60*60)
        return resp
    return render_template('admin_auth.html', url=f'{config.main_url}admin/auth', error='Неверный пароль')

@application.route('/admin/calendar_events')
def admin_calendar_events_page():
    cookie = request.cookies.get('token')
    print(cookie)
    if cookie == config.token:
        dbase = db.calendar_events_db()
        events = dbase.get_events_json()
        return render_template('admin_calendar_events.html', events=events, url_new_event=f'{config.main_url}admin/add_new_calendar_event')
    abort(404)

@application.route('/admin/add_new_calendar_event')
def admin_add_new_calendar_event_page():
    cookie = request.cookies.get('token')
    print(cookie)
    if cookie == config.token:
        return render_template('admin_calendar_add_event.html', url_back=f'{config.main_url}admin/calendar_events', url=f'{config.main_url}admin/calendar/add_event')
    abort(404)

@application.route('/admin/calendar/add_event', methods=["POST"])
def admin_calendar_add_event_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        data = request.form
        dbase = db.calendar_events_db()
        dbase.add_event(data['event_name'], data['description'], data['organizer'], data['region'], data['format'], data['direction'], data['person'], data['phone_number'], data['email'], data['date_start'], data['dates'])
        events = dbase.get_events_json()
        return render_template('admin_calendar_events.html', events=events, url_new_event=f'{config.main_url}admin/add_new_calendar_event')
    abort(404)

if __name__ == '__main__':
    application.run(debug=True)

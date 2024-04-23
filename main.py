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
        calendar_events_base = db.db_calendar_events()
        data = calendar_events_base.get_events_list()
        return jsonify({"status": True, "data": data})
    except Exception as e:
        print(e)
        return jsonify({"status": False})

@application.route('/api/add_calendar_event', methods=["POST"])
def add_calendar_event_apipage():
    data = request.json
    try:
        calendar_events_base = db.db_calendar_events()
        calendar_events_base.add_event(data["short_name"], data["short_description"], data["organizer"], data["region"], data["format"],
                                       data["person"], data["phone_number"], data["email"], data["start_registration_date"],
                                       data["end_registration_date"], data["date_start"], data["date_end"], data["full_name"],
                                       data["checkpoints"], data["full_description"], data["age"], data["restrictions"],
                                       data["awards"], data["universitets"], data["partners"], data["documents"], data["event_url"])
    except:
        return jsonify({"status": False})

'''ADMIN'''
@application.route('/admin')
def admin_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        return render_template('admin_main.html', url_calendar_events=f'/admin/calendar_events', url_calendar_events_list=f'/admin/calendar/list', url_calendar_events_applications=f'/admin/calendar/applications')
    return render_template('admin_auth.html', url=f'/admin/auth', error='')

@application.route('/admin/auth', methods=["POST"])
def admin_auth_page():
    data = request.form
    password = data['password']
    if password == config.token:
        resp = make_response(render_template('admin_main.html', url_calendar_events_list=f'/admin/calendar/list', url_calendar_events_applications=f'/admin/calendar/applications'))
        resp.set_cookie('token', config.token, 30*24*60*60)
        return resp
    return render_template('admin_auth.html', url=f'/admin/auth', error='Неверный пароль')

@application.route('/admin/calendar/info')
def admin_calendar_event_info_page():
    full_name = request.args.get('full_name')
    calendar_events_base = db.db_calendar_events()
    data = calendar_events_base.get_event_info(full_name)
    full_name = data['full_name']
    checkpoints_list = []
    try:
        for i in data['checkpoints']:
            checkpoints_list.append(f'{i["date"]}: {i["description"]}')
    except:
        pass
    checkpoints = '<br>'.join(checkpoints_list)
    full_description = data['full_description']
    age = data['age']
    restrictions = data['restrictions']
    awards = data['awards']
    universitets = data['universitets']
    partners = data['partners']
    documents = data['documents']
    return render_template('admin_event_info.html', full_name=full_name, full_description=full_description, checkpoints=checkpoints, age=age, restrictions=restrictions, awards=awards, universitets=universitets, partners=partners, documents=documents)

@application.route('/admin/calendar/list')
def admin_celandar_events_list_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        calendar_events_base = db.db_calendar_events()
        events = calendar_events_base.get_events_list(True)
        return render_template('admin_calendar_events_list.html', admin_main_url='/admin', events=events)
    abort(404)

@application.route('/admin/calendar/applications')
def admin_calendar_applications_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        calendar_events_base = db.db_calendar_events()
        events = calendar_events_base.get_events_list(True, True)
        return render_template('admin_calendar_applications.html', admin_main_url='/admin', events=events)

@application.route('/admin/calendar/del')
def admin_calendar_del_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        full_name = request.args.get('full_name')
        organizer = request.args.get('organizer')
        calendar_events_base = db.db_calendar_events()
        calendar_events_base.delete_event(full_name)
        accept = request.args.get('accept')
        print(accept)
        if accept == 'yes':
            events = calendar_events_base.get_events_list(True, True)
            print(events)
            return render_template('admin_calendar_applications.html', admin_main_url='/admin', events=events)
        events = calendar_events_base.get_events_list(True)
        return render_template('admin_calendar_events_list.html', admin_main_url='/admin', events=events)
    abort(404)

@application.route('/admin/calendar/accept')
def admin_calendar_event_accept():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        full_name = request.args.get('full_name')
        calendar_events_base = db.db_calendar_events()
        calendar_events_base.accept_event(full_name)
        events = calendar_events_base.get_events_list(True, True)
        return render_template('admin_calendar_applications.html', admin_main_url='/admin', events=events)

'''ORGANIZERS'''
@application.route('/organizer/calendar/add')
def organizer_calendar_add():
    return render_template('admin_calendar_add_event.html', url='/organizer/calendar/add_event')

@application.route('/organizer/calendar/add_event', methods=["POST"])
def organizer_calendar_add_event_page():
    data = request.form
    print(data["full_name"])
    if data['full_name'] == None or data["full_name"] == '':
        return render_template('admin_calendar_add_event.html', url='/organizer/calendar/add_event', error='Поле "Полное название мероприятия" обязательно')
    try:
        checkpoits_str_list = data["checkpoints"].split('\n')
        checkpoints_list = '['
        for i in checkpoits_str_list:
            splited = i.split(':')
            date, description = splited[0], splited[1]
            item = {'date': date, "description": description}
            checkpoints_list += f'{item},'
        checkpoints = checkpoints_list[:-1] + ']'
    except:
        checkpoints = '[]'
    calendar_events_base = db.db_calendar_events()
    calendar_events_base.add_event(data["short_name"], data["short_description"], data["organizer"], data["region"],
                                   data["format"],
                                   data["person"], data["phone_number"], data["email"], data["start_registration_date"],
                                   data["end_registration_date"], data["date_start"], data["date_end"],
                                   data["full_name"],
                                   checkpoints, data["full_description"], data["age"], data["restrictions"],
                                   data["awards"], data["universitets"], data["partners"], data["documents"],
                                   data["event_url"])
    return render_template('organizer_form_sended.html')


if __name__ == '__main__':
    #application.run(host='10.10.34.251', port=12345, debug=True) # schnet
    #application.run(host='100.123.95.222', port=12345, debug=True) #okean_10
    application.run(host='192.168.173.237', port=12345, debug=True) #A53
    #application.run(debug=True)
from flask import Flask, render_template, request, jsonify, abort, make_response, send_file
import config
import db

app = Flask(__name__)

'''API'''
@app.route('/api/get_calendar_events')
def get_calendar_events_apipage():
    try:
        calendar_events_base = db.db_calendar_events()
        data = calendar_events_base.get_events_list()
        return jsonify({"status": True, "data": data})
    except Exception as e:
        print(e)
        return jsonify({"status": False})

@app.route('/api/add_calendar_event', methods=["POST"])
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

@app.route('/api/get_federal_events')
def get_federal_events_apipage():
    try:
        federal_events_base = db.db_federal_events()
        data = federal_events_base.get_events_list()
        return jsonify({"status": True, "data": data})
    except Exception as e:
        print(e)
        return jsonify({"status": False})

@app.route('/api/get_federal_event_info', methods=["POST"])
def get_federal_event_info_apipage():
    data = request.json
    try:
        federal_events_base = db.db_federal_events()
        data = federal_events_base.get_event_info(data["custom_url"])
        return jsonify({"status": True, "data": data})
    except Exception as e:
        print(e)
        return jsonify({"status": False})

'''ADMIN'''
@app.route('/admin')
def admin_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        return render_template('admin_main.html', url_calendar_events=f'/admin/calendar_events', url_calendar_events_list=f'/admin/calendar/list', url_calendar_events_applications=f'/admin/calendar/applications')
    return render_template('admin_auth.html', url=f'/admin/auth', error='')

@app.route('/admin/auth', methods=["POST"])
def admin_auth_page():
    data = request.form
    password = data['password']
    if password == config.token:
        resp = make_response(render_template('admin_main.html', url_calendar_events_list=f'/admin/calendar/list', url_calendar_events_applications=f'/admin/calendar/applications'))
        resp.set_cookie('token', config.token, 30*24*60*60)
        return resp
    return render_template('admin_auth.html', url=f'/admin/auth', error='Неверный пароль')

@app.route('/admin/calendar/info')
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
    checkpoints = ' | '.join(checkpoints_list)
    full_description = data['full_description']
    age = data['age']
    restrictions = data['restrictions']
    awards = data['awards']
    universitets = data['universitets']
    partners = data['partners']
    documents = data['documents']
    return render_template('admin_event_info.html', full_name=full_name, full_description=full_description, checkpoints=checkpoints, age=age, restrictions=restrictions, awards=awards, universitets=universitets, partners=partners, documents=documents)

@app.route('/admin/calendar/list')
def admin_celandar_events_list_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        calendar_events_base = db.db_calendar_events()
        events = calendar_events_base.get_events_list(True)
        return render_template('admin_calendar_events_list.html', admin_main_url='/admin', events=events)
    abort(404)

@app.route('/admin/calendar/applications')
def admin_calendar_applications_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        calendar_events_base = db.db_calendar_events()
        events = calendar_events_base.get_events_list(True, True)
        return render_template('admin_calendar_applications.html', admin_main_url='/admin', events=events)

@app.route('/admin/calendar/del')
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

@app.route('/admin/calendar/accept')
def admin_calendar_event_accept():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        full_name = request.args.get('full_name')
        calendar_events_base = db.db_calendar_events()
        calendar_events_base.accept_event(full_name)
        events = calendar_events_base.get_events_list(True, True)
        return render_template('admin_calendar_applications.html', admin_main_url='/admin', events=events)
    abort(404)

@app.route('/admin/federal')
def admin_federal_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        federal_events_base = db.db_federal_events()
        events = federal_events_base.get_events_list()
        return render_template('admin_federal_events.html', events=events)
    abort(404)

@app.route('/admin/federal/add')
def admin_federal_add_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        return render_template('admin_add_federal_event.html')
    abort(404)

@app.route('/admin/federal/add_event', methods=["POST"])
def admin_federal_add_event_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        data = request.form
        if data["full_name"] == None or data["full_name"] == '':
            return render_template('admin_add_federal_event.html', error='Поле "Полное название мероприятия" обязательно')
        if data['custom_url'] == None or data['custom_url'] == '':
            return render_template('admin_add_federal_event.html', error='Поле "Ссылка мероприятия" обязательно')
        # checkpoint = {"date", "description"}
        # track = {"title", "direction", "description", "url"}
        # partners = {"title", "image_url"}
        # social_network = {"title", "url"}
        # document = {"title", "url"}
        checkpoints_date = request.form.getlist('checkpoint-date')
        checkpoints_description = request.form.getlist('checkpoint-description')
        checkpoints = []
        for i in range(len(checkpoints_date)):
            checkpoints.append({"date": checkpoints_date[i], "description": checkpoints_description[i]})

        tracks_title = request.form.getlist('track-title')
        tracks_direction = request.form.getlist('track-direction')
        tracks_description = request.form.getlist('track-direction')
        tracks_url = request.form.getlist('track-url')
        tracks = []
        for i in range(len(tracks_title)):
            tracks.append({"title": tracks_title[i], "description": tracks_description[i], "direction": tracks_direction[i], "url": tracks_url[i]})

        partners_title = request.form.getlist("partner-title")
        partners_image_url = request.form.getlist('partner-image_url')
        partners = []
        for i in range(len(partners_title)):
            partners.append({"title": partners_title[i], "image_url": partners_image_url[i]})

        social_networks_title = request.form.getlist("social_network-title")
        social_networks_url = request.form.getlist("social_network-url")
        social_networks = []
        for i in range(len(social_networks_title)):
            social_networks.append({"title": social_networks_title[i], "url": social_networks_url[i]})

        documents_title = request.form.getlist("document-title")
        document_url = request.form.getlist("document-url")
        documents = []
        for i in range(len(documents_title)):
            documents.append({"title": documents_title[i], "url": document_url[i]})

        federal_events_base = db.db_federal_events()
        federal_events_base.add_event(data["short_name"], data["short_description"], data["full_name"], data["full_description"],
                                      str(checkpoints), str(tracks), str(partners), data["person_name"], data['person_role'], data["phone_number"],
                                      data['email'], str(documents), str(social_networks), data['end_description'], data['custom_url'],
                                      data['person_image_url'], data['video_url'])
        events = federal_events_base.get_events_list()
        return render_template('admin_federal_events.html', events=events)
    abort(404)

@app.route('/admin/federal/del')
def admin_federal_del_page():
    cookie = request.cookies.get('token')
    if cookie == config.token:
        full_name = request.args.get('event')
        federal_events_base = db.db_federal_events()
        federal_events_base.delete_event(full_name)
        events = federal_events_base.get_events_list()
        return render_template('admin_federal_events.html', events=events)
    abort(404)

'''ORGANIZERS'''
@app.route('/organizer/calendar/add')
def organizer_calendar_add():
    return render_template('admin_calendar_add_event.html', url='/organizer/calendar/add_event', regions=config.regions)

@app.route('/organizer/calendar/add_event', methods=["POST"])
def organizer_calendar_add_event_page():
    data = request.form
    if data['full_name'] == None or data["full_name"] == '':
        return render_template('admin_calendar_add_event.html', url='/organizer/calendar/add_event', error='Поле "Полное название мероприятия" обязательно')
    checkpoints_date = request.form.getlist("checkpoint-date")
    checkpoints_description = request.form.getlist("checkpoint-description")
    checkpoints = []
    for i in range(len(checkpoints_date)):
        checkpoints.append({"date": checkpoints_date[i], "description": checkpoints_description[i]})
    checkpoints = str(checkpoints)
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

'''IMAGES'''
@app.route('/images')
def images_apipage():
    image = request.args.get('image')
    return send_file(f'images/{image}')

if __name__ == '__main__':
    #application.run(host='10.10.34.252', port=12345, debug=True) # schnet
    #application.run(host='100.123.95.222', port=12345, debug=True) #okean_10
    #app.run(host='192.168.173.237', port=12345, debug=True) #A53
    app.run(debug=True)
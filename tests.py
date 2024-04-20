import requests

def get_calendar_events():
    url = 'http://127.0.0.1:5000/get_calendar_events'
    return requests.get(url).json()

def add_calendar_event():
    url = 'http://127.0.0.1:5000/add_calendar_event'
    #calendar_events_base.add_event(data['event_name'], data['description'], data['organizer'], data['region'],
    # data['format'], data['direction'], data['person'], data['phone_number'], data['email'], data['date_start'], data['dates'])
    token = 'admintk12345'
    event_name = 'Курсы по Python'
    description = 'Курсы по Python для школьников 7-11 классов. Научись кодить онлайн!'
    organizer = 'Онлайн школа 1'
    region = 'Приморский край'
    format = 'Онлайн'
    direction = 'IT'
    person = 'Иван Иванов Иванович'
    phone_number = '+7 (800) 555-35-35'
    email = 'ivanich@yandex.ru'
    date_start = '21.04.2024'
    dates = '21.04.2024-23.04.2024'
    json_data = {'token': token, 'event_name': event_name, 'description': description, 'organizer': organizer, 'region': region,
                 'format': format, 'direction': direction, 'person': person, 'phone_number': phone_number, 'email': email,
                 'date_start': date_start, 'dates': dates}
    return requests.post(url, json=json_data).json()

def delete_calendar_event():
    pass

if __name__ == '__main__':
    print(add_calendar_event())
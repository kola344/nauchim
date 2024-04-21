import sqlite3
import json

import config


class calendar_events_db:
    def __init__(self):
        self.db = sqlite3.connect('database/calendar_events.db')
        self.cursor = self.db.cursor()

    def add_event(self, event_name, description, organizer, region, format, direction, person, phone_number, email, date_start, dates, event_url):
        item = (event_name, description, organizer, region, format, direction, person, phone_number, email, date_start, dates, event_url)
        self.cursor.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', item)
        self.db.commit()

    def get_events_json(self):
        self.cursor.execute('SELECT * FROM events')
        data = self.cursor.fetchall()
        json = {}
        for i in range(len(data))[::-1]:
            item = data[i]
            json[i] = {"event_name": item[0], "description": item[1], "organizer": item[2], "region": item[3], "format": item[4], "direction": item[5], "person": item[6], "phone_number": item[7], "email": item[8], "date_start": item[9], "dates": item[10], "url": item[11], "del_url": f'{config.main_url}admin/del_calendar_event?event_name={item[0]}'}
        return json

    def delete_event(self, event_name):
        self.cursor.execute('DELETE FROM events WHERE event_name = ?', (event_name, ))
        self.db.commit()

if __name__ == '__main__':
    db = calendar_events_db()
    db.add_event('event', 'vot tak', 'organizer', 'nn', 'online', 'it', 'kp', '7997', '@ya.ru', '`7.04', '7-15')
    print(db.get_events_json())
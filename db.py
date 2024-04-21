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
            json[i] = {"event_name": item[0], "description": item[1], "organizer": item[2], "region": item[3], "format": item[4], "direction": item[5], "person": item[6], "phone_number": item[7], "email": item[8], "date_start": item[9], "dates": item[10], "url": item[11], "del_url": f'/admin/del_calendar_event?event_name={item[0]}'}
        return json

    def delete_event(self, event_name):
        self.cursor.execute('DELETE FROM events WHERE event_name = ?', (event_name, ))
        self.db.commit()

    def get_filters(self):
        self.cursor.execute('SELECT organizer, region, format, direction FROM events')
        json = {"organizers": [], "regions": [], "formats": [], "directions": []}
        data = self.cursor.fetchall()
        for item in data:
            if not item[0] in json["organizers"]:
                json["organizers"].append(item[0])
            if not item[1] in json["regions"]:
                json["regions"].append(item[1])
            if not item[2] in json["formats"]:
                json["formats"].append(item[2])
            if not item[3] in json["directions"]:
                json["directions"].append(item[3])
        return json

    def get_events_with_filters_json(self, direction, format, organizer, region):
        self.cursor.execute('SELECT * FROM events')
        data = self.cursor.fetchall()
        json = {}
        for i in range(len(data))[::-1]:
            item = data[i]
            if organizer == item[2] or organizer == '' or organizer == None:
                if region == item[3] or region == '' or region == None:
                    if format == item[4] or format == '' or format == None:
                        if direction == item[5] or direction == '' or direction == None:
                            json[i] = {"event_name": item[0], "description": item[1], "organizer": item[2], "region": item[3], "format": item[4], "direction": item[5], "person": item[6], "phone_number": item[7], "email": item[8], "date_start": item[9], "dates": item[10], "url": item[11], "del_url": f'/admin/del_calendar_event?event_name={item[0]}'}
        return json

if __name__ == '__main__':
    db = calendar_events_db()
    print(db.get_filters())

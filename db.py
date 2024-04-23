import sqlite3

class db_calendar_events:
    def __init__(self):
        self.db = sqlite3.connect('database/cal_events.db')
        self.cursor = self.db.cursor()

    def add_event(self, short_name, short_description, organizer, region, format, person, phone_number, email, start_registration_date,
                  end_registration_date, date_start, date_end, full_name, checkpoints, full_description, age, restrictions, awards,
                  universitets, partners, documents, event_url):
        # checkpoints = [{"date": "01.01.01", "description": "text"}, {}, {}]
        item = (short_name, short_description, organizer, region, format, person, phone_number, email, start_registration_date,
                end_registration_date, date_start, date_end, full_name, checkpoints, full_description, age, restrictions, awards,
                universitets, partners, documents, event_url, "False")
        self.cursor.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', item)
        self.db.commit()

    def get_events_list(self, admin = False, accept = False):
        if accept == True:
            self.cursor.execute('SELECT * FROM events WHERE accepted = "False"')
        else:
            self.cursor.execute('SELECT * FROM events WHERE accepted = "True"')
        data = self.cursor.fetchall()
        events_list = []
        for i in range(len(data))[::-1]:
            item = data[i]
            events_list.append({"short_name": item[0], "short_description": item[1], "organizer": item[2], "region": item[3],
                                "format": item[4], "person": item[5], "phone_number": item[6], "email": item[7],
                                "start_registration_date": item[8], "end_registration_date": item[9], "date_start": item[10],
                                "date_end": item[11], "full_name": item[12], "checkpoints": eval(item[13]), "full_description": item[14],
                                "age": item[15], "restrictions": item[16], "awards": item[17], "universitets": item[18], "partners": item[19],
                                "documents": item[20], "event_url": item[21], "accepted": item[22]})
            if admin == True:
                events_list[-1]["url_info"] = f'/admin/calendar/info?full_name={item[12]}&organizer={item[2]}'
                if accept == False:
                    events_list[-1]["del_url"] = f'/admin/calendar/del?full_name={item[12]}&organizer={item[2]}'
                else:
                    events_list[-1]["del_url"] = f'/admin/calendar/del?full_name={item[12]}&organizer={item[2]}&accept=yes'
                    events_list[-1]["accept_url"] = f'/admin/calendar/accept?full_name={item[12]}&organizer={item[2]}'
        return events_list

    def get_event_info(self, full_name):
        self.cursor.execute('SELECT * FROM events WHERE full_name = ?', (full_name, ))
        item = self.cursor.fetchone()
        event = {"short_name": item[0], "short_description": item[1], "organizer": item[2], "region": item[3],
                                "format": item[4], "person": item[5], "phone_number": item[6], "email": item[7],
                                "start_registration_date": item[8], "end_registration_date": item[9], "date_start": item[10],
                                "date_end": item[11], "full_name": item[12], "checkpoints": eval(item[13]), "full_description": item[14],
                                "age": item[15], "restrictions": item[16], "awards": item[17], "universitets": item[18], "partners": item[19],
                                "documents": item[20], "event_url": item[21]}
        return event

    def delete_event(self, full_name):
        self.cursor.execute('DELETE FROM events WHERE full_name = ?', (full_name, ))
        self.db.commit()

    def accept_event(self, full_name):
        self.cursor.execute('UPDATE events SET accepted = "True" WHERE full_name = ?', (full_name, ))
        self.db.commit()

if __name__ == '__main__':
    db = db_calendar_events()
    db.add_event('11', 'короткое описание', 'школа', 'нн', 'online', 'ivan', '7997', '@ya', '17.04', '18.04', '17.04', '19.04', 'full name', '[{"date": "18.04.2024", "description": "desc"}]', "fdsc", "17", "fasd", "awr", 'nn', "okean", "doki", "google.com")

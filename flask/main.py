from flask import Flask, render_template, request, redirect, url_for, make_response, abort
import os
from flask_compress import Compress
import datetime

app = Flask(__name__)
COMPRESS_MIMETYPES = ['text/html', 'text/css', 'application/json']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)

app.config['SECRET_KEY'] = os.urandom(24)

import gspread
gc = gspread.service_account(filename='service_account.json')
sh = gc.open("Weekly Digest Submission Form (Responses)")
sheet = sh.sheet1

@app.route('/')
def generate_weekly_digest():
    info = {}
    info["date"] = datetime.date.today() + datetime.timedelta(days=6-datetime.date.today().weekday())
    info["deadline"] = info["date"] + datetime.timedelta(days=5)
    info["spirit_events"] = []
    info["club_meetings"] = []
    info["deadlines"] = []
    info["other"] = []
    all_announcements = sheet.get_all_values()
    all_announcements.pop(0)
    for announcement in all_announcements:
        this_announcement = {"timestamp":announcement[0], "email":announcement[1], "type":announcement[2], "title":announcement[3], "description":announcement[4], "date":announcement[5], "time":announcement[6], "link":announcement[7]}
        if this_announcement["type"] == "Spirit Event":
            info["spirit_events"].append(this_announcement)
        elif this_announcement["type"] == "Club Meeting":
            info["club_meetings"].append(this_announcement)
        elif this_announcement["type"] == "Deadline":
            info["deadlines"].append(this_announcement)
        else:
            info["other"].append(this_announcement)
    info["weekdates"] = str(info["date"] + datetime.timedelta(days=1))+" - "+str(info["deadline"])
    return render_template('base.html', info = info)



app.jinja_env.cache = {}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
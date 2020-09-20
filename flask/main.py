from flask import Flask, render_template, request, redirect, url_for, make_response, abort, Response
import os
from flask_compress import Compress
import datetime
from calendar_setup import create_event

app = Flask(__name__)
COMPRESS_MIMETYPES = ['text/html', 'text/css', 'application/json']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)

app.config['SECRET_KEY'] = os.urandom(24)

import gspread
gc = gspread.service_account(filename='service_account.json')
sh = gc.open("Weekly Digest Submission Form (Responses)")
sheet = sh.worksheet("data")

@app.route('/generate-by-announcement-type')
def generate_weekly_digest_by_type():
    info = {}
    info["date"] = datetime.date.today() + datetime.timedelta(days=6-datetime.date.today().weekday())
    info["deadline"] = info["date"] + datetime.timedelta(days=5)
    info["spirit_events"] = []
    info["club_meetings"] = []
    info["deadlines"] = []
    info["general_announcements"] = []
    all_announcements = sheet.get_all_values()
    all_announcements.pop(0)
    for announcement in all_announcements:
        if announcement[8] != "x":
            this_announcement = {"timestamp":announcement[0], "email":announcement[1], "type":announcement[2], "title":announcement[3], "description":announcement[4], "date":announcement[5], "time":announcement[6], "link":announcement[7]}
            # if this_announcement["time"]:
                # this_announcement["time"] = this_announcement["time"].split(":00 ")[0]+" "+this_announcement["time"].split(":00 ")[1]
            if "<a href" in this_announcement["description"]:
                the_link = this_announcement["description"].split("<a")[1].split("</a>")[0]
                the_link = '<a style="box-sizing: border-box;color: #ab192d !important;text-decoration: underline;background-color: transparent;-webkit-text-decoration-skip: objects;" '+the_link+"</a>"
                this_announcement["description"] = this_announcement["description"].split("<a")[0] + the_link + this_announcement["description"].split("</a>")[1]
            if this_announcement["type"] == "Spirit Event":
                this_announcement["title"] = '<img src="https://img.icons8.com/color/48/000000/evil--v1.png"/>'+" "+this_announcement["title"]
                info["spirit_events"].append(this_announcement)
            elif this_announcement["type"] == "Club Meeting":
                info["club_meetings"].append(this_announcement)
            elif this_announcement["type"] == "Deadline":
                info["deadlines"].append(this_announcement)
            else:
                info["general_announcements"].append(this_announcement)
    info["weekdates"] = str((info["date"] + datetime.timedelta(days=1)).strftime("%B %d"))+" - "+str(info["deadline"].strftime("%B %d, %Y"))
    info["date"] = info["date"].strftime("%A, %B %d")
    info["deadline"] = info["deadline"].strftime("%A, %B %d")
    return render_template('mailchimp.html', info = info)

@app.route('/by-day')
def generate_weekly_digest_by_day():
    info = {}
    info["date"] = datetime.date.today() + datetime.timedelta(days=6-datetime.date.today().weekday(),hours=datetime.datetime.now().hour,minutes=datetime.datetime.now().minute)
    info["date"] = datetime.date.today() + datetime.timedelta(days=-3)
    info["date"] = datetime.date.today() + datetime.timedelta(days=-1)
    info["deadline"] = info["date"] + datetime.timedelta(days=5)
    info["monday"] = []
    info["tuesday"] = []
    info["wednesday"] = []
    info["thursday"] = []
    info["friday"] = []
    info["weekend"] = []
    info["miscellaneous"] = []
    all_announcements = sheet.get_all_values()
    all_announcements.pop(0)
    for announcement in all_announcements:
        if announcement[13] != "x":
            this_announcement = {"timestamp":announcement[0], "email":announcement[1], "type":announcement[2], "title":announcement[3], "description":announcement[4], "date":announcement[5], "time":announcement[6], "link":announcement[7], "weekday_number":announcement[8],"hour_number":announcement[9],"minute_number":announcement[10],"start_time":announcement[11],"end_time":announcement[12]}
            # if this_announcement["time"]:
                # this_announcement["time"] = this_announcement["time"].split(":00 ")[0]+" "+this_announcement["time"].split(":00 ")[1]
            # if this_announcement["date"]:
                # monday_date = datetime.datetime.now() - datetime.timedelta(days = datetime.datetime.now().weekday())
                # try:
                #     this_announcement["formatted_time"] = monday_date+datetime.timedelta(days=int(this_announcement["weekday_number"])-1,hours=int(this_announcement["hour_number"]),minutes=int(this_announcement["minute_number"]))
                # except Exception as e:
                #     print(e)
                #     print(this_announcement["title"])
                #     this_announcement["formatted_time"] = monday_date
                # this_announcement["formatted_time"] = (str(this_announcement["formatted_time"].isoformat())+"/"+str((this_announcement["formatted_time"]+datetime.timedelta(hours=1)).isoformat())).replace("-","").replace(":","")
                # print(this_announcement['formatted_time'])
                # this_announcement["calendar_link"] = "https://calendar.google.com/calendar/r/eventedit?text="+this_announcement["title"]+"&dates="+this_announcement["start_time"]+"/"+this_announcement["end_time"]+"&ctz=America/Los_Angeles"+"&details="+this_announcement["description"]
                # if this_announcement["link"]:
                #     this_announcement["calendar_link"] = this_announcement["calendar_link"]+"\n Link: "+this_announcement["link"]
                # print(this_announcement["calendar_link"])
                    # if this_announcement["title"] == "Red Cross: Covid-19 Discussion":
                        # this_announcement["calendar_link"] = create_event(this_announcement["title"],this_announcement["description"],this_announcement["start_time"], this_announcement["end_time"],this_announcement["link"])
            if "<a href" in this_announcement["description"]:
                the_link = this_announcement["description"].split("<a")[1].split("</a>")[0]
                the_link = '<a style="box-sizing: border-box;color: #ab192d !important;text-decoration: underline;background-color: transparent;-webkit-text-decoration-skip: objects;" '+the_link+"</a>"
                this_announcement["description"] = this_announcement["description"].split("<a")[0] + the_link + this_announcement["description"].split("</a>")[1]
            if this_announcement["type"] == "Spirit Event":
                this_announcement["title"] = '<img style="width:25px" src="https://img.icons8.com/color/48/000000/evil--v1.png"/>'+" "+this_announcement["title"]
            elif this_announcement["type"] == "Club Meeting":
                this_announcement["title"] = '<img style="width:25px" src="https://img.icons8.com/dotty/80/000000/group-foreground-selected.png"/>'+" "+this_announcement["title"]
            elif this_announcement["type"] == "Deadline":
                this_announcement["title"] = '<img style="width:25px" src="https://img.icons8.com/pastel-glyph/64/000000/clock.png"/>'+" "+this_announcement["title"]
            else:
                this_announcement["title"] = '<img style="width:25px" src="https://img.icons8.com/cotton/64/000000/commercial--v2.png"/>'+" "+this_announcement["title"]
            if this_announcement["date"] == "Monday":
                info["monday"].append(this_announcement)
            elif this_announcement["date"] == "Tuesday":
                info["tuesday"].append(this_announcement)
            elif this_announcement["date"] == "Wednesday":
                info["wednesday"].append(this_announcement)
            elif this_announcement["date"] == "Thursday":
                info["thursday"].append(this_announcement)
            elif this_announcement["date"] == "Friday":
                info["friday"].append(this_announcement)
            elif this_announcement["date"] == "Saturday" or this_announcement["date"] == "Sunday":
                info["weekend"].append(this_announcement)
            else:
                info["miscellaneous"].append(this_announcement)
    info["weekdates"] = str((info["date"] + datetime.timedelta(days=1)).strftime("%B %d"))+" - "+str(info["deadline"].strftime("%B %d, %Y"))
    info["date"] = info["date"].strftime("%A, %B %d")
    info["deadline"] = info["deadline"].strftime("%A, %B %d")
    return render_template('by_day.html', info = info)

@app.route('/')
def generate_new_template():
    info = {}
    info["date"] = datetime.date.today() + datetime.timedelta(days=6-datetime.date.today().weekday(),hours=datetime.datetime.now().hour,minutes=datetime.datetime.now().minute)
    info["date"] = datetime.date.today() + datetime.timedelta(days=-3)
    info["date"] = datetime.date.today() + datetime.timedelta(days=-1)
    info["deadline"] = info["date"] + datetime.timedelta(days=5)
    info["monday"] = []
    info["tuesday"] = []
    info["wednesday"] = []
    info["thursday"] = []
    info["friday"] = []
    info["weekend"] = []
    info["miscellaneous"] = []
    all_announcements = sheet.get_all_values()
    all_announcements.pop(0)
    for announcement in all_announcements:
        if announcement[13] != "x":
            this_announcement = {"timestamp":announcement[0], "email":announcement[1], "type":announcement[2], "title":announcement[3], "description":announcement[4], "date":announcement[5], "time":announcement[6], "link":announcement[7], "weekday_number":announcement[8],"hour_number":announcement[9],"minute_number":announcement[10],"start_time":announcement[11],"end_time":announcement[12]}
            # if this_announcement["time"]:
                # this_announcement["time"] = this_announcement["time"].split(":00 ")[0]+" "+this_announcement["time"].split(":00 ")[1]
            # if this_announcement["date"]:
                # monday_date = datetime.datetime.now() - datetime.timedelta(days = datetime.datetime.now().weekday())
                # try:
                #     this_announcement["formatted_time"] = monday_date+datetime.timedelta(days=int(this_announcement["weekday_number"])-1,hours=int(this_announcement["hour_number"]),minutes=int(this_announcement["minute_number"]))
                # except Exception as e:
                #     print(e)
                #     print(this_announcement["title"])
                #     this_announcement["formatted_time"] = monday_date
                # this_announcement["formatted_time"] = (str(this_announcement["formatted_time"].isoformat())+"/"+str((this_announcement["formatted_time"]+datetime.timedelta(hours=1)).isoformat())).replace("-","").replace(":","")
                # print(this_announcement['formatted_time'])
                # this_announcement["calendar_link"] = "https://calendar.google.com/calendar/r/eventedit?text="+this_announcement["title"]+"&dates="+this_announcement["start_time"]+"/"+this_announcement["end_time"]+"&ctz=America/Los_Angeles"+"&details="+this_announcement["description"]
                # if this_announcement["link"]:
                #     this_announcement["calendar_link"] = this_announcement["calendar_link"]+"\n Link: "+this_announcement["link"]
                # print(this_announcement["calendar_link"])
                    # if this_announcement["title"] == "Red Cross: Covid-19 Discussion":
                        # this_announcement["calendar_link"] = create_event(this_announcement["title"],this_announcement["description"],this_announcement["start_time"], this_announcement["end_time"],this_announcement["link"])
            if "<a href" in this_announcement["description"]:
                the_link = this_announcement["description"].split("<a")[1].split("</a>")[0]
                the_link = '<a style="box-sizing: border-box;color: #ab192d !important;text-decoration: underline;background-color: transparent;-webkit-text-decoration-skip: objects;" '+the_link+"</a>"
                this_announcement["description"] = this_announcement["description"].split("<a")[0] + the_link + this_announcement["description"].split("</a>")[1]
            if this_announcement["type"] == "Spirit Event":
                this_announcement["title"] = '<img style="width:25px" src="https://img.icons8.com/color/48/000000/evil--v1.png"/>'+" "+this_announcement["title"]
            elif this_announcement["type"] == "Club Meeting":
                this_announcement["title"] = '<img style="width:25px" src="https://img.icons8.com/dotty/80/000000/group-foreground-selected.png"/>'+" "+this_announcement["title"]
            elif this_announcement["type"] == "Deadline":
                this_announcement["title"] = '<img style="width:25px" src="https://img.icons8.com/pastel-glyph/64/000000/clock.png"/>'+" "+this_announcement["title"]
            else:
                this_announcement["title"] = '<img style="width:25px" src="https://img.icons8.com/cotton/64/000000/commercial--v2.png"/>'+" "+this_announcement["title"]
            if this_announcement["date"] == "Monday":
                info["monday"].append(this_announcement)
            elif this_announcement["date"] == "Tuesday":
                info["tuesday"].append(this_announcement)
            elif this_announcement["date"] == "Wednesday":
                info["wednesday"].append(this_announcement)
            elif this_announcement["date"] == "Thursday":
                info["thursday"].append(this_announcement)
            elif this_announcement["date"] == "Friday":
                info["friday"].append(this_announcement)
            elif this_announcement["date"] == "Saturday" or this_announcement["date"] == "Sunday":
                info["weekend"].append(this_announcement)
            else:
                info["miscellaneous"].append(this_announcement)
    info["weekdates"] = str((info["date"] + datetime.timedelta(days=1)).strftime("%B %d"))+" - "+str(info["deadline"].strftime("%B %d, %Y"))
    info["date"] = info["date"].strftime("%A, %B %d")
    info["deadline"] = info["deadline"].strftime("%A, %B %d")
    return render_template('index.html', info = info)

@app.route('/calendar')
def calendar():
    start = datetime.datetime.utcnow().isoformat() + 'Z'
    end = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z'
    event_url = create_event("test","please work teehee",start, end,"https://zoom.us/j/99082913301?pwd=ZVRPRkgvbFN5TFQxZE5yS3o2NkVkUT09")
    return event_url


app.jinja_env.cache = {}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
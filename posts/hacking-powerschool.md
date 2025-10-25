---
title: "Hacking PowerSchool"
date: "2025-10-25"
excerpt: "Wouldn't it be nice if my school schedule was automatically added to my calendar?"
---

PowerSchool is a popular student information system used by schools worldwide. However, most students don't regularly check it. Every semester, I'd log into PowerSchool, copy-paste my schedule into a spreadsheet, then manually add events to Google Calendar. With classes changing rooms, teachers, and times, it was a weekly chore.

In this post, I'll walk you through how I reverse-engineered PowerSchool's backend to fetch my schedule programmatically, convert it to an ICS file, and sync it with Google Calendar.

## Understanding PowerSchool's Backend

I started by inspecting the network requests PowerSchool made when I logged in and viewed my schedule to find the relevant API endpoints.

![Some network requests related to "calendar" in PowerSchool](https://hc-cdn.hel1.your-objectstorage.com/s/v3/45dd68f3feb79923a372ba3c958d060d18aad6b3_image.png)
*Some network requests related to "calendar" in PowerSchool*

The first interesting request I found was to the following endpoint:

```http
GET /api/calendar/eventdetails?timezone=<timezone>&startdate=2025-10-01&enddate=2025-10-31&studentpersonuid=<student_id>&organizationId=<school_id> HTTP/2
Host: api.calendar.mfe.powerschool.com
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Origin: https://<school>.student.powerschool.com
Referer: https://<school>.student.powerschool.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
superFetch: true
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15
Cookie: sessiontoken=<session_token>; incap_ses_<id>=<incap_ses>; visid_incap_<id>=<visid_incap>`
```

Even though this wasn't the endpoint I needed, it yielded a couple of important insights:

1. The request was sent to `https://api.calendar.mfe.powerschool.com/api/calendar/eventdetails`. This means that the calendar data is most likely stored in `https://api.calendar.mfe.powerschool.com/api/calendar/[something]`.
2. The request included several query parameters, such as `studentpersonuid` and `organizationId`, which are likely unique identifiers for the student and school, respectively. This makes sense, as the API needs to know whose schedule to fetch.
3. The request included 3 cookies: `sessiontoken`, `incap_ses_<id>`, and `visid_incap_<id>`. I will need those later.

Using the insights from the previous request, I then saw another request to the following endpoint when I viewed my schedule:

```http
GET /api/calendar/eventdetails?timezone=<timezone>&startdate=2025-11-01&enddate=2025-11-30&studentpersonuid=<student_id>&organizationId=<school_id> HTTP/2
Host: api.calendar.mfe.powerschool.com
... (other headers) ...
```

This time, the endpoint was `https://api.calendar.mfe.powerschool.com/api/calendar/eventdetails`, which aligned with my earlier hypothesis. The query parameters were similar, but the `startdate` and `enddate` were for November 2025. There were other requests to this exact endpoint with different date ranges.

However, curiously, the response contained no events:

```json
{
  "StatusCode": 200,
  "CalendarResponse": {
    "EventDetails": []
  }
}
```

Nevertheless, this gave me the JSON structure of the response, which would be useful later.

Looking at the JavaScript files loaded by the web app, I found `remoteEntry.js` to be first loaded by the site. This file was not particularly useful, as it essentially loaded up all the other bundled JavaScript files. However, looking through these bundled files, I found some curious code snippets that hinted at how the calendar data was fetched.

For instance, in `336.bundle.js`, I found the following code:

```javascript
var ...,
    ce = "SisSchedule",
    le = "SisTeacherSchedule",
    ie = "CalendarEvent",
    ue = "IsStaff",
    se = "IsStudent",
    de = "IsGuardian",
    ...;
```

This indicated that there were different types of calendar events, such as `SisSchedule` and `SisTeacherSchedule`. Therefore, I hypothesized that the actual endpoint to fetch the schedule might be something like `https://api.calendar.mfe.powerschool.com/api/calendar/SisSchedule`.

I then searched for where the `SisSchedule` variable was used and found a function in `513.bundle.js` that made an API call:

```javascript
e.prototype.getSISScheduleCalendarData = function (e, t, n, a, o) {
  return m(this, void 0, void 0, function () {
    var i = this;
    return f(this, function (l) {
      return [
        2,
        this.fetchAndMapEvents(
          function () {
            return i.apiService.getSISScheduleCalendarData({
              schooldcid: e,
              studentdcid: t,
              timezone: n,
              startdate: a,
              enddate: o,
            });
          },
          ["CalendarResponse", "EventDetails"],
          function (e) {
            return {
              Title: e.Title,
              StartDateTime: r()(e.StartDateTime).tz(n).format(s.qo),
              EndDateTime: r()(e.EndDateTime).tz(n).format(s.qo),
              EventType: e.EventType,
              SisInfo: e.SisInfo,
            };
          }
        ),
      ];
    });
  });
};
```

This function, `getSISScheduleCalendarData`, seemed to fetch the schedule data for a student. It took parameters like `schooldcid`, `studentdcid`, `timezone`, `startdate`, and `enddate`, which aligned with the query parameters I had seen earlier.

## Fetching the Schedule

With this information, I can now construct the correct API endpoint to fetch my schedule. The endpoint is:

```http
https://api.calendar.mfe.powerschool.com/api/calendar/sisschedule
```

To authenticate the request, I needed to set up some environment variables first, such as my `sessiontoken`, `incap_ses_1219_3183297`, `visid_incap_3183297`, `schooldcid`, `studentdcid`, and `timezone`. These values were all relatively easy to find by inspecting the cookies and network requests in my browser.

Here's a simplified version of the code:

```python
headers = {
    ...
}

cookies = {
    "sessiontoken": SESSION_TOKEN,
    "incap_ses_<id>": INCAP_SES,
    "visid_incap_<id>": VISID_INCAP,
}


current = datetime(2025, 8, 1) # Start of school year
all_events = []
while current.year < 2026 or (current.year == 2026 and current.month <= 6):
    _, last_day = monthrange(current.year, current.month)
    start_date = current.strftime("%Y-%m-%d")
    end_date = f"{current.year}-{current.month:02d}-{last_day:02d}"

    url = (
        f"{BASE_URL}/api/calendar/sisschedule"
        f"?schooldcid={SCHOOL_DCID}"
        f"&studentdcid={STUDENT_DCID}"
        f"&timezone={TIMEZONE.replace('/', '%2F')}"
        f"&startdate={start_date}"
        f"&enddate={end_date}"
    )

    resp = requests.get(url, headers=headers, cookies=cookies, timeout=15)
    resp.raise_for_status()
    monthly_events = resp.json().get("CalendarResponse", {}).get("EventDetails", [])
    all_events.extend(monthly_events)

    if current.month == 12:
        current = current.replace(year=current.year + 1, month=1, day=1)
    else:
        current = current.replace(month=current.month + 1, day=1)
```

This code iterates through each month from August 2025 to June 2026 (a school year), fetching the schedule for each month and accumulating the events in the `all_events` list.

## Generating the ICS File

Once I had all the events, I needed to convert them into an ICS file format that Google Calendar could understand.

However, there were some minor challenges I had to overcome first:

1. The event times were in UTC, so I had to convert them to my local timezone. To do this, I needed to use a timezone library like `pytz`.
2. Additionally, I needed to extract relevant information like course name, section, teacher, room, and event type from the nested JSON structure.

I ended up with the following code:

```python
local_tz = pytz.timezone(TIMEZONE) # Convenient, as PowerSchool uses IANA timezones
processed_events = []

for e in events:
    start_str = e["StartDateTime"].replace("+0000", "")
    end_str = e["EndDateTime"].replace("+0000", "")
    start_utc = datetime.fromisoformat(start_str).replace(tzinfo=timezone.utc)
    end_utc = datetime.fromisoformat(end_str).replace(tzinfo=timezone.utc)
    start = start_utc.astimezone(local_tz)
    end = end_utc.astimezone(local_tz)

    sis_info = e.get("SisInfo", {})
    instructor = sis_info.get("InstructorInfo", {})
    schedule = sis_info.get("ScheduleInfo", {})

    course_name = e.get("Title", "")
    section = schedule.get("PeriodNumber", "")
    teacher = f"{instructor.get('InstructorFirstName', '')} {instructor.get('InstructorLastName', '')}".strip()
    room = schedule.get("RoomNumber", "")
    schedule_type = e.get("EventType", "")

    processed_events.append(
        {
            "date": start.date(),
            "start_time": start.time(),
            "end_time": end.time(),
            "course": course_name,
            "section": section,
            "teacher": teacher,
            "room": room,
            "type": schedule_type,
            "start": start,
            "end": end,
        }
    )

processed_events.sort(key=lambda x: (x["date"], x["start_time"]))
```

With the processed events ready, I then generated the ICS file:

```python
lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//PowerSchool Schedule Export//EN"]

for event in processed_events:
    dtstart = event["start"].strftime("%Y%m%dT%H%M%S")
    dtend = event["end"].strftime("%Y%m%dT%H%M%S")

    lines.extend(
        [
            "BEGIN:VEVENT",
            f"SUMMARY:{event['course']} ({event['section']})",
            f"DTSTART;TZID={TIMEZONE}:{dtstart}",
            f"DTEND;TZID={TIMEZONE}:{dtend}",
            f"LOCATION:{event['room']}",
            f"DESCRIPTION:Teacher: {event['teacher']}",
            f"CATEGORIES:{event['course']}",
            "END:VEVENT",
        ]
    )

lines.append("END:VCALENDAR")

ics_path = Path("powerschool_schedule.ics")
ics_path.write_text("\n".join(lines), encoding="utf-8")
```

This ICS file could then be imported into Google Calendar.

## Conclusion

Retrospectively, I should have done this 2 or 3 years ago! It would have saved me so much time and effort every semester.

There were some caveats to this method. Firstly, the script relies on hardcoded cookies for authentication, which may expire. However, for the purpose of this project, manual authentication sufficed.

Another caveat was that the ICS file treated each class session as a separate event. I accidentally introduced a bug by forgetting to convert the date to UTC+8 before I imported the ICS file, so I had to manually delete 840 events from my calendar. The amount of emails that I received from Google Calendar was a problem.

An elegant solution would involve creating recurring events for each class. However, there were several challenges to this approach, such as handling holidays and changes in schedule. Therefore, I opted for the simpler approach of individual events for now.

All in all, this project was a fun exercise in reverse-engineering and automation. If your school uses PowerSchool, I highly recommend giving this a try!

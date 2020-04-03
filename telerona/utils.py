import time
from telethon import Button

from .config import countries


def get_last_checked(a):
    d = round(time.time() - a / 1000)

    if d < 10:
        last_checked = "just now"
    elif d < 60:
        last_checked = str(d) + " seconds ago"
    elif d < 120:
        last_checked = "1 minutes ago"
    elif d < 3600:
        last_checked = str(d // 60) + " minutes ago"
    elif d < 7200:
        last_checked = "1 hour ago"
    else:
        last_checked = str(d // 3600) + " hours ago"
    return last_checked


backcancel = [
    Button.inline("⬅️ Go back", data="back"),
    Button.inline("❌ Cancel", data="cancel"),
]
cbackcancel = [
    Button.inline("⬅️ Go back", data="select"),
    Button.inline("❌ Cancel", data="cancel"),
]


def create_loc_buttons():
    try:
        loc_btn = []
        tmp_list = []
        for x in countries:
            if len(tmp_list) == 3:
                loc_btn.append(tmp_list.copy())
                tmp_list.clear()
            tmp_list.append(
                Button.inline(x["flag"] + " " + x["name"], data="loc_" + x["name"])
            )
    finally:
        if tmp_list:
            loc_btn.append(tmp_list.copy())
        tmp_list.clear()

    loc_btn.append(backcancel)
    return loc_btn

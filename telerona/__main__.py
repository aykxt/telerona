from datetime import datetime

from telethon import Button, events

from . import api, bot, config, db, loc_btn, logger
from .utils import backcancel, cbackcancel, get_last_checked


@bot.on(events.NewMessage(pattern="/ping"))
async def ping(event):
    a = datetime.now()
    msg = await event.respond("pong")
    ping = (datetime.now() - a).microseconds / 1000
    await msg.edit(f"Pong\n{ping:.2f}ms")
    raise events.StopPropagation


@bot.on(events.NewMessage())
async def start(event, from_query=False):
    g = api.glob
    last_checked = get_last_checked(g["updated"])

    if from_query:
        answer = event.edit
    else:
        answer = event.respond

    await answer(
        "**🦠🧻 Coronavirus tracker 🦠🧻**\n\n"
        "**Global**\n"
        f"✔️ __{g['cases']}__ confirmed\n"
        f"😷 __{g['active']}__ active\n"
        f"🩹 __{g['recovered']}__ recovered\n"
        f"🤒 __{g['critical']}__ critical\n"
        f"⚰️ __{g['deaths']}__ deaths\n\n"
        f"🌐 __{g['affectedCountries']}__ countries affected\n"
        f"😷 __{g['casesPerOneMillion']}__ cases per one million\n"
        f"💀 __{g['deathsPerOneMillion']}__ deaths per one million\n\n"
        "**Today**\n"
        f"😷 __{g['todayCases']}__ confirmed\n"
        f"💀 __{g['todayDeaths']}__ deaths\n\n"
        f"__Last updated: {last_checked}__",
        buttons=[
            [
                Button.inline("🔝 Top 10", data="top"),
                Button.inline("🌍 Countries", data="loc"),
            ],
            [Button.inline("ℹ️ About", data="info")],
        ],
    )

    if not from_query:
        if event.text == "/start":
            db.init_user(await event.get_sender())


@bot.on(events.CallbackQuery(data=b"info"))
async def info(event):
    await event.edit(
        "**🦠 Coronavirus tracker 🦠**\n\n"
        f"ℹ️ Version: {config.version}\n"
        f"🖋️ Creator: {config.creator}\n\n"
        f"👥 Total users: {db.get_user_count()}",
        buttons=[[Button.url("💻 Source code", config.repository)], backcancel,],
    )


@bot.on(events.CallbackQuery(data=b"cancel"))
async def cancel(event):
    await event.delete()


@bot.on(events.CallbackQuery(data=b"back"))
async def go_back(event):
    await start(event, from_query=True)


@bot.on(events.CallbackQuery(data=b"select"))
async def go_select(event):
    await select_location(event)


@bot.on(events.CallbackQuery(data=b"loc"))
async def select_location(event):
    await event.edit("Choose:", buttons=loc_btn)


@bot.on(events.CallbackQuery(pattern="loc_"))
async def loc_ger(event):
    data = event.data.decode()
    country = data[4:]

    i = next(
        (index for (index, d) in enumerate(api.countries) if d["country"] == country),
        None,
    )

    c = api.countries[i]

    last_checked = get_last_checked(c["updated"])

    if c["todayCases"] == 0:
        c["todayCases"] = "N/A"
    if c["todayDeaths"] == 0:
        c["todayDeaths"] = "N/A"

    await event.edit(
        "**🦠 Coronavirus tracker 🦠**\n\n"
        f"**{country}**\n"
        f"🧪 __{c['tests']}__ tests\n"
        f"✔️ __{c['cases']}__ confirmed\n"
        f"😷 __{c['active']}__ active\n"
        f"🩹 __{c['recovered']}__ recovered\n"
        f"💀 __{c['deaths']}__ deaths\n\n"
        f"**Per one million**\n"
        f"🧪 __{c['testsPerOneMillion']}__ tests\n"
        f"😷 __{c['casesPerOneMillion']}__ cases\n"
        f"💀 __{c['deathsPerOneMillion']}__ deaths\n\n"
        f"**Today**\n"
        f"😷 __{c['todayCases']}__ confirmed\n"
        f"💀 __{c['todayDeaths']}__ deaths\n\n"
        f"Last updated: {last_checked}",
        buttons=[cbackcancel],
    )


@bot.on(events.CallbackQuery(data=b"top"))
async def top(event):
    glo = api.glob
    last_checked = get_last_checked(glo["updated"])

    string = ""

    for x in api.countries[:10]:
        string += (
            f"**{x['country']}**\n"
            f"{x['cases']} confirmed\n"
            f"{x['recovered']} recovered\n"
            f"{x['deaths']} deaths\n\n"
        )

    await event.edit(
        "**🦠 Top 10 🦠**\n\n" f"{string}" f"__Last updated: {last_checked}__",
        buttons=[backcancel],
    )


with bot:
    logger.info("Bot started")
    bot.run_until_disconnected()
    logger.info("Bot stopped")

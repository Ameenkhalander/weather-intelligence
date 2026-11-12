from string import Template

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(page_title="Weather Intelligence", page_icon="🌦️", layout="wide")

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
AQ_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# ----------------------------------------------------------------- themes
THEMES = {
    "🌙 Midnight": dict(bg="linear-gradient(160deg,#0b1020 0%,#141b34 100%)", sidebar="#0e1428",
                        card="rgba(255,255,255,0.06)", border="rgba(255,255,255,0.10)",
                        text="#e8ecf8", muted="#9aa4c2", accent="#6ea8fe", grid="rgba(255,255,255,0.08)"),
    "☀️ Light": dict(bg="linear-gradient(160deg,#eef3fb 0%,#f9fbff 100%)", sidebar="#ffffff",
                    card="rgba(255,255,255,0.85)", border="rgba(20,30,60,0.10)",
                    text="#1a2233", muted="#5d6b88", accent="#2f6fed", grid="rgba(20,30,60,0.08)"),
    "🌌 Aurora": dict(bg="linear-gradient(160deg,#0f2027 0%,#203a43 50%,#2c5364 100%)", sidebar="#0f2027",
                      card="rgba(255,255,255,0.08)", border="rgba(255,255,255,0.14)",
                      text="#eafffb", muted="#9fc7c2", accent="#5eead4", grid="rgba(255,255,255,0.10)"),
    "🌇 Sunset": dict(bg="linear-gradient(160deg,#2b1055 0%,#7a3c8f 50%,#e0736f 100%)", sidebar="#2b1055",
                      card="rgba(255,255,255,0.10)", border="rgba(255,255,255,0.18)",
                      text="#fff6ee", muted="#f0c9c0", accent="#ffd166", grid="rgba(255,255,255,0.12)"),
}

CSS = Template("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: $bg; background-attachment: fixed; }
.stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp div[data-testid="stMarkdownContainer"], .stApp div[data-testid="stMetricValue"] { color: $text; }
header[data-testid="stHeader"] { background: transparent; }
section[data-testid="stSidebar"] { background: $sidebar; border-right: 1px solid $border; }
.block-container { padding-top: 2rem; max-width: 1250px; }
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { background: $card !important; border-color: $border !important; border-radius: 12px !important; }
div[data-baseweb="input"] input, div[data-baseweb="select"] * { color: $text !important; }
.stButton > button, .stDownloadButton > button { border-radius: 12px; border: 1px solid $border; background: $card; color: $text; font-weight: 600; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color: $accent; color: $accent; }
button[data-baseweb="tab"] { font-weight: 600; }
button[data-baseweb="tab"][aria-selected="true"] { color: $accent !important; }
div[data-baseweb="tab-highlight"] { background-color: $accent !important; }
.title { font-size: 2.3rem; font-weight: 800; letter-spacing: -0.02em;
         background: linear-gradient(90deg, $accent, $text); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { color: $muted !important; margin-bottom: 1rem; }
.hero { border-radius: 26px; padding: 28px 34px; display: flex; justify-content: space-between; align-items: center;
        box-shadow: 0 20px 50px rgba(0,0,0,.28); margin-bottom: 18px; }
.hero, .hero * { color: #fff !important; text-shadow: 0 2px 10px rgba(0,0,0,.25); }
.hero .city { font-size: 1.1rem; font-weight: 600; opacity: .92; }
.hero .temp { font-size: 5rem; font-weight: 800; line-height: 1; margin: 6px 0; }
.hero .cond { font-size: 1.3rem; font-weight: 600; }
.hero .sub { opacity: .9; margin-top: 4px; }
.hero .big { font-size: 7rem; line-height: 1; }
.tile { background: $card; border: 1px solid $border; border-radius: 18px; padding: 16px 18px; backdrop-filter: blur(12px);
        transition: transform .2s, border-color .2s; height: 100%; margin-bottom: 12px; }
.tile:hover { transform: translateY(-3px); border-color: $accent; }
.tile .lbl { font-size: .72rem; text-transform: uppercase; letter-spacing: .09em; color: $muted !important; }
.tile .val { font-size: 1.75rem; font-weight: 700; margin: 2px 0; }
.tile .sub { font-size: .8rem; color: $muted !important; }
.insight { background: $card; border: 1px solid $border; border-left: 4px solid $accent; border-radius: 14px;
           padding: 12px 16px; margin-bottom: 10px; }
.insight.good { border-left-color: #34d399; } .insight.warn { border-left-color: #fbbf24; }
.insight.alert { border-left-color: #f87171; }
.chip { display: inline-block; background: $card; border: 1px solid $border; border-radius: 999px;
        padding: 6px 14px; margin: 0 8px 8px 0; font-weight: 600; font-size: .9rem; }
.days { display: grid; grid-template-columns: repeat(auto-fit, minmax(125px, 1fr)); gap: 12px; margin-bottom: 18px; }
.day { background: $card; border: 1px solid $border; border-radius: 18px; padding: 14px; text-align: center;
       transition: transform .2s, border-color .2s; }
.day:hover { transform: translateY(-4px); border-color: $accent; }
.day .d { font-weight: 700; } .day .e { font-size: 2rem; margin: 4px 0; }
.day .hi { font-weight: 700; } .day .lo { color: $muted !important; } .day .r { color: $accent !important; font-size: .85rem; }
.section { font-size: 1.15rem; font-weight: 700; margin: 8px 0 10px; }
</style>
""")

# ---------------------------------------------------------------- helpers
WMO = {0: ("☀️", "Clear sky", "clear"), 1: ("🌤️", "Mainly clear", "clear"), 2: ("⛅", "Partly cloudy", "cloud"),
       3: ("☁️", "Overcast", "cloud"), 45: ("🌫️", "Fog", "cloud"), 48: ("🌫️", "Rime fog", "cloud"),
       51: ("🌦️", "Light drizzle", "rain"), 53: ("🌦️", "Drizzle", "rain"), 55: ("🌧️", "Heavy drizzle", "rain"),
       56: ("🌧️", "Freezing drizzle", "rain"), 57: ("🌧️", "Freezing drizzle", "rain"),
       61: ("🌦️", "Light rain", "rain"), 63: ("🌧️", "Rain", "rain"), 65: ("🌧️", "Heavy rain", "rain"),
       66: ("🌧️", "Freezing rain", "rain"), 67: ("🌧️", "Freezing rain", "rain"),
       71: ("🌨️", "Light snow", "snow"), 73: ("🌨️", "Snow", "snow"), 75: ("❄️", "Heavy snow", "snow"),
       77: ("❄️", "Snow grains", "snow"), 80: ("🌦️", "Rain showers", "rain"), 81: ("🌧️", "Rain showers", "rain"),
       82: ("⛈️", "Violent showers", "storm"), 85: ("🌨️", "Snow showers", "snow"), 86: ("🌨️", "Snow showers", "snow"),
       95: ("⛈️", "Thunderstorm", "storm"), 96: ("⛈️", "Thunderstorm + hail", "storm"),
       99: ("⛈️", "Severe thunderstorm", "storm")}

HERO_GRADIENTS = {
    "clear_day": "linear-gradient(135deg,#f6a52f,#f0643c)", "clear_night": "linear-gradient(135deg,#0f2027,#2c5364)",
    "cloud": "linear-gradient(135deg,#6b7a99,#a3b1cc)", "rain": "linear-gradient(135deg,#2c3e68,#4a7bd0)",
    "snow": "linear-gradient(135deg,#6f93c7,#a8d4f0)", "storm": "linear-gradient(135deg,#1f2227,#454b57)",
}

ACTIVITIES = {
    "🏃 Running": dict(t=16, tw=3.0, rw=0.7, ww=1.0), "🚴 Cycling": dict(t=18, tw=2.5, rw=0.8, ww=2.0),
    "🧺 Picnic": dict(t=24, tw=2.5, rw=1.2, ww=1.2), "🏖️ Beach": dict(t=30, tw=2.0, rw=1.0, ww=0.6),
    "📸 Photo walk": dict(t=22, tw=1.5, rw=1.0, ww=0.8),
}
COMPASS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def wmo(code):
    return WMO.get(int(code), ("🌡️", "Unknown", "cloud"))


def tile(lbl, val, sub=""):
    return f'<div class="tile"><div class="lbl">{lbl}</div><div class="val">{val}</div><div class="sub">{sub}</div></div>'


def aqi_info(v):
    for limit, label, color in [(50, "Good", "#34d399"), (100, "Moderate", "#fbbf24"),
                                (150, "Unhealthy for sensitive groups", "#fb923c"), (200, "Unhealthy", "#f87171"),
                                (300, "Very unhealthy", "#a855f7")]:
        if v <= limit:
            return label, color
    return "Hazardous", "#9f1239"


def style_fig(fig, th, height=360):
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color=th["text"],
                      margin=dict(l=10, r=10, t=30, b=10), height=height, hovermode="x unified",
                      legend=dict(orientation="h", y=1.12, x=0))
    fig.update_xaxes(gridcolor=th["grid"], zeroline=False)
    fig.update_yaxes(gridcolor=th["grid"], zeroline=False)
    return fig


# -------------------------------------------------------------- data layer
@st.cache_data(ttl=3600, show_spinner=False)
def geocode(name):
    r = requests.get(GEO_URL, params={"name": name, "count": 6}, timeout=10)
    r.raise_for_status()
    return r.json().get("results", [])


@st.cache_data(ttl=900, show_spinner=False)
def get_forecast(lat, lon):
    params = {
        "latitude": lat, "longitude": lon, "timezone": "auto", "past_days": 7, "forecast_days": 7,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m,"
                   "wind_direction_10m,weather_code,pressure_msl,is_day,cloud_cover",
        "hourly": "temperature_2m,apparent_temperature,relative_humidity_2m,precipitation_probability,"
                  "wind_speed_10m,uv_index,weather_code,is_day",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,"
                 "precipitation_probability_max,uv_index_max,sunrise,sunset,wind_speed_10m_max",
    }
    r = requests.get(FORECAST_URL, params=params, timeout=12)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=900, show_spinner=False)
def get_air(lat, lon):
    try:
        r = requests.get(AQ_URL, params={
            "latitude": lat, "longitude": lon, "timezone": "auto", "forecast_days": 2,
            "current": "us_aqi,pm2_5,pm10,ozone,nitrogen_dioxide,sulphur_dioxide,carbon_monoxide",
            "hourly": "us_aqi,pm2_5"}, timeout=12)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return None


def prep(data):
    cur = data["current"]
    now = pd.to_datetime(cur["time"]).floor("h")
    h = pd.DataFrame(data["hourly"])
    h["time"] = pd.to_datetime(h["time"])
    h = h[h["time"] >= now].reset_index(drop=True)
    d = pd.DataFrame(data["daily"])
    for c in ("time", "sunrise", "sunset"):
        d[c] = pd.to_datetime(d[c])
    today = now.normalize()
    return cur, h, d[d["time"] < today].reset_index(drop=True), d[d["time"] >= today].reset_index(drop=True), d


def activity_matrix(h24):
    rows = {}
    for name, p in ACTIVITIES.items():
        s = (100 - (h24["apparent_temperature"] - p["t"]).abs() * p["tw"]
             - h24["precipitation_probability"] * p["rw"] * 0.6
             - (h24["wind_speed_10m"] - 12).clip(lower=0) * p["ww"]
             - (h24["uv_index"] - 7).clip(lower=0) * 4
             - (1 - h24["is_day"]) * 40)
        rows[name] = s.clip(0, 100).round(0).values
    return pd.DataFrame(rows, index=h24["time"]).T


# ----------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### 🎛️ Customize")
    theme_name = st.selectbox("Theme", list(THEMES))
    units = st.radio("Units", ["Metric (°C, km/h)", "Imperial (°F, mph)"], horizontal=False)
    st.markdown("---")
    st.markdown("### 📍 Location")
    query = st.text_input("Search a city", value="Bengaluru")

th = THEMES[theme_name]
st.markdown(CSS.substitute(th), unsafe_allow_html=True)

imperial = units.startswith("Imperial")
TU, WU = ("°F", "mph") if imperial else ("°C", "km/h")


def T(c):
    return c * 9 / 5 + 32 if imperial else c


def dT(c):
    return c * 9 / 5 if imperial else c


def W(k):
    return k * 0.621371 if imperial else k


if "favs" not in st.session_state:
    st.session_state.favs = {}


def label_of(p):
    return ", ".join(x for x in [p["name"], p.get("admin1"), p.get("country")] if x)


place = None
with st.sidebar:
    try:
        results = geocode(query) if query else []
    except requests.RequestException:
        results = []
        st.error("Geocoding service unreachable.")
    if results:
        idx = st.selectbox("Matches", range(len(results)), format_func=lambda i: label_of(results[i]))
        place = results[idx]
    elif query:
        st.warning("No matching city found.")

    if st.session_state.favs:
        fav = st.selectbox("⭐ Favorites", ["—"] + list(st.session_state.favs))
        if fav != "—":
            place = st.session_state.favs[fav]

    if place and st.button("⭐ Save this city", width="stretch"):
        st.session_state.favs[label_of(place)] = place
        st.rerun()

if not place:
    st.markdown('<div class="title">Weather Intelligence</div>', unsafe_allow_html=True)
    st.info("Search for a city in the sidebar to begin.")
    st.stop()

# -------------------------------------------------------------- fetch data
try:
    with st.spinner("Fetching live weather..."):
        data = get_forecast(place["latitude"], place["longitude"])
except requests.RequestException:
    st.error("Couldn't fetch the forecast. Please try again shortly.")
    st.stop()

air = get_air(place["latitude"], place["longitude"])
cur, h, past, fut, full = prep(data)
today = fut.iloc[0]
emoji, cond, cat = wmo(cur["weather_code"])
hero_key = ("clear_day" if cur["is_day"] else "clear_night") if cat == "clear" else cat

# ------------------------------------------------------------------ header
st.markdown('<div class="title">Weather Intelligence</div>'
            '<div class="subtitle">Live conditions, smart insights and planning for any city.</div>',
            unsafe_allow_html=True)

st.markdown(f"""
<div class="hero" style="background:{HERO_GRADIENTS[hero_key]}">
  <div>
    <div class="city">📍 {label_of(place)}</div>
    <div class="temp">{T(cur['temperature_2m']):.0f}{TU}</div>
    <div class="cond">{emoji} {cond}</div>
    <div class="sub">Feels like {T(cur['apparent_temperature']):.0f}{TU} · High {T(today['temperature_2m_max']):.0f}° · Low {T(today['temperature_2m_min']):.0f}°</div>
  </div>
  <div class="big">{emoji}</div>
</div>""", unsafe_allow_html=True)

# ----------------------------------------------------------- derived values
comfort = float(np.clip(100 - abs(cur["apparent_temperature"] - 22) * 3
                        - max(0, cur["relative_humidity_2m"] - 60) * 0.5
                        - max(0, cur["wind_speed_10m"] - 20) * 1.5, 0, 100))
comfort_label = "Excellent" if comfort >= 80 else "Comfortable" if comfort >= 60 else "Fair" if comfort >= 40 else "Harsh"
compass = COMPASS[round(cur["wind_direction_10m"] / 22.5) % 16]
daylight = (today["sunset"] - today["sunrise"]).total_seconds() / 3600


def build_insights():
    out, tips = [], []
    feels, temp = cur["apparent_temperature"], cur["temperature_2m"]
    if feels - temp >= 3:
        out.append(("🥵", "Feels hotter than it reads. Humidity is trapping heat, so hydrate and avoid midday sun.", "warn"))
    elif temp - feels >= 4:
        out.append(("🧥", "Wind chill makes it feel colder than the thermometer says. Add a layer.", "info"))
    if cur["wind_speed_10m"] >= 30:
        out.append(("💨", f"Strong winds ({W(cur['wind_speed_10m']):.0f} {WU}). Secure loose outdoor items.", "alert"))
        tips.append("🧢 Windbreaker")

    n24 = h.head(24)
    wet = n24[n24["precipitation_probability"] >= 60]
    if not wet.empty:
        out.append(("🌧️", f"Rain likely around {wet.iloc[0]['time']:%I:%M %p} (up to {int(n24['precipitation_probability'].max())}% chance). Plan indoor backups.", "warn"))
        tips.append("☂️ Umbrella")
    elif n24["precipitation_probability"].max() < 20:
        out.append(("✅", "Next 24 hours look dry. Great for outdoor plans.", "good"))

    if today["uv_index_max"] >= 8:
        out.append(("☀️", f"Very high UV today (index {today['uv_index_max']:.0f}). Seek shade around midday.", "alert"))
        tips.append("🧴 Sunscreen")
    elif today["uv_index_max"] >= 6:
        out.append(("🕶️", f"High UV today (index {today['uv_index_max']:.0f}). Sunscreen recommended.", "warn"))
        tips.append("🧴 Sunscreen")

    if air and air.get("current", {}).get("us_aqi") is not None:
        a = air["current"]["us_aqi"]
        if a > 100:
            out.append(("😷", f"Air quality is {aqi_info(a)[0].lower()} (AQI {a:.0f}). Limit strenuous outdoor activity.", "alert" if a > 150 else "warn"))
            tips.append("😷 Mask")

    if len(past):
        diff = today["temperature_2m_max"] - past["temperature_2m_max"].mean()
        if abs(diff) >= 2:
            out.append(("📈" if diff > 0 else "📉", f"Today's high is {abs(dT(diff)):.1f}{TU} {'warmer' if diff > 0 else 'cooler'} than last week's average.", "info"))

    swing = fut["temperature_2m_max"].max() - fut["temperature_2m_min"].min()
    if swing >= 12:
        out.append(("🌡️", f"Big temperature swing this week ({dT(swing):.0f}{TU} range). Dress in layers.", "info"))
    if n24["temperature_2m"].min() < 15:
        tips.append("🧥 Light jacket")
    if n24["temperature_2m"].max() >= 32:
        tips.append("💧 Water bottle")
    return out or [("✅", "No notable weather risks right now.", "good")], tips


insights, tips = build_insights()

# -------------------------------------------------------------------- tabs
tab_over, tab_hour, tab_week, tab_air, tab_act, tab_cmp, tab_map = st.tabs(
    ["🏠 Overview", "⏱️ Hourly", "📅 7-Day", "🌬️ Air Quality", "🎯 Activity Planner", "⚖️ Compare", "🗺️ Map"])

# ---- Overview
with tab_over:
    c = st.columns(4)
    c[0].markdown(tile("Feels like", f"{T(cur['apparent_temperature']):.0f}{TU}", "Apparent temperature"), unsafe_allow_html=True)
    c[1].markdown(tile("Humidity", f"{cur['relative_humidity_2m']:.0f}%", f"Cloud cover {cur['cloud_cover']:.0f}%"), unsafe_allow_html=True)
    arrow = f'<span style="display:inline-block;transform:rotate({cur["wind_direction_10m"] + 180}deg)">↑</span>'
    c[2].markdown(tile("Wind", f"{W(cur['wind_speed_10m']):.0f} {WU}", f"{arrow} from {compass}"), unsafe_allow_html=True)
    c[3].markdown(tile("Pressure", f"{cur['pressure_msl']:.0f} hPa", "Sea level"), unsafe_allow_html=True)
    c = st.columns(4)
    c[0].markdown(tile("UV index (max)", f"{today['uv_index_max']:.0f}", "Today's peak"), unsafe_allow_html=True)
    c[1].markdown(tile("Sunrise", f"{today['sunrise']:%I:%M %p}", f"{daylight:.1f} h of daylight"), unsafe_allow_html=True)
    c[2].markdown(tile("Sunset", f"{today['sunset']:%I:%M %p}", "Local time"), unsafe_allow_html=True)
    c[3].markdown(tile("Comfort score", f"{comfort:.0f}/100", comfort_label), unsafe_allow_html=True)

    left, right = st.columns([3, 2])
    with left:
        st.markdown('<div class="section">🧠 Smart insights</div>', unsafe_allow_html=True)
        for icon, text, level in insights:
            st.markdown(f'<div class="insight {level}">{icon}&nbsp; {text}</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section">🎒 Take with you</div>', unsafe_allow_html=True)
        st.markdown("".join(f'<span class="chip">{t}</span>' for t in tips) if tips
                    else '<span class="chip">Nothing special needed 👍</span>', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(mode="gauge+number", value=cur["relative_humidity_2m"],
                                     number={"suffix": "%"}, title={"text": "Humidity"},
                                     gauge={"axis": {"range": [0, 100]}, "bar": {"color": th["accent"]},
                                            "bgcolor": "rgba(0,0,0,0)"}))
        st.plotly_chart(style_fig(fig, th, 240), width="stretch")

# ---- Hourly
h48 = h.head(48).copy()
with tab_hour:
    h48["t"] = h48["temperature_2m"].map(T)
    h48["f"] = h48["apparent_temperature"].map(T)
    h48["w"] = h48["wind_speed_10m"].map(W)
    fig = go.Figure()
    fig.add_bar(x=h48["time"], y=h48["precipitation_probability"], name="Rain %", yaxis="y2",
                marker_color="rgba(96,165,250,.40)")
    fig.add_scatter(x=h48["time"], y=h48["t"], name=f"Temp ({TU})", line=dict(color=th["accent"], width=3, shape="spline"))
    fig.add_scatter(x=h48["time"], y=h48["f"], name="Feels like", line=dict(color="#fbbf24", width=2, dash="dot", shape="spline"))
    fig.update_layout(yaxis2=dict(overlaying="y", side="right", range=[0, 100], showgrid=False, ticksuffix="%"))
    st.markdown('<div class="section">Temperature & rain probability · next 48 h</div>', unsafe_allow_html=True)
    st.plotly_chart(style_fig(fig, th, 400), width="stretch")

    c1, c2 = st.columns(2)
    fig = go.Figure(go.Scatter(x=h48["time"], y=h48["w"], fill="tozeroy", line=dict(color="#34d399", shape="spline")))
    c1.markdown(f'<div class="section">💨 Wind ({WU})</div>', unsafe_allow_html=True)
    c1.plotly_chart(style_fig(fig, th, 280), width="stretch")
    fig = go.Figure(go.Bar(x=h48["time"], y=h48["uv_index"], marker_color="#f59e0b"))
    c2.markdown('<div class="section">☀️ UV index</div>', unsafe_allow_html=True)
    c2.plotly_chart(style_fig(fig, th, 280), width="stretch")

# ---- 7-Day
with tab_week:
    cards = ""
    for _, r in fut.iterrows():
        e = wmo(r["weather_code"])[0]
        cards += (f'<div class="day"><div class="d">{r["time"]:%a %d}</div><div class="e">{e}</div>'
                  f'<div class="hi">{T(r["temperature_2m_max"]):.0f}°</div><div class="lo">{T(r["temperature_2m_min"]):.0f}°</div>'
                  f'<div class="r">💧 {r["precipitation_probability_max"]:.0f}%</div></div>')
    st.markdown(f'<div class="days">{cards}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">14-day trend · past week vs forecast</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_scatter(x=full["time"], y=full["temperature_2m_max"].map(T), name="High", line=dict(color="#f87171", shape="spline", width=3))
    fig.add_scatter(x=full["time"], y=full["temperature_2m_min"].map(T), name="Low", line=dict(color=th["accent"], shape="spline", width=3),
                    fill="tonexty", fillcolor="rgba(130,160,255,.14)")
    fig.add_shape(type="line", x0=today["time"], x1=today["time"], y0=0, y1=1, yref="paper",
                  line=dict(color=th["muted"], dash="dash"))
    fig.add_annotation(x=today["time"], y=1, yref="paper", text="Today", showarrow=False, yshift=12)
    st.plotly_chart(style_fig(fig, th, 340), width="stretch")

    table = fut[["time", "temperature_2m_max", "temperature_2m_min", "precipitation_sum",
                 "precipitation_probability_max", "uv_index_max", "wind_speed_10m_max"]].copy()
    table["time"] = table["time"].dt.strftime("%a %d %b")
    table["temperature_2m_max"] = table["temperature_2m_max"].map(T).round(1)
    table["temperature_2m_min"] = table["temperature_2m_min"].map(T).round(1)
    table["wind_speed_10m_max"] = table["wind_speed_10m_max"].map(W).round(1)
    table.columns = ["Date", f"High {TU}", f"Low {TU}", "Rain mm", "Rain %", "UV", f"Wind {WU}"]
    st.dataframe(table, hide_index=True, width="stretch")
    st.download_button("⬇️ Download forecast (CSV)", table.to_csv(index=False).encode(),
                       file_name=f"forecast_{place['name']}.csv", mime="text/csv")

# ---- Air quality
with tab_air:
    if not air or air.get("current", {}).get("us_aqi") is None:
        st.info("Air quality data isn't available for this location.")
    else:
        a = air["current"]
        label, color = aqi_info(a["us_aqi"])
        c1, c2 = st.columns([2, 3])
        with c1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=a["us_aqi"], title={"text": f"US AQI · {label}"},
                                         gauge={"axis": {"range": [0, 300]}, "bar": {"color": color},
                                                "bgcolor": "rgba(0,0,0,0)",
                                                "steps": [{"range": [0, 50], "color": "rgba(52,211,153,.18)"},
                                                          {"range": [50, 100], "color": "rgba(251,191,36,.18)"},
                                                          {"range": [100, 150], "color": "rgba(251,146,60,.18)"},
                                                          {"range": [150, 200], "color": "rgba(248,113,113,.18)"},
                                                          {"range": [200, 300], "color": "rgba(168,85,247,.18)"}]}))
            st.plotly_chart(style_fig(fig, th, 320), width="stretch")
        with c2:
            cc = st.columns(3)
            for i, (k, name) in enumerate([("pm2_5", "PM2.5"), ("pm10", "PM10"), ("ozone", "Ozone"),
                                           ("nitrogen_dioxide", "NO₂"), ("sulphur_dioxide", "SO₂"),
                                           ("carbon_monoxide", "CO")]):
                v = a.get(k)
                cc[i % 3].markdown(tile(name, "–" if v is None else f"{v:.0f}", "µg/m³"), unsafe_allow_html=True)
        ah = pd.DataFrame(air["hourly"])
        ah["time"] = pd.to_datetime(ah["time"])
        fig = go.Figure(go.Scatter(x=ah["time"], y=ah["us_aqi"], fill="tozeroy", line=dict(color=color, shape="spline")))
        st.markdown('<div class="section">AQI forecast · next 48 h</div>', unsafe_allow_html=True)
        st.plotly_chart(style_fig(fig, th, 280), width="stretch")

# ---- Activity planner
with tab_act:
    st.markdown('<div class="section">Best time for your plans · next 24 h</div>', unsafe_allow_html=True)
    h24 = h.head(24)
    mat = activity_matrix(h24)
    cols = st.columns(len(ACTIVITIES))
    for col, (name, row) in zip(cols, mat.iterrows()):
        best = row.idxmax()
        col.markdown(tile(name, f"{row.max():.0f}/100", f"Best at {best:%I %p}"), unsafe_allow_html=True)
    fig = go.Figure(go.Heatmap(z=mat.values, x=h24["time"].dt.strftime("%I %p"), y=mat.index, zmin=0, zmax=100,
                               colorscale="RdYlGn", colorbar=dict(title="Score")))
    st.plotly_chart(style_fig(fig, th, 340), width="stretch")
    st.caption("Scores combine feels-like temperature, rain chance, wind, UV and daylight for each activity.")

# ---- Compare
with tab_cmp:
    st.markdown('<div class="section">Compare cities · next 48 h</div>', unsafe_allow_html=True)
    extra = st.text_input("Cities to compare (comma separated)", "Mumbai, Delhi")
    cities = [(label_of(place), place)]
    for name in [x.strip() for x in extra.split(",") if x.strip()][:3]:
        try:
            res = geocode(name)
        except requests.RequestException:
            res = []
        if res:
            cities.append((label_of(res[0]), res[0]))
        else:
            st.warning(f"Couldn't find '{name}'.")
    fig, rows = go.Figure(), []
    for lbl, p in cities:
        try:
            cd = get_forecast(p["latitude"], p["longitude"])
        except requests.RequestException:
            st.warning(f"Couldn't load {lbl}.")
            continue
        ccur, ch, _, cfut, _ = prep(cd)
        c48 = ch.head(48)
        fig.add_scatter(x=c48["time"], y=c48["temperature_2m"].map(T), name=lbl.split(",")[0], line=dict(shape="spline", width=3))
        rows.append({"City": lbl, f"Now {TU}": round(T(ccur["temperature_2m"]), 1),
                     f"High {TU}": round(T(cfut.iloc[0]["temperature_2m_max"]), 1),
                     f"Low {TU}": round(T(cfut.iloc[0]["temperature_2m_min"]), 1),
                     "Rain %": cfut.iloc[0]["precipitation_probability_max"],
                     "Condition": " ".join(wmo(ccur["weather_code"])[:2])})
    st.plotly_chart(style_fig(fig, th, 380), width="stretch")
    if rows:
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

# ---- Map
with tab_map:
    st.map(pd.DataFrame({"lat": [place["latitude"]], "lon": [place["longitude"]]}), zoom=8)
    c = st.columns(3)
    c[0].markdown(tile("Coordinates", f"{place['latitude']:.2f}, {place['longitude']:.2f}"), unsafe_allow_html=True)
    c[1].markdown(tile("Elevation", f"{data.get('elevation', 0):.0f} m"), unsafe_allow_html=True)
    c[2].markdown(tile("Timezone", data.get("timezone", "–")), unsafe_allow_html=True)

st.caption("Data: Open-Meteo · Built with Streamlit")

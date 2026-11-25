"""Deterministic API world, 20 recurring procedures, and API drift."""

import copy

CITIES = {
    "Paris": dict(temp_c=12.5, humidity=71, millions=2.1, utc_offset=1, lat=48.9, lon=2.4),
    "Lima": dict(temp_c=19.0, humidity=80, millions=10.7, utc_offset=-5, lat=-12.0, lon=-77.0),
    "Tokyo": dict(temp_c=16.4, humidity=60, millions=14.0, utc_offset=9, lat=35.7, lon=139.7),
    "Cairo": dict(temp_c=24.8, humidity=40, millions=9.5, utc_offset=2, lat=30.0, lon=31.2),
    "Oslo": dict(temp_c=4.2, humidity=75, millions=0.7, utc_offset=1, lat=59.9, lon=10.8),
    "Perth": dict(temp_c=21.3, humidity=50, millions=2.1, utc_offset=8, lat=-31.9, lon=115.9),
}
DIST = {("Paris", "Lima"): 10230.0, ("Paris", "Tokyo"): 9710.0, ("Paris", "Cairo"): 3210.0,
        ("Paris", "Oslo"): 1340.0, ("Paris", "Perth"): 14250.0, ("Lima", "Tokyo"): 15490.0,
        ("Lima", "Cairo"): 12350.0, ("Lima", "Oslo"): 11000.0, ("Lima", "Perth"): 14100.0,
        ("Tokyo", "Cairo"): 9560.0, ("Tokyo", "Oslo"): 8410.0, ("Tokyo", "Perth"): 7920.0,
        ("Cairo", "Oslo"): 3620.0, ("Cairo", "Perth"): 11250.0, ("Oslo", "Perth"): 13400.0}
USERS = {
    "u1": dict(email="ana@mail.com", age=34, city="Paris"),
    "u2": dict(email="bo@corp.io", age=19, city="Oslo"),
    "u3": dict(email="chen@uni.edu", age=45, city="Tokyo"),
    "u4": dict(email="dia@shop.net", age=28, city="Cairo"),
    "u5": dict(email="eli@mail.com", age=61, city="Lima"),
    "u6": dict(email="fay@corp.io", age=23, city="Perth"),
}
PRODUCTS = {
    "p1": dict(usd=12.99, units=140, kg=0.4, category="books"),
    "p2": dict(usd=249.0, units=18, kg=3.2, category="electronics"),
    "p3": dict(usd=5.49, units=600, kg=0.1, category="grocery"),
    "p4": dict(usd=89.9, units=37, kg=1.5, category="garden"),
    "p5": dict(usd=19.5, units=75, kg=0.8, category="toys"),
    "p6": dict(usd=1200.0, units=9, kg=12.0, category="furniture"),
}
ORDERS = {
    "o1": dict(items=[["p1", 2], ["p3", 5]], status="shipped", user_id="u2"),
    "o2": dict(items=[["p2", 1]], status="pending", user_id="u1"),
    "o3": dict(items=[["p5", 3], ["p1", 1], ["p4", 1]], status="delivered", user_id="u4"),
    "o4": dict(items=[["p6", 1], ["p5", 2]], status="cancelled", user_id="u3"),
    "o5": dict(items=[["p3", 10], ["p2", 2]], status="delivered", user_id="u6"),
    "o6": dict(items=[["p4", 2], ["p6", 1]], status="shipped", user_id="u5"),
}
FX = {"EUR": 0.92, "JPY": 151.3, "INR": 83.2, "GBP": 0.79}
TICKERS = {"ACME": 41.25, "GLOBX": 312.8, "NOVA": 7.65, "ZENT": 128.4}
HOLIDAYS = {"FR": 11, "JP": 16, "IN": 21, "US": 10}
WORDS = {"cat": "chat", "house": "maison", "water": "eau", "bread": "pain", "tree": "arbre", "sun": "soleil"}
DOCS = {"d1": 1840, "d2": 560, "d3": 7300, "d4": 2950}


def _dist(a, b):
    return DIST.get((a, b)) or DIST[(b, a)]


# name, args, v1 doc, impl, main key, breaking (new fn name, new key), silent transform.
SPECS = [
    ("weather", ["city"], "{'temp_c': float, 'humidity': int}  # current temperature in Celsius",
     lambda city: {"temp_c": CITIES[city]["temp_c"], "humidity": CITIES[city]["humidity"]},
     "temp_c", ("weather_v2", "temperature_c"), lambda v: round(v * 9 / 5 + 32, 2)),
    ("population", ["city"], "{'millions': float}  # city population in millions",
     lambda city: {"millions": CITIES[city]["millions"]},
     "millions", ("city_population", "count_millions"), lambda v: v * 1000),
    ("timezone", ["city"], "{'utc_offset': int}  # hours ahead of UTC",
     lambda city: {"utc_offset": CITIES[city]["utc_offset"]},
     "utc_offset", ("tz_info", "offset_hours"), lambda v: -v),
    ("coords", ["city"], "{'lat': float, 'lon': float}  # latitude and longitude in degrees",
     lambda city: {"lat": CITIES[city]["lat"], "lon": CITIES[city]["lon"]},
     "lat", ("geo_lookup", "latitude"), lambda v: -v),
    ("user_email", ["user_id"], "{'email': str}  # the user's email address",
     lambda user_id: {"email": USERS[user_id]["email"]},
     "email", ("get_contact", "email_address"), lambda v: v.upper()),
    ("user_age", ["user_id"], "{'age': int}  # the user's age in years",
     lambda user_id: {"age": USERS[user_id]["age"]},
     "age", ("user_profile", "age_years"), lambda v: 2026 - v),
    ("user_city", ["user_id"], "{'city': str}  # the user's home city",
     lambda user_id: {"city": USERS[user_id]["city"]},
     "city", ("user_location", "city_name"), lambda v: v.lower()[:3]),
    ("price", ["product_id"], "{'usd': float}  # list price in US dollars",
     lambda product_id: {"usd": PRODUCTS[product_id]["usd"]},
     "usd", ("get_price", "amount_usd"), lambda v: round(v * 100)),
    ("stock", ["product_id"], "{'units': int}  # units in the warehouse",
     lambda product_id: {"units": PRODUCTS[product_id]["units"]},
     "units", ("inventory", "quantity"), lambda v: v // 12),
    ("weight", ["product_id"], "{'kg': float}  # shipping weight in kilograms",
     lambda product_id: {"kg": PRODUCTS[product_id]["kg"]},
     "kg", ("shipping_weight", "weight_kg"), lambda v: v * 1000),
    ("category", ["product_id"], "{'category': str}  # product category",
     lambda product_id: {"category": PRODUCTS[product_id]["category"]},
     "category", ("product_category", "cat"), lambda v: "cat_" + v),
    ("order_items", ["order_id"], "{'items': list}  # list of [product_id, quantity] pairs in cart order",
     lambda order_id: {"items": copy.deepcopy(ORDERS[order_id]["items"])},
     "items", ("order_lines", "lines"), lambda v: v[::-1]),
    ("order_status", ["order_id"], "{'status': str}  # one of pending, shipped, delivered, cancelled",
     lambda order_id: {"status": ORDERS[order_id]["status"]},
     "status", ("get_order_state", "state"), lambda v: v[:3]),
    ("order_user", ["order_id"], "{'user_id': str}  # id of the user who placed the order",
     lambda order_id: {"user_id": ORDERS[order_id]["user_id"]},
     "user_id", ("order_owner", "owner_id"), lambda v: v.upper()),
    ("exchange_rate", ["currency"], "{'per_usd': float}  # units of currency per 1 USD",
     lambda currency: {"per_usd": FX[currency]},
     "per_usd", ("fx_rate", "rate"), lambda v: round(1 / v, 6)),
    ("stock_price", ["ticker"], "{'close': float}  # last closing price in USD",
     lambda ticker: {"close": TICKERS[ticker]},
     "close", ("quote", "last_close"), lambda v: round(v * 100)),
    ("holiday_count", ["country"], "{'days': int}  # public holidays per year",
     lambda country: {"days": HOLIDAYS[country]},
     "days", ("public_holidays", "n_days"), lambda v: v * 8),
    ("distance", ["city_a", "city_b"], "{'km': float}  # great-circle distance in kilometres",
     lambda city_a, city_b: {"km": _dist(city_a, city_b)},
     "km", ("route_distance", "distance_km"), lambda v: round(v * 0.621371, 1)),
    ("translate", ["word"], "{'fr': str}  # French translation, lowercase",
     lambda word: {"fr": WORDS[word]},
     "fr", ("translate_v2", "translation"), lambda v: "le " + v),
    ("word_count", ["doc_id"], "{'words': int}  # number of words in the document",
     lambda doc_id: {"words": DOCS[doc_id]},
     "words", ("doc_stats", "n_words"), lambda v: v / 100),
]
API_NAMES = [s[0] for s in SPECS]


class Api:
    """The live API. `drift` maps API name -> 'breaking' | 'silent'."""

    def __init__(self, drift=None):
        drift = drift or {}
        for name, args, _doc, impl, key, (new_name, new_key), silent in SPECS:
            kind = drift.get(name)
            if kind == "breaking":
                setattr(self, new_name, _renamed(impl, key, new_key))
            elif kind == "silent":
                setattr(self, name, _silent(impl, key, silent))
            else:
                setattr(self, name, impl)


def _renamed(impl, key, new_key):
    def f(*a, **k):
        out = impl(*a, **k)
        out[new_key] = out.pop(key)
        if new_key == "latitude":
            out["longitude"] = out.pop("lon")
        return out
    return f


def _silent(impl, key, transform):
    def f(*a, **k):
        out = impl(*a, **k)
        out[key] = transform(out[key])
        return out
    return f


def docs(drift=None):
    """Signatures the agent sees. Breaking drift is documented; silent drift is not."""
    drift = drift or {}
    lines = []
    for name, args, doc, _impl, key, (new_name, new_key), _ in SPECS:
        if drift.get(name) == "breaking":
            doc = doc.replace(f"'{key}'", f"'{new_key}'").replace("'lon'", "'longitude'")
            name = new_name
        lines.append(f"api.{name}({', '.join(args)}) -> {doc}")
    return "\n".join(lines)


# Procedures: one per API. Each: api, args pool, lesson text, canonical tool code, test inputs.
C = list(CITIES)
PAIRS = [dict(city_a=a, city_b=b) for a, b in DIST]
PROCS = [
    dict(api="weather", inputs=[dict(city=c) for c in C],
         lesson="Report the current temperature in Fahrenheit: call api.weather(city), read the 'temp_c' field (Celsius), convert with F = C * 9 / 5 + 32, round to 1 decimal and return the number.",
         tool="def proc(api, city):\n    c = api.weather(city)['temp_c']\n    return round(c * 9 / 5 + 32, 1)\n"),
    dict(api="population", inputs=[dict(city=c) for c in C],
         lesson="Report the population of a city as a whole number of people: call api.population(city), read 'millions', multiply by 1,000,000 and return it as an int (round first).",
         tool="def proc(api, city):\n    m = api.population(city)['millions']\n    return int(round(m * 1000000))\n"),
    dict(api="timezone", inputs=[dict(city=c) for c in C],
         lesson="Report the local hour in the city when it is 12:00 UTC: call api.timezone(city), read 'utc_offset' (hours ahead of UTC) and return (12 + offset) % 24 as an int.",
         tool="def proc(api, city):\n    off = api.timezone(city)['utc_offset']\n    return (12 + off) % 24\n"),
    dict(api="coords", inputs=[dict(city=c) for c in C],
         lesson="Report the hemisphere of a city: call api.coords(city), read 'lat'; return the string 'north' if lat > 0 else 'south'.",
         tool="def proc(api, city):\n    lat = api.coords(city)['lat']\n    return 'north' if lat > 0 else 'south'\n"),
    dict(api="user_email", inputs=[dict(user_id=u) for u in USERS],
         lesson="Report a user's email domain: call api.user_email(user_id), read 'email', and return the part after the '@' exactly as written.",
         tool="def proc(api, user_id):\n    email = api.user_email(user_id)['email']\n    return email.split('@')[1]\n"),
    dict(api="user_age", inputs=[dict(user_id=u) for u in USERS],
         lesson="Report a user's age in months: call api.user_age(user_id), read 'age' (years) and return age * 12 as an int.",
         tool="def proc(api, user_id):\n    return api.user_age(user_id)['age'] * 12\n"),
    dict(api="user_city", inputs=[dict(user_id=u) for u in USERS],
         lesson="Report the greeting for a user's city: call api.user_city(user_id), read 'city' and return the string 'Hello from ' + city.",
         tool="def proc(api, user_id):\n    return 'Hello from ' + api.user_city(user_id)['city']\n"),
    dict(api="price", inputs=[dict(product_id=p) for p in PRODUCTS],
         lesson="Report a product's price including 10% tax: call api.price(product_id), read 'usd' (dollars), multiply by 1.1, round to 2 decimals and return the number.",
         tool="def proc(api, product_id):\n    return round(api.price(product_id)['usd'] * 1.1, 2)\n"),
    dict(api="stock", inputs=[dict(product_id=p) for p in PRODUCTS],
         lesson="Report how many full dozens of a product are in stock: call api.stock(product_id), read 'units' and return units // 12.",
         tool="def proc(api, product_id):\n    return api.stock(product_id)['units'] // 12\n"),
    dict(api="weight", inputs=[dict(product_id=p) for p in PRODUCTS],
         lesson="Report the shipping cost of a product: call api.weight(product_id), read 'kg' (kilograms) and return round(5 + 2 * kg, 2).",
         tool="def proc(api, product_id):\n    kg = api.weight(product_id)['kg']\n    return round(5 + 2 * kg, 2)\n"),
    dict(api="category", inputs=[dict(product_id=p) for p in PRODUCTS],
         lesson="Report the shelf label of a product: call api.category(product_id), read 'category' and return it in upper case.",
         tool="def proc(api, product_id):\n    return api.category(product_id)['category'].upper()\n"),
    dict(api="order_items", inputs=[dict(order_id=o) for o in ORDERS],
         lesson="Report the first product added to an order: call api.order_items(order_id), read 'items' (a list of [product_id, quantity] pairs in cart order) and return the product_id of the first pair.",
         tool="def proc(api, order_id):\n    return api.order_items(order_id)['items'][0][0]\n"),
    dict(api="order_status", inputs=[dict(order_id=o) for o in ORDERS],
         lesson="Report whether an order has left the warehouse: call api.order_status(order_id), read 'status' and return True if it is 'shipped' or 'delivered', otherwise False.",
         tool="def proc(api, order_id):\n    return api.order_status(order_id)['status'] in ('shipped', 'delivered')\n"),
    dict(api="order_user", inputs=[dict(order_id=o) for o in ORDERS],
         lesson="Report the customer reference for an order: call api.order_user(order_id), read 'user_id' and return the string 'CUST-' + user_id.",
         tool="def proc(api, order_id):\n    return 'CUST-' + api.order_user(order_id)['user_id']\n"),
    dict(api="exchange_rate", inputs=[dict(currency=c) for c in FX],
         lesson="Report what 100 USD is worth in a currency: call api.exchange_rate(currency), read 'per_usd' (units per 1 USD), return round(100 * per_usd, 2).",
         tool="def proc(api, currency):\n    return round(100 * api.exchange_rate(currency)['per_usd'], 2)\n"),
    dict(api="stock_price", inputs=[dict(ticker=t) for t in TICKERS],
         lesson="Report the value of 10 shares: call api.stock_price(ticker), read 'close' (USD per share) and return round(10 * close, 2).",
         tool="def proc(api, ticker):\n    return round(10 * api.stock_price(ticker)['close'], 2)\n"),
    dict(api="holiday_count", inputs=[dict(country=c) for c in HOLIDAYS],
         lesson="Report the paid holiday hours per year in a country: call api.holiday_count(country), read 'days' and return days * 8.",
         tool="def proc(api, country):\n    return api.holiday_count(country)['days'] * 8\n"),
    dict(api="distance", inputs=PAIRS,
         lesson="Report the driving time in hours between two cities at 80 km/h: call api.distance(city_a, city_b), read 'km' and return round(km / 80, 1).",
         tool="def proc(api, city_a, city_b):\n    return round(api.distance(city_a, city_b)['km'] / 80, 1)\n"),
    dict(api="translate", inputs=[dict(word=w) for w in WORDS],
         lesson="Report the French word for a label: call api.translate(word), read 'fr' and return it with the first letter capitalized (str.capitalize()).",
         tool="def proc(api, word):\n    return api.translate(word)['fr'].capitalize()\n"),
    dict(api="word_count", inputs=[dict(doc_id=d) for d in DOCS],
         lesson="Report the reading time of a document in minutes: call api.word_count(doc_id), read 'words' and return round(words / 200, 1).",
         tool="def proc(api, doc_id):\n    return round(api.word_count(doc_id)['words'] / 200, 1)\n"),
]
for p in PROCS:
    p["tests"] = p["inputs"][:2]
    p["episode_inputs"] = p["inputs"][2:]
    ns = {}
    exec(p["tool"], ns)
    v1 = Api()
    p["expected"] = {repr(sorted(i.items())): ns["proc"](v1, **i) for i in p["inputs"]}


def expected(proc, inputs):
    return proc["expected"][repr(sorted(inputs.items()))]


def correct(out, want):
    if isinstance(want, bool) or isinstance(out, bool):
        return out is want or out == want and type(out) is type(want)
    if isinstance(want, (int, float)) and isinstance(out, (int, float)):
        return abs(out - want) <= 0.011 + 1e-9 * abs(want)
    return out == want

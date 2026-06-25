import json
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

# ─────────────────────────────────────────
#  CLASSES
# ─────────────────────────────────────────

class Coffee:
    def __init__(self, product_type, name, size, additions, price, date):
        self.product_type = product_type
        self.name = name
        self.size = size
        self.additions = additions
        self.price = price
        self.date = date

    def __str__(self):
        adds = ", ".join(self.additions) if self.additions else "no additions"
        return f"{self.name} ({self.size}) — {adds} — ${self.price:.2f}"


class Visit:
    def __init__(self, date, visit_type, items_looked_at, duration_minutes, note):
        self.date = date
        self.visit_type = visit_type
        self.items_looked_at = items_looked_at
        self.duration_minutes = duration_minutes
        self.note = note

    def __str__(self):
        return f"{self.date} - {self.visit_type} - {self.items_looked_at} ({self.duration_minutes} min)"



class Customer:
    def __init__(self, first_name, last_name, gender, age, marital_status,
                 has_kids, kids_count, state, home_address, work_address,
                 phone, email, job, monthly_salary, social_activities, has_car,
                 addiction_level, cups_per_day, preferred_time,
                 favorite_coffee, favorite_cake, accessory_interest):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age
        self.marital_status = marital_status
        self.has_kids = has_kids
        self.kids_count = kids_count
        self.state = state
        self.home_address = home_address
        self.work_address = work_address
        self.phone = phone
        self.email = email
        self.job = job
        self.monthly_salary = monthly_salary
        self.social_activities = social_activities
        self.has_car = has_car
        self.addiction_level = addiction_level
        self.cups_per_day = cups_per_day
        self.preferred_time = preferred_time
        self.favorite_coffee = favorite_coffee
        self.favorite_cake = favorite_cake
        self.accessory_interest = accessory_interest
        self.purchases = []
        self.visits = []

    def add_purchase(self, coffee):
        self.purchases.append(coffee)

    def add_visit(self, visit):
        self.visits.append(visit)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.age} yrs - {self.job} - {self.state}"


class CoffeeShop:
    def __init__(self, name):
        self.name = name
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def remove_customer(self, customer):
        self.customers.remove(customer)

    def find_customer(self, first_name, last_name):
        for c in self.customers:
            if c.first_name == first_name and c.last_name == last_name:
                return c
        return None

    def list_customers(self):
        for c in self.customers:
            print(c)



# ─────────────────────────────────────────
#  DATA PERSISTENCE
# ─────────────────────────────────────────



def save_data(shop, filename="data.json"):
    data = []
    for c in shop.customers:
        data.append({
            "first_name": c.first_name,
            "last_name": c.last_name,
            "gender": c.gender,
            "age": c.age,
            "marital_status": c.marital_status,
            "has_kids": c.has_kids,
            "kids_count": c.kids_count,
            "state": c.state,
            "home_address": c.home_address,
            "work_address": c.work_address,
            "phone": c.phone,
            "email": c.email,
            "job": c.job,
            "monthly_salary": c.monthly_salary,
            "social_activities": c.social_activities,
            "has_car": c.has_car,
            "addiction_level": c.addiction_level,
            "cups_per_day": c.cups_per_day,
            "preferred_time": c.preferred_time,
            "favorite_coffee": c.favorite_coffee,
            "favorite_cake": c.favorite_cake,
            "accessory_interest": c.accessory_interest,
            "purchases": [
                {"product_type": p.product_type, "name": p.name, "size": p.size,
                 "additions": p.additions, "price": p.price, "date": p.date}
                for p in c.purchases
            ],
            "visits": [
                {"date": v.date, "visit_type": v.visit_type,
                 "items_looked_at": v.items_looked_at,
                 "duration_minutes": v.duration_minutes, "note": v.note}
                for v in c.visits
            ]
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_data(filename="data.json"):
    shop = CoffeeShop("Manifestingo Coffee")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        for c in data:
            customer = Customer(
                c["first_name"], c["last_name"], c["gender"], c["age"],
                c["marital_status"], c["has_kids"], c["kids_count"],
                c["state"], c["home_address"], c["work_address"],
                c["phone"], c["email"], c["job"], c["monthly_salary"],
                c["social_activities"], c["has_car"],
                c["addiction_level"], c["cups_per_day"], c["preferred_time"],
                c["favorite_coffee"], c["favorite_cake"], c["accessory_interest"]
            )
            for p in c["purchases"]:
                customer.add_purchase(Coffee(
                    p["product_type"], p["name"], p["size"],
                    p["additions"], p["price"], p["date"]
                ))
            for v in c["visits"]:
                customer.add_visit(Visit(
                    v["date"], v["visit_type"], v["items_looked_at"],
                    v["duration_minutes"], v["note"]
                ))
            shop.add_customer(customer)
    except FileNotFoundError:
        pass
    return shop



# ─────────────────────────────────────────
#  AI PREDICTION ENGINE
# ─────────────────────────────────────────



ALL_COFFEES = ["Espresso", "Americano", "Latte", "Cappuccino", "Flat White",
               "Cortado", "Mocha", "Cold Brew", "Pour Over", "Chemex",
               "Ristretto", "Macchiato", "Caramel Macchiato", "Iced Latte",
               "Drip Coffee", "Turkish Coffee", "Affogato", "Irish Coffee"]

ALL_CAKES = ["Croissant", "Blueberry Muffin", "Chocolate Cake", "Cheesecake",
             "Banana Bread", "Cinnamon Roll", "Brownie", "Carrot Cake",
             "Lemon Tart", "Scone"]


def predict_customer(customer):
    score = 0
    reasons = []

    if customer.addiction_level == "Addict":
        score += 35
        reasons.append(f"coffee addict — drinks {customer.cups_per_day} cups/day")
    elif customer.addiction_level == "Regular":
        score += 20
        reasons.append(f"regular drinker — {customer.cups_per_day} cups/day")
    else:
        score += 5
        reasons.append(f"casual drinker — {customer.cups_per_day} cups/day")

    if len(customer.visits) >= 15:
        score += 25
        reasons.append("very frequent visitor")
    elif len(customer.visits) >= 8:
        score += 15
        reasons.append("regular visitor")
    elif len(customer.visits) >= 3:
        score += 8
        reasons.append("occasional visitor")

    if customer.visits:
        last_visit = sorted(customer.visits, key=lambda v: v.date, reverse=True)[0]
        if last_visit.visit_type == "just_looking":
            score += 15
            reasons.append("recently browsed — likely deciding")
        elif last_visit.visit_type == "accessory":
            score += 10
            reasons.append("showed interest in accessories")
        elif last_visit.visit_type == "cake":
            score += 8
            reasons.append("recently bought food items")

    if len(customer.purchases) >= 10:
        score += 20
        reasons.append(f"loyal buyer — {len(customer.purchases)} purchases")
    elif len(customer.purchases) >= 5:
        score += 12
        reasons.append(f"{len(customer.purchases)} previous purchases")

    if customer.accessory_interest == "Yes":
        score += 8
        reasons.append("interested in accessories")

    if customer.monthly_salary >= 10000:
        segment = "premium"
        score += 10
        reasons.append("high income — premium products suitable")
    elif customer.monthly_salary >= 5000:
        segment = "mid"
        score += 6
        reasons.append("mid income")
    else:
        segment = "budget"
        score += 3
        reasons.append("budget segment")

    if customer.preferred_time == "All Day":
        score += 10
        reasons.append("drinks coffee all day long")

    likelihood = min(score, 100)


    # Coffee probability distribution


    coffee_counts = {}
    for p in customer.purchases:
        if p.product_type == "coffee":
            coffee_counts[p.name] = coffee_counts.get(p.name, 0) + 1

    total_coffee_purchases = sum(coffee_counts.values())
    base_weights = {}
    for coffee in ALL_COFFEES:
        history_weight = (coffee_counts.get(coffee, 0) / total_coffee_purchases * 70
                          if total_coffee_purchases > 0 else 0)
        favorite_bonus = 20 if coffee == customer.favorite_coffee else 0
        base = 10 / len(ALL_COFFEES)
        base_weights[coffee] = history_weight + favorite_bonus + base

    total_w = sum(base_weights.values())
    coffee_probs = {k: round((v / total_w) * 100, 1) for k, v in base_weights.items()}
    sorted_coffees = sorted(coffee_probs.items(), key=lambda x: x[1], reverse=True)
    top_coffees = sorted_coffees[:4]
    other_pct = round(sum(v for _, v in sorted_coffees[4:]), 1)
    if other_pct > 0:
        top_coffees.append(("Other Drinks", other_pct))
    top_sum = sum(v for _, v in top_coffees)
    if top_coffees:
        top_coffees[0] = (top_coffees[0][0], round(top_coffees[0][1] + (100 - top_sum), 1))


    # Cake probability


    cake_purchases = sum(1 for p in customer.purchases if p.product_type == "cake")
    total_visits_cnt = max(len(customer.visits), 1)
    cake_rate = cake_purchases / total_visits_cnt
    if customer.favorite_cake != "None":
        cake_rate += 0.15
    if customer.addiction_level == "Addict":
        cake_rate += 0.1
    if customer.has_kids:
        cake_rate += 0.1
    cake_prob = min(round(cake_rate * 100), 90)
    fav_cake = customer.favorite_cake if customer.favorite_cake != "None" else "any cake"



    # Accessory probability


    acc_purchases = sum(1 for p in customer.purchases if p.product_type == "accessory")
    acc_prob = min(round((acc_purchases / total_visits_cnt) * 100 +
                         (20 if customer.accessory_interest == "Yes" else 0)), 80)

    if likelihood >= 70:
        status = f"🔴  {likelihood}% chance of buying coffee"
        status_color = "#ff4d6d"
    elif likelihood >= 50:
        status = f"🟡  {likelihood}% chance of buying coffee"
        status_color = "#ffb347"
    elif likelihood >= 30:
        status = f"🟢  {likelihood}% chance of buying coffee"
        status_color = "#69db7c"
    else:
        status = f"⚪  {likelihood}% chance of buying coffee"
        status_color = "#666666"

    return {
        "customer": f"{customer.first_name} {customer.last_name}",
        "likelihood": likelihood,
        "top_coffees": top_coffees,
        "cake_prob": cake_prob,
        "fav_cake": fav_cake,
        "acc_prob": acc_prob,
        "reasons": reasons,
        "segment": segment,
        "status": status,
        "status_color": status_color
    }




# ─────────────────────────────────────────
#  MOCK DATA GENERATOR
# ─────────────────────────────────────────



def generate_mock_data():
    random.seed(42)
    shop = CoffeeShop("Manifestingo Coffee")

    first_names_m = ["James","Robert","Michael","William","David","Richard","Joseph",
                     "Thomas","Charles","Daniel","Matthew","Anthony","Mark","Donald",
                     "Steven","Paul","Andrew","Joshua","Kevin","Brian","George",
                     "Edward","Ronald","Timothy","Jason","Jeffrey","Ryan","Jacob",
                     "Gary","Nicholas","Eric","Jonathan","Stephen","Larry","Justin",
                     "Scott","Brandon","Benjamin","Samuel","Frank","Gregory","Raymond",
                     "Alexander","Patrick","Jack","Dennis","Jerry","Tyler","Aaron","Henry"]
    first_names_f = ["Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth",
                     "Susan","Jessica","Sarah","Karen","Lisa","Nancy","Betty",
                     "Margaret","Sandra","Ashley","Dorothy","Kimberly","Emily",
                     "Donna","Michelle","Carol","Amanda","Melissa","Deborah",
                     "Stephanie","Rebecca","Sharon","Laura","Cynthia","Kathleen",
                     "Amy","Angela","Shirley","Anna","Brenda","Pamela","Emma",
                     "Nicole","Helen","Samantha","Katherine","Christine","Olivia",
                     "Hannah","Megan","Rachel","Brittany","Kayla","Alexis"]
    last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller",
                  "Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez",
                  "Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
                  "Lee","Perez","Thompson","White","Harris","Sanchez","Clark",
                  "Ramirez","Lewis","Robinson","Walker","Young","Allen","King",
                  "Wright","Scott","Torres","Nguyen","Hill","Flores","Green",
                  "Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell",
                  "Carter","Roberts","Phillips","Evans","Turner","Parker","Collins"]
    states = ["California","Texas","New York","Florida","Illinois","Pennsylvania",
              "Ohio","Georgia","North Carolina","Michigan","New Jersey","Virginia",
              "Washington","Arizona","Massachusetts","Tennessee","Indiana","Missouri",
              "Maryland","Wisconsin","Colorado","Minnesota","South Carolina",
              "Alabama","Louisiana","Kentucky","Oregon","Oklahoma","Connecticut","Nevada"]
    jobs = ["Software Engineer","Teacher","Nurse","Marketing Manager","Accountant",
            "Graphic Designer","Sales Representative","Doctor","Attorney",
            "Business Owner","Architect","Journalist","Financial Analyst",
            "Pharmacist","Professor","Chef","Real Estate Agent","Electrician",
            "Plumber","Mechanic","Police Officer","Firefighter","Social Worker",
            "Dentist","Veterinarian","Photographer","Writer","Consultant",
            "Project Manager","Data Analyst","Student","Barista","Retail Worker"]
    social_opts = ["Reading","Art","Photography","Music","Travel","Yoga","Fitness",
                   "Cycling","Hiking","Gaming","Cooking","Golf","Sailing","Cinema","Writing"]
    cakes = ALL_CAKES + ["None"]
    additions_pool = ["Extra Shot","Oat Milk","Almond Milk","Soy Milk","Vanilla Syrup",
                      "Caramel Drizzle","Cinnamon","Whipped Cream","No Sugar","Hazelnut Syrup"]
    accessories = ["Ceramic Mug","Travel Tumbler","French Press","Coffee Bean Bag 500g",
                   "Coffee Bean Bag 1kg","Designer Mug Set","Espresso Cup Set",
                   "Coffee Grinder","AeroPress","Chemex Kit"]
    visit_notes = ["Quick morning stop","Stayed to work remotely","First visit, loved the vibe",
                   "Regular morning visit","Came in with a friend","Study session",
                   "Business meeting","Just passing by","Checked seasonal menu",
                   "Tried a new drink","Bought gift for someone","Long afternoon visit"]

    addiction_levels = ["Casual","Regular","Addict"]
    addiction_weights = [0.3, 0.45, 0.25]
    cups_map = {"Casual":["1","2"],"Regular":["2","3"],"Addict":["4","5","6+"]}
    times = ["Morning","Afternoon","Evening","All Day"]
    time_weights_map = {
        "Casual":[0.4,0.3,0.2,0.1],
        "Regular":[0.35,0.25,0.15,0.25],
        "Addict":[0.2,0.15,0.1,0.55]
    }

    for i in range(250):
        gender = random.choice(["Male","Female"])
        first_name = random.choice(first_names_m if gender == "Male" else first_names_f)
        last_name = random.choice(last_names)
        age = random.randint(18, 65)
        marital = random.choice(["Single","Married","Divorced"])
        has_kids = random.choice([True,False])
        kids_count = random.randint(1,3) if has_kids else 0
        state = random.choice(states)
        job = random.choice(jobs)
        salary = random.randint(2000, 25000)
        activities = random.sample(social_opts, k=random.randint(1,4))
        has_car = random.choice([True,False])
        addiction = random.choices(addiction_levels, weights=addiction_weights)[0]
        cups = random.choice(cups_map[addiction])
        pref_time = random.choices(times, weights=time_weights_map[addiction])[0]
        fav_coffee = random.choice(ALL_COFFEES)
        fav_cake = random.choice(cakes)
        acc_interest = random.choice(["Yes","No"])

        street_num = random.randint(10,9999)
        street_names = ["Main St","Oak Ave","Maple Dr","Cedar Ln","Park Blvd",
                        "Lake Rd","Hill St","River Ave","Forest Dr","Sunset Blvd"]
        home_addr = f"{street_num} {random.choice(street_names)}, {state}"
        work_addr = f"{random.randint(100,9999)} Business Center, {state}"
        phone = f"+1 {random.randint(200,999)} {random.randint(100,999)} {random.randint(1000,9999)}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1,99)}@email.com"

        customer = Customer(
            first_name, last_name, gender, age, marital,
            has_kids, kids_count, state, home_addr, work_addr,
            phone, email, job, salary, activities, has_car,
            addiction, cups, pref_time, fav_coffee, fav_cake, acc_interest
        )

        num_purchases = {"Casual":random.randint(1,5),
                         "Regular":random.randint(5,15),
                         "Addict":random.randint(15,40)}[addiction]
        years = list(range(2015,2026))
        for _ in range(num_purchases):
            year = random.choice(years)
            month = random.randint(1,12)
            day = random.randint(1,28)
            date_str = f"{year}-{month:02d}-{day:02d}"
            ptype = random.choices(["coffee","cake","accessory"], weights=[0.7,0.2,0.1])[0]
            if ptype == "coffee":
                name = fav_coffee if random.random() > 0.3 else random.choice(ALL_COFFEES)
                size = random.choice(["Small","Medium","Large"])
                adds = random.sample(additions_pool, k=random.randint(0,2))
                price = round(random.uniform(3.5,8.5),2)
            elif ptype == "cake":
                name = fav_cake if fav_cake != "None" else random.choice(ALL_CAKES)
                size = "-"; adds = []; price = round(random.uniform(2.5,6.5),2)
            else:
                name = random.choice(accessories)
                size = "-"; adds = []; price = round(random.uniform(12.0,55.0),2)
            customer.add_purchase(Coffee(ptype, name, size, adds, price, date_str))

        num_visits = {"Casual":random.randint(2,8),
                      "Regular":random.randint(8,20),
                      "Addict":random.randint(20,50)}[addiction]
        visit_types = ["purchase","just_looking","accessory","cake"]
        visit_weights = [0.55,0.25,0.1,0.1]
        for _ in range(num_visits):
            year = random.choice(years)
            month = random.randint(1,12)
            day = random.randint(1,28)
            date_str = f"{year}-{month:02d}-{day:02d}"
            vtype = random.choices(visit_types, weights=visit_weights)[0]
            duration = random.randint(5,120)
            note = random.choice(visit_notes)
            items = fav_coffee if vtype == "purchase" else random.choice(ALL_COFFEES+ALL_CAKES)
            customer.add_visit(Visit(date_str, vtype, items, duration, note))

        shop.add_customer(customer)

    return shop




# ─────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────



STATES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
          "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
          "Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
          "Maine","Maryland","Massachusetts","Michigan","Minnesota",
          "Mississippi","Missouri","Montana","Nebraska","Nevada",
          "New Hampshire","New Jersey","New Mexico","New York",
          "North Carolina","North Dakota","Ohio","Oklahoma","Oregon",
          "Pennsylvania","Rhode Island","South Carolina","South Dakota",
          "Tennessee","Texas","Utah","Vermont","Virginia","Washington",
          "West Virginia","Wisconsin","Wyoming"]
SOCIAL_OPTIONS = ["Reading","Art","Photography","Music","Travel","Yoga","Fitness",
                  "Cycling","Hiking","Gaming","Cooking","Golf","Sailing","Cinema","Writing"]
COFFEE_TYPES = ALL_COFFEES
CAKE_TYPES   = ALL_CAKES + ["None"]
CUPS_OPTIONS = ["1","2","3","4","5","6+"]

BG      = "#0f0f0f"
SIDEBAR = "#141414"
CARD    = "#1a1a1a"
ACCENT  = "#e8c07d"
ACCENT2 = "#ffffff"
TEXT    = "#e8e8e8"
SUBTEXT = "#555555"
SEL     = "#222222"
DANGER  = "#ff4d6d"
WARN    = "#ffb347"
OK      = "#69db7c"




# ─────────────────────────────────────────
#  TKINTER UI
# ─────────────────────────────────────────



class CoffeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manifestingo Coffee — CRM")
        self.root.geometry("1280x750")
        self.root.configure(bg=BG)
        self.shop = shop
        self._setup_styles()
        self.build_ui()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=32,
                        font=("Helvetica", 9), borderwidth=0)
        style.configure("Treeview.Heading",
                        background="#1f1f1f", foreground=SUBTEXT,
                        font=("Helvetica", 8, "bold"), relief="flat")
        style.map("Treeview",
                  background=[("selected", SEL)],
                  foreground=[("selected", ACCENT)])
        style.configure("Vertical.TScrollbar",
                        background=SIDEBAR, troughcolor=BG,
                        arrowcolor="#333333", borderwidth=0, width=6)
        style.configure("TCombobox",
                        fieldbackground=SEL, background=SEL,
                        foreground=TEXT, arrowcolor=ACCENT,
                        selectbackground=SEL, selectforeground=TEXT,
                        borderwidth=0, relief="flat")
        style.map("TCombobox",
                  fieldbackground=[("readonly", SEL)],
                  foreground=[("readonly", TEXT)])

    def _btn(self, parent, text, command, bg=SEL, fg=TEXT, font_size=10, pad_x=14, pad_y=8):
        return tk.Button(parent, text=text, command=command,
                         font=("Helvetica", font_size), bg=bg, fg=fg,
                         activebackground="#2a2a2a", activeforeground=ACCENT,
                         relief="flat", bd=0, padx=pad_x, pady=pad_y, cursor="hand2")

    def _label(self, parent, text, size=10, bold=False, color=TEXT, **kwargs):
        weight = "bold" if bold else "normal"
        return tk.Label(parent, text=text, font=("Helvetica", size, weight),
                        bg=parent["bg"], fg=color, **kwargs)

    def build_ui(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Frame(self.sidebar, bg=SIDEBAR, height=32).pack()
        self._label(self.sidebar, "MANIFESTINGO", size=13, bold=True, color=ACCENT).pack(padx=20)
        self._label(self.sidebar, "COFFEE", size=8, color=SUBTEXT).pack(pady=(2,0))
        tk.Frame(self.sidebar, bg="#222222", height=1).pack(fill="x", padx=16, pady=20)

        self.nav_buttons = {}
        nav_items = [
            ("customers", "  Customers",     self.show_customers),
            ("add",       "  Add Customer",  self.show_add_customer),
            ("predict",   "  AI Prediction", self.show_predictions),
        ]
        for key, text, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=text, anchor="w",
                            font=("Helvetica", 10), bg=SIDEBAR, fg=SUBTEXT,
                            activebackground=SEL, activeforeground=TEXT,
                            relief="flat", bd=0, padx=20, pady=12,
                            cursor="hand2", command=cmd)
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.pack(side="left", fill="both", expand=True)

        topbar = tk.Frame(self.main_frame, bg=BG, height=58)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Frame(self.main_frame, bg="#1f1f1f", height=1).pack(fill="x")

        self.page_title = tk.Label(topbar, text="Customers",
                                   font=("Helvetica", 16, "bold"),
                                   bg=BG, fg=TEXT)
        self.page_title.pack(side="left", padx=28, pady=16)

        sf = tk.Frame(topbar, bg=SEL)
        sf.pack(side="right", padx=24, pady=14)
        tk.Label(sf, text="⌕", bg=SEL, fg=SUBTEXT,
                 font=("Helvetica", 12)).pack(side="left", padx=(10,4))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        tk.Entry(sf, textvariable=self.search_var, font=("Helvetica", 10),
                 bg=SEL, fg=TEXT, insertbackground=ACCENT,
                 bd=0, width=20, relief="flat").pack(side="left", padx=(0,10), ipady=6)

        self.content = tk.Frame(self.main_frame, bg=BG)
        self.content.pack(fill="both", expand=True, padx=24, pady=20)

        self.show_customers()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def reset_nav(self):
        for btn in self.nav_buttons.values():
            btn.config(bg=SIDEBAR, fg=SUBTEXT)

    def set_nav(self, key):
        self.reset_nav()
        self.nav_buttons[key].config(bg=SEL, fg=TEXT)

    def _stat_card(self, parent, label, value, color=ACCENT):
        card = tk.Frame(parent, bg=CARD, padx=20, pady=12)
        card.pack(side="left", padx=(0,8))
        tk.Label(card, text=label, font=("Helvetica",8),
                 bg=CARD, fg=SUBTEXT).pack(anchor="w")
        tk.Label(card, text=str(value), font=("Helvetica",22,"bold"),
                 bg=CARD, fg=color).pack(anchor="w")



    # ── CUSTOMERS ───────────────────────────────────



    def show_customers(self):
        self.clear_content()
        self.set_nav("customers")
        self.page_title.config(text="Customers")

        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", pady=(0,16))
        self._stat_card(stats, "Total Customers", len(self.shop.customers))
        self._stat_card(stats, "Total Purchases",
                        sum(len(c.purchases) for c in self.shop.customers))
        self._stat_card(stats, "Total Visits",
                        sum(len(c.visits) for c in self.shop.customers))
        self._stat_card(stats, "Addicts",
                        sum(1 for c in self.shop.customers if c.addiction_level=="Addict"),
                        color=DANGER)
        self._stat_card(stats, "High Priority",
                        sum(1 for c in self.shop.customers
                            if predict_customer(c)["likelihood"]>=60),
                        color=WARN)

        table_wrap = tk.Frame(self.content, bg=CARD)
        table_wrap.pack(fill="both", expand=True)

        cols = ("Full Name","Age","State","Job","Addiction","Cups/Day","Fav Coffee","Purchases","Visits")
        self.tree = ttk.Treeview(table_wrap, columns=cols, show="headings", height=20)
        widths = [155,45,115,145,85,70,135,80,60]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        self.tree.column("Full Name", anchor="w")
        self.tree.column("Fav Coffee", anchor="w")

        sb = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_customer_click)
        self.populate_table(self.shop.customers)

    def populate_table(self, customers):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for c in customers:
            self.tree.insert("", "end", values=(
                f"{c.first_name} {c.last_name}", c.age, c.state, c.job,
                c.addiction_level, c.cups_per_day, c.favorite_coffee,
                len(c.purchases), len(c.visits)
            ))

    def on_search(self, *args):
        q = self.search_var.get().lower()
        filtered = [c for c in self.shop.customers
                    if q in c.first_name.lower() or q in c.last_name.lower()
                    or q in c.state.lower() or q in c.job.lower()
                    or q in c.favorite_coffee.lower() or q in c.addiction_level.lower()]
        self.populate_table(filtered)

    def on_customer_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        q = self.search_var.get().lower()
        customers = ([c for c in self.shop.customers
                      if q in c.first_name.lower() or q in c.last_name.lower()
                      or q in c.state.lower() or q in c.job.lower()
                      or q in c.favorite_coffee.lower() or q in c.addiction_level.lower()]
                     if q else self.shop.customers)
        if idx < len(customers):
            self.show_customer_detail(customers[idx])



    # ── CUSTOMER DETAIL ─────────────────────────────


    def show_customer_detail(self, customer):
        self.clear_content()
        self.page_title.config(text=f"{customer.first_name} {customer.last_name}")

        top_row = tk.Frame(self.content, bg=BG)
        top_row.pack(fill="x", pady=(0,14))
        self._btn(top_row, "← Back", self.show_customers).pack(side="left")
        self._btn(top_row, "🗑  Delete Customer",
                  lambda: self.delete_customer(customer),
                  bg="#2a1010", fg=DANGER, font_size=9).pack(side="right")

        cols_frame = tk.Frame(self.content, bg=BG)
        cols_frame.pack(fill="both", expand=True)

        left = tk.Frame(cols_frame, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0,12))
        right = tk.Frame(cols_frame, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        pred = predict_customer(customer)

        def info_card(parent, title, rows, title_color=ACCENT):
            card = tk.Frame(parent, bg=CARD, padx=16, pady=14)
            card.pack(fill="x", pady=(0,10))
            tk.Label(card, text=title, font=("Helvetica",10,"bold"),
                     bg=CARD, fg=title_color).pack(anchor="w", pady=(0,8))
            for lbl, val, col in rows:
                r = tk.Frame(card, bg=CARD)
                r.pack(fill="x", pady=1)
                tk.Label(r, text=f"{lbl}", font=("Helvetica",8),
                         bg=CARD, fg=SUBTEXT, width=16, anchor="w").pack(side="left")
                tk.Label(r, text=val, font=("Helvetica",8), bg=CARD,
                         fg=col, anchor="w", wraplength=220).pack(side="left")

        add_col = {"Casual": OK, "Regular": WARN, "Addict": DANGER}

        info_card(left, "Personal Information", [
            ("Gender",         customer.gender,                           TEXT),
            ("Age",            str(customer.age),                         TEXT),
            ("Marital Status", customer.marital_status,                   TEXT),
            ("Children",       f"{'Yes' if customer.has_kids else 'No'} ({customer.kids_count})", TEXT),
            ("State",          customer.state,                            TEXT),
            ("Phone",          customer.phone,                            TEXT),
            ("Email",          customer.email,                            TEXT),
            ("Job",            customer.job,                              TEXT),
            ("Monthly Salary", f"${customer.monthly_salary:,}",           TEXT),
            ("Has Car",        "Yes" if customer.has_car else "No",       TEXT),
            ("Activities",     ", ".join(customer.social_activities),     TEXT),
        ])

        info_card(left, "☕  Coffee Profile", [
            ("Addiction Level", customer.addiction_level, add_col.get(customer.addiction_level, TEXT)),
            ("Cups Per Day",    customer.cups_per_day,    TEXT),
            ("Preferred Time",  customer.preferred_time,  TEXT),
            ("Favorite Coffee", customer.favorite_coffee, ACCENT),
            ("Favorite Cake",   customer.favorite_cake,   TEXT),
            ("Accessories",     customer.accessory_interest, TEXT),
        ])

        ai_card = tk.Frame(left, bg=CARD, padx=16, pady=14)
        ai_card.pack(fill="x")
        tk.Label(ai_card, text="🤖  AI Prediction", font=("Helvetica",10,"bold"),
                 bg=CARD, fg=ACCENT).pack(anchor="w", pady=(0,8))
        tk.Label(ai_card, text=pred["status"], font=("Helvetica",10,"bold"),
                 bg=CARD, fg=pred["status_color"]).pack(anchor="w")
        tk.Label(ai_card, text=f"Top recommendation: {pred['top_coffees'][0][0]} ({pred['top_coffees'][0][1]}%)",
                 font=("Helvetica",9), bg=CARD, fg=ACCENT).pack(anchor="w", pady=(4,0))

        # Right — purchases + visits
        canvas = tk.Canvas(right, bg=BG, highlightthickness=0)
        sb2 = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        pcard = tk.Frame(inner, bg=CARD, padx=14, pady=12)
        pcard.pack(fill="x", pady=(0,10))
        tk.Label(pcard, text="Purchase History", font=("Helvetica",10,"bold"),
                 bg=CARD, fg=ACCENT).pack(anchor="w", pady=(0,6))
        icons = {"coffee":"☕","cake":"🍰","accessory":"🛍️"}
        for p in sorted(customer.purchases, key=lambda x: x.date, reverse=True):
            tk.Label(pcard, text=f"{icons.get(p.product_type,'•')}  {p.date}  —  {p}",
                     font=("Helvetica",8), bg=CARD, fg=TEXT).pack(anchor="w", pady=1)

        vcard = tk.Frame(inner, bg=CARD, padx=14, pady=12)
        vcard.pack(fill="x")
        tk.Label(vcard, text="Visit History", font=("Helvetica",10,"bold"),
                 bg=CARD, fg=ACCENT).pack(anchor="w", pady=(0,6))
        vcols = {"purchase":ACCENT,"just_looking":SUBTEXT,"accessory":WARN,"cake":OK}
        for v in sorted(customer.visits, key=lambda x: x.date, reverse=True):
            col = vcols.get(v.visit_type, SUBTEXT)
            vf = tk.Frame(vcard, bg=CARD); vf.pack(fill="x", pady=2)
            tk.Label(vf, text="●", fg=col, bg=CARD, font=("Helvetica",9)).pack(side="left")
            tk.Label(vf, text=f"  {v.date}  —  {v.visit_type.replace('_',' ')}  ({v.duration_minutes} min)",
                     font=("Helvetica",8), bg=CARD, fg=TEXT).pack(side="left")
            nf = tk.Frame(vcard, bg=CARD); nf.pack(fill="x")
            tk.Label(nf, text=f"     📝 {v.note}", font=("Helvetica",8),
                     bg=CARD, fg=SUBTEXT).pack(anchor="w")

    def delete_customer(self, customer):
        if messagebox.askyesno("Delete Customer",
                               f"Delete {customer.first_name} {customer.last_name}? This cannot be undone."):
            self.shop.remove_customer(customer)
            save_data(self.shop)
            messagebox.showinfo("Deleted", "Customer removed successfully.")
            self.show_customers()




    # ── ADD CUSTOMER ────────────────────────────────



    def show_add_customer(self):
        self.clear_content()
        self.set_nav("add")
        self.page_title.config(text="Add New Customer")

        canvas = tk.Canvas(self.content, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        form = tk.Frame(canvas, bg=BG)
        form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=form, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._label(form, "New Customer Registration", size=13, bold=True).pack(anchor="w", pady=(0,16))
        self.form_vars = {}

        def field(parent, label, var_name, wtype="entry", options=None):
            row = tk.Frame(parent, bg=BG); row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=("Helvetica",9), bg=BG,
                     fg=SUBTEXT, width=20, anchor="w").pack(side="left")
            if wtype == "entry":
                var = tk.StringVar()
                tk.Entry(row, textvariable=var, font=("Helvetica",9),
                         bg=SEL, fg=TEXT, insertbackground=ACCENT,
                         bd=0, width=26, relief="flat").pack(side="left", padx=4, ipady=5)
                self.form_vars[var_name] = var
            elif wtype == "combo":
                var = tk.StringVar(value=options[0])
                ttk.Combobox(row, textvariable=var, values=options,
                             font=("Helvetica",9), width=24,
                             state="readonly").pack(side="left", padx=4)
                self.form_vars[var_name] = var

        three = tk.Frame(form, bg=BG); three.pack(fill="x")
        c1 = tk.Frame(three, bg=BG); c1.pack(side="left", fill="both", expand=True, padx=(0,16))
        c2 = tk.Frame(three, bg=BG); c2.pack(side="left", fill="both", expand=True, padx=(0,16))
        c3 = tk.Frame(three, bg=BG); c3.pack(side="left", fill="both", expand=True)

        self._label(c1, "Personal Info", size=10, bold=True, color=ACCENT).pack(anchor="w", pady=(0,6))
        field(c1,"First Name","first_name")
        field(c1,"Last Name","last_name")
        field(c1,"Gender","gender","combo",["Male","Female"])
        field(c1,"Age","age")
        field(c1,"Marital Status","marital_status","combo",["Single","Married","Divorced"])
        field(c1,"Has Kids","has_kids","combo",["No","Yes"])
        field(c1,"Number of Kids","kids_count")
        field(c1,"State","state","combo",STATES)

        self._label(c2, "Contact & Work", size=10, bold=True, color=ACCENT).pack(anchor="w", pady=(0,6))
        field(c2,"Phone","phone")
        field(c2,"Email","email")
        field(c2,"Home Address","home_address")
        field(c2,"Work Address","work_address")
        field(c2,"Job Title","job")
        field(c2,"Monthly Salary ($)","monthly_salary")
        field(c2,"Has a Car","has_car","combo",["Yes","No"])

        self._label(c3, "☕ Coffee Profile", size=10, bold=True, color=ACCENT).pack(anchor="w", pady=(0,6))
        field(c3,"Addiction Level","addiction_level","combo",["Casual","Regular","Addict"])
        field(c3,"Cups Per Day","cups_per_day","combo",CUPS_OPTIONS)
        field(c3,"Preferred Time","preferred_time","combo",["Morning","Afternoon","Evening","All Day"])
        field(c3,"Favorite Coffee","favorite_coffee","combo",COFFEE_TYPES)
        field(c3,"Favorite Cake","favorite_cake","combo",CAKE_TYPES)
        field(c3,"Accessory Interest","accessory_interest","combo",["No","Yes"])

        self._label(form, "Social Activities", size=10, bold=True, color=ACCENT).pack(anchor="w", pady=(16,6))
        self.activity_vars = {}
        af = tk.Frame(form, bg=BG); af.pack(fill="x")
        for i, act in enumerate(SOCIAL_OPTIONS):
            var = tk.BooleanVar()
            self.activity_vars[act] = var
            tk.Checkbutton(af, text=act, variable=var,
                           font=("Helvetica",9), bg=BG, fg=TEXT,
                           selectcolor=SEL, activebackground=BG,
                           activeforeground=ACCENT).grid(row=i//5, column=i%5,
                                                         sticky="w", padx=8, pady=3)

        self._btn(form, "  Save Customer  ", self.save_new_customer,
                  bg=ACCENT, fg="#0f0f0f", font_size=11,
                  pad_x=24, pad_y=10).pack(pady=20)

    def save_new_customer(self):
        try:
            fn = self.form_vars["first_name"].get().strip()
            ln = self.form_vars["last_name"].get().strip()
            if not fn or not ln:
                messagebox.showerror("Error", "First and last name are required.")
                return
            age    = int(self.form_vars["age"].get())
            salary = int(self.form_vars["monthly_salary"].get())
            kids_n = int(self.form_vars["kids_count"].get() or 0)
            has_kids = self.form_vars["has_kids"].get() == "Yes"
            has_car  = self.form_vars["has_car"].get() == "Yes"
            acts = [a for a, v in self.activity_vars.items() if v.get()]
            customer = Customer(
                fn, ln,
                self.form_vars["gender"].get(), age,
                self.form_vars["marital_status"].get(), has_kids, kids_n,
                self.form_vars["state"].get(),
                self.form_vars["home_address"].get().strip(),
                self.form_vars["work_address"].get().strip(),
                self.form_vars["phone"].get().strip(),
                self.form_vars["email"].get().strip(),
                self.form_vars["job"].get().strip(),
                salary, acts, has_car,
                self.form_vars["addiction_level"].get(),
                self.form_vars["cups_per_day"].get(),
                self.form_vars["preferred_time"].get(),
                self.form_vars["favorite_coffee"].get(),
                self.form_vars["favorite_cake"].get(),
                self.form_vars["accessory_interest"].get()
            )
            self.shop.add_customer(customer)
            save_data(self.shop)
            messagebox.showinfo("Success", f"{fn} {ln} added successfully!")
            self.show_customers()
        except ValueError:
            messagebox.showerror("Error", "Age, salary and kids count must be numbers.")



    # ── AI PREDICTION ────────────────────────────────


    def show_predictions(self):
        self.clear_content()
        self.set_nav("predict")
        self.page_title.config(text="AI Prediction")
        self.pred_page = 0
        self.pred_page_size = 20
        self.all_results = sorted(
            [predict_customer(c) for c in self.shop.customers],
            key=lambda x: x["likelihood"], reverse=True
        )

        self._label(self.content, "Purchase Probability & Product Recommendation",
                    size=13, bold=True).pack(anchor="w", pady=(0,4))
        self._label(self.content,
                    "Based on purchase history, addiction level, visit behavior and lifestyle.",
                    size=9, color=SUBTEXT).pack(anchor="w", pady=(0,10))

        nav_frame = tk.Frame(self.content, bg=BG)
        nav_frame.pack(fill="x", pady=(0,10))
        self.pred_info_label = self._label(nav_frame, "", size=9, color=SUBTEXT)
        self.pred_info_label.pack(side="left")
        self._btn(nav_frame, "Next →", self.pred_next).pack(side="right")
        self._btn(nav_frame, "← Prev", self.pred_prev).pack(side="right", padx=(0,6))

        canvas = tk.Canvas(self.content, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        self.pred_scroll_frame = tk.Frame(canvas, bg=BG)
        self.pred_scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.pred_scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self.pred_canvas = canvas
        self.render_pred_page()

    def pred_next(self):
        total_pages = (len(self.all_results) - 1) // self.pred_page_size
        if self.pred_page < total_pages:
            self.pred_page += 1
            self.render_pred_page()

    def pred_prev(self):
        if self.pred_page > 0:
            self.pred_page -= 1
            self.render_pred_page()

    def render_pred_page(self):
        for w in self.pred_scroll_frame.winfo_children():
            w.destroy()

        start = self.pred_page * self.pred_page_size
        end   = start + self.pred_page_size
        page_results = self.all_results[start:end]
        total = len(self.all_results)
        self.pred_info_label.config(
            text=f"Showing {start+1}–{min(end,total)} of {total} customers  |  Page {self.pred_page+1}"
        )
        self.pred_canvas.yview_moveto(0)

        for r in page_results:
            lh = r["likelihood"]
            bc = r["status_color"]

            card = tk.Frame(self.pred_scroll_frame, bg=CARD, padx=16, pady=14)
            card.pack(fill="x", pady=4, padx=2)

            top = tk.Frame(card, bg=CARD); top.pack(fill="x")
            tk.Label(top, text=r["customer"], font=("Helvetica",11,"bold"),
                     bg=CARD, fg=TEXT).pack(side="left")
            tk.Label(top, text=r["status"], font=("Helvetica",9,"bold"),
                     bg=CARD, fg=bc).pack(side="right", padx=4)

            bar_bg = tk.Frame(card, bg=SEL, height=4)
            bar_bg.pack(fill="x", pady=(6,4))
            bar_bg.pack_propagate(False)
            tk.Frame(bar_bg, bg=bc, height=4).place(relwidth=lh/100, relheight=1)

            body = tk.Frame(card, bg=CARD); body.pack(fill="x", pady=(4,0))
            left_b  = tk.Frame(body, bg=CARD); left_b.pack(side="left", fill="both", expand=True)
            right_b = tk.Frame(body, bg=CARD); right_b.pack(side="left", fill="both", expand=True)

            tk.Label(left_b, text="☕  What will they order?",
                     font=("Helvetica",9,"bold"), bg=CARD, fg=ACCENT).pack(anchor="w", pady=(0,4))
            max_pct = max(p for _, p in r["top_coffees"]) if r["top_coffees"] else 1
            for name, pct in r["top_coffees"]:
                rf = tk.Frame(left_b, bg=CARD); rf.pack(fill="x", pady=2)
                tk.Label(rf, text=name, font=("Helvetica",8),
                         bg=CARD, fg=TEXT, width=22, anchor="w").pack(side="left")
                bw = tk.Frame(rf, bg=SEL, width=120, height=8)
                bw.pack(side="left", padx=4); bw.pack_propagate(False)
                bar_col = ACCENT if pct == max_pct else "#333333"
                tk.Frame(bw, bg=bar_col, height=8,
                         width=max(1,int(1.2*pct))).place(x=0,y=0)
                tk.Label(rf, text=f"%{pct}", font=("Helvetica",8,"bold"),
                         bg=CARD, fg=bar_col).pack(side="left", padx=2)

            tk.Label(right_b, text="🍰  Cake alongside?",
                     font=("Helvetica",9,"bold"), bg=CARD, fg=ACCENT).pack(anchor="w", pady=(0,4))
            cake_col = OK if r["cake_prob"] >= 50 else "#333333"
            crow = tk.Frame(right_b, bg=CARD); crow.pack(fill="x", pady=2)
            tk.Label(crow, text=r["fav_cake"].capitalize(),
                     font=("Helvetica",8), bg=CARD, fg=TEXT,
                     width=20, anchor="w").pack(side="left")
            bw2 = tk.Frame(crow, bg=SEL, width=100, height=8)
            bw2.pack(side="left", padx=4); bw2.pack_propagate(False)
            tk.Frame(bw2, bg=cake_col, height=8,
                     width=max(1,int(r["cake_prob"]))).place(x=0,y=0)
            tk.Label(crow, text=f"%{r['cake_prob']}", font=("Helvetica",8,"bold"),
                     bg=CARD, fg=cake_col).pack(side="left", padx=2)

            tk.Label(right_b, text="🛍️  Accessory purchase?",
                     font=("Helvetica",9,"bold"), bg=CARD, fg=ACCENT).pack(anchor="w", pady=(8,4))
            acc_col = WARN if r["acc_prob"] >= 30 else "#333333"
            arow = tk.Frame(right_b, bg=CARD); arow.pack(fill="x", pady=2)
            tk.Label(arow, text="Accessory", font=("Helvetica",8),
                     bg=CARD, fg=TEXT, width=20, anchor="w").pack(side="left")
            bw3 = tk.Frame(arow, bg=SEL, width=100, height=8)
            bw3.pack(side="left", padx=4); bw3.pack_propagate(False)
            tk.Frame(bw3, bg=acc_col, height=8,
                     width=max(1,int(r["acc_prob"]))).place(x=0,y=0)
            tk.Label(arow, text=f"%{r['acc_prob']}", font=("Helvetica",8,"bold"),
                     bg=CARD, fg=acc_col).pack(side="left", padx=2)

            tk.Frame(card, bg=SEL, height=1).pack(fill="x", pady=(10,6))
            rrow = tk.Frame(card, bg=CARD); rrow.pack(fill="x")
            tk.Label(rrow, text="Analysis:  ", font=("Helvetica",8,"bold"),
                     bg=CARD, fg=SUBTEXT).pack(side="left", anchor="n")
            tk.Label(rrow, text="  •  ".join(r["reasons"]),
                     font=("Helvetica",8), bg=CARD, fg=SUBTEXT,
                     wraplength=700, justify="left").pack(side="left", anchor="w")




# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────



if not os.path.exists("data.json"):
    print("Generating 250 customers...")
    shop = generate_mock_data()
    save_data(shop)
    print("Done.")

shop = load_data()
print(f"Loaded {len(shop.customers)} customers.")

root = tk.Tk()
app = CoffeeApp(root)
root.mainloop()

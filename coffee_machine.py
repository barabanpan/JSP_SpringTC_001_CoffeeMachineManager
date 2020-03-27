import sqlite3

HISTORYPATH = "history.txt"
HISTORYDBNAME = 'history.sqlite'


class Beverage(object):
    """Class represents beverage with attributes:
    name, coffee (g), milk (ml), and water (ml).
    """

    def __init__(self, name, coffee, milk, water):
        self.name = name
        self.coffee = coffee
        self.milk = milk
        self.water = water

    def __repr__(self):
        return f"{self.name.lower().center(20, ' ')}"


class CoffeeMachine(object):
    """Class represents coffee machine with attributes:
    beverages - dict of beverages a machine can make,
    coffee and milk stored.
    """

    def __init__(self, coffee=1000, milk=2000):
        self.coffee = coffee
        self.milk = milk
        self.beverages = {
            1: Beverage("small latte", coffee=2, milk=60, water=40),
            2: Beverage("big latte", coffee=2, milk=200, water=80),
            3: Beverage("small cappuccino", coffee=2, milk=30, water=60),
            4: Beverage("big cappuccino", coffee=4, milk=100, water=80),
            5: Beverage("espresso", coffee=2, milk=0, water=60),
            6: Beverage("double espresso", coffee=4, milk=0, water=100),
            7: Beverage("mochaccino", coffee=4, milk=60, water=100),
            8: Beverage("americano", coffee=2, milk=0, water=80),
            9: Beverage("milk", coffee=0, milk=200, water=0)
        }

        # create tables in database if they don't exist
        self._get_db_ready()

    def _get_db_ready(self):
        """Creates before first use, if they don't exist, tables
        beverages and orders in an order loging database.

        If beverages table is empty, fills it with self.beverages data.
        """

        db = sqlite3.connect(HISTORYDBNAME)
        cur = db.cursor()
        cur.execute("PRAGMA foreign_keys = ON")

        # if not exists, create beverages
        cur.execute('''CREATE TABLE IF NOT EXISTS beverages (
                       id INTEGER NOT NULL,
                       name VARCHAR NOT NULL,
                       coffee INTEGER NOT NULL,
                       milk INTEGER NOT NULL,
                       water INTEGER NOT NULL,
                       PRIMARY KEY (id))''')

        # if not exists, create orders
        cur.execute('''CREATE TABLE IF NOT EXISTS orders (
                       bev_id VARCHAR NOT NULL REFERENCES beverages(id),
                       [date] DATETIME NOT NULL)''')

        # fill with beverages if empty
        cur.execute("SELECT * FROM beverages")
        if len(cur.fetchall()) == 0:
            bevs = [(k, v.name, v.coffee, v.milk, v.water)
                    for k, v in self.beverages.items()]

            cur.executemany("INSERT INTO beverages VALUES(?,?,?,?,?)",
                            bevs)
        db.commit()
        db.close()

    def get_dict_of_available_beverages(self):
        """Returns a dictionary of those beverages that machine has
        enough ingrediens to prepare."""

        available = dict([(i, bev) for i, bev in self.beverages.items()
                          if bev.coffee <= self.coffee and
                          bev.milk <= self.milk])
        return available

    def add_milk(self, milk):
        self.milk += milk

    def add_coffee(self, coffee):
        self.coffee += coffee

    def prepare_beverage(self, number):
        """If a machine doesn't have enough coffee and milk
        to prepare ordered beverage, an Exception is raised.

        Otherwise, coffee and milk, needed to make a beverage,
        are subtracted from coffee and milk that machine has.
        """

        if number not in self.beverages:
            raise Exception(f"No beverage with such number! ({number})")

        if self.coffee < self.beverages[number].coffee:
            raise Exception("No coffee enough!")

        if self.milk < self.beverages[number].milk:
            raise Exception("No milk enough!")

        self.coffee -= self.beverages[number].coffee
        self.milk -= self.beverages[number].milk

        self._write_to_history(number)     # log this order

        return self.beverages[number]

    def _write_to_history(self, number):
        """Writes to log that beverage with given number
        was just ordered."""

        from datetime import datetime

        now = datetime.now().strftime("%H:%M %d.%m.%Y")

        db = sqlite3.connect(HISTORYDBNAME)
        cur = db.cursor()
        cur.execute("INSERT INTO orders(bev_id, [date]) VALUES(?, ?)",
                    (number, now))
        db.commit()
        db.close()

    def get_history(self):
        """Returns a string with history log."""

        n = 30
        db = sqlite3.connect(HISTORYDBNAME)
        cur = db.cursor()
        cur.execute('''SELECT b.name, o.[date]
                        FROM orders o
                        INNER JOIN beverages b
                        ON o.bev_id = b.id
                        ORDER BY o.rowid DESC
                        LIMIT ''' + str(n))
        history = [f"{order[0]} ordered at {order[1]}"
                   for order in cur.fetchall()]
        db.close()

        history_str = (f"Coffee left: {self.coffee} " +
                       f"milk left: {self.milk}\n\n")
        history_str += f"Last {n} orders:\n"
        history_str += "\n".join(history)

        return history_str

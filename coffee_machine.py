class Beverage(object):
    """Class represents beverage with attributes:
       name, coffee (g), milk (ml), and water (ml). 
    """

    def __init__(self, name, coffee, milk, water):
        self.name = name
        self.coffee = coffee
        self.milk = milk
    
    def __repr__(self):
        return f"{self.name.lower().center(20, ' ')}"


HISTORYPATH = "history.txt"


class CoffeeMachine(object):
    """Class represents coffee machine with attributes:
       beverages - dict of beverages a machine can make,
       coffee and milk stored.
    """
       
    def __init__(self, coffee=1000, milk=2000):
        self.coffee = coffee
        self.milk = milk
        self.beverages = { 1: Beverage("small latte",      coffee=2, milk=60,  water=40),
                           2: Beverage("big latte",        coffee=2, milk=200, water=80),
                           3: Beverage("small cappuccino", coffee=2, milk=30,  water=60),
                           4: Beverage("big cappuccino",   coffee=4, milk=100, water=80),
                           5: Beverage("espresso",         coffee=2, milk=0,   water=60),
                           6: Beverage("double espresso",  coffee=4, milk=0,   water=100),
                           7: Beverage("mochaccino",       coffee=4, milk=60,  water=100),
                           8: Beverage("americano",        coffee=2, milk=0,   water=80),
                           9: Beverage("milk",             coffee=0, milk=200, water=0)
                         }
        
    def get_dict_of_available_beverages(self):
        available = dict([(i, bev) for i, bev in self.beverages.items() if bev.coffee <= self.coffee 
                                                                        and bev.milk <= self.milk])
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

        if not number in self.beverages:
            raise Exception(f"No beverage with such number! ({number})")
        
        if self.coffee < self.beverages[number].coffee:
            raise Exception("No coffee enough!")
        
        if self.milk < self.beverages[number].milk:
            raise Exception("No milk enough!")
            
        self.coffee -= self.beverages[number].coffee
        self.milk   -= self.beverages[number].milk
        
        self._write_to_history(number)     # log this order
  
        return self.beverages[number]
    
    def _write_to_history(self, number):
        
        from datetime import datetime
        
        now = datetime.now().strftime("%H:%M %d.%m.%Y")
        bev = self.beverages[number]

        with open(HISTORYPATH, 'a') as log:
            log.write(f"{str(bev)} ordered at {now}\n")

    def get_history(self):
        """Returns a string with history log."""
        
        with open(HISTORYPATH, 'r') as log:
            history = log.readlines() # list of lines
        
        history_str  = f"Coffee left: {self.coffee}, milk left: {self.milk}\n\n"
        history_str += "Last 30 orders:\n"
        history_str += "".join(history[-30:][::-1])
        
        return history_str
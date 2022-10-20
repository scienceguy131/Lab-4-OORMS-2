"""

    Description:
        This is the module that contains all the restaurant's models, including that of the Restaurant itself,
        the Tables, the Orders made with a selected chair, and the OrderItems and MenuItems for the OORMS in lab 4
        of the EEE320 course. These were all modeled with the use of classes and instantiating objects from them (duh).

    Modified by: OCdt Al-Ansar Mohammed, OCdt Liethan Velasco

    Notes:
        - None for now :P.

"""


# ---- Importing from other modules -----
from constants import TABLES, MENU_ITEMS

# --------------- Defining the classes of the Restaurant objects -------------

class Restaurant:

    def __init__(self):
        """ Constructor to the Restaurant Class.

        Upon instantiation, retrieves table and menu item data, creates a list of each of the objects
        and stores the lists in instance variables. """

        # TODO -  ayy wtf why's there a super constructor called here? There's no parent class as far as I see ://.
        super().__init__()

        # Getting the table and chair data from TABLES in  constants.py and creating a list of Table objects
        self.tables = [Table(seats, loc) for seats, loc in TABLES]

        # Initializing list of menu items for this restaurant object
        self.menu_items = [MenuItem(name, price) for name, price in MENU_ITEMS]

        # Ahh, here's the list that stores all the current views of this restaurant object
        self.views = []


    def add_view(self, view):
        """ Pretty self-explanatory. Method adds the  <view> passed through args into the self.views attribute """
        self.views.append(view)


    def notify_views(self):
        """ Ahh, so this method does update all the views stored in self.views. """
        for view in self.views:
            view.update()


class Table:

    def __init__(self, seats, location):
        """ Constructor to the Table Class.

        <seats> argument refers to the number of seats the Table object to be created will have.
        <location> argument refers to the location the Table object is to placed on the canvas. """

        # Setting the instance vars of the Table object to be created
        self.n_seats = seats
        self.location = location

        # Creating the list of Order objects associated with each seat at the table.
        # Storing it in an instance var attribute.
        self.orders = [Order() for _ in range(seats)]


    def has_any_active_orders(self):
        """ Oop here's a new one. This one I'm guessing returns True if there are still active orders
        pending that have not been served. If none, then obviously returns false. """
        for order in self.orders:
            for item in order.items:
                if item.has_been_ordered() and not item.has_been_served():
                    return True
        return False


    def has_order_for(self, seat):
        """ Function returns a boolean that indicates whether the given
        seat of number <seat> has ordered yet. """

        # Return True if there are 0 orders pending to be ordered, and the total cost
        # of the given order is greater than 0, insinuating that this chair has already placed an order.
        # "" return (len(this_order.unordered_items()) == 0) and (this_order.total_cost() > 0); ""

        # huh, will this one work?
        return bool(self.orders[seat].items)


    def order_for(self, seat):
        """ Function returns the specific Order object associated with the seat whose
        number <seat> has been passed through the arguments. """
        return self.orders[seat]


class Order:

    def __init__(self):
        """ Constructor for Order object.

        In short, this object is responsible for keeping track of the orders placed by a given
        seat in the restaurant.

        Every chair gets their own Order object associated with it. """

        # Creating empty list attribute to contain all items
        # that were ordered and that are pending to be ordered.
        self.items = []

    def add_item(self, menu_item):
        """ Function simply adds the OrderItem object <menu_item> passed through
        the arguments into the self.items list attribute of the Order object. """
        item = OrderItem(menu_item)
        self.items.append(item)

    def remove_item(self, item):
        """ Function simply removes the <item> object passed through args from the self.items list"""
        self.items.remove(item)

    def unordered_items(self):
        """ Function returns a list of all OrderItem objects in self.items that have yet
        to have their order status be set to 'ordered' """
        return [item for item in self.items if not item.has_been_ordered()]

    def place_new_orders(self):
        """ Function goes through the list attribute self.items of the given Order object and
        sets all OrderItem objects in the list from "unordered" to "ordered" status. """
        for item in self.unordered_items():
            item.mark_as_ordered()

    def remove_unordered_items(self):
        """ Function removes all the items in the list attribute self.items that have an "unordered" status. """
        for item in self.unordered_items():
            self.items.remove(item)

    def total_cost(self):
        """ Function simply calculates the total cost of all the OrderItem
        objects currently in the self.items list attribute.

        Ohh wow this one's given to us xD not that it was difficult to implement. """
        return sum((item.details.price for item in self.items))


class OrderItem:


    def __init__(self, menu_item):
        """ Constructor for the OrderItem class.

        Upon instantiation, sets the order status of the OrderItem object to False (obviously).
        Also stores the <menu_item> MenuItem object (object that contains the information
        regarding the given OrderItem object) in the instance var self.details. """

        # TODO: need to represent item state, not just ordered

        # --------------- Code added here ---------------

        # Alright it's gonna be a little messy here, but whatever.

        # We should have three different states that tells KitchenView what the next action of a certain order item:
        # display "START COOKING", "MARK AS READY" OR "MARK AS SERVED"

        # Let's use a string for now, and perhaps find cleaner methods to do this functionality,
        # (I swear there was a way for us to create our own "literals", like TO_COOK or something.
        # I know we definitely did it last year in C with O'Handley)

        # Let's have these as the states based off of the lab instructions:
        # "PLACED" => "START COOKING"       <-- This is the default upon instantiation
        # "COOKED" => "MARK AS READY"
        # "READY" => "MARK AS SERVED"

        self.status = "PLACED";

        # -----------------------------------------------

        self.details = menu_item
        self.__ordered = False


    def mark_as_ordered(self):
        """ Sets the self.ordered instance boolean var to true.  """
        self.__ordered = True

    def has_been_ordered(self):
        """ Returns True if this OrderItem has been ordered. Returns False otherwise. """
        return self.__ordered

    def has_been_served(self): # Changed
        """ I'm guessing we have this return True if been ordered, False otherwise. """
        return self.status == "SERVED";

    def can_be_cancelled(self):
        """ I'm guessing we have this return True if can be cancelled. False otherwise. """

        # TODO: When are going to decide when order can still be cancelled?
        return True


    # ------------- Creating more methods here ----------------

    def advance_status(self):
        """ Method advances current status of current item (PLACED --> COOKED --> READY --> SERVED). """

        match self.status:

            case "PLACED":
                self.status = "COOKED";
            case "COOKED":
                self.status = "READY";
            case "READY":
                self.status = "SERVED";  # OrderItem should disappear form view after this

    # ------------------------------------------------------


class MenuItem:
    """ Objects of this class hold the information pertaining to each OrderItem set on the menu. """

    def __init__(self, name, price):
        """ Constructor of MenuItem class.

        Upon instantiation, sets the name of the MenuItem to <name> and the
        price of the menu item to <price>. """

        self.name = name
        self.price = price

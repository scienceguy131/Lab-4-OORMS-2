"""

    Description:

        Code module that contains the controller classes. These classes are to be used in the
        OORMS lab 4 assignment in the EEE320 class.

    Classes defined in this module:
         - Controller Class (abstract class)
         - RestaurantController Class (inherits Controller)
         - TableController Class (inherits Controller)
         - OrderController Class (inherits Controller)
         - KitchenController Class (you guessed it. Inherits Controller)

    Modified by: OCdt Al-Ansar Mohammed, OCdt Liethan Velasco

    Notes:
        1 - A few minor code changes were made in this module, ie. creating objects
        first before passing them into arguments, rather than declaring the object
        within a methods arguments. This is done so that creating the sequence diagrams is more clear.


"""

# ------ Defining the classes of controllers ---------

class Controller:

    def __init__(self, view, restaurant):
        """ Constructor of Controller object.

        <view> is a ServerView object that handles all the drawing of the user interfaces, and <restaurant>
        is a Restaurant object which contains all the data used to draw out the tables, chairs, and orders. """

        self.view = view
        self.restaurant = restaurant


class RestaurantController(Controller):

    # Uses its parents constructor

    def create_ui(self):
        """ Calling .create_ui() method from this class back in the ServerView object calls the create_restaurant_ui().
        Essentially calls the method to draw the entire restaurant into the canvas. """
        self.view.create_restaurant_ui()

    def table_touched(self, table_number):
        """ I'm guessing this method does the same from lab 3 - set's the controller of whatever current view is
        active to the table that was touched. A little bit of a different way to write the code for it. """
        self.view.set_controller(TableController(self.view, self.restaurant, self.restaurant.tables[table_number]))
        self.view.update()


class TableController(Controller):

    def __init__(self, view, restaurant, table):
        """ Constructor of TableController object.

        <view> is a ServerView object that handles all the drawing of the user interfaces, <restaurant>
        is the Restaurant object which contains all the data used to draw out the tables, chairs, and orders,
        <table> is a specific table object that was clicked on (TableController object only gets created
        when that happens). """

        # Calling parent constructor
        super().__init__(view, restaurant)

        # Setting this object's table attribute to <table> passed through args
        self.table = table

    def create_ui(self):
        """ Calling .create_ui() method from this class back in the ServerView object calls the create_table_ui().
        Essentially calls the method to draw the specific table selected and its associated chairs onto the canvas. """
        self.view.create_table_ui(self.table)

    def seat_touched(self, seat_number):
        """ Different way to write it, but this method essentially changes the current controller to the
        one associated with the seat touched so that it can open up the corresponding order menu. """
        self.view.set_controller(OrderController(self.view, self.restaurant, self.table, seat_number))
        self.view.update()

    def done(self):
        """ Again, different way to write it, but the method switches the controller back to RestaurantController
        so that we can now see the entire restaurant. """
        self.view.set_controller(RestaurantController(self.view, self.restaurant))
        self.view.update()


class OrderController(Controller):

    def __init__(self, view, restaurant, table, seat_number):
        """ Constructor of OrderController object.

        <view> is a ServerView object that handles all the drawing of the user interfaces, <restaurant>
        is the Restaurant object which contains all the data used to draw out the tables, chairs, and orders,
        <table> is a specific table object that was clicked on, <seat_number> is the number of the seat at the table
        that was clicked on. """

        # Calling parent constructor
        super().__init__(view, restaurant)

        # Setting this object's attributes to the values passed through args
        self.table = table
        self.order = self.table.order_for(seat_number)

    def create_ui(self):
        """ Calling .create_ui() method from this class back in the ServerView object calls the create_order_ui().
        Essentially calls the method to draw the order menu associated with the specific chair selected. """
        self.view.create_order_ui(self.order)

    def add_item(self, menu_item):
        """ Function that adds item to the "to be ordered" list when the order user interface is up.

        Function does this by adding the item through the Order object's .add_item() method, and
        updates the order user_interface() by calling .create_ui().  """
        self.order.add_item(menu_item)
        self.view.update()

    def update_order(self):

        # Setting the "to be ordered" items to ordered status.
        self.order.place_new_orders()

        # Creating the table controller object and switching the controller back
        # in the view:ServerView to the created table controller
        table_controller = TableController(self.view, self.restaurant, self.table);
        self.view.set_controller(table_controller)

        # Huh, this is a new one, but I'm guessing this also updates all the views, including RestaurantView
        # and the KitchenView
        self.restaurant.notify_views()

    def cancel_changes(self):
        """ Function is responsible for cancelling an order in progress.

        NOT SURE IF THIS DOCSTRING WORKS FOR THIS METHOD. WILL CHECK.

        This function gets called when the 'Cancel' button gets pressed while in the order user interface.
        Pressing the button returns the view to the table associated with the chair whose order was just cancelled."""

        # Removing the list of items under "to be ordered" status
        self.order.remove_unordered_items()

        # Creating the table controller object and switching the controller back
        # in the view:ServerView to the created table controller
        table_controller = TableController(self.view, self.restaurant, self.table);
        self.view.set_controller(table_controller)

        # Updating the RestaurantView and KithcenView windows
        self.restaurant.notify_views()


class KitchenController(Controller):
    """ Well, here's the newest Controller subclass that we need to implement :)). """

    # Utilizes parent constructor

    def create_ui(self):
        """ Creates the user interface of the KitchenController. Damn, pretty half-assed docstring this is xD. """
        self.view.create_kitchen_order_ui()

    # TODO: implement a method to handle button presses on the KitchenView

    # Ahhh I see what we have to do here.

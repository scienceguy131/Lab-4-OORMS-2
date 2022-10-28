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

# ------ Creating Abstract Controller Class ---------

class Controller:

    def __init__(self, view, restaurant):
        """ Constructor of Controller object.

        <view> is a RestaurantView object that handles all the drawing of the user interfaces of its child classes,
         and <restaurant> is a Restaurant object which contains all the data used to draw out the tables, chairs,
         and orders. """

        self.view = view
        self.restaurant = restaurant



# --------- Creating Child Controller Classes ---------

class RestaurantController(Controller):
    """ Controller for the restaurant view in the ServerView object. """

    # Uses its parents constructor

    def create_ui(self):
        """ Calling .create_ui() method from this class back in the ServerView object calls the create_restaurant_ui().
        Essentially calls the method to draw the entire restaurant into the canvas. """
        self.view.create_restaurant_ui()


    def table_touched(self, table_number):
        """ Sets the current controller of the ServerView object to the TableController
        associated with the table of <table_number>.  """
        self.view.set_controller(TableController(self.view, self.restaurant, self.restaurant.tables[table_number]))
        self.view.update()



class TableController(Controller):
    """ Controller for the view of a given table within the restaurant in the ServerView object. """

    def __init__(self, view, restaurant, table):
        """ Constructor of TableController object.

        <view> is a ServerView object that handles all the drawing of the user interfaces, <restaurant>
        is the Restaurant object which contains all the data used to draw out the tables, chairs, and orders,
        <table> is a specific table object that was clicked on. """

        # Calling parent constructor
        super().__init__(view, restaurant)

        # Setting this object's table attribute to <table> passed through args
        self.table = table


    # -------- Defining Methods --------

    def create_ui(self):
        """ Calling .create_ui() method calls the create_table_ui() back in the user interface.
        Essentially draws the specific table and associated chairs of this TableController onto the canvas. """
        self.view.create_table_ui(self.table)


    def seat_touched(self, seat_number):
        """ Sets the current controller of the ServerView window to be the OrderController associated with the
        seat that just touched - opens up the order menu of the corresponding chair.  """
        self.view.set_controller(OrderController(self.view, self.restaurant, self.table, seat_number))
        self.view.update()


    def done(self):
        """ Method returns the controller back to RestaurantController - setting the user interface back
        to the view of the restaurant. """
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


    # --------- Defining Methods ---------

    def create_ui(self):
        """ Calling .create_ui() method calls the create_table_ui() back in the user interface.
        Essentially draws the order menu associated with the specific chair touched onto the canvas. """
        self.view.create_order_ui(self.order)


    def add_item(self, menu_item):
        """ Method that adds item to the "to be ordered" list when the order user interface is up.

        Function does this by adding the item through the Order object's .add_item() method, and
        updates the order user_interface by calling view.update().  """
        self.order.add_item(menu_item)
        self.view.update()


    def update_order(self):
        """ Method responsible for placing the requested orders into the PLACED status and set its __ordered attribute
        to True. Furthermore, placed orders show up in the KitchenView window, and ServerView returns to the table
        that was previously click on. """

        # Setting the __ordered attribute to true, and advancing status to PLACED.
        self.order.place_new_orders()

        # Creating the table controller object and switching the controller back
        # in the view:ServerView to the created table controller
        table_controller = TableController(self.view, self.restaurant, self.table);
        self.view.set_controller(table_controller)

        # Updating the ServerView and KitchenView user interfaces
        self.restaurant.notify_views()


    def cancel_changes(self):
        """ Method is responsible for cancelling an order whose items have yet to be placed (still in REQUESTED status).

        Method is called when 'Cancel' button in order user interface is pressed. After pressing, returns ServerView
        to the table associated with the chair whose order was just cancelled. """

        # Removing the list of items in REQUESTED status/ whose __unordered is False
        self.order.remove_unordered_items()

        # Creating the table controller object and switching the controller back
        # in the view:ServerView to the created table controller
        table_controller = TableController(self.view, self.restaurant, self.table);
        self.view.set_controller(table_controller)

        # Updating the RestaurantView and KithcenView windows
        self.restaurant.notify_views()


    def remove_spec_item(self, this_item):
        """ Method is responsible for removing the specific OrderItem <this_item> from the current order list -
        happens when red 'X' button is pressed next to an item in the order.

        If item was in the PLACED status when cancelled, is also removed from the KitchenView window. """

        # Removing the specific item from the order
        self.order.remove_item(this_item);

        # Updating the ServerView and KitchenView user interfaces
        self.restaurant.notify_views()



class KitchenController(Controller):
    """ Controller associated with the KitchenView object.  """


    def create_ui(self):
        """ Calling .create_ui() method calls the create_table_ui() back in the user interface.
        Essentially draws the view of the kitchen and currently cooking orders onto the window dedicated for the
        KitchenView. """
        self.view.create_kitchen_order_ui()


    def button_pressed(self, this_order_item):
        """ Advances status of order item pressed and updates the KitchenView user interface. """

        # Advance the order item's status
        this_order_item.advance_status();

        # Update the KitchenView user interface and ServerView userinterface
        self.restaurant.notify_views();



# cleaned up and ready to go.
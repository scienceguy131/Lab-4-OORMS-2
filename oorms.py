"""
    Description:
        This is the main module to the OORMS Lab 4 assignment from the EEE320 Object Oriented Analysis class.

    Task:
        P1 - To draw the sequence diagrams of specific sequences of the system as detailed in the lab instructions
        P2 - Actually doing some implementation and coding of the new desired functionalities :))


    Lab Started: October 7, 2022
    Lab Members: OCdt Al-Ansar Mohammed, OCdt Liethan Velasco.


    Notes:
          1 - damn, the code in this lab is simply another iteration of the same code from lab 3. And guess what?
          I commented the hell out of lab 3 explaining the back end xD and you bet I'm gonna migrate the same
          comments into the code for this lab. Of course, not everything will be exact, but of course it'll be a
          great help indeed

          2 - We ultimately chose to use the enum.IntEnum class for our enumerated constants, since it allows us to access the
          values of our status constants with int(Status.this_status). This way it doesn't give us a warning unlike
          using Status.this_status.value with the regular enum.Enum
            a - Strange. I noticed we don't need to import the enumerated status class from model.py/Status in order
            to use its enumerated constants within any other module.

          3 - Huh I think I figured out what this extra argument stuff does. It essentially ensures that each handler
          created for a given object actually gets set to said object. For example, when creating the tables in the
          restaurant view, well we have to make sure that when we touch a certain table, its handler opens up the
          table interface for the table touched. That's what passing that extra argument of table_number which is
          set to the current iterated value of ix into the table's handler is for. Without it, if we were just to
          pass ix into the handler function (the dummy var looping through each table as they get drawn onto the canvas)
          it results in all the handlers intended for each table getting associated with the last iterated through
          table. Just like that pre-added comment, using the extra arg table_number captures the current value of ix
          so that it gets associated with its intended table (lol I just said that twice). Now we know.

          4 - Well I know it's written in the lab instructions, but I'm just going to re-iterate here how we're
          going to implement the status functionality of the items placed. First of all, here's the progression of the
          statuses:

          REQUESTED -> PLACED -> COOKED -> READY -> SERVED.

          The status is set to REQUESTED when the button of an order item is pressed, however has not yet been placed
          (we know it's not placed since the circle to the left of the item's name is white). Here, the item can still
          be cancelled.

          The status thus becomes PLACED when the place order button is pressed, and its associated circle turns green.
          Additionally, the item then gets added to the KitchenView window with a button next to it saying
          "start cooking". The item can still be cancelled here.

          The status of an item becomes COOKED when the "start cooking" button is pressed. The item can no longer be
          cancelled. The button then reads "Mark as ready".

          The status of an item turns READY when the "Mark as Ready" button is pressed. The button then reads
          "Mark as Served".

          The status of an item turns SERVED when the "Mark as Served" button is pressed. Once this happens, the
          item in question is then removed from the KitchenView, simulating that it has left the kitchen and has
          been served to the customer who has ordered it.


          As previously mentioned, these status' were implemented using IntEnum constants, where REQUESTED is -1,
          PLACED is 0, up until SERVED is 3. Doing so also provides the ability to easily set the button text of a
          certain item, by storing the text in an array where the corresponding text of each status is placed at
          the the respective indices (ie. "Mark as Served" at button_text[int(Status.COOKED)] ). It also allows more
          far more elegant methods of status comparisons among a few of the class methods.


    Status:
        - Velasco and Mohammed (October 7, 2022) COMPLETED - ish: worked on the warmup of part 1
        - Velasco (October 12, 2022) COMPLETED: Beginning comment migration from lab 3 into code here
        - Velasco (October 12, 2022) COMPLETED: Beginning sequence diagram #2
        - Mohammed (October 21, 2022) COMPLETED: Bug fix in notify_views() made idk
        - Velasco and Mohammed (October 21, 2022) COMPLETED: Beginning sequence diagram #3
        - Velasco and Mohammed (October 23 2022)COMPLETED: Beginning implementation of sequence diagram #4
             - Implementing can be cancelled functionality for orders --> Adding REQUESTED Status
        - Velasco COMPLETED (October 24 2022): Cleaning up the code
            - (October 24, 2022) COMPLETED: Cleaning up oorms.py
            - (October 24, 2022) COMPLETED: Cleaning up model.py
            - (October 24, 2022) COMPLETED: Cleaning up controller.py

        - __ (October __ 2022): Writing the 4 tests
        - __ (October __ 2022): Writing the lab report

"""


# --- Importing from Built-in Libraries ---

import math
import tkinter as tk
from abc import ABC


# --- Importing from Local Modules ---

from constants import *
from controller import RestaurantController, KitchenController
from model import Restaurant  # Refer to Notes 2a for a comment


# --------------------- Defining Abstract Classes ---------------------

class RestaurantView(tk.Frame, ABC):
    """  An abstract superclass for the views in the system. """


    def __init__(self, master, restaurant, window_width, window_height, controller_class):
        """ Constructor to RestaurantView class. """

        # Calling superclass constructor that gives us the window to put the view in
        super().__init__(master)

        # Setting up the window for the server view using tkinter methods and objects.
        # <root> gets passed through master arg, which is basically a window object from tkinter.
        self.grid()
        self.canvas = tk.Canvas(self, width = window_width, height = window_height, borderwidth = 0,
                                highlightthickness = 0)
        self.canvas.grid()
        self.canvas.update()

        # Setting up instance var of the restaurant
        self.restaurant = restaurant

        # Adding this RestaurantView object to collection of views within the restaurant model
        self.restaurant.add_view(self)

        # Initializing controller of this view to controller passed through <controller_class>
        self.controller = controller_class(self, restaurant)
        self.controller.create_ui()


    # ---------------- Defining Methods ----------------

    def _make_button(self, text, action, size=BUTTON_SIZE, location=BUTTON_BOTTOM_RIGHT,
                     rect_style=BUTTON_STYLE, text_style=BUTTON_TEXT_STYLE):
        """ Provided method that handles button creation in the views. """
        w, h = size
        x0, y0 = location
        box = self.canvas.create_rectangle(x0, y0, x0 + w, y0 + h, **rect_style)
        label = self.canvas.create_text(x0 + w / 2, y0 + h / 2, text=text, **text_style)
        self.canvas.tag_bind(box, '<Button-1>', action)
        self.canvas.tag_bind(label, '<Button-1>', action)


    def update(self):
        """ Method calls current controller's create_ui() method which tells this view re-draw the user interface. """
        self.controller.create_ui()


    def set_controller(self, controller):
        """ Method switches current controller object to <controller> object passed through args. """
        self.controller = controller



# --------------------- Defining Children Classes ---------------------

class ServerView(RestaurantView):
    """ Inherits RestaurantView class.

    This view appears on the left window when the system is run. View contains the entire view of the restaurant -
    including the tables and chairs in it - and when pressed, shows the order views of the associated tables and chairs.
    Same view found in Lab 3.
    """

    def __init__(self, master, restaurant):
        """ Constructor to ServerView. """

        # Using solely superclass' constructor
        super().__init__(master, restaurant, SERVER_VIEW_WIDTH, SERVER_VIEW_HEIGHT, RestaurantController)


    # ---------------- Defining Methods ----------------

    def create_restaurant_ui(self):
        """ This method gets called in the RestaurantController object.

        When called, uses tkinter's provided canvas methods to create the restaurant's user interface.
        More specifically, it calls the methods that draws out the tables, and defines the function handler
        in the event a table is touched.
        """

        # Wiping canvas of all its current pixels
        self.canvas.delete(tk.ALL)

        # Creating empty list that will contain the IDs of the tables and chairs created.
        view_ids = []

        # Taking table and chair data stored in self.restaurant object attribute, drawing the tables
        # and chairs onto the canvas using protected method self._draw_table(). Filling up view_ids while doing so.
        for ix, table in enumerate(self.restaurant.tables):
            table_id, seat_ids = self._draw_table(table, scale = RESTAURANT_SCALE)
            view_ids.append((table_id, seat_ids))

        # Creating a handler for when a table is clicked on
        for ix, (table_id, seat_ids) in enumerate(view_ids):

            # Pre-written message here: (ayy I get what this means now)
            # §54.7 "extra arguments trick" in Tkinter 8.5 reference by Shipman
            # Used to capture current value of ix as table_index for use when
            # handler is called (i.e., when screen is clicked).
            # Refer to Notes 3 for a comment on this.

            # Creating the handler function for each table when it is touched.
            def table_touch_handler(_, table_number = ix):
                self.controller.table_touched(table_number)

            # Binding the table touch event to the tables on the user interface,
            # passing in the table_touch_handler through .tag_bind() wrapper function
            self.canvas.tag_bind(table_id, '<Button-1>', table_touch_handler)

            # Doing the same thing for each seat in the restaurant user interface
            # (Passing in table_touch_handler() function so that touching a particular seat opens
            # up the user interface of the table said seat is associated with. Ha ha I figured it out :D)
            for seat_id in seat_ids:
                self.canvas.tag_bind(seat_id, '<Button-1>', table_touch_handler)


    def create_table_ui(self, table):
        """ This method Is called within the TableController object.

        The Table object that was selected is the <table> passed through the argument.

        When a specific table/chair is clicked, method uses provided tkinter methods to create the clicked upon table's
        user interface by drawing it and its selected chairs onto the canvas, and defines the handler for when a given
        seat is clicked on. """

        # Wiping the canvas of all currently drawn pixels
        self.canvas.delete(tk.ALL)

        # Drawing out the clicked on table and its associated seats in the specified location defined
        # in the constants module (in the top left corner of the window lol)
        table_id, seat_ids = self._draw_table(table, location = SINGLE_TABLE_LOCATION)

        # Creating the handler function for each of the table's seats
        for ix, seat_id in enumerate(seat_ids):

            # Creating the seat touched event handler for each seat when touched.
            # Refer to Notes 3 for a comment on this.
            def handler(_, seat_number = ix):
                self.controller.seat_touched(seat_number)

            # Binding the click event to each seat around the table. Passing the
            # seat handler function into this wrapper function.
            self.canvas.tag_bind(seat_id, '<Button-1>', handler)

        # Creating the button that which closes the current table user interface
        # and return to the restaurant user interface.
        self._make_button('Done', action = lambda event: self.controller.done())


    def _draw_table(self, table, location = None, scale = 1):
        """ Uses Tkinter's provided canvas methods to draw a given table object out onto the canvas.

        <table> is the table object to be drawn, <location, defaulted to None> refers to where the table object
        is to be drawn on the canvas, and <scale, defaulted to 1> is how large the table is to be drawn.

        Returns the IDs of the table and seats created by tkinter for event binding with the handlers."""

        # Unpacking the coordinates for the offset depending on arguments passed
        offset_x0, offset_y0 = location if location else table.location

        # DAMN, there's still a bunch of variables used to draw out the tables and seats here xD.
        seats_per_side = math.ceil(table.n_seats / 2)
        table_height = SEAT_DIAM * seats_per_side + SEAT_SPACING * (seats_per_side - 1)
        table_x0 = SEAT_DIAM + SEAT_SPACING
        table_bbox = _scale_and_offset(table_x0, 0, TABLE_WIDTH, table_height,
                                       offset_x0, offset_y0, scale)

        # Drawing the table here.
        table_id = self.canvas.create_rectangle(*table_bbox, **TABLE_STYLE)

        # Drawing the seats here.
        far_seat_x0 = table_x0 + TABLE_WIDTH + SEAT_SPACING
        seat_ids = []
        for ix in range(table.n_seats):
            seat_x0 = (ix % 2) * far_seat_x0
            seat_y0 = (ix // 2 * (SEAT_DIAM + SEAT_SPACING) +
                       (table.n_seats % 2) * (ix % 2) * (SEAT_DIAM + SEAT_SPACING) / 2)
            seat_bbox = _scale_and_offset(seat_x0, seat_y0, SEAT_DIAM, SEAT_DIAM,
                                          offset_x0, offset_y0, scale)
            style = FULL_SEAT_STYLE if table.has_order_for(ix) else EMPTY_SEAT_STYLE
            seat_id = self.canvas.create_oval(*seat_bbox, **style)
            seat_ids.append(seat_id)

            # Returning table_id's and seat_id's
        return table_id, seat_ids


    def create_order_ui(self, order):
        """ This method is called within the OrderController object.

        Uses tkinter's provided methods to create the user interface of the order menu
        when a given seat object is selected from the table user interface.

        <order> is the order object that is to track all the orders made for the selected seat. """

        # Wipe canvas of all currently drawn pixels
        self.canvas.delete(tk.ALL)

        # Creating buttons for the order user interface, and the handler
        # for when each button is clicked on.
        for ix, item in enumerate(self.restaurant.menu_items):

            w, h, margin = MENU_ITEM_SIZE
            x0 = margin
            y0 = margin + (h + margin) * ix

            # Creating the handler function for each button.
            # Refer to Notes 3 for a comment on this.
            def handler(_, menuitem = item):
                self.controller.add_item(menuitem)

            # Creating each button, and passing their handler into the wrapper function
            self._make_button(item.name, handler, (w, h), (x0, y0))

        # Literally drawing out the food items put up for order
        self._draw_order(order)

        # Creating the two buttons for the order user interface: Cancel and Place Orders button
        self._make_button('Cancel', lambda event: self.controller.cancel_changes(), location = BUTTON_BOTTOM_LEFT)
        self._make_button('Place Orders', lambda event: self.controller.update_order())


    def _draw_order(self, order):
        """ Draws out the orders placed after pressing a menu item button.  """

        x0, h, m = ORDER_ITEM_LOCATION
        for ix, item in enumerate(order.items):

            y0 = m + ix * h
            self.canvas.create_text(x0, y0, text=item.details.name, anchor = tk.NW)
            dot_style = ORDERED_STYLE if item.has_been_ordered() else NOT_YET_ORDERED_STYLE
            self.canvas.create_oval(x0 - DOT_SIZE - DOT_MARGIN, y0, x0 - DOT_MARGIN, y0 + DOT_SIZE, **dot_style)

            # The code below is used to cancel an item made in an order if it is still in REQUESTED or PLACED state
            if item.can_be_cancelled():

                # Handler that removes the specific object when 'X' button pressed.
                # Refer to Notes 3 for a comment on this.
                def handler(_, cancelled_item = item):
                    self.controller.remove_spec_item(cancelled_item);

                # Making the cancel button
                self._make_button('X', handler, size=CANCEL_SIZE, rect_style=CANCEL_STYLE,
                                  location=(x0 - 2*(DOT_SIZE + DOT_MARGIN), y0))

        # Drawing the total price below the orders placed.
        self.canvas.create_text(x0, m + len(order.items) * h, text = f'Total: {order.total_cost():.2f}', anchor = tk.NW)



class KitchenView(RestaurantView):
    """ Inherits RestaurantView superclass.

    View object that handles the "prep" of all orders placed. """


    def __init__(self, master, restaurant):
        """ Constructor to the KitchenView class. """

        # Using parent's constructor - basically creates another window for the kitchen.
        super().__init__(master, restaurant, KITCHEN_VIEW_WIDTH, KITCHEN_VIEW_HEIGHT, KitchenController)


    # ---------------- Defining Methods ----------------

    def create_kitchen_order_ui(self):
        """ This method gets called by the KitchenController object.

        When called, uses tkinter's provided canvas methods to re-draw the kitchen's user interface this window. """

        # Clear the canvas as usual
        self.canvas.delete(tk.ALL)

        # Finding the orders for the given table selected
        line = 0
        for table_number, table in enumerate(self.restaurant.tables):

            # Printing out the active orders made of all the tables
            if table.has_any_active_orders():

                # Drawing table title
                self.draw_text_line(f'Table {table_number}', K_LEFT, (line + 0.5) * K_LINE_HEIGHT)
                line += 1

                # For each item in the orders of each table...
                for order in table.orders:
                    for item in order.items:

                        # Draw out the item if it has been ordered and not yet served
                        if item.has_been_ordered() and not item.has_been_served():

                            # Refer to Notes 4 for an explanation on the Status functionality of the items.

                            # Setting the button text depending on current status value
                            button_options = ["START COOKING", "MARK AS READY", "MARK AS SERVED"];
                            button_text = button_options[item.get_status().value]

                            # Creating the handler for when the text button for item in KitchenView is touched.
                            # Refer to Notes 3 for a comment on this.
                            def handler(_, order_item = item):
                                self.controller.button_pressed(order_item);

                            # Creating the buttons for each of the orders
                            self._make_button(button_text, handler,
                                              location=(K_LEFT, line * K_LINE_HEIGHT),
                                              size=K_BUTTON_SIZE)
                            self.draw_text_line(item.details.name, K_LEFT + K_BUTTON_SIZE[0] + K_SPACE,
                                                (line + 0.4) * K_LINE_HEIGHT)
                            line += 1


    def draw_text_line(self, text, x, y):
        """ This method gets called in the create_kitchen_order_ui() method. """
        self.canvas.create_text(x, y, text = text, anchor = tk.W)





# --------- Defining Separate Functions -----------

def _scale_and_offset(x0, y0, width, height, offset_x0, offset_y0, scale):
    """ Function to make the code for drawing more clean and organized. """
    return ((offset_x0 + x0) * scale,
            (offset_y0 + y0) * scale,
            (offset_x0 + x0 + width) * scale,
            (offset_y0 + y0 + height) * scale)




# ----- Entry Point -----

if __name__ == "__main__":

    # Creating the restaurant object
    restaurant_info = Restaurant()

    # Retrieving a window object from tkinter
    root = tk.Tk()

    # Creating the ServerView object
    ServerView(root, restaurant_info)
    root.title('Server View v2')
    root.wm_resizable(0, 0)

    # Creating the KitchenView object
    kitchen_window = tk.Toplevel()
    KitchenView(kitchen_window, restaurant_info)
    kitchen_window.title('Kitchen View v2')
    kitchen_window.wm_resizable(0, 0)

    # Aligning the two windows with each other upon creation
    root.update_idletasks()
    kh = kitchen_window.winfo_height()
    kw = kitchen_window.winfo_width()
    sw = root.winfo_width()
    sx = root.winfo_x()
    sy = root.winfo_y()
    kitchen_window.geometry(f'{kw}x{kh}+{sx + sw + 10}+{sy}')

    # Calling the mainloop of the program.
    root.mainloop()


# nice. cleaned up and good to go.
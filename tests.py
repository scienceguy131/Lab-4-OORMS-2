import unittest
from enum import Enum, auto

from controller import RestaurantController, TableController, OrderController, KitchenController

from model import Restaurant, OrderItem, Status


class UI(Enum):
    """
    Used by ServerViewMock to represent the last user interface that was
    drawn.
    """
    RESTAURANT = auto()
    TABLE = auto()
    ORDER = auto()


class ServerViewMock:
    """
    A non-graphical replacement for `oorms.ServerView`, used for testing. Allow
    tests to check what was the last user interface rendered. Fully replicates the
    public interface of `ServerView`. The `set_controller` and `update` methods
    are exact copies of those in `oorms.RestaurantView`.
    """

    def __init__(self, restaurant):
        self.controller = None
        self.last_UI_created = None
        self.restaurant = restaurant
        self.set_controller(RestaurantController(self, self.restaurant))
        self.update()

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.controller.create_ui()

    def create_restaurant_ui(self):
        self.last_UI_created = UI.RESTAURANT

    def create_table_ui(self, table):
        self.last_UI_created = (UI.TABLE, table)

    def create_order_ui(self, order):
        self.last_UI_created = (UI.ORDER, order)


class KitchenViewMock:

    def __init__(self, restaurant):
        self.controller = None
        self.UI = 0
        self.restaurant = restaurant
        self.set_controller(KitchenController(self,self.restaurant))
        self.update()

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.controller.create_ui()
        self.UI += 1

    def create_kitchen_order_ui(self):
        pass


class OORMSTestCase(unittest.TestCase):

    def setUp(self):
        self.restaurant = Restaurant()
        self.view = ServerViewMock(self.restaurant)
        self.restaurant.add_view(self.view)

        self.kitchen_view = KitchenViewMock(self.restaurant)
        self.restaurant.add_view(self.kitchen_view)


    def test_initial_state(self):
        self.assertEqual(UI.RESTAURANT, self.view.last_UI_created)
        self.assertIsInstance(self.view.controller, RestaurantController)

    def test_restaurant_controller_touch_table(self):
        self.view.controller.table_touched(3)
        self.assertIsInstance(self.view.controller, TableController)
        self.assertEqual(self.view.controller.table, self.restaurant.tables[3])
        self.assertEqual((UI.TABLE, self.restaurant.tables[3]), self.view.last_UI_created)

    def test_table_controller_done(self):
        self.view.controller.table_touched(5)
        self.view.controller.done()
        self.assertIsInstance(self.view.controller, RestaurantController)
        self.assertEqual(UI.RESTAURANT, self.view.last_UI_created)

    def test_table_controller_seat_touched(self):
        self.view.controller.table_touched(4)
        self.view.controller.seat_touched(0)
        self.assertIsInstance(self.view.controller, OrderController)
        self.assertEqual(self.view.controller.table, self.restaurant.tables[4])
        the_order = self.restaurant.tables[4].order_for(0)
        self.assertEqual(self.view.controller.order, the_order)
        self.assertEqual((UI.ORDER, the_order), self.view.last_UI_created)

    def order_an_item(self):
        """
        Starting from the restaurant UI, orders one instance of item 0
        for table 2, seat 4
        """
        self.view.controller.table_touched(2)
        self.view.controller.seat_touched(4)
        the_menu_item = self.restaurant.menu_items[0]
        self.view.last_UI_created = None
        self.view.controller.add_item(the_menu_item)
        return self.restaurant.tables[2].order_for(4), the_menu_item

    def test_order_controller_add_item(self):
        the_order, the_menu_item = self.order_an_item()
        self.assertIsInstance(self.view.controller, OrderController)
        self.assertEqual((UI.ORDER, the_order), self.view.last_UI_created)
        self.assertEqual(1, len(the_order.items))
        self.assertIsInstance(the_order.items[0], OrderItem)
        self.assertEqual(the_order.items[0].details, the_menu_item)
        self.assertFalse(the_order.items[0].has_been_ordered())

    def test_order_controller_update_order(self):
        the_order, the_menu_item = self.order_an_item()
        self.view.last_UI_created = None
        self.view.controller.update_order()
        self.assertEqual((UI.TABLE, self.restaurant.tables[2]), self.view.last_UI_created)
        self.assertEqual(1, len(the_order.items))
        self.assertIsInstance(the_order.items[0], OrderItem)
        self.assertEqual(the_order.items[0].details, the_menu_item)
        self.assertTrue(the_order.items[0].has_been_ordered())

    def test_order_controller_cancel(self):
        the_order, the_menu_item = self.order_an_item()
        self.view.last_UI_created = None
        self.view.controller.cancel_changes()
        self.assertEqual((UI.TABLE, self.restaurant.tables[2]), self.view.last_UI_created)
        self.assertEqual(0, len(the_order.items))

    def test_order_controller_update_several_then_cancel(self):
        self.view.controller.table_touched(6)
        self.view.controller.seat_touched(7)
        the_order = self.restaurant.tables[6].order_for(7)
        self.view.controller.add_item(self.restaurant.menu_items[0])
        self.view.controller.add_item(self.restaurant.menu_items[3])
        self.view.controller.add_item(self.restaurant.menu_items[5])
        self.view.controller.update_order()

        def check_first_three_items(menu_items, items):
            self.assertEqual(menu_items[0], items[0].details)
            self.assertEqual(menu_items[3], items[1].details)
            self.assertEqual(menu_items[5], items[2].details)

        self.assertEqual(3, len(the_order.items))
        check_first_three_items(self.restaurant.menu_items, the_order.items)

        def add_two_more(menu_items, view):
            view.controller.seat_touched(7)
            view.controller.add_item(menu_items[1])
            view.controller.add_item(menu_items[2])

        add_two_more(self.restaurant.menu_items, self.view)
        self.view.controller.cancel_changes()

        self.assertEqual(3, len(the_order.items))
        check_first_three_items(self.restaurant.menu_items, the_order.items)

        add_two_more(self.restaurant.menu_items, self.view)
        self.view.controller.update_order()

        self.assertEqual(5, len(the_order.items))
        check_first_three_items(self.restaurant.menu_items, the_order.items)
        self.assertEqual(self.restaurant.menu_items[1], the_order.items[3].details)
        self.assertEqual(self.restaurant.menu_items[2], the_order.items[4].details)

    def test_kitchen_initial_state(self):
        self.assertIsInstance(self.kitchen_view.controller, KitchenController)
        self.assertEqual(2, len(self.restaurant.views))

    def test_press_x(self):
        """
        Orders an item, checks whether it has been ordered and if its status is correct.
        Cancels the item (as though a server pressed X), then tests whether the item exists
        and whether the kitchen UI has been updated after the fact
        """
        the_order, the_menu_item = self.order_an_item()
        order_item = the_order.items[0]

        self.kitchen_view.controller.button_pressed(order_item)

        self.assertEqual(order_item.status, Status.PLACED)
        self.assertEqual(2, self.kitchen_view.UI)

        self.view.controller.cancel_changes()

        self.assertEqual(len(the_order.items), 0)
        self.assertEqual(3, self.kitchen_view.UI)

    def test_start_cooking(self):
        """
        Orders an item and advances the item to PLACED and then to COOKED
        checks whether the state has been correctly updated
        and that the item cannot be cancelled
        also checks that the kitchen UI has been updated the correct amount of times
        """
        the_order, the_menu_item = self.order_an_item()
        order_item = the_order.items[0]

        self.assertEqual(1, self.kitchen_view.UI)
        self.kitchen_view.controller.button_pressed(order_item)
        self.assertEqual(2, self.kitchen_view.UI)
        self.kitchen_view.controller.button_pressed(order_item)

        self.assertEqual(order_item.status, Status.COOKED)
        self.assertFalse(order_item.can_be_cancelled())
        self.assertEqual(3, self.kitchen_view.UI)

    def test_mark_as_served(self):
        """
        Orders an item and advances the item to PLACED, to COOKED, to READY, and to SERVED
        checks whether the state has been correctly updated and
        also checks that the kitchen UI has been updated the correct amount of times
        """
        the_order, the_menu_item = self.order_an_item()
        order_item = the_order.items[0]

        self.assertEqual(1, self.kitchen_view.UI)
        self.kitchen_view.controller.button_pressed(order_item)
        self.assertEqual(2, self.kitchen_view.UI)
        self.kitchen_view.controller.button_pressed(order_item)
        self.assertEqual(3, self.kitchen_view.UI)
        self.kitchen_view.controller.button_pressed(order_item)
        self.assertEqual(4, self.kitchen_view.UI)
        self.kitchen_view.controller.button_pressed(order_item)

        self.assertEqual(order_item.status, Status.SERVED)
        self.assertFalse(order_item.can_be_cancelled())
        self.assertEqual(5, self.kitchen_view.UI)


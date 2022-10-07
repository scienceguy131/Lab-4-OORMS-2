# Restaurant data

TABLES = [(6, (20, 20)),
          (4, (20, 225)),
          (5, (20, 370)),
          (2, (270, 20)),
          (2, (270, 100)),
          (2, (270, 180)),
          (8, (270, 280)),
          (2, (270, 520))]

MENU_ITEMS = [('House burger', 16),
              ('Chicken club', 14.5),
              ('Crispy Pork Belly', 14.5),
              ('Fried Chicken', 14.5),
              ('Butter Chicken Tacos', 16),
              ('Roasted Squash', 14),
              ('Portabella Burger', 14),
              ('Striploin Sandwich', 16),
              ('Beef Cheek', 24),
              ('Cornish Rock Hen', 23),
              ('Grilled Local Trout', 19),
              ('Hunters Rabbit Stew', 19)]

# Server view constants

RESTAURANT_SCALE = 0.75

TABLE_STYLE = {'fill': '#ccc', 'outline': '#999'}
TABLE_WIDTH = 80
SINGLE_TABLE_LOCATION = (30, 30)

SEAT_DIAM = 40
SEAT_SPACING = 10

EMPTY_SEAT_STYLE = {'fill': '#ccc', 'outline': '#999'}
FULL_SEAT_STYLE = {'fill': '#090', 'outline': '#090'}

SERVER_VIEW_WIDTH = 380
SERVER_VIEW_HEIGHT = 500

# Kitchen view constants

KITCHEN_VIEW_WIDTH = 325
KITCHEN_VIEW_HEIGHT = 800
K_LEFT = 20
K_BUTTON_SIZE = (130, 22)
K_LINE_HEIGHT = 25
K_SPACE = 10


# Button constants

BUTTON_SIZE = (100, 30)
BUTTON_MARGIN = (10, 10)
BUTTON_BOTTOM_RIGHT = (SERVER_VIEW_WIDTH - BUTTON_SIZE[0] - BUTTON_MARGIN[0],
                       SERVER_VIEW_HEIGHT - BUTTON_SIZE[1] - BUTTON_MARGIN[1])
BUTTON_BOTTOM_LEFT = (BUTTON_MARGIN[0], SERVER_VIEW_HEIGHT - BUTTON_SIZE[1] - BUTTON_MARGIN[1])
BUTTON_STYLE = {'fill': '#090', 'outline': '#090'}
BUTTON_TEXT_STYLE = {'fill': '#fff'}

# Order view constants

MENU_ITEM_SIZE = (150, 20, 5)

ORDER_ITEM_LOCATION = (230, 20, 5)
DOT_SIZE = 15
DOT_MARGIN = 5
CANCEL_SIZE = (DOT_SIZE, DOT_SIZE)
CANCEL_STYLE = {'fill': '#900', 'outline': '#900'}
NOT_YET_ORDERED_STYLE = {'fill': '#fff', 'outline': '#090'}
ORDERED_STYLE = BUTTON_STYLE



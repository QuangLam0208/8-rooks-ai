# --- WINDOW ---
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
LIGHT_GRAY  = (200, 200, 200)
DARK_GRAY   = (64, 64, 64)
MYOSOTIS = (0x64, 0x74, 0x7B)
CADETGRAY = (0x93, 0xA8, 0xAC)
STONE = (0xA3, 0xAC, 0xA9)
COTTON = (0xE2, 0xDC, 0xD0)
ECRU = (0xBD, 0xBB, 0xA5)
SAGE = (0x8D, 0x9B, 0x86)

BORDER_RADIUS = 10

# --- NHÓM THUẬT TOÁN ---
ALG_SPACING = 8
ALG_WIDTH = 210
# NHÓM CHA
ALG_GROUP_TOP = ALG_LEFT = 50
ALG_GROUP_HEIGHT = 40
TOTAL_GROUP_HEIGHT = 6 * ALG_GROUP_HEIGHT + 5 * ALG_SPACING
PARENT_CHILD_SPACING = 30
# NHÓM CON
ALG_LIST_TOP = ALG_GROUP_TOP + TOTAL_GROUP_HEIGHT + PARENT_CHILD_SPACING
ALG_LIST_HEIGHT = 60
TOTAL_LIST5_HEIGHT = 5 * ALG_LIST_HEIGHT + 4 * ALG_SPACING

# --- NHÓM NÚT CHỨC NĂNG ---
ACTION_TOP = ALG_LIST_TOP + TOTAL_LIST5_HEIGHT + 30
ACTION_WIDTH = 100
ACTION_HEIGHT = 50
ACTION_SPACING = 20

# --- BOARD ---
BOARD_SIZE = 8 # kích cỡ bàn cờ
SQUARE_SIZE = TOTAL_GROUP_HEIGHT // BOARD_SIZE
LEFT_BOARD_X = ALG_LEFT + ALG_WIDTH + 90 
RIGHT_BOARD_X = LEFT_BOARD_X + BOARD_SIZE * SQUARE_SIZE + 50
# Màu sắc các ô
WHITE_CELL = (238, 238, 210)   # ô sáng
BLACK_CELL = (118, 150, 86)    # ô tối 

def update_board_size(new_size):
    """Cập nhật lại các giá trị phụ thuộc vào BOARD_SIZE khi đổi kích thước bàn cờ."""
    global BOARD_SIZE, SQUARE_SIZE, LEFT_BOARD_X, RIGHT_BOARD_X
    global WINDOW_WIDTH, WINDOW_HEIGHT
    global ACTION_TOP, TOTAL_LIST5_HEIGHT

    # ==== Kiểm tra hợp lệ ====
    if not (3 <= new_size <= 8):
        print("Board size must be between 3 and 8!")
        return

    # ==== Cập nhật kích thước cơ bản ====
    BOARD_SIZE = new_size
    SQUARE_SIZE = TOTAL_GROUP_HEIGHT // BOARD_SIZE

    # ==== Cập nhật vị trí các phần trên giao diện ====
    LEFT_BOARD_X = ALG_LEFT + ALG_WIDTH + 90
    RIGHT_BOARD_X = LEFT_BOARD_X + BOARD_SIZE * SQUARE_SIZE + 50

    # ==== Cập nhật layout các phần phụ thuộc ====
    TOTAL_LIST5_HEIGHT = 5 * ALG_LIST_HEIGHT + 4 * ALG_SPACING
    ACTION_TOP = ALG_LIST_TOP + TOTAL_LIST5_HEIGHT + 30

    # ==== Tự co giãn cửa sổ để đủ chứa 2 bàn cờ + stats ====
    board_area_width = (RIGHT_BOARD_X - LEFT_BOARD_X) + BOARD_SIZE * SQUARE_SIZE + 500
    WINDOW_WIDTH = max(1400, board_area_width)
    WINDOW_HEIGHT = 800

    print(f"Board resized to {BOARD_SIZE}x{BOARD_SIZE}")
    print(f"Each square: {SQUARE_SIZE}px, Window width: {WINDOW_WIDTH}px")

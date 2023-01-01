import serial
import vgamepad as vg

gamepad = vg.VX360Gamepad()

arduino = serial.Serial('COM9', 115200, timeout=.1)

KEYS = [
  'a', 'b', 'x', 'y', 'up', 'down', 'left', 'right', 
  'lt', 'lb', 'rt', 'rb', 'lpress', 'rpress', 'start', 'back'
]

KEY_TO_BUTTON = {
  'a': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
  'b': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
  'x': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
  'y': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
  'up': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
  'down': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
  'left': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
  'right': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
  'lt': 'LEFT_TRIGGER',
  'lb': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
  'rt': 'RIGHT_TRIGGER',
  'rb': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
  'lpress': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
  'rpress': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
  'start': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
  'back': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
}

keys_down = {}

def release_key(key):
  if key in keys_down:
    keys_down[key] = False

    if key=='lt':
      gamepad.left_trigger_float(value_float=0)
    elif key=='rt':
      gamepad.right_trigger_float(value_float=0)
    else:
      gamepad.release_button(button=KEY_TO_BUTTON[key])

def press_key(key):
  if key not in keys_down or not keys_down[key]:
    keys_down[key] = True
    
    if key=='lt':
      gamepad.left_trigger_float(value_float=1)
    elif key=='rt':
      gamepad.right_trigger_float(value_float=1)
    else:
      print(key)
      gamepad.press_button(button=KEY_TO_BUTTON[key])

def handle_keys(keys):
  for i in range(len(KEYS)):
    key_pressed = bool(keys & (1 << i))

    if key_pressed:
      press_key(KEYS[i])
    else:
      release_key(KEYS[i])

def get_joystick_pos(pos, 
    INVERT_X=False, INVERT_Y=False, ROTATE=False):
  x, y = pos
  if abs(x) < 100:
    x = 0
  if abs(y) < 100:
    y = 0
    
  x = float(x) / 512
  y = float(y) / 512

  if INVERT_X:
    x = -x
  if INVERT_Y:
    y = -y

  if ROTATE:
    x, y = y, x
  return x, y

def handle_left_joystick(pos):
  x, y = get_joystick_pos(pos, INVERT_X=True)
  gamepad.left_joystick_float(x_value_float=x, y_value_float=y)

def handle_right_joystick(pos):
  x, y = get_joystick_pos(pos, INVERT_Y=True)
  gamepad.right_joystick_float(x_value_float=x, y_value_float=y)

while True:
  data = arduino.readline()
  data = data.decode('utf-8').strip()
  data = data.split(',')
  
  if len(data) > 1: 
    data = [int(x) for x in data]
    
    handle_keys(data[4])
    handle_left_joystick((data[0], data[1]))
    handle_right_joystick((data[2], data[3]))
    
    gamepad.update()
import os
import json

# Libinput gestures configuration file path
LIG_CONF_FILE_PATH_ROOT='/etc/libinput-gestures.conf'

# paths for gestures manager own configuration file
HOME = os.environ.get('HOME')
CONFDIR = HOME+('/.config')
LIG_USER_CONF_FILE_PATH = CONFDIR+'/libinput-gestures.conf'
GM_CONF_FILE_PATH = CONFDIR+'/gesturesmanger.json'

if not os.path.isdir(CONFDIR):
    os.makedirs(CONFDIR)

if not os.path.isfile(LIG_USER_CONF_FILE_PATH):
    out=open(LIG_USER_CONF_FILE_PATH, 'w')
    out.write('# Gestures Manager created this configuration file for Libinput Gestures')
    out.close()

LIG_CONF_FILE_COMMENTS= \
"""# Configuration file for libinput-gestures.
#
# The default configuration file exists at /etc/libinput-gestures.conf
# but a user can create a personal custom configuration file at
# ~/.config/libinput-gestures.conf.
#
# Lines starting with '#' and blank lines are ignored.
# At present only gesture lines are configured in this file.
#
# Each gesture: line has 3 [or 4] arguments:
#
# action motion [finger_count] command
#
# where action and motion is either:
#     swipe up
#     swipe down
#     swipe left
#     swipe right
#     pinch in
#     pinch out
#
# command is the remainder of the line and is any valid shell command +
# arguments.
#
# finger_count is optional (and is typically 3 or 4). If specified then
# the command is executed when exactly that number of fingers is used in
# the gesture. If not specified then the command is executed when that
# gesture is executed with any number of fingers. Gesture lines
# specified with finger_count have priority over the same gesture
# specified without any finger_count.
#
# Typically command will be xdotool, or wmctrl. See "man xdotool" for
# the many things you can action with that tool."""

GESTURE_PREFIX='gesture:'

ACTION_SWIPE='swipe'
ACTION_PINCH='pinch'

ACTIONS=[ACTION_SWIPE, ACTION_PINCH]

D_UP='up'
D_DOWN='down'
D_LEFT='left'
D_RIGHT='right'
D_IN='in'
D_OUT='out'

DIRECTIONS=[D_UP, D_DOWN, D_LEFT, D_RIGHT, D_IN, D_OUT]

EXCEPTION_ACTION_NOT_IN_ACTIONS='The specified action is neither swipe or pinch'
EXCEPTION_DIRECTION_NOT_IN_DIRECTIONS='The specified direction is invalid'
EXCEPTION_FINGER_COUNT_OUT_OF_RANGE='The specified finger count is out of range'

BASE_XDOTOOL_KEYSTROKE='xdotool key '


class Gesture:
    def __init__(self, action, direction, fingers):
        if not action in ACTIONS:
            raise ValueError(EXCEPTION_ACTION_NOT_IN_ACTIONS)
        if not direction in DIRECTIONS:
            raise ValueError(EXCEPTION_DIRECTION_NOT_IN_DIRECTIONS)
        if not fingers in [2,3,4]:
            raise ValueError(EXCEPTION_FINGER_COUNT_OUT_OF_RANGE)
        self.action=action
        self.direction=direction
        self.fingers=fingers

    def build_gesture_string(self, command):
        gesture_string=' '.join([GESTURE_PREFIX, self.action, self.direction, str(self.fingers), command])
        return gesture_string

    def __repr__(self):
        return ' '.join([str(self.fingers), 'fingers', self.action, self.direction])

    def __str__(self):
        return self.__repr__()

GESTURES_POSSIBLE=[
    Gesture(ACTION_PINCH, D_IN, 2),
    Gesture(ACTION_PINCH, D_OUT, 2),
    Gesture(ACTION_SWIPE, D_UP, 3),
    Gesture(ACTION_SWIPE, D_DOWN, 3),
    Gesture(ACTION_SWIPE, D_LEFT, 3),
    Gesture(ACTION_SWIPE, D_RIGHT, 3),
    Gesture(ACTION_PINCH, D_IN, 3),
    Gesture(ACTION_PINCH, D_OUT, 3),
    Gesture(ACTION_SWIPE, D_UP, 4),
    Gesture(ACTION_SWIPE, D_DOWN, 4),
    Gesture(ACTION_SWIPE, D_LEFT, 4),
    Gesture(ACTION_SWIPE, D_RIGHT, 4),
    Gesture(ACTION_PINCH, D_IN, 4),
    Gesture(ACTION_PINCH, D_OUT, 4),
]

# initialize empty dict of gesture:animationPath
animation_files=dict()
for g in GESTURES_POSSIBLE:
    animation_files[str(g)] = os.path.realpath(os.path.dirname(__file__)) + \
        "/" + \
        'gesturesAnimations/'+ \
        str(g.fingers)+ \
        g.action+ \
        g.direction.capitalize()+ \
        '.gif'

# initialize empty gesture:command dict
gestures_list=dict()
for g in GESTURES_POSSIBLE:
    gestures_list[str(g)]=''

if not os.path.isfile(GM_CONF_FILE_PATH):
    out=open(GM_CONF_FILE_PATH, 'w')
    out.write(json.dumps(gestures_list))
    out.close()

def save_gm_conf_file():
    gestures_f=open(GM_CONF_FILE_PATH, 'w')
    gestures_f.write(json.dumps(gestures_list))
    gestures_f.close()

gestures_f=open(GM_CONF_FILE_PATH, 'r')

try:
    gestures_text=gestures_f.read()
    gestures_list=json.loads(gestures_text)
    gestures_f.close()
except ValueError:
    gestures_f.close()
    save_gm_conf_file()

def save_lig_conf_file():
    s=''
    for g in GESTURES_POSSIBLE:
        command=gestures_list[str(g)]
        if command != '':
            s+=g.build_gesture_string(command)
            s+='\n'
    lig_f=open(LIG_USER_CONF_FILE_PATH, 'w')
    lig_f.write(s)
    lig_f.close()

def build_xdotool_keystroke(keys):
    command=BASE_XDOTOOL_KEYSTROKE
    for key in keys:
        if keys.index(key) == 0:
            command+=key
        else:
            command+='+'+key
    return command

def add_gesture(gesture, command):
    gestures_list[str(gesture)]=command
    save_gm_conf_file()
    save_lig_conf_file()

def remove_gesture(gesture):
    gestures_list[str(gesture)]=''
    save_gm_conf_file()
    save_lig_conf_file()

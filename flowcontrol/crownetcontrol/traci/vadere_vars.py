from . import constants as tc


# control commands
# todo move to correct files
RESPONSE_CMD_CONTROLLER = 0x1D
VAR_REDIRECT = 0xFF
VAR_INIT = 0x00
CMD_FILE_SEND = 0x75
#  command: simulation state
CMD_SIMSTATE = 0x04
CMD_CONTROLLER = 0x06




# rename variable to match vadere versions
VAR_ID_LIST = tc.TRACI_ID_LIST
VAR_COUNT = tc.ID_COUNT
VAR_ADD = tc.ADD
VAR_POSITION_CONVERSION = tc.POSITION_CONVERSION

# New Vadere only commands and variables

# VaderePersonApi
VAR_HAS_NEXT_TARGET = 0x03
VAR_NEXT_TARGET_LIST_INDEX = 0x04
VAR_VELOCITY = 0x41
VAR_INFORMATION_ITEM = 0xFD
VAR_TARGET_LIST = 0xFE
VAR_POSITION_LIST = 0xFF
VAR_NEXT_ID = 0x02

# VaderePolygon
VAR_TOPOGRAPHY_BOUNDS = 0x02
VAR_CENTROID = 0x50

# VadereSimulationAPI
VAR_SIM_CONFIG = 0x7E
VAR_CACHE_HASH = 0x7D
VAR_DEPARTED_PEDESTRIAN_IDS = 0x74
VAR_ARRIVED_PEDESTRIAN_PEDESTRIAN_IDS = 0x7A
VAR_COORD_REF = 0x90
VAR_EXTERNAL_INPUT = 0x20
VAR_EXTERNAL_INPUT_INIT = 0x21
VAR_DENSITY_MAP = 0x22

# VadereMiscAPI
VAR_ADD_TARGET_CHANGER = 0x00
VAR_REMOVE_TARGET_CHANGER = 0x01
VAR_ADD_STIMULUS_INFOS = 0x02
VAR_GET_ALL_STIMULUS_INFOS = 0x03
#VAR_DISSEMINATION = 0x06

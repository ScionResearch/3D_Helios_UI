import os

HELIOS_BASE_DIR = f'{os.path.dirname(os.path.realpath(__file__))}{os.sep}helios-plusplus'
HELIOS_DATA_DIR = f'{HELIOS_BASE_DIR}{os.sep}data'
SCENE_UPLOAD_FOLDER = f'{HELIOS_BASE_DIR}{os.sep}'
HELIOS_SURVEY_DIR = f'{HELIOS_DATA_DIR}{os.sep}surveys'
HELIOS_SCENE_DIR = f'{HELIOS_DATA_DIR}{os.sep}scenes{os.sep}'
HELIOS_LOG_FILE = f'{HELIOS_BASE_DIR}{os.sep}helios-run.log'
HELIOS_BIN = f'{HELIOS_BASE_DIR}{os.sep}run{os.sep}helios'
HELIOS_WAYPOINT_FILE = f'{HELIOS_DATA_DIR}{os.sep}waypoint.xml'

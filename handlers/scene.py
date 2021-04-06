import glob
import xml.etree.ElementTree as et

import xmltodict

from constant import *

ALLOWED_EXTENSIONS = ['zip']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_scenes():
    scenes = []
    # root_dir needs a trailing slash (i.e. /root/dir/)
    for filename in glob.iglob(HELIOS_SCENE_DIR + '*.xml', recursive=True):
        scene_file = filename.split(os.sep)[-1]
        if scene_file.find('xml') != -1:
            scenes.append(scene_file.split('.')[0])
    return scenes


def get_scenes():
    return load_scenes()


def transform_scenes():
    for filename in glob.iglob(HELIOS_SCENE_DIR + '*.xml'):
        if filename.find('.xml') == -1:
            continue
        tree = et.parse(filename)
        for node in tree.iter('param'):
            if node.attrib['key'] == 'filepath':
                node.attrib['value'] = f"data/sceneparts{node.attrib['value'].split('data/sceneparts')[1]}"
        tree.write(filename, encoding="utf-8", xml_declaration=True)

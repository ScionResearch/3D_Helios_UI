import os
import xmltodict

from collections import OrderedDict
from constant import *


def load_platforms():
    with open(f'{HELIOS_DATA_DIR}/platforms2.xml') as fd:
        platforms = xmltodict.parse(fd.read())
    return platforms


def get_platforms():
    return load_platforms()


def save_platforms(form):
    # Initialize data structure
    doc = OrderedDict()
    doc['document'] = OrderedDict()
    doc['document']['platform'] = parse_form(form)
    write_to_file(doc)


def write_to_file(doc):
    with open(f'{HELIOS_DATA_DIR}{os.sep}platforms2.xml', 'w') as fd:
        fd.write(xmltodict.unparse(doc, pretty=True))


def parse_form(form):
    all_val = dict()
    for key, val in form.items():
        inferred = key.split('-')
        if len(inferred) == 3:
            if inferred[1] in all_val:
                all_val[inferred[1]][inferred[2]] = val
            else:
                all_val[inferred[1]] = dict()
                all_val[inferred[1]][inferred[2]] = val
        elif len(inferred) == 4:
            if inferred[2] in all_val[inferred[1]]:
                all_val[inferred[1]][inferred[2]][inferred[3]] = val
            else:
                all_val[inferred[1]][inferred[2]] = dict()
                all_val[inferred[1]][inferred[2]][inferred[3]] = val
        elif len(inferred) == 7:
            if inferred[3] in all_val[inferred[1]][inferred[2]]:
                temp_dict = OrderedDict()
                temp_dict[inferred[4]] = inferred[5]
                temp_dict[inferred[6]] = val
                all_val[inferred[1]][inferred[2]][inferred[3]].append(temp_dict)
            else:
                temp_dict = OrderedDict()
                temp_dict[inferred[4]] = inferred[5]
                temp_dict[inferred[6]] = val
                all_val[inferred[1]][inferred[2]][inferred[3]] = list()
                all_val[inferred[1]][inferred[2]][inferred[3]].append(temp_dict)

    return [OrderedDict(dict_val) for dict_val in all_val.values()]


def add_single_platform(platform):
    xyz_rot = ['x', 'y', 'z', 'rotations']
    xyz = ['x', 'y', 'z']
    platforms = load_platforms()
    platform_id = platform['@id']
    single_platform = OrderedDict()
    for key, val in platform.items():
        if len(key.split('-')) == 1:
            single_platform[key] = val

    single_platform['scannerMount'] = OrderedDict()
    for axis in xyz_rot:
        single_platform['scannerMount'][f'@{axis}'] = platform[f'scannerMount-@{axis}']

    single_platform['scannerMount']['rot'] = list()

    for axis in xyz:
        rot = OrderedDict()
        rot['@axis'] = axis
        rot['@angle_deg'] = platform[f'scannerMount-rot-@axis-{axis}-@angle_deg']
        single_platform['scannerMount']['rot'].append(rot)

    # add single platform
    platforms['document']['platform'].append(single_platform)
    write_to_file(platforms)
    return platform_id

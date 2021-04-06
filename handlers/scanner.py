import os
import xmltodict

from collections import OrderedDict
from constant import *


def load_scanners():
    with open(f'{HELIOS_DATA_DIR}{os.sep}scanners2.xml') as fd:
        scanners = xmltodict.parse(fd.read())
    return scanners


def get_scanners():
    return load_scanners()


def get_scanner(scanner_id):
    scanners = load_scanners()
    for scanner in scanners['document']['scanner']:
        if scanner['@id'] == scanner_id:
            return scanner


def save_scanners(form):
    # Initialize data structure
    doc = OrderedDict()
    doc['document'] = OrderedDict()
    doc['document']['scanner'] = parse_form(form)
    write_to_file(doc)


def write_to_file(doc):
    with open(f'{HELIOS_DATA_DIR}{os.sep}scanners2.xml', 'w') as fd:
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


def add_single_scanner(scanner):
    xyz = ['x', 'y', 'z']
    scanners = load_scanners()
    scanner_id = scanner['@id']
    single_scanner = OrderedDict()
    for key, val in scanner.items():
        if len(key.split('-')) == 1:
            single_scanner[key] = val

    single_scanner['headRotateAxis'] = OrderedDict()
    for axis in xyz:
        single_scanner['headRotateAxis'][f'@{axis}'] = scanner[f'headRotateAxis-@{axis}']

    single_scanner['beamOrigin'] = OrderedDict()
    for axis in xyz:
        single_scanner['beamOrigin'][f'@{axis}'] = scanner[f'beamOrigin-@{axis}']

    single_scanner['beamOrigin']['rot'] = list()

    for axis in xyz:
        beam = OrderedDict()
        beam['@axis'] = axis
        beam['@angle_deg'] = scanner[f'beamOrigin-rot-@axis-{axis}-@angle_deg']
        single_scanner['beamOrigin']['rot'].append(beam)

    # add single scanner
    scanners['document']['scanner'].append(single_scanner)
    write_to_file(scanners)
    return scanner_id

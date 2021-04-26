from collections import OrderedDict

import xmltodict
from constant import *

SURVEY_SETTINGS_FIELDS = ['survey-setting-@name',
                          'survey-setting-@scanner',
                          'survey-setting-@platform',
                          'survey-setting-@scene'
                          ]
SCANNER_SETTINGS_FIELDS = ['scanner-setting-@id',
                           'scanner-setting-@pulseFreq_hz',
                           'scanner-setting-@scanAngle_deg',
                           'scanner-setting-@scanFreq_hz',
                           'scanner-setting-@headRotatePerSec_deg',
                           'scanner-setting-@headRotateStart_deg',
                           'scanner-setting-@headRotateStop_deg',
                           'scanner-setting-@trajectoryTimeInterval_s',
                           'scanner-setting-@active']
WAYPOINT_PLATFORM_SETTINGS_FIELDS = ['waypoint-platform-{}-setting-@x',
                                     'waypoint-platform-{}-setting-@y',
                                     'waypoint-platform-{}-setting-@z',
                                     'waypoint-platform-{}-setting-@onGround',
                                     'waypoint-platform-{}-setting-@movePerSec_m']
WAYPOINT_SCANNER_SETTINGS_FIELDS = ['waypoint-{}-setting-@pulseFreq_hz',
                                    'waypoint-{}-setting-@scanAngle_deg',
                                    'waypoint-{}-setting-@scanFreq_hz',
                                    'waypoint-{}-setting-@headRotatePerSec_deg',
                                    'waypoint-{}-setting-@headRotateStart_deg',
                                    'waypoint-{}-setting-@headRotateStop_deg',
                                    'waypoint-{}-setting-@trajectoryTimeInterval_s',
                                    'waypoint-{}-setting-@active'
                                    ]
FWF_SETTINGS_FIELDS = ['@beamSampleQuality',
                       '@binSize_ns',
                       '@maxFullwaveRange_ns',
                       '@winSize_ns'
                       ]


def load_survey(survey):
    with open(f'{HELIOS_SURVEY_DIR}{survey}{os.sep}{survey}.xml') as fd:
        survey = xmltodict.parse(fd.read())
    return survey


def get_survey(survey):
    return load_survey(survey)


def save_survey(form):
    survey = parse_form(form)
    survey['survey']['@platform'] = f"data/platforms2.xml#{survey['survey']['@platform']}"
    survey['survey']['@scanner'] = f"data/scanners2.xml#{survey['survey']['@scanner']}"
    survey['survey']['@scene'] = f"data/scenes/{survey['survey']['@scene']}.xml#{survey['survey']['@scene']}"
    doc = OrderedDict()
    doc['document'] = OrderedDict()
    doc['document'] = survey
    survey_path = f"{HELIOS_SURVEY_DIR}{os.sep}"
    os.makedirs(survey_path, exist_ok=True)
    with open(f"{survey_path}{os.sep}{survey['survey']['@name']}.xml", 'w') as fd:
        fd.write(xmltodict.unparse(doc, pretty=True))

    return f"data/surveys/{survey['survey']['@name']}.xml"


def parse_form(form):
    # scanner_settings = OrderedDict()
    survey_settings = OrderedDict()
    fwf_settings = OrderedDict()
    legs = list()
    # for setting in SCANNER_SETTINGS_FIELDS:
    #     scanner_settings[setting.split('-')[2]] = form[setting]
    #     form.pop(setting)
    for survey_setting in SURVEY_SETTINGS_FIELDS:
        survey_settings[survey_setting.split('-')[2]] = form[survey_setting]
        form.pop(survey_setting)
    for fwf in FWF_SETTINGS_FIELDS:
        fwf_settings[fwf] = form[fwf]
        form.pop(fwf)

    keys = form.keys()
    idxs = list()
    for key in keys:
        splitted = key.split('-')
        if len(splitted) == 4:
            idxs.append(splitted[1])
        elif len(splitted) == 5:
            idxs.append(splitted[2])

    for idx in list(set(idxs)):
        temp = OrderedDict()
        temp['platformSettings'] = OrderedDict()
        temp['scannerSettings'] = OrderedDict()
        for waypoint_platform in WAYPOINT_PLATFORM_SETTINGS_FIELDS:
            temp['platformSettings'][waypoint_platform.split('-')[4]] = form[waypoint_platform.format(idx)]
        for waypoint_scanner in WAYPOINT_SCANNER_SETTINGS_FIELDS:
            temp['scannerSettings'][waypoint_scanner.split('-')[3]] = form[waypoint_scanner.format(idx)]
        legs.append(temp)

    survey = OrderedDict()
    #survey['scannerSettings'] = scanner_settings
    survey['survey'] = survey_settings
    survey['survey']['FWFSettings'] = fwf_settings
    survey['survey']['leg'] = legs

    return survey



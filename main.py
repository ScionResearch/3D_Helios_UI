import subprocess
import pathlib
import time
import zipfile, io
import shutil
from collections import OrderedDict

from flask import Flask, render_template, request, redirect, flash, send_file, Response, jsonify, make_response
from werkzeug.utils import secure_filename
from pygtail import Pygtail

from handlers.scanner import get_scanners, save_scanners, add_single_scanner
from handlers.platform import get_platforms, save_platforms, add_single_platform
from handlers.survey import save_survey
from handlers.scene import allowed_file, get_scenes, transform_scenes
from handlers.waypoint import get_waypoints
from constant import *

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024
app.secret_key = "super secret key"


@app.route('/')
@app.route('/index', methods=['post', 'get'])
def index():
    """if request.method == 'POST':
        pass"""
    return render_template('index.html')


@app.route('/survey', methods=['post', 'get'])
def survey():
    if request.method == 'POST':
        survey_file = save_survey(dict(request.form))
        run(survey_file)
        return Response('Survey was saved successfully')
    scanners = get_scanners()
    platforms = get_platforms()
    scenes = get_scenes()
    waypoints = get_waypoints()
    return render_template('survey.html', message={
        'scanners': scanners,
        'platforms': platforms,
        'scenes': scenes,
        'waypoints': waypoints
    })


def run(survey_file):
    kill_helios()
    pathlib.Path(HELIOS_LOG_FILE).unlink(missing_ok=True)
    pathlib.Path(f'{HELIOS_LOG_FILE}.offset').unlink(missing_ok=True)
    logfile = open(HELIOS_LOG_FILE, 'w')
    command = f'cd helios-plusplus; run/helios {survey_file}'
    subprocess.Popen(command, shell=True, stdout=logfile, stderr=logfile)


@app.route('/kill-helios')
def kill_helios():
    try:
        pids = subprocess.check_output(['pidof', 'run/helios'])
        pids = pids.decode().split()
        print(pids)
        for pid in pids:
            subprocess.run(['kill', '-9', pid])
    except subprocess.CalledProcessError:
        print('No process found')
        pass
    return Response('')


@app.route('/initial-logs')
def get_initial_logs():
    with open(HELIOS_LOG_FILE) as fd:
        content = fd.read()
    return Response(content)


@app.route('/log')
def progress_log():
    def generate():
        for line in Pygtail(HELIOS_LOG_FILE):
            yield "data:" + str(line) + "\n\n"
            time.sleep(0.2)
    return Response(generate(), mimetype='text/event-stream')


@app.route('/platform', methods=['post', 'get'])
def platform():
    if request.method == 'POST':
        ordered_form = OrderedDict(request.form)
        save_platforms(ordered_form)
        return redirect('/platform')
    platforms = get_platforms()
    return render_template('platform.html', platforms=platforms)


@app.route('/platform-async', methods=['post'])
def platform_async():
    single_platform = OrderedDict(request.form)
    platform_id = add_single_platform(single_platform)
    platforms = get_platforms()
    return jsonify({
        'platforms': dict(platforms),
        'id': platform_id
    })


@app.route('/platform-download')
def download_platform():
    return send_file(f'{HELIOS_DATA_DIR}{os.sep}platforms2.xml', as_attachment=True)


@app.route('/scanner', methods=['post', 'get'])
def scanner():
    if request.method == 'POST':
        ordered_form = OrderedDict(request.form)
        save_scanners(ordered_form)
        return redirect('/scanner')
    scanners = get_scanners()
    return render_template('scanner.html', scanners=scanners)


@app.route('/scanner-async', methods=['post', 'get'])
def scanner_async():
    if request.method == 'GET':
        scanners = get_scanners()
        return jsonify({'scanners': dict(scanners)})
    single_scanner = OrderedDict(request.form)
    scanner_id = add_single_scanner(single_scanner)
    scanners = get_scanners()
    return jsonify({
        'scanners': dict(scanners),
        'id': scanner_id
    })


@app.route('/entities')
def get_entites():
    scanners = get_scanners()
    platforms = get_platforms()
    return jsonify({'scanners': dict(scanners), 'platforms': dict(platforms)})


@app.route('/scanner-download')
def download_scanner():
    return send_file(f'{HELIOS_DATA_DIR}{os.sep}scanners2.xml', as_attachment=True)


@app.route('/scene', methods=['post', 'get'])
def scene():
    if request.method == 'POST':
        if 'file1' not in request.files:
            flash('No file part')
            return Response('Error: No file part', status=400)
        uploaded_file = request.files['file1']
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            flash('No selected file')
            return Response('Error: No selected file', status=400)
        if filename and allowed_file(filename):
            uploaded_file.save(os.path.join(SCENE_UPLOAD_FOLDER, filename))
            zip_reference = zipfile.ZipFile(os.path.join(SCENE_UPLOAD_FOLDER, filename), 'r')
            zip_reference.extractall(SCENE_UPLOAD_FOLDER)
            zip_reference.close()
            transform_scenes()
            scenes = get_scenes()
            return jsonify({
                'message': 'Scene was uploaded successfully',
                'scenes': scenes
            })
    scenes = get_scenes()
    return render_template('scene.html', scenes=scenes)


@app.route('/waypoint', methods=['post'])
def waypoint():
    if request.method == 'POST':
        if 'waypointFile' not in request.files:
            flash('No file part')
            return Response('Error: No file part', status=400)
        uploaded_file = request.files['waypointFile']
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            flash('No selected file')
            return Response('Error: No selected file', status=400)
        uploaded_file.save(os.path.join(HELIOS_DATA_DIR, 'waypoint.xml'))
        return Response('Upload was successful')


@app.route('/download_helios_output/<survey_name>')
def download_helios_output(survey_name):
    dir_name = f'{HELIOS_OUTPUT}{os.sep}{survey_name}'
    shutil.make_archive(survey_name, 'zip', root_dir=HELIOS_BASE_DIR, base_dir=dir_name)
    return send_file(f'{survey_name}.zip', mimetype='application/zip', as_attachment=True)


if __name__ == '__main__':
    host = "localhost"
    if os.environ.get('ENV') == 'PROD':
        host = "0.0.0.0"
    app.run(host=host, port=5000, debug=1)

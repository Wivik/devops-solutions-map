from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask_frozen import Freezer
from flask_wtf.csrf import CSRFProtect
import argparse
import json
import markdown
import os
import pathlib
import sys
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['TEMPLATES_AUTO_RELOAD'] = True
csrf = CSRFProtect()
csrf.init_app(app)
freezer = Freezer(app)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', '--freeze', dest='freeze_mode', action='store_true', default=False, help='Produce a static website instead of starting the web server')
arg_parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='Enable Flask debug mode')
arg_parser.add_argument('--host', dest='host', action='store', default='127.0.0.1', help='Host exposition. Set 0.0.0.0 for outside localhost.')
arg_parser.add_argument('-p', '--port', dest='port', action='store', default='5000', help='Expose port (default 5000)')
args = arg_parser.parse_args()

## solutions file is expected to be an env var
## defaulting to solutions.yaml

if os.environ.get('DEVOPS_SOLUTIONS_FILE'):
    solutions_file_name = os.environ('DEVOPS_SOLUTIONS_FILE')
else:
    solutions_file_name = 'solutions.yaml'

app_path = pathlib.Path(__file__).parent.absolute()
data_path = os.path.join(app_path, 'data')
solutions_file = os.path.join(data_path, solutions_file_name)

if not os.path.exists(data_path):
    print('Data path missing, creating directory')
    try:
        os.mkdir(data_path)
    except:
        print('Could not create data dir')
        raise

## here we go

def markdown_filter(text):
    return markdown.markdown(text, extensions=['markdown.extensions.tables', 'markdown.extensions.fenced_code', 'markdown.extensions.codehilite'])

app.jinja_env.filters['markdown'] = markdown_filter


def test_solutions_file(solutions_file):
    if os.path.exists(solutions_file):
        return True
    else:
        return False

def read_solutions(solutions_file):
    """load the whole content of the file and return it"""
    with open(solutions_file, 'r') as file:
        solutions_content = yaml.load(file, Loader=yaml.FullLoader)
    return solutions_content

def get_tool_usage(search_tool, solutions):
    tool_usage = []
    for side in solutions['sides']:
        for step in side['steps']:
            for usecase in step['usecases']:
                for tool in usecase['tools']:
                    if tool['name'] == search_tool:
                        # test optional keys
                        try:
                            uc = usecase['name']
                        except KeyError:
                            uc = None
                        try:
                            isnew = tool['isnew']
                        except KeyError:
                            isnew = None
                        tool_usage.append({
                            'step': step['name'],
                            'side': side['name'],
                            'state': tool['state'],
                            'uc': uc,
                            'isnew': isnew,
                        })
    return tool_usage

## render main template

@app.route("/")
def main(side=None, step=None):

    if not test_solutions_file(solutions_file):
        return render_template('no-file.html.j2')

    solutions_content = read_solutions(solutions_file)
    devops_content = solutions_content['devops']

    return render_template('main.html.j2', devops_content=devops_content)

@app.route("/tool/<string:tool>.html")
def tool_view(tool):

    if not test_solutions_file(solutions_file):
        return render_template('no-file.html.j2')

    solutions_content = read_solutions(solutions_file)
    devops_content = solutions_content['devops']
    tool_content = None
    for entry in solutions_content['tools']:
        if entry['name'] == tool:
            tool_content = entry

    tool_usage = get_tool_usage(tool, devops_content)

    return render_template('tool.html.j2', tool_content=tool_content, tool_usage=tool_usage)

@app.route("/about.html")
def about():

    changelog = open(os.path.join(app_path, 'CHANGELOG.md'), 'r')
    changelog_content = markdown.markdown(changelog.read())

    data_spec_file = open(os.path.join(app_path, 'data-format.md'), 'r')
    data_spec = markdown.markdown(data_spec_file.read(), extensions=['markdown.extensions.tables', 'markdown.extensions.fenced_code', 'markdown.extensions.codehilite'])

    version_file = open(os.path.join(app_path, 'version_file.json'), 'r')
    version = json.load(version_file)
    version = str(version['version'])

    return render_template('about.html.j2', changelog_content=changelog_content, version=version, data_spec=data_spec)

if __name__ == '__main__':
    if args.freeze_mode:
        freezer.freeze()
    else:
        Flask.run(app, debug=args.debug, port=args.port, host=args.host)

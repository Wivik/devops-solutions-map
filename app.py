from flask import Flask
import os
from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
import pathlib
import sys
import yaml


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['TEMPLATES_AUTO_RELOAD'] = True
csrf = CSRFProtect()
csrf.init_app(app)

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
        os.path.mkdir(data_path)
    except:
        print('Could not create data dir')
        raise



## here we go

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

@app.route("/tool/<string:tool>")
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

@app.route("/about")
def about():
    return render_template('about.html.j2')

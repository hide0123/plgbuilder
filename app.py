import os
from flask import Flask, url_for, render_template, request
from github import Github

app = Flask(__name__)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    
    g = Github(os.environ['GITHUB_API'])
    repo = g.get_repo('HIDE810/plgbuilder')
    user = request.form['user']
    name = request.form['name']
    menu = request.form['menu'].replace('"', r'\"')
    code = request.form['code'].replace('"', r'\"')
    repo.create_repository_dispatch(user, {"name":name,"menu":menu,"code":code})
    
    return render_template('result.html')

if __name__ == '__main__':
    app.run()
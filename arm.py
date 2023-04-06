from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    users = requests.get('http://localhost:5000/users').json()['users']
    spl = lambda A, n=5: [A[i:i+n] for i in range(0, len(A), n)]
    users = spl(users)
    return render_template('index.html', users=users)
@app.route('/<int:id>')
def upage(id):
    r = requests.get(f'http://localhost:5000/get/id/{id}').json()
    link = r['link']
    code = r['code']
    return render_template('upage.html', link=link, code=code, id=id)
    
app.run(port=8080)
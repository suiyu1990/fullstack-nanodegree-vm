# Game Catalog Web App
This web app is the fourth project for the Udacity Full Stack web Developer Nanodegree

## About
The web applicaton is a game catalog for a gaming enthusiast, which supports create, read, update and delete function (CRUD).  This project is a RESTful web application utilizing the Flask framework which accesses a SQL database for data storage. OAuth2 provides authentication and is implemented for Google Accounts.  

## In The Project Folder
This project has one main Python module `project.py` which runs the Flask application. A SQL database is created using the `database_setup.py` module and you can initialize the database using `database_init.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application. The CSS and image files are stored in the static folder.

## Software Requirement
Vagrant, Virtualbox, Flask, SQLalchemy, python2.7

## Software Installation
1. Install Vagrant & VirtualBox, clone the udacity Vagrant file and launch the vagrant VM (`vagrant up`) and (`vagrant ssh`)
2. Download and place the file in the vagrant directory
3. Navigate to `cd/vagrant` from the vagrant top directory
4. Setup the database `python database_setup.py`
5. Insert some test data data `python database_init.py`
6. Run application using `python project.py`
7. Access the application locally using http://localhost:8000

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com), sign in
2. Go to Credentials
3. Select Create Crendentials > OAuth Client ID
4. Select Web application
5. Enter name 'Game-Catalog' or other arbitrary name
6. Authorized JavaScript origins = 'http://localhost:8000'
7. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
8. Select Create
9. Copy the Client ID and paste it into the `data-clientid` in login.html
10. Download JSON file
11. Rename JSON file to client_secrets.json
12. Place JSON file in the game catalog directory
13. Run application using `python python.py`

## JSON Endpoints
The following are open to the public:
Categories JSON: `/category/JSON`
    - Displays all game categories

Category Games JSON: `/category/<int:category_id>/game/JSON`
    - Displays games for a specific game category

Category Game JSON: `/category/<int:category_id>/game/<int:game_id>/JSON`
    - Displays a specific category game.

# Assignment2-Cloud
This project is a simple-ish website inspired by Reddit-like forum sites. Building on OpenStack (Chameleon Cloud) using Docker and DockerCompose to an extent.

## How to setup locally
Without dockerizing the application, you can setup the application locally:

- Add your connection to your local SQL server f.ex: "root@localhost/fakeredditdb" or "root:root@localhost/fakeredditdb" if you have a password.
Found on this line in app.py: "app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/fakeredditdb'"

- Copy the sql schema from /database/init.db.
- Open up the sql server locally on your machine, and run the schema as a query.
- CD to ./app.
- Run python app.py.
- Open the flask in the browser.
- Register a new user and login.

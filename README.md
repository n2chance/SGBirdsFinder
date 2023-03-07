# SGBirdsFinder

## About

A web app to identify birds in Singapore based on their features.

## Features

- Identify a bird by answering at most 5 questions
- Browse through the database of 400+ birds
- View detailed information about each bird
- Admin page for editing the database of birds

## Usage

Go to the [website](https://jycx50.pythonanywhere.com). Refer to the about page for help.

For admin login, the username is `admin-kgi` and the password is `iFE79iUd45`

## Project Structure

```text
.
├── app
│   ├── admin.py
│   ├── app.py
│   ├── auth.py
│   ├── Birds.db
│   ├── Birds.sql
│   ├── browse.py
│   ├── errors.py
│   ├── general.py
│   ├── identify.py
│   ├── static
│   │   ├── sass
│   │   │   └── styles.scss
│   │   └── stylesheets
│   │       └── styles.css
│   ├── templates
│   │   ├── admin
│   │   │   ├── dashboard.html
│   │   │   ├── delete_bird.html
│   │   │   ├── new_bird.html
│   │   │   └── update_bird.html
│   │   ├── auth
│   │   │   └── login_page.html
│   │   ├── base.html
│   │   ├── browse
│   │   │   └── browse_birds.html
│   │   ├── errors
│   │   │   ├── page_not_found.html
│   │   │   └── server_error.html
│   │   ├── general
│   │   │   ├── about.html
│   │   │   └── index.html
│   │   ├── identify
│   │   │   ├── identify_bird.html
│   │   │   ├── no_birds.html
│   │   │   └── possible_birds.html
│   │   └── viewbird
│   │       ├── bird_info.html
│   │       └── bird_not_found.html
│   └── viewbird.py
├── Birds.db
├── package.json
├── package-lock.json
├── README.md
├── requirements.txt
└── setup.py
```

The app is split into 7 main parts or features:

- Administering the database (admin)
- Authentication of admin (auth)
- Browsing the database of birds (browse)
- Handling errors which could occur, e.g: 404 (errors)
- General information about the app/static pages (general)
- Identification of a bird (indentify)
- Viewing more information about a particular bird (viewbird)

Each main part has a corresponding Flask blueprint and folder with Jinja template(s).

## Prerequisites

### Python

A virtual environment is recommended to be installed.
To run the app locally, the Python 3 must be installed, along with the following modules:

- flask
- python-dotenv
- requests

To do so, run:

```bash
pip install -r requirements.txt
```

### npm

Optionally, npm and the following npm dependencies can be installed to generate the CSS file from the sass file:

- bulma
- node-sass

To do so, run:

```bash
npm install
```

The following npm scripts `css-build` and `start` are included to build the CSS and automatically watch for changes respectively

```bash
npm run css-build
npm start
```

## Running

If the app is running for the first time, run the `setup.py` script, and select "y" for both questions. The script generates and prints the admin credentials and initialises the database `Birds.db` from the `Birds.sql` file. It can also be run to reset the data in the database.

Finally, run `app.py` to start the web app.

```bash
python3 setup.py
python3 app/app.py
```

## Credits

- [The Singapore Birds Project](https://singaporebirds.com/) - Database of local birds
- [Bulma](https://bulma.io/) - CSS framework

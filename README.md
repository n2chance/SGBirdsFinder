# SGBirdsFinder

## About

A web app to identify birds in Singapore based on their features.

## Features

- Identify a bird by answering at most 5 questions
- Browse through the database of 400+ birds
- View detailed information about each bird, including their photos
- Admin page for editing the database of birds

## Usage

Go to (website). Refer to the about page for more usage instructions.

## Project Structure

```text
.
├── app
│   ├── app.py
│   ├── auth.py
│   ├── browse.py
│   ├── errors.py
│   ├── general.py
│   ├── identify.py
│   ├── static
│   │   ├── sass
│   │   │   └── styles.scss
│   │   └── stylesheets
│   │       └── styles.css
│   ├── templates
│   │   ├── auth
│   │   │   └── login_page.html
│   │   ├── base.html
│   │   ├── browse
│   │   │   └── browse_birds.html
│   │   ├── errors
│   │   │   ├── page_not_found.html
│   │   │   └── server_error.html
│   │   ├── general
│   │   │   ├── about.html
│   │   │   └── index.html
│   │   ├── identify
│   │   │   ├── identify_bird.html
│   │   │   ├── no_birds.html
│   │   │   └── possible_birds.html
│   │   └── viewbird
│   │       ├── bird_info.html
│   │       └── bird_not_found.html
│   └── viewbird.py
├── Birds.db
├── package.json
├── package-lock.json
├── README.md
└── scripts
    └── generate-credentials.py
```

The app is split into 7 main parts or features:

- Administering the database (admin)
- Authentication (auth)
- Browsing the database of birds (browse)
- Handling errors which could occur, e.g: 404 (errors)
- General information about the app (general)
- Identification of a bird (indentify)
- Viewing more information about a particular bird (viewbird)

Each main part has a corresponding Flask blueprint and template(s).

## Running

To run the app locally, the Python 3 should be installed, along with the Flask module.

The following npm dependencies should also be installed to generate the CSS file:

- bulma
- node-sass

Finally, run `app.py` from the app folder.

## Credits

- [The Singapore Birds Project](https://singaporebirds.com/) - Database of local birds
- [Bulma](https://bulma.io/) - CSS framework

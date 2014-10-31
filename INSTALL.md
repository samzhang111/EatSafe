# Local installation instructions

1. Clone this repo

2. Download the eatsafe database dump of [version 0.1](https://drive.google.com/file/d/0Bym3PguSObjFOC1hZEY3dkd0bW8/view?usp=sharing) and load it into postgres. This involves installing postgres, and running

    `sudo -u postgres psql -e 'CREATE DATABASE eatsafe'`

    `psql eatsafe < eatsafe.sql`

3. Configure environment variables. Specifically, you need:
    - DATABASE\_URL, the postgres configuration variable that points to the database,
    - GOOGLE\_PLACES\_KEY, a Google Places API key, and
    - YELP\_KEY, a Yelp API key.

Neither Google Places nor Yelp are being used on this current branch, so that is some garbage that needs to get cleaned up. Sorry.

4. (Optional) Install virtualenv. Create a virtual environment for this project, and activate it.

5. Install the requirements.py file (`pip install -r requirements.txt`)

6. Run python run.py

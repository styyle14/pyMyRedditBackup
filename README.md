# pyMyRedditBackup
Python Library and Tools to Backup Personal Saved and Upvoted Posts and Comments

---
## User Guide
#### User Setup
This package currently supports Python versions 3.7 and 3.8.

It is recommended that you use the latest versions pip, venv, and poetry. These can be installed on an Ubuntu 18.04 system as follows:

`sudo apt install git python3.7 python3.7-venv`

or

`sudo apt install git python3.8 python3.8-venv`

then

`python3 -m pip install --user --upgrade pip poetry testresources`

### User Installation
To install this package, then run:

`python3 -m pip install --user --upgrade git+https://github.com/styyle14/pyMyRedditBackup.git`

### Usage
Usage has yet to be defined.

---
## Developer Guide
### Developer Setup
Please follow all steps in the above "User Setup" section. Note that you must have both Python versions 3.7 and 3.8 installed to run `tox` before making pull requests.

### Developer Source Installation
Clone down the repo:

`git clone https://github.com/styyle14/pyMyRedditBackup.git`

`cd pyMyRedditBackup`

Create your development venv:

`python3 -m venv .venv`

`source .venv/bin/activate`

Install the package into you venv:

`poetry install`

### Development Steps
Make changes to code.

Test changes locally.

Validate with tox:

`tox`

Submit pull request.

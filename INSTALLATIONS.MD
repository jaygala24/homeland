# Steps for Project Setup

### Requirements
* __Django 2__
* __Python 3__


### Installation
* Clone the repository using `git clone https://github.com/jaygala24/homeland.git`
* Then go to the homeland folder using `cd homeland`
* Create the virtual environment using `virtualenv -p python3 .`
* Activate the virtual environment using `source bin/activate`
* Install all the dependencies using `pip3 install -r requirements.txt`
* Then go to the src folder using `cd src`
* Then makemigrations using `python manage.py makemigrations`
* Then migrate the database using `python manage.py migrate`
* Run the server using `python manage.py runserver`

You are all setup to use the web app..

> Note => Use your EMAIL and PASSWORD in the settings.py for Email Config 

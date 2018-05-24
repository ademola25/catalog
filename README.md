# Spa Item Catalog

## Project Description
To develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
I have a Spa Business so i decided to do this for my real life business, name of my spa is HEADLINES BARBING LOUNGE, The real logo was used in the project.

## Technologies used
- Python      - Flask
- HTML        - Google Login
- CSS         - SQLAchemy
- OAuth       - Bootstrap


## Project Setup:
This project is run on a virutal machine created using Vagrant:
#### Installing the dependencies and setting up the files:
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)

# How to install
1. Install Vagrant and VirtualBox
2. Clone the Vagrantfile from Udacity Repository
3. cd into vagrant directory and Clone  or download this repo 
4. vagrant up to start up the VM.
5. vagrant ssh to log into the VM.
6. cd /vagrant to change to your vagrant directory.
7. `python application.py` to run the application within its directory
8. To access Application `http://localhost:8000/spacategory` 

## Uses Google Auth to authenticate users and  generating of client_secrets.json,

* First Create a project on [developers.google.com](https://console.developers.google.com/), i named mine Headline Spa.
* Go to Credentials and select "Add Credentials" click on  "OAuth (v2) token". Choose `Web`.
* you should have `http://localhost:8000` in authorized JavaScript origins and `http://localhost:8000/gconnect` in Redirect URIs.
* Get your client ID and client secret.
* All this will be in the application.py file.

      Generating client_secrets.json.
 * client on the credential
 * then click on edit,
 * Finally click on DOWNLOAD JSON to copy..
 * create a file named client_secrets.json and then paste DOWNLOADED JSON copied inside.
     
## JSON EndPoints to view Spa Category Information
 * To display all Spa Categories:   /spacategory/JSON'
 * To display all spa Item in Details: /spacategory/<int:categories_id>/spaitem/JSON

# License
Project is released under the [MIT License](http://opensource.org/licenses/MIT).

## References:

https://www.linuxquestions.org/questions/programming-9/flask-google-sign-in-problem-4175609886/

http://jinja.pocoo.org/docs/2.10/templates/#include

https://github.com/googleplus/gplus-quickstart-python/blob/master/signin.py

https://www.reddit.com/r/learnpython/comments/3gh7lu/keep_running_into_typeerror_int_object_is_not/

http://docs.sqlalchemy.org/en/latest/core/tutorial.html

https://stackoverflow.com/questions/29549714/python-form-drop-down-options-populated-by-sql

https://stackoverflow.com/questions/43445027/populate-dropdown-from-mysql-database-python?rq=1

https://stackoverflow.com/questions/25925024/how-to-delete-items-from-database-using-a-flask-framework

https://www.w3schools.com/html/tryit.asp?filename=tryhtml_elem_select

https://www.ntu.edu.sg/home/ehchua/programming/webprogramming/Python3_Flask.html#zz-3.6

https://www.sitepoint.com/responsive-fluid-width-variable-item-navigation-css/

https://www.w3schools.com/html/tryit.asp?filename=tryhtml_elem_textarea

https://stackoverflow.com/questions/29144972/make-that-my-categories-displays-each-respective-content-isolatedly

https://docs.python.org/3/genindex-Symbols.html

https://stackoverflow.com/questions/10407433/how-do-i-get-my-html-button-to-delete-the-right-list-item-from-a-sqlite-database

http://learnlayout.com/inline-block-layout.html



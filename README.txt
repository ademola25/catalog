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

## JSON EndPoints to view Spa Category Information
To display all Spa Categories: /spacategory/JSON'
To display all spa Item in Details: '/spacategory/<int:categories_id>/spaitem/JSON


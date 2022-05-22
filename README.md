## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/abhishek-dhanraj-TI/JTU-2K22-BestPractices-abhishekdhanraj.git
$ cd JTU-2K22-BestPractices-abhishekdhanraj
```

## Method 1: Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
Make migrations to the db and run the server
```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

## Method 2: Build the Docker Image and run the container.
```sh
$  docker build -t <image-name> .
$  docker run -p 8080:8080 <image-name>
```
# Instructions
This assignment consists of a django-rest-framework app that has several violations of common best practices.
The assignment is mostly open-ended, just like the definition of what exactly is a best practice and what's not 😉

Fork this repository and make a new branch named jtu-2k22-<ad_username>, fix as many best practices violations as you can find and make a PR, and assign kushal-ti as the reviewer.

If you don't know anything about django-rest-framework don't worry. You don't have to run the project or make any changes that requires knowledge intimate knowledge of django-rest-framework

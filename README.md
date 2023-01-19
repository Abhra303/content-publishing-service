# Micro-Service Architechture - A Content Publishing Service

This is a microservice assignment project made with Django, Django-rest-framework and DRF_simplejwt. Its primary objective is to serve contents. This is simple and focuses more on micro-service architechture.

## Architechture

The project has three micro-services. These are -

 - **User/Auth Service:** This service handles all the authentication related
 operations. Responsible for providing CRUD APIs for Users. It also exposes endpoints for login, token-verification and token refreshment.
 - **User Interaction Service:** This service is responsible for handling user interactions in any content. Two types of Interactions are recognized here - Read and Like. It also exposes an internal-api to sort contents on the basis of most interactions.
 - **Content Service:** This is the main service of the project. It handles requests to create, update, get and delete contents. Provides CRUD APIs for content. It also exposes two additional endpoints - one for `new-content` and another for `top-content`. The Top content view internally consults the User Interaction Service to get the Ids of top contents in sorted order.

 Below is the diagram of the project architechture:

 ![project architechture](/assets/project_architechture.png)

 However the NGNIX Gateway is not properly set up yet. So for now, you have to go to each port and make requests. But I will soon fix the NGINX in dev branch. So stay tuned! 

 **[EDIT] FINALLY NGINX API GATEWAY (RUNNING IN DOCKER CONTAINER) IS FIXED. YOU CAN NOW ADD PREFIX TO THE BELOW MENTIONED APIS. THE NGINX PORT IS AT `8000`**


## Design Overview
This project consists of three micro-services. Every service has their own codebase. Throughout the building process of this project, I ensured that the project follow DRY rule strictly. The services communicate with themselves when necessary (e.g. `content_service` needs `user_interaction_service` for getting `top-contents` information on the basis of most number of interactions. For content-service, one can create content without using drf APIs. `content-service` has a command (`python3 manage.py upload_csv <csv_file_path>`) using which you can create contents from csv files. Content service provides a test API (`books/upload-csv`) that receives csv file as request body and internally calls the `upload_csv` command to create instances.

## Low Level Design

The `content-service` stores data in database with the following columns.
 - id (id of the content)
 - title
 - author (author user id)
 - description (optional)
 - story
 - published_date (automatically calculated)
 - updated_on (automatically calculated)

Note that neither `content_service` nor `user_interaction_service` use django's default Users. It uses tokens to validate the authentication of an user (more on this later). The `author` field is simply a positive integer field.

`content_service` has lots of APIs to interact with it. It provides CRUD APIs on `book` model. The API endpoints are mentioned in `API docs` section. There are three additional APIs. Two of them are List APIs i.e. the sends back a list of contents. `book/upload-csv` API is a special API that can receive csv files. It then creates book instances by parsing the csv file.

`user_interaction_service` stores data related to content interaction (like read and like). The table columns are -
 - id
 - user_id
 - type ('R' for Read, 'L' for Like)
 - content_id
 - timestamp (datetime)

It has two event based APIS (`read/` and `like/`) that are used to register read and like events. There is another endpoint (`contents/books/top-contents/`) which is meant to be used only by `content_service` (to sort book instances on the basis of user interactions).Note that duplicate rows are not allowed. As mentioned previously, user_id and content_ids are just positive integer numbers (instead of Foreign Key).

The `User` service is the service that stores all user/authentication related data. Some important table columns are - 
- id
- email_id
- first_name
- last_name
- phone_no

It provides an endpoint named 'login/' (POST method) where existing users can get access token and refresh token as response. This access token can then be used to authenticate accross different services. It also has a `user/create` endpoint to register new users (NOTE that only anonymous users can register for a new user).

### Authentication accross different micro-services
As I mentioned earlier that once an user get the access token, it can use this access token to authenticate accross different micro-services. But how? Is this logic replicated for each non-auth service (i.e. `content_service` and `user_interaction_service`)?

The answer is NO, I took a tough stance for following DRY rule. I ensured that all the services are 'copied-code' free. Here `auth_sdk` comes into picture. It is a python package (developed by me) that handles all the auth related communication between the `user_service` and other services. With this, services don't have to worry about authentications; nor they have to write/implement code. This package handles all by itself. All they have to do is that they have to mention `auth_sdk`'s authentication class and permission class in `rest_framework`'s settings.

If you used requirements.txt files (for each service) to download required packages, `auth_sdk` is already installed in your virtual-env/local-machine. Both `content_service` and `user_interaction_service` has specified `auth_sdk.authentication.UserAuthentication` as the default Authentication class for `rest_framework`. They also used `auth_sdk.permissions.IsAuthenticatedOrReadOnly` permission class as the default permission class.

`auth_sdk` looks for bearer access token in the header of the request. If an access token is found, `auth_sdk` will make a verify request to `user_service` to check whether the token is valid. If it is valid then `auth_sdk` will set `request.META['user_id']`. The permission class use this value to check whether the user is authenticated or not.

## API docs

Note that, all POST, PATCH, DELETE methods require a bearer access token to validate authentication.

### content-service

If you are want to send request using NGINX server, you can use the following prefix `/api/content/` to the below APIs e.g. `localhost:8000/api/content/books/` (GET method) will give the same result as below.

#### [GET] books/
Get the list of books

#### [POST] books/

request.body -
```json
{
	"title": string,
	"description": string, # optional
	"story": string
}
```

#### [PATCH] books/

request.body - 
```json
{
	"title": string, # atleast one field required to make patch request
	"description": string,
	"story": string
}
```

#### [GET] books/\<content-id>/
Get content data of content having id = \<content-id>

#### [DELETE] books/\<content-id>/
delete the content specified by \<content-id>


#### [GET] books/new-contents/
Get contents in the most recent sort order

#### [GET] books/top-contents/
Get contents sorted in the order of most interactions

#### [POST] books/upload-csv
Parse the given csv file and create instance from csv data.
The request content-type should be multipart/formdata or something. The key for the csv file is "csv_file". Only one key is valid (i.e. "csv_file"). It needs nothing else in request.body. The csv file should be a valid csv file and each
row should contain `title string, author_id, description (optional), story`.

### User Interaction Service

NGINX server route prefix - `/api/user-interaction/` e.g. you can use `localhost:8000/api/user-interaction/like` to do the same job as below one.

#### [POST] /like
register a like event on the content_id specified in request.body

request.body - 
```json
{
	"content_id": int
}
```

#### [POST] /read
register a read event on the content_id specified in request.body

request.body -
```json
{
	"content_id": int
}
```

### User Service

NGINX server prefix - `/api/auth/` e.g. you can use `localhost:8000/api/auth/users/` to get the list of users as mentioned below.

#### [GET] users/
Get the list of all users

#### [GET] users/\<user-id>/
retreive details about the specified \<user-id>

#### [PATCH] users/\<user-id>

updates some columns in the user with user id \<user-id>

request.body - 
```json
{
	"first_name": string, # atleast one is required
	"last_name": string,
	"phone_no": string,
}
```

#### [DELETE] users/\<user-id>/
Deletes the specified user

#### [POST]  users/create
Creates new user. (Only valid for unauthenticated users)

request.body - 
```json
{
	"email_id": string, # valid-email
	"first_name": string,
	"last_name": string,
	"password": string,
	"phone_no": string,
}
```

#### [POST] login/

gives access token and refresh tokens as response. It doesn't require any bearer token in header.

request.body -
```json
{
	"email_id": string,
	"password": string,
}
```

#### [POST] refresh-token/
gives a new set of access token and refresh token

request.body -
```json
{
	"refresh": string
}
```
## Get Started

To install in a local machine, you can either fork it and then clone the forked repo's url to your local machine:
```bash
git clone https://github.com/<your-username>/pr-assign.git
```

Or you can directly clone my repository:
```bash
git clone https://github.com/Abhra303/pr-assign.git
```

There are two options to run the application on your local machine - with docker and without docker

## With docker
It is the easiest and the recommended method to run the application. 

### Pre-Requistics - 
You need to have docker and docker-compose installed(installing docker desktop will install both tools)

### Procedure - 
Open your terminal and type `sudo docker-compose up`. That's it! You will see that three services have started running after some time. So, now you can access the services on `127.0.0.1:8001/`, `127.0.0.1:8002/` and `127.0.0.1:8003/`. Therefore, you can start querying APIs (see below) offered by these services.

## Without docker - 
This procedure is little bit complex compared to the previous one and can produce `Works on my computer` type errors. So be ready to solve those.
Note that each services has their own django project i.e. they don't depend on each other in terms of their project structure, written codes or modules. Each of the services has their own requirements.txt, manage.py and projects and apps created by django-admin. That's why you have to repeat the same process every time.
Let's take an example of content-service. To run the content-service, create a virtual environment first.

### creating a virtual enviornment
You have to create a virtual enviornment for your project so that the python dependencies do not create conflicts due to different versions of same package. To create a virtual enviornment run the following commands - 
```bash
cd content-service/
python -m venv venv
```
**Note: The above command is for windows. In linux/unix you have to write `python3` instead of python**
This will create a virtual enviornment named `venv`. While creating virtual enviornment, make sure you named it as `venv`. Git will automatically ignore it.
### activate the virtual environment
Before running any other command, first activate the virtual environment. The command for activating the `venv` is different across different OS. For windows, run `venv/Scripts/activate` on the terminal, `source venv/bin/activate` for the rest of others.
### install python dependencies 
Run the following command to install all python package requirements - 
```bash
pip install -r requirements.txt
```

### run content-service

Now that you have installed the dependencies, Run command `python3 manage.py migrate && python3 manage.py runserver 127.0.0.1:8003`. It will start the server.

Repeat the process for user_service/ and user-interaction-service/.

## Future Goals

1. I tried to use NGINX as API Gateway that can route urls to different services based on the url prefix. But I didn't get enough time to make it work. In future, I would like to use NGINX as API Gateway.

2. Currently the databases are using simple sqlite. Instead I should use mysql database.
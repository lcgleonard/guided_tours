# guided_tours
Social media platform for uploading and accessing guided tour content based on location

## Installation
This application requires Vagrant which can be downloaded here:
https://www.vagrantup.com/downloads.html
"Vagrant is an open-source software product for building and maintaining portable virtual software development environments"

Vagrant has a dependency on VirtualBox which can be downloaded here:
https://www.virtualbox.org/wiki/Downloads

## How to run
```
cd guided_tours/vagrant/
vagrant up
vagrant ssh
```
Note: that `vagrant up` will create a new virtual machine (an Ubuntu 16.04 image) and install application dependencies
such as Docker, NodeJS, Python3.6 NPM, make, etc.  See Vagrantfile and script.sh located inside the vagrant directory
for further details.

## Accessing the virtual machine
The virtual machine can be accessed with the command `vagrant ssh` from inside the vagrant directory.

NOTE: if accessing the machine via Virtualbox, the username to log in is "vagrant" and the password is "vagrant"
## Creating the database
The database used here is PostgreSQL running inside a Docker container.  When you first create the virtual machine, you
must next create the database.  Use the following commands to access the PostgreSQL Docker container and create the database:
```
docker exec -it apostgres psql -U postgres
CREATE DATABASE guided_tours;
\l  # to confirm "guided tours" db has been created
\q  # to exit
```

### Configuration

The following line must be updated in ./vagrant/Vagrantfile.  "/home/lorcan/development/" is where the guided_tours repo
was stored on my machine:
`  config.vm.synced_folder "/home/lorcan/development/guided_tours/src", "/home/vagrant/src"`

All application config is stored in the config directories inside the repo.  There is no need to change any application
config. 

## Starting the applications
```
# Start the client SPA
cd ~/src/client && npm start

# Start the Proxy Server
cd ~/src/proxy && source venv/bin/activate && python main.py

# Start the REST API
cd ~/src/api && make start

# Start the database
docker start apostgres

# Start the cache
docker start aredis
```

## Stopping the applications
```
# Stop the client SPA
Ctrl+C

# Stop the Proxy Server
Ctrl+C

# Stop the REST API
cd ~/src/api && make stop

# Stop the database
docker stop apostgres

# Stop the cache
docker stop aredis
```

### Web Architecture
[Architecture Diagram](https://github.com/lcgleonard/guided_tours/blob/master/architecture_diagram.png)

* Client-Side Single Page App
    * React using [React Router](https://github.com/ReactTraining/react-router#readme)
* Server-Side Proxy Server
    * Python using Tornado
    * "[Tornado](https://www.tornadoweb.org/en/stable/) is a Python web framework and asynchronous networking library...
    By using non-blocking network I/O, Tornado can scale to tens of thousands of open connections, making it ideal for
    long polling, WebSockets, and other applications that require a long-lived connection to each user."
* Server-Side REST API
    * Python using [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) running inside a Docker container
* Relational Database
    * PostgreSQL running inside a Docker container
* Cache
    * Redis running inside a Docker container
    * "[Redis](https://redis.io/)  is an open source (BSD licensed), in-memory data structure store, used as a database,
    cache and message broker."
### CRUD (Create/Read/Update/Delete)

This platform allows for the creating, accessing, updating and deleting user profiles and tour content.

A user account is created via the registration flow, accessed via the login flow, can be suspended or
closed via a pending deletion in 7 days unless the user logs back in.

Tour content can be created with a title, description, location (latitude and longitude coordinates) with accompanying
audio and images.  The tour details, title, description and location, are uploaded first.  A tour with specific id is
created and then the content, audio and images, are uploaded for that tour.  This is a two stage transaction which is distributed
across the REST API and the Proxy Server.  The REST API stores the tour details in the database. The Proxy Server stores
the audio and images in the public content directory so users can access them.

### REST API

```
GET /  # Hello World
POST /users  # create a new user
PUT /users/<string:username>  # update a user's account with username - currently only closes an account
PATCH /users/<string:username>  # update  user's account with username - currently only suspends account
DELETE /users  # delete users with accounts marked as closed


/tours/?latitude=<string:latitude>&longitude<string:longitude>  # get tours with 5 km of given coordinates
/tours/?username=<string:username>  # get tours created by a specific user
/tours/<int:tour_id>  # get tour with id
/tours/<int:tour_id>/audio  # get audio for tour with id
/tours/<int:tour_id>/images/<int:image_number> # get image number x for tour with id

# The following endpoints are also part of the API but are not strictly RESTful.
# These endpoints involve commands and would be better suited to a RPC API
/login  # log a user in
/logout  # log a user out
/ping  # check the application is alive and well

```

### Advanced search and filtering mechanisms
Tours near the user are loaded on first load.  The user needs to provide their location which is handled by HTML5's
Geolocation API.  When the user types into the search box suggestions are displayed to the user based on the characters
which have been typed in.  In order to keep the client up to date with the current state of the tours, whenever a tour
is created, updated of deleted, the Proxy Server sends an update to the client via a Websocket if that tour is near the
user.


### Asynchronous communication (AJAX)
The new Javascript [Fetch API] is used with async/await and arrow functions when making requests to the REST API via the Proxy Server.
For example:
```
  handleSubmit = async event => {
    event.preventDefault();

    try {
      let res = await fetch("/api/v1/users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "email": this.state.email,
          "username": this.state.username,
          "password": this.state.password
        })
      });

      if (res.status === 201) {
        this.props.userHasAuthenticated(true);
        let data = await res.json();
        this.props.setUsername(data.username);
      } else {
        throw new Error("Registration failed");
      }

    } catch(err) {
      alert(err.message);
    }
  }
```

### Application Security

User authentication and authorization are handled passing JSON Web Tokens to the client.  There tokens are created the
Proxy Server and are transmitted via a HTTPonly secure cookie (provided HTTPS is enabled).

Websockets are authentication by passing a token generated by the Proxy Server and stored in Redis.

CORS is currently not enabled.

The biggest security threat currently in this app is the uploading of files to the server.  The issue of a user uploading
malicious files still needs to be resolved.  In the future a "Content Validating" service will be creating that would
these files for virus before allowing them be written to disk and allowing other users access them.

## Useful commands
```
# identify what process is listening on specific port
netstat -tulpn | grep <PORT NUMBER>
```

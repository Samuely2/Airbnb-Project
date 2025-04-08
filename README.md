# This project is used to simulate a minimal clone of Airbnb

- Where the user(Owner) can create halls, update, and edit your halls, putting the start and end date and control all reservations.
- The contractor can be reservate halls of the owner.

# How to start the project?

# Starting the back-end API
- First you need to enter on the folder of backend, and start the docker with this command

DOCKER-COMPOSE UP --BUILD

After this command, you need to start the database with this command

docker-compose exec web python -m flask db upgrade

All the migrations already done.

After this, your back-end is ready to be used for the front-end

# Starting the front-end 

First you need to install the dependences.

NPM I

After all the steps, your project is ready to use.

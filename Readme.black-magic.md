# Black Magic - putting a UI on the coffee data.

## Get the munged data into the db
tar -xvf coffee-db.tar
mongorestore

## Run the rest server
node black-magic/index.js

## Run the UI ( requires angular-cli )
ng serve

## Open browser to http://localhost:4200



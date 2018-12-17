# sbb_parking for LauzHack2018 Challenge

Provides a visual indication using a light, of whether a parking spot has been reserved or not.
This reservation is done online through a web application.

## INSPIRATION

SBB the national railway company of Switzerland was looking for a way to increase Swiss participation in their rail system.
SBB is the largest parking operator in Switzerland. The parking options are not digital and reservations are not possible.
They wanted to incentivise the people to park the car and to take the train. 

## HARDWARE USED
LoRaWAN Technology based router, distance sensor and a smart plug. The distance sensor and the smart plug were pre-configured with the router.
The API references were given.

## BUILD STATUS

We used distance sensor connected to a LoRaWAN to indicate if a car was in a parking spot or not. 
This data was then utilized by the web application through an API.
Clients can then see how many of their desired parking spots are available.
Once a client has made a reservation, this data is then transmitted back through the LoRaWAN and used turn on a light that will indicate to those who are not using the web application that this parking spot has been reserved.

## BUILT WITH

Python, Flask, RESTful API, JSON

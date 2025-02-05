# Track and Trace API

POC for a Track and Trace API

The project implements the ability to receive information about the order and the current weather at the delivery location.

## Setup and run

- Use `make run` to start the API
- Use `make down` to stop the API
- Use `make load-fixtures` to load fixtures
- Use `make test` to run the tests
- Use `make check` and `make format` to check and format the code (requires ruff)

## Usage

After starting the API, open the Swagger UI at [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/) to see the available endpoints and try them out.

## Details about weather functionality

The OpenWeatherMap service is used to obtain weather data.
Due to recent changes in their API, it is necessary to use a geocoder service (also provided by them) to convert the address to coordinates.
To reduce the number of repeated requests to get weather in the same place (also taking into account the requirement of "no more than once every two hours"), a caching mechanism is used.
The main functionality for this is in the Address model and in the utils.py file.

Also, in order to maintain up-to-date data in the cache, two approaches are used:
- a periodic Celery task that updates the data in the cache for records for which this data has become outdated
- hooks tied to the creation and change of the Shipment model

## Extra information

Due to the time constraints for completing this task, some things have been simplified, omitted, or not implemented optimally.
Django 3.1.2 project example to show off how websockets work using async Django views and nothing more.

##### Run using uvicorn

`uvicorn djangoAsync.asgi:application --reload --debug --ws websockets`


##### core app

general views for websocket views, template views, etc

##### websocket app

main websocket logic, low level stuff like getting messages, sending them and handling errors.

also, middleware that needed for websockets views is here.

##### other

example of websockets using aiohttp and aiohttp requests with a bit complex logic.


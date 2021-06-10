# Geopandas Flask App Template

###### This is a template repo for dockerized geopandas flask api

### How to run



1. To deploy and run: `docker compose up`
3. To use rest api refer to [Rest Api description](#rest-api)

Application running at address: `http://localhost:5000`

### Features

* Read GDB
* Read CSV


### Technology

* Python 3.9
* pip3 install -r requirements.txt


### Resources

* HTTP: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview>
* Flask doc: <https://flask.palletsprojects.com/en/1.1.x/>
* Flask summary: <https://devopedia.org/flask>
* Geopandas: <https://geopandas.org/community/ecosystem.html>
    * GDAL: general C(++) based library for GEO related calculations.


# REST API

The REST API described below. (TODO: document rest api with swagger)

## Upload files and run geopandas app

### Request

`POST /upload/`
    
    curl --location --request POST 'http://127.0.0.1:5000/upload' 
    --form 'files[]=@"/C:/geodatabase/Buildings.gdb.zip"' 

### Response

    HTTP/1.1 201 Created
    Date: Tue, 18 May 2021 12:22:01 GMT
    Status: 201 Created
    Connection: close
    Content-Type: application/json
    Content-Length: 11796

    {
        "name": "test1",
        "value": "test2a",
    }

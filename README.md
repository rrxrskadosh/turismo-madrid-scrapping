# Turismo Madrid Scrapping

This project is a web scraping tool that extracts data from the Turismo Madrid website. The extracted data includes image URLs, descriptions, maps, and stage links for various tourist routes in Madrid. The project is built using the Python Scrapy framework and uses MySQL as the database management system to store the extracted data.

## Environment

```sh
virtualenv <name-environment>
cd <name-environment>
cd Scripts/source activate
```

## Dependencies

Install the dependencies and devDependencies and start the server.

scrapy:
```sh
pip install scrapy
```

mysql connector:
```sh
pip install mysql.connector
```
dotenv:
```sh
pip install python-dotenv

```

## Database

Create an file .env with this structure:

```sh

DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=

```

## Python Modules needed for operations Scripts Scrapy
import scrapy

import mysql.connector

import os

from dotenv import load_dotenv

## Usage

In spiders directory with active environment:

```sh
scrapy runspider <name-crawler>
```

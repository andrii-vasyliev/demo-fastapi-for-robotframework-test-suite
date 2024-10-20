# Demo API for Demo Robot Framework test suite

**Table of contents**

- [Demo API for Demo Robot Framework test suite](#demo-api-for-demo-robot-framework-test-suite)
  - [Description](#description)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Docker](#docker)

This is a RESTful API built with FastAPI for a demo Robot Framework test suite. It provides endpoints for managing customers and other e-commerce-related functionality.

## Description

The demo API is designed to handle various operations related to an online store, such as customer management, product catalog, orders, and more. It is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python.

Currently only customer management endpoint is implemented.

## Prerequisites

- Python >= 3.11
- PostgreSQL

## Installation

1. Clone the repository:

    `git clone https://github.com/ZNenatzka/demo-fastapi-for-robotframework-test-suite`

2. Navigate to the project directory:

    `cd demo-fastapi-for-robotframework-test-suite`

3. Create database, schema, roles, tables and functions using scripts provided in the `demo-fastapi-for-robotframework-test-suite/db`

4. Create a virtual environment and activate it:

    `python -m venv .venv`

    On Linux, use

    `source .venv/bin/activate`

    On Windows, use

    `.venv\Scripts\activate`

5. Install the required dependencies:

    `pip install -r requirements.txt`

6. Set up the environment variables for the database connection and other configurations in the `demo-fastapi-for-robotframework-test-suite/.env` and `demo-fastapi-for-robotframework-test-suite/app/config.py`.

## Usage

1. Navigate to the project directory:

    `cd demo-fastapi-for-robotframework-test-suite`

2. Activate a virtual environment

    On Linux, use

    `source .venv/bin/activate`

    On Windows, use

    `.venv\Scripts\activate`

3. Start the development server:

    `python -m app.main`

    or

    `uvicorn app.main:app --reload`

    This will start the API server at `http://localhost:8000`.

4. Navigate to `http://localhost:8000/api/docs` to access the interactive API documentation (provided by Swagger UI).

5. You can now send requests to the API endpoints for various operations, such as:

   - `POST /api/customers` to create a new customer
   - `GET /api/customers/{customer_id}` to retrieve details of a specific customer
   - `GET /api/customers?name={customer_name}&email={customer_email}` to retrieve a list of customers by name and / or email

## Docker

1. Navigate to the project directory:

    `cd demo-fastapi-for-robotframework-test-suite`

2. Build an image:

    `docker build --tag demo--api-for-robot .`

3. Create and run container:

    `docker run --detach --publish 8000:8000 --name=demo-api --restart=always demo--api-for-robot`

4. Check container status:

    `docker container inspect -f {{.State.Status}} demo-api`

    Container status should be `running`.

5. Check container logs:

    `docker container logs demo-api`

    Logs should not contain errors.

6. To stop and remove container, use following commands:

    `docker stop demo-api`

    `docker rm demo-api`

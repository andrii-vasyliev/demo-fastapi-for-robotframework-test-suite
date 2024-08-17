# demo-fastapi-for-robotframework-test-suite

This is a RESTful API built with FastAPI for a demo Robot Framework test suite. It provides endpoints for managing customers and other e-commerce-related functionality.

## Description

The demo API is designed to handle various operations related to an online store, such as customer management, product catalog, orders, and more. It is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python.

Currently only customer management endpoint is implemented.

## Installation

1. Clone the repository:

    git clone https://github.com/ZNenatzka/demo-fastapi-for-robotframework-test-suite

2. Navigate to the project directory:

    cd demo-fastapi-for-robotframework-test-suite

3. Create a virtual environment and activate it:

    python -m venv .venv

    On Linux, use

    source .venv/bin/activate

    On Windows, use

    .venv\Scripts\activate

4. Install the required dependencies:

    pip install -r requirements.txt

5. Set up the environment variables for the database connection and other configurations.

## Usage

1. Start the development server:

    uvicorn app.main:app --reload

    This will start the API server at `http://localhost:8000`.

2. Navigate to `http://localhost:8000/api/docs` to access the interactive API documentation (provided by Swagger UI).

3. You can now send requests to the API endpoints for various operations, such as:

- `POST /api/customers` to create a new customer
- `GET /api/customers/{customer_id}` to retrieve details of a specific customer
- `GET /api/customers?name={customer_name}&email={customer_email}` to retrieve a list of customers by name and / or email

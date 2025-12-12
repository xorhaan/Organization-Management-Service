# Organization Management Service

A multi-tenant backend service built with **FastAPI** and **MongoDB** that implements a "Collection-per-Tenant" architecture. This service allows for the dynamic creation, management, and secure isolation of organization data.

![Arch](<static/image.png>)

> **Live Demo:** [[Live URL](https://organization-management-service-production.up.railway.app/)]
>
> **Note for Evaluators:** The deployed version includes a **Live Database Console** on the frontend. You can use this to verify that MongoDB collections are physically created (`org_tesla`) and renamed (`org_spacex`) in real-time without needing direct database access.

-----

##  Key Features

  * **Multi-Tenancy:** Implements physical data isolation by creating a separate MongoDB collection for each organization.
  * **Dynamic Operations:** Programmatically creates and renames collections on the fly.
  * **Secure Authentication:** Admin login system using **JWT (JSON Web Tokens)** with `bcrypt` password hashing.
  * **Atomic Updates:** Uses MongoDB's atomic `renameCollection` for safe and instant organization renaming (O(1) operation).
  * **Interactive Frontend:** Includes a built-in dashboard for testing all API endpoints visually.
  * **Scalability Testing:** Includes a **Locust** load testing script to measure read throughput.

-----

##  Tech Stack

  * **Framework:** Python 3.11+, FastAPI
  * **Database:** MongoDB (using `pymongo` driver)
  * **Authentication:** PyJWT, Passlib (Bcrypt)
  * **Testing:** Locust (Load Testing)
  * **Deployment:** Railway (Dockerized)

-----

##  Project Structure

```text
├── app/
│   ├── main.py              # Application entry point & Exception Handlers
│   ├── config.py            # Environment configuration
│   ├── dependencies.py      # JWT Authentication dependency
│   ├── database/            # Database connection logic
│   ├── routers/             # API Routes (Org & Admin)
│   ├── schemas/             # Pydantic Models (Request/Response validation)
│   ├── services/            # Business Logic (CRUD, Auth, Collections)
│   └── utils/               # Hashing & Token helpers
├── static/
│   └── index.html           # Frontend Dashboard
├── locustfile.py            # Scalability/Load Testing script
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

-----

## Setup & Installation (Local)

Follow these steps to run the project on your local machine.

### 1\. Prerequisites

  * Python 3.9 or higher
  * MongoDB installed and running locally (Default: `mongodb://localhost:27017`)

### 2\. Clone the Repository

```bash
git clone https://github.com/xorhaan/Organization-Management-Service
cd Organization-Management-Service
```

### 3\. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 4\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5\. Configuration (.env)

Create a `.env` file in the root directory (optional if using defaults).

```ini
MONGO_URI=mongodb://localhost:27017
MASTER_DB=master_db
TENANT_DB=tenant_db
JWT_SECRET=supersecretkey123
JWT_ALGORITHM=HS256
```

### 6\. Run the Server

Start the application using Uvicorn.

```bash
python -m uvicorn app.main:app --reload
```

-----

## Usage

### 1\. Frontend Dashboard

Open **`http://127.0.0.1:8000`** in your browser.
This interactive dashboard lets you:

  * **Create** new organizations.
  * **Login** as an admin to get a JWT token.
  * **Rename** organizations (requires original credentials).
  * **Delete** organizations (requires JWT).
  * **View Live Collections:** Use the "Evaluator Console" at the bottom to see MongoDB collections being created in real-time.

### 2\. Swagger API Docs

Open **`http://127.0.0.1:8000/docs`** for the automatic interactive API documentation.

-----

## Load Testing (Locust)

To test the scalability of the **Read** operations:

1.  Ensure the server is running.
2.  Make sure you have created an organization named `org_test` (or update `locustfile.py` with an existing name).
3.  Run Locust:
    ```bash
    cd app
    locust -f locustfile.py
    ```
4.  Open `http://localhost:8089`.
5.  Set **Host** to `http://localhost:8000`.
6.  Start swarming\!

-----

##  Design Choices & Trade-offs

This project follows the **Collection-per-Tenant** pattern as requested.

### 1\. Architecture: Collection-per-Tenant

  * **Why:** Provides strict physical isolation of data. It is impossible to query another tenant's data by accident.
  * **Trade-off:** High resource overhead (RAM/File Descriptors) at scale. Not suitable for 10k+ tenants compared to a "Pool" architecture (Shared Collection + Indexed `org_id`).

### 2\. Renaming vs. Copying

  * **Decision:** I implemented atomic **Renaming** (`db.renameCollection`) instead of creating a new collection and copying data.
  * **Reasoning:** Copying data is an O(N) operation that is slow and risky (potential for data loss/corruption). Renaming is an O(1) metadata operation that is instant and safe.

### 3\. Dependency Injection

  * **Decision:** Services are injected into Routers using FastAPI's `Depends()`.
  * **Reasoning:** Decouples business logic from the HTTP layer, making the code modular and testable.

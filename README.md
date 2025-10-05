# Aid-Request-using-python-flask
Project name
DisasterAid — community helpers and aid-requests API

DisasterAid
DisasterAid is a lightweight Flask REST API to register community helpers and create/manage aid requests during emergencies. It uses PostgreSQL with a connection pool for reliable concurrent access and exposes simple CRUD endpoints for helpers and aid requests.
Key features
- Register and list helpers (name, type, location)
- Create and list aid requests (requester, aid type, location)
- Update helper and aid request records
- Query helpers by location and aid requests by aid type
- PostgreSQL connection pooling using psycopg2 for improved performance
- Minimal, easy-to-extend codebase suitable for prototyping emergency coordination systems
Tech stack
- Python 3.x
- Flask
- psycopg2 (PostgreSQL driver and SimpleConnectionPool)
- PostgreSQL
Database schema
helpers
- helper_id SERIAL PRIMARY KEY
- helper_name VARCHAR UNIQUE NOT NULL
- type VARCHAR NOT NULL
- location VARCHAR NOT NULL
aidrequests
- aidrequest_id SERIAL PRIMARY KEY
- requester_name VARCHAR NOT NULL
- aid_type VARCHAR NOT NULL
- location VARCHAR NOT NULL
API endpoints
- POST /add-helpers
- Body JSON: { "helper_name": "name", "type": "medicalfoodshelter", "location": "city" }
- Response: 201 created or 400/500 error
- GET /get-helpers
- Response: 200 with list of helpers or 404 if none
- GET /get-helpersbylocation/<location>
- Response: 200 with helpers in location or 404 if none
- PUT /update-helpers/<helper_id>
- Body JSON: { "helper_name": "...", "type": "...", "location": "..." }
- Response: 200 updated or 404 not found
- POST /add-aidrequests
- Body JSON: { "requester_name": "name", "aid_type": "foodmedicalshelter", "location": "city" }
- Response: 201 created or 400/500 error
- GET /get-aidrequests
- Response: 200 with list of requests or 404 if none
- GET /get-aidrequestbyaidtype/<aid_type>
- Response: 200 with requests by aid_type or 404 if none
- PUT /update-aidrequests/<aidrequest_id>
- Body JSON: { "requester_name": "...", "aid_type": "...", "location": "..." }
- Response: 200 updated or 404 not found
Quick start (developer)
- Clone the repo and create a Python virtual environment:
python -m venv venv && source venv/bin/activate
- Install dependencies:
pip install flask psycopg2-binary
- Configure PostgreSQL connection in the app (HOST, DATABASE, DB_USERNAME, DB_PASSWORD). Ensure the DB is reachable.
- Run the app locally:
python app.py
- The app will auto-create tables on first run. Use Postman or curl to test endpoints on http://localhost:5000.
Example curl requests
- Create a helper: curl -X POST -H "Content-Type: application/json" -d '{"helper_name":"Ravi","type":"medical","location":"Hyderabad"}' http://localhost:5000/add-helpers
- List helpers: curl http://localhost:5000/get-helpers
Notes and next steps
- Add input validation and sanitization (e.g., stricter type enums, length limits).
- Add authentication/authorization for protected operations.
- Add pagination for list endpoints.
- Add proper error handling and structured logging.
- Consider migrating to async frameworks (FastAPI) and use connection pooling libraries for production.
License
MIT License

Suggested repo structure
- app.py (your main Flask app)
- requirements.txt (flask, psycopg2-binary)
- README.md (use the content above)
- .gitignore
- migrations/ (optional for future Alembic scripts)

Commit message to use for initial push
chore: initial commit — DisasterAid Flask API with PostgreSQL pooling and CRUD endpoints

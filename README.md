Credit Approval System — Detailed Assignment README
Date prepared: Tuesday, July 22, 2025, 12:17 AM IST

Table of Contents
Project Overview

Technology Stack

Project Structure

What You Need (Before Starting)

How to Set Up the Project

Importing Customer and Loan Data

Starting and Using Django Admin Panel

API Endpoints with Sample Requests and Responses

How to Test the API with Postman or curl

How to Create and Export a Postman Collection

Submission Checklist and Exact Steps

Troubleshooting Guide

Contact and Support

1. Project Overview
This project is a Credit Approval System built with Django, REST Framework, Celery, and PostgreSQL, fully containerized using Docker. It allows you to:

Import customer and loan data from Excel files

Register new customers and create new loans via API

Check customer eligibility for loans

View, search, and edit customer and loan records in the Django admin panel

2. Technology Stack
Python & Django: Backend framework for rapid development.

Django REST Framework: Provides REST API endpoints.

PostgreSQL: Relational database for data persistence.

Celery & Redis: Background job processing for data imports.

Docker & Docker Compose: Containerize and manage environments.

Postman: Send API requests and view responses (optional but recommended).

3. Project Structure
text
credit_approval_system/
├── apps/
│   ├── customers/
│   └── loans/
├── data/
│   ├── customer_data.xlsx
│   └── loan_data.xlsx
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
└── my_apis.postman_collection.json (optional, for API testing)
4. What You Need (Before Starting)
Docker Desktop: Download and install Docker on your computer

(Optional) Postman: A graphical tool for API testing.

Data Files: Ensure you have customer_data.xlsx and loan_data.xlsx, and place them in the project’s data/ folder.

5. How to Set Up the Project
Step 1: Get the Project Files
If you received them as a ZIP, unzip and place in any directory (e.g., C:\Users\YourName\credit_approval_system).
If from git:

bash
git clone <your-assignment-repository-url>
cd credit_approval_system
Step 2: Start Project Services
Start all containers (web server, database, etc.):

bash
docker-compose up
Leave this terminal open—it shows live logs.

Step 3: Open a New Terminal Tab/Window
Step 4: Apply Database Migrations
Run these commands to create all needed database tables:

bash
docker-compose run --rm web python manage.py makemigrations customers
docker-compose run --rm web python manage.py makemigrations loans
docker-compose run --rm web python manage.py migrate
Each should display “OK” and create tables for customers and loans.

Step 5: Create Django Superuser (Admin Account)
To manage your data in the admin site:

bash
docker-compose run --rm web python manage.py createsuperuser
Enter a username (e.g., admin), your email, and password.

6. Importing Customer and Loan Data
Ensure Excel files are named customer_data.xlsx and loan_data.xlsx and are inside the data/ folder in your project.

Import the data with:

bash
docker-compose run --rm web python manage.py import_initial_data
Watch the logs in your first terminal (with docker-compose up) for messages like “Successfully loaded … customers/loans”.

7. Starting and Using Django Admin Panel
In your web browser, go to:
http://localhost:8000/admin

Log in using the superuser credentials you created earlier.

Click on Customers and Loans in the sidebar to view, add, or change data.

8. API Endpoints with Sample Requests and Responses
All endpoints accept JSON.

Function	Method	Endpoint	Example Payload or Parameter
Register customer	POST	/register	{ "first_name":"John", "last_name":"Doe", "age":30, "monthly_income":50000, "phone_number":"9876543210" }
Check loan eligibility	POST	/check-eligibility	{ "customer_id":1, "loan_amount":50000, "interest_rate":12, "tenure":12 }
Create a new loan	POST	/create-loan	{ "customer_id":1, "loan_amount":50000, "interest_rate":12, "tenure":12 }
View single loan (by ID)	GET	/view-loan/<loan_id>	No body required
View loans by customer	GET	/view-loans/<customer_id>	No body required
Example API Request and Response
Register Customer

Request to /register with:

json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_income": 50000,
  "phone_number": "9876543210"
}
Typical success response:

json
{
  "customer_id": 1,
  "approved_limit": "150000.00"
}
If there’s missing information, you’ll get a 400 or 500 error with a message.

9. How to Test the API with Postman or curl
Using Postman (Step-by-Step for Beginners):
Open Postman

Click “+” to add new request

Set method (e.g., POST), and enter the URL (e.g., http://localhost:8000/register)

Click the “Body” tab, select “raw”, choose “JSON”

Paste your JSON payload (example above)

Click "Send"

The response will appear below the Send button—view status code, response body, etc.

Using curl (Terminal):
For registration endpoint:

bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","age":30,"monthly_income":50000,"phone_number":"9876543210"}'
Response will be shown in your terminal.

10. How to Create and Export a Postman Collection
Save each API request by clicking “Save” in Postman after you configure/test it.

Add all saved requests to a new Collection (create a new collection if none exists).

Once all endpoints are included, hover your mouse over the collection name in the sidebar.

Click the three dots (…) beside it, select “Export”.

In the dialog, choose Collection v2.1 (recommended) and save as my_apis.postman_collection.json.

Place this file at the root of your project before zipping.

11. Submission Checklist and Exact Steps
Hand-in Steps
Check your app: Confirm endpoints, admin, and sample data all work as described above.

Ensure you have these files/folders in your project root:

All source code (apps/, manage.py, etc.)

data/ folder with both Excel files

docker-compose.yml, Dockerfile

README.md (this file)

my_apis.postman_collection.json (if created)

Remove unnecessary files:
Exclude any .pyc, __pycache__/, .git/ directories from the ZIP.

Zip the project folder:

In Windows: right click folder > Send to > Compressed (zipped) folder

In Mac/Linux: run zip -r credit_approval_system.zip credit_approval_system/

Upload or submit the zip file to your assignment portal/GitHub as per instructions.

(Optional) Include screenshots of your admin dashboard and example API responses to show successful operation.

12. Troubleshooting Guide
Problem	                        Solution
Docker won’t start	        Close other Docker apps, restart computer if needed
Error: Table missing	    Re-run migrations (see “How to set up”)
No data in admin	        Re-import Excel data and confirm success message
API gives 500/400 error	    Double-check your JSON keys and content, watch backend terminal log
Login issues/admin	        Reset your superuser password with createsuperuser
Postman can’t export	    Use desktop app, check for collection and export permissions
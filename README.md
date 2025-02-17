Railway Management System

A Flask-based Railway Management System that allows users to register, log in, view and book trains, and manage bookings. It is equipped with JWT-based authentication and role-based access control.

Requirements :-
Database: System should use MySQL, and the database schema should be created using migrations via Flask-Migrate.
JWT Token Expiry: The JWT tokens are set to expire after 1 hour by default. Make sure to log in again to get a fresh token after expiration.
Admin Access: The Admin API key is required for certain actions such as adding trains or updating seats.

Prerequisites:-
Python 3.12.0
MySQL Database
pip 
Postman or any API testing tool

Setup Instructions
Step 1: Clone the Repository
Clone the repository to your local machine:
git clone [https://github.com/your-username/railway-management-system.git](https://github.com/vish9431/WorkIndia.git)

Step 2: Install Dependencies
Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -r requirements.txt

Step 3: Set Up Environment Variables
Change the following according to your in .env file at the root of the project:
DB_USERNAME=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=railway_management

JWT_SECRET_KEY=super-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600

ADMIN_API_KEY=admin-secret-key

FLASK_APP=app.py
FLASK_ENV=development

Step 4: Set Up MySQL Database
Make sure MySQL is installed and running, then create the database:
CREATE DATABASE railway_management;
Then run migrations to create the database tables:
flask db init  # If not initialized yet
flask db migrate -m "Initial migration"
flask db upgrade

Step 5: Start the Flask Application
Run the Flask development server:
flask run
The application should now be running at http://127.0.0.1:5000.

API Endpoints Overview :- 
Authentication: Register and login to obtain a JWT token for accessing protected routes.
Train Management: Admin-only endpoints to add trains and check seat availability.
Booking Management: Book seats, view bookings, and get booking details.

Prerequisites:-
Before testing the API in Postman, ensure the following:
API running: The Flask server is running at http://127.0.0.1:5000.
JWT Token: For user-related requests, you must log in to obtain a JWT token.
Admin API Key: For admin actions, an API key is required (X-Api-Key).

Postman API Test Instructions :- 

1. User Registration (POST /api/auth/register)
URL: http://127.0.0.1:5000/api/auth/register
Method: POST
Headers: None
Body (JSON):
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123"
}
Expected Response:
{
    "success": true,
    "message": "User registered successfully",
    "user_id": 1
}

2. User Login (POST /api/auth/login)
URL: http://127.0.0.1:5000/api/auth/login
Method: POST
Headers: None
Body (JSON):
{
    "username": "testuser",
    "password": "password123"
}
Expected Response (with a JWT token):
{
    "success": true,
    "message": "Login successful",
    "access_token": "jwt_token",
    "user_id": 1,
    "is_admin": false
}

3. Add Train (POST /api/trains)
URL: http://127.0.0.1:5000/api/trains
Method: POST
Headers:
Authorization: Bearer <JWT_token>
X-Api-Key: admin-secret-key (admin-only route)
Body (JSON):
{
    "train_number": "12345",
    "name": "Express Train",
    "source": "Station A",
    "destination": "Station B",
    "total_seats": 100,
    "departure_time": "10:00",
    "arrival_time": "14:00"
}
Expected Response:
{
    "success": true,
    "message": "Train added successfully",
    "train_id": 1
}

4. Get Train Availability (GET /api/trains/availability)
URL: http://127.0.0.1:5000/api/trains/availability?source=Station%20A&destination=Station%20B&date=2025-02-17
Method: GET
Headers: None
Query Parameters:
source: "Station A"
destination: "Station B"
date: "2025-02-17"
Expected Response:
{
    "success": true,
    "trains": [
       {
            "train_id": 1,
            "train_number": "12345",
            "name": "Express Train",
            "source": "Station A",
            "destination": "Station B",
            "departure_time": "10:00",
            "arrival_time": "14:00",
            "total_seats": 100,
            "available_seats": 90
        }
    ]
}

5. Book Seat (POST /api/bookings)
URL: http://127.0.0.1:5000/api/bookings
Method: POST
Headers:
Authorization: Bearer <JWT_token>
Body (JSON):
{
    "train_id": 1,
    "source": "Station A",
    "destination": "Station B",
    "booking_date": "2025-02-17",
    "number_of_seats": 2
}
Expected Response:
{
    "success": true,
    "message": "Successfully booked 2 seats",
    "booking_ids": ["unique-booking-id-1", "unique-booking-id-2"],
    "train_number": "12345",
    "train_name": "Express Train",
    "source": "Station A",
    "destination": "Station B",
    "booking_date": "2025-02-17",
    "seat_numbers": [1, 2]
}

6. Get Booking Details (GET /api/bookings/{booking_id})
URL: http://127.0.0.1:5000/api/bookings/{booking_id}
Method: GET
Headers:
Authorization: Bearer <JWT_token>
Expected Response:
{
    "success": true,
    "booking_id": "unique-booking-id-1",
    "train_number": "12345",
    "train_name": "Express Train",
    "source": "Station A",
    "destination": "Station B",
    "seat_number": 1,
    "booking_date": "2025-02-17",
    "status": "CONFIRMED",
    "created_at": "2025-02-17 10:00:00"
}

7. Get User's Bookings (GET /api/bookings/user)
URL: http://127.0.0.1:5000/api/bookings/user
Method: GET
Headers:
Authorization: Bearer <JWT_token>
Expected Response:
{
    "success": true,
    "bookings": [
        {
            "booking_id": "unique-booking-id-1",
            "train_number": "12345",
            "train_name": "Express Train",
            "source": "Station A",
            "destination": "Station B",
            "seat_number": 1,
            "booking_date": "2025-02-17",
            "status": "CONFIRMED",
            "created_at": "2025-02-17 10:00:00"
        },
        {
            "booking_id": "unique-booking-id-2",
            "train_number": "12345",
            "train_name": "Express Train",
            "source": "Station A",
            "destination": "Station B",
            "seat_number": 2,
            "booking_date": "2025-02-17",
            "status": "CONFIRMED",
            "created_at": "2025-02-17 10:00:00"
        }
    ]
}

8. Update Train Seats (PUT /api/trains/{train_id}/seats)
URL: http://127.0.0.1:5000/api/trains/{train_id}/seats
Method: PUT
Headers:
Authorization: Bearer <JWT_token> (Admin user only)
X-Api-Key: admin-secret-key (Admin API key)
Body (JSON):
{
    "total_seats": 120
}
Expected Response:
{
    "success": true,
    "message": "Train seats updated successfully",
    "train_id": 1,
    "new_total_seats": 120
}



1. User Registeration :-
<img width="999" alt="Screenshot 2025-02-17 at 10 59 30 PM" src="https://github.com/user-attachments/assets/e39f5720-ae15-4052-80c6-61d80e6ff66c" />

2. User Login :-
<img width="1010" alt="Screenshot 2025-02-17 at 11 00 31 PM" src="https://github.com/user-attachments/assets/ac49c8dd-5c30-4912-9fa8-56534f50cfdd" />

3. Add Train(Admin) :- 
<img width="1007" alt="Screenshot 2025-02-17 at 11 01 35 PM" src="https://github.com/user-attachments/assets/c2cad2ec-905f-4ed8-abea-439a4e3e731e" />

4. List of Trains :-
<img width="1000" alt="Screenshot 2025-02-17 at 11 02 46 PM" src="https://github.com/user-attachments/assets/8ab589f4-2452-4cae-b4c3-4f568444193d" />
<img width="961" alt="Screenshot 2025-02-17 at 11 03 05 PM" src="https://github.com/user-attachments/assets/5fe058c5-761c-4677-871b-4b7cf5dec24b" />

5. Update Seat :- 
<img width="857" alt="Screenshot 2025-02-17 at 11 03 31 PM" src="https://github.com/user-attachments/assets/286a24ce-a377-45b3-823d-e5df67a4768c" />

6. Book Train :- 
<img width="904" alt="Screenshot 2025-02-17 at 11 04 52 PM" src="https://github.com/user-attachments/assets/178c2778-fb5b-47df-9e1e-b4d81b801236" />

7. Get Booking By Booking Id :-
<img width="1008" alt="Screenshot 2025-02-17 at 11 05 38 PM" src="https://github.com/user-attachments/assets/d71379e5-47b8-40a0-b20f-a84c900e78d3" />

8. User Train Bookings :- 
<img width="934" alt="Screenshot 2025-02-17 at 11 06 58 PM" src="https://github.com/user-attachments/assets/e2200384-89fc-470e-b7f4-d13ab410269c" />







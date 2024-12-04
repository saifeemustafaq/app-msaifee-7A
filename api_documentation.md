# Student Token Management API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
All endpoints except authentication endpoints require a JWT token in the header:
```
Authorization: Bearer <token>
```

## Endpoints

### Users

#### Get All Users
```http
GET /users
```
**Auth Required:** Yes (Admin only)  
**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)

**Response (200):**
```json
{
    "items": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "campus_affiliation": "School of CS",
            "token_balance": 100,
            "is_admin": false
        }
    ],
    "total": 20,
    "pages": 2,
    "current_page": 1
}
```

#### Get User by ID
```http
GET /users/{user_id}
```
**Auth Required:** Yes  
**Response (200):**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "campus_affiliation": "School of CS",
    "token_balance": 100,
    "is_admin": false
}
```

#### Create User
```http
POST /users
```
**Auth Required:** Yes (Admin only)  
**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "campus_affiliation": "School of CS"
}
```

#### Update User
```http
PUT /users/{user_id}
```
**Auth Required:** Yes  
**Request Body:**
```json
{
    "email": "new_email@example.com",
    "username": "new_username",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "campus_affiliation": "School of CS",
    "password": "new_password"  // Optional
}
```

#### Delete User
```http
DELETE /users/{user_id}
```
**Auth Required:** Yes (Admin only)

### Profiles

#### Get All Profiles
```http
GET /profiles
```
**Auth Required:** Yes (Admin only)  
**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)

#### Get Profile
```http
GET /profiles/{profile_id}
```
**Auth Required:** Yes

#### Create Profile
```http
POST /profiles
```
**Auth Required:** Yes  
**Request Body:**
```json
{
    "academic_program": "Computer Science",
    "graduation_year": 2024,
    "bio": "Student bio",
    "linkedin_url": "https://linkedin.com/in/username",
    "language_preferences": "English, Spanish",
    "cultural_background": "International Student"
}
```

#### Update Profile
```http
PUT /profiles/{profile_id}
```
**Auth Required:** Yes  
**Request Body:**
```json
{
    "academic_program": "Computer Science",
    "graduation_year": 2024,
    "bio": "Updated bio",
    "linkedin_url": "https://linkedin.com/in/username",
    "language_preferences": "English, Spanish",
    "cultural_background": "International Student"
}
```

#### Delete Profile
```http
DELETE /profiles/{profile_id}
```
**Auth Required:** Yes

### Token Activities

#### Get All Activities
```http
GET /activities
```
**Auth Required:** Yes  
**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)

#### Get Activity
```http
GET /activities/{activity_id}
```
**Auth Required:** Yes

#### Create Activity
```http
POST /activities
```
**Auth Required:** Yes (Admin only)  
**Request Body:**
```json
{
    "user_id": 1,
    "activity_type": "CREDIT",  // or "DEBIT"
    "amount": 100,
    "description": "Token reward for event participation"
}
```

#### Delete Activity
```http
DELETE /activities/{activity_id}
```
**Auth Required:** Yes (Admin only)

## Response Codes

- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

## Data Models

### User
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "campus_affiliation": "string",
    "token_balance": "integer",
    "is_admin": "boolean"
}
```

### Profile
```json
{
    "id": "integer",
    "user_id": "integer",
    "academic_program": "string",
    "graduation_year": "integer",
    "bio": "string",
    "linkedin_url": "string",
    "language_preferences": "string",
    "cultural_background": "string"
}
```

### Activity
```json
{
    "id": "integer",
    "user_id": "integer",
    "activity_type": "string",
    "amount": "integer",
    "description": "string",
    "created_at": "datetime"
}
```
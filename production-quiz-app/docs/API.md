# API Documentation

## Overview

The Production Quiz App provides a RESTful API for authentication, quiz management, and user interactions. All endpoints follow REST conventions and return JSON responses.

**Base URL:** `http://localhost:5000` (development) or `https://your-domain.com` (production)

**Authentication:** Session-based (cookies) with CSRF protection

**Rate Limiting:** Enforced on sensitive endpoints

---

## Authentication Endpoints

### Register User

**POST** `/auth/register`

Create a new user account with email verification.

**Rate Limit:** 3 requests per hour per IP

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123"
}
```

**Validation Rules:**
- Username: 3-20 characters, alphanumeric + underscore
- Email: Valid email format, unique
- Password: Min 8 characters, must contain uppercase, lowercase, and numbers

**Success Response (200):**
```json
{
  "message": "Registration successful! Please check your email to verify your account.",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "email_verified": false,
    "created_at": "2025-12-22T10:30:00Z"
  }
}
```

**Error Responses:**

**400 Bad Request:**
```json
{
  "error": "Username already taken"
}
```

**429 Too Many Requests:**
```json
{
  "error": "Rate limit exceeded. Please try again later."
}
```

---

### Login

**POST** `/auth/login`

Authenticate user and create session.

**Rate Limit:** 5 requests per 15 minutes per IP

**Request Body:**
```json
{
  "username_or_email": "johndoe",
  "password": "SecurePass123",
  "remember_me": false
}
```

**Success Response (200):**
```json
{
  "message": "Welcome back, johndoe!",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "email_verified": true,
    "is_admin": false
  }
}
```

**Error Responses:**

**401 Unauthorized:**
```json
{
  "error": "Invalid username/email or password"
}
```

**423 Locked:**
```json
{
  "error": "Account temporarily locked due to multiple failed login attempts."
}
```

---

### Logout

**GET** `/auth/logout`

End user session.

**Authentication:** Required

**Success Response (302):**
- Redirects to login page
- Session cleared

---

### Verify Email

**GET** `/auth/verify/<token>`

Verify user email address with token.

**URL Parameters:**
- `token` (string): Email verification token

**Success Response (200):**
```json
{
  "message": "Email verified successfully! You can now log in."
}
```

**Error Response (400):**
```json
{
  "error": "Invalid or expired verification token"
}
```

---

### Request Password Reset

**POST** `/auth/forgot-password`

Request password reset link via email.

**Rate Limit:** 3 requests per hour per email

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Success Response (200):**
```json
{
  "message": "If your email is registered, you will receive password reset instructions."
}
```

**Note:** Always returns success to prevent email enumeration.

---

### Reset Password

**POST** `/auth/reset-password/<token>`

Reset password using reset token.

**URL Parameters:**
- `token` (string): Password reset token

**Request Body:**
```json
{
  "new_password": "NewSecurePass123",
  "confirm_password": "NewSecurePass123"
}
```

**Success Response (200):**
```json
{
  "message": "Password reset successfully! You can now log in."
}
```

**Error Responses:**

**400 Bad Request:**
```json
{
  "error": "Reset token has expired. Please request a new one."
}
```

---

### Update Profile

**POST** `/auth/profile`

Update user profile information.

**Authentication:** Required

**Request Body:**
```json
{
  "username": "johndoe_updated",
  "email": "newemail@example.com"
}
```

**Success Response (200):**
```json
{
  "message": "Profile updated successfully!",
  "user": {
    "id": 1,
    "username": "johndoe_updated",
    "email": "newemail@example.com",
    "email_verified": false
  }
}
```

**Note:** Changing email requires re-verification.

---

### Change Password

**POST** `/auth/change-password`

Change user password.

**Authentication:** Required

**Request Body:**
```json
{
  "current_password": "OldPass123",
  "new_password": "NewPass123",
  "confirm_password": "NewPass123"
}
```

**Success Response (200):**
```json
{
  "message": "Password changed successfully!"
}
```

**Error Response (400):**
```json
{
  "error": "Current password is incorrect"
}
```

---

## Quiz Endpoints

### Get Dashboard

**GET** `/dashboard` or `/`

Get user dashboard with stats and available quizzes.

**Authentication:** Required

**Success Response (200):**
```json
{
  "user": {
    "username": "johndoe",
    "stats": {
      "total_attempts": 10,
      "average_score": 75.5,
      "best_score": 95.0
    }
  },
  "quizzes": [
    {
      "id": 1,
      "category": "Agent Fundamentals",
      "title": "Agent Fundamentals Quiz",
      "description": "Test your knowledge of AI agents",
      "icon": "🤖",
      "total_questions": 10,
      "is_active": true,
      "user_best_score": 85.0,
      "user_attempts": 2
    }
  ],
  "recent_attempts": [
    {
      "id": 1,
      "quiz_category": "Agent Fundamentals",
      "score": 8,
      "percentage": 80.0,
      "completed_at": "2025-12-22T10:30:00Z"
    }
  ]
}
```

---

## Common Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 302 | Redirect (successful action) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional context"
  }
}
```

---

## Rate Limiting

Rate limits are enforced on the following endpoints:

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/auth/register` | 3 requests | 1 hour |
| `/auth/login` | 5 requests | 15 minutes |
| `/auth/forgot-password` | 3 requests | 1 hour |
| API endpoints | 100 requests | 1 hour |
| Quiz submission | 10 requests | 1 minute |

**Headers:**
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Timestamp when limit resets

---

## CSRF Protection

All POST, PUT, DELETE requests require a valid CSRF token.

**How to get token:**
1. Retrieve from cookie: `csrf_token`
2. Include in form data or headers:
   - Form: `<input name="csrf_token" value="token">`
   - Header: `X-CSRFToken: token`

**Exempt endpoints:**
- None (all state-changing requests require CSRF token)

---

## Security Headers

All responses include security headers:

```
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

---

## Pagination

Endpoints returning lists support pagination:

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_pages": 5,
    "total_items": 100,
    "has_prev": false,
    "has_next": true
  }
}
```

---

## Example API Usage

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:5000"
session = requests.Session()

# Register
response = session.post(f"{BASE_URL}/auth/register", data={
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123"
})
print(response.json())

# Login
response = session.post(f"{BASE_URL}/auth/login", data={
    "username_or_email": "johndoe",
    "password": "SecurePass123"
})
print(response.json())

# Get dashboard
response = session.get(f"{BASE_URL}/dashboard")
print(response.json())
```

### JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:5000";

// Login
async function login(username, password) {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Include cookies
    body: JSON.stringify({
      username_or_email: username,
      password: password,
      remember_me: false
    })
  });

  return await response.json();
}

// Get CSRF token
function getCSRFToken() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrf_token='))
    ?.split('=')[1];
}
```

### cURL

```bash
# Register
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123"
  }'

# Login (save cookies)
curl -X POST http://localhost:5000/auth/login \
  -c cookies.txt \
  -d "username_or_email=johndoe&password=SecurePass123"

# Dashboard (use cookies)
curl http://localhost:5000/dashboard \
  -b cookies.txt
```

---

## Testing the API

### Using Postman

1. Import the Postman collection (if provided)
2. Set environment variable: `base_url = http://localhost:5000`
3. Enable "Automatically follow redirects"
4. Enable "Send cookies with requests"

### Using pytest

```python
def test_register_api(client):
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123',
        'confirm_password': 'TestPass123'
    })
    assert response.status_code in [200, 302]
```

---

## Webhooks (Future)

*Webhook support planned for future release*

---

## API Versioning

Current version: **v1** (implicit)

Future versions will be prefixed: `/api/v2/...`

---

## Support

For API issues or questions:
- Check the [Development Guide](DEVELOPMENT.md)
- Open an issue with the `api` label
- Contact: support@your-domain.com

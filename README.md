# 🏨 StayEase – Hotel Room Booking API (Spring Boot)

StayEase is a RESTful backend service built using **Spring Boot** to manage hotel listings and room bookings for a hotel aggregator platform.  
It implements **JWT-based authentication**, **role-based authorization**, and follows a **clean layered architecture**.

This project is developed as part of the **ME_BUILDOUT_STAYEASE** assessment.

---

## 📌 High-Level Architecture

```
Client (Postman / Curl / Frontend)
        |
        v
Controller Layer  →  Service Layer  →  Repository Layer  →  MySQL DB
        |
        v
   Security Layer (JWT + Roles)
```

---

## 🧩 Folder Structure (Detailed)

```
src/main/java/com/takehome/stayease
│
├── controller
│   ├── AuthController.java
│   ├── HotelController.java
│   └── BookingController.java
│
├── service
│   ├── UserService.java
│   ├── HotelService.java
│   ├── BookingService.java
│   └── Impl
│       ├── UserServiceImpl.java
│       ├── HotelServiceImpl.java
│       └── BookingServiceImpl.java
│
├── repository
│   ├── UserRepository.java
│   ├── HotelRepository.java
│   └── BookingRepository.java
│
├── entity
│   ├── User.java
│   ├── Hotel.java
│   └── Booking.java
│
├── dto
│   ├── auth
│   │   ├── SignupRequest.java
│   │   ├── LoginRequest.java
│   │   └── AuthResponse.java
│   │
│   ├── hotel
│   │   ├── CreateHotelRequest.java
│   │   ├── UpdateHotelRequest.java
│   │   └── HotelResponse.java
│   │
│   └── booking
│       ├── CreateBookingRequest.java
│       └── BookingResponse.java
│
├── security
│   ├── SecurityConfig.java
│   ├── JwtUtil.java
│   ├── JwtAuthenticationFilter.java
│   ├── CustomUserDetails.java
│   └── CustomUserDetailsService.java
│
├── exception
│   └── GlobalExceptionHandler.java
│
└── StayEaseApplication.java
```

---

## 🔐 Role-Based Access Control (RBAC)

| Role | Permissions |
|-----|------------|
| **USER** | View hotels, create booking |
| **HOTEL_MANAGER** | Update hotels, cancel bookings |
| **ADMIN** | Create hotels, delete hotels |

### Role Enforcement
Implemented using:
```java
@PreAuthorize("hasRole('ADMIN')")
@PreAuthorize("hasRole('HOTEL_MANAGER')")
@PreAuthorize("hasRole('USER')")
```

JWT token contains role information and is validated on every request.

---

## 🔑 Authentication Flow (JWT)

1. User registers or logs in
2. Server validates credentials
3. JWT token is generated
4. Client sends token in header:
   ```
   Authorization: Bearer <JWT_TOKEN>
   ```
5. JWT filter validates token and sets security context

---

## 📡 API Endpoints (Detailed)

### 👤 User APIs

#### Register User (Public)
```http
POST /api/users/register
```
```json
{
  "email": "user@test.com",
  "password": "Test@1234",
  "firstName": "John",
  "lastName": "Doe",
  "role": "USER"
}
```
Response:
```json
{ "token": "jwt-token" }
```

---

#### Login User (Public)
```http
POST /api/users/login
```
```json
{
  "email": "user@test.com",
  "password": "Test@1234"
}
```
Response:
```json
{ "token": "jwt-token" }
```

---

### 🏨 Hotel APIs

#### Get All Hotels (Public)
```http
GET /api/hotels
```

---

#### Create Hotel (Admin)
```http
POST /api/hotels
Authorization: Bearer <ADMIN_TOKEN>
```
```json
{
  "name": "StayEase Hotel",
  "location": "Pune",
  "description": "Business Hotel",
  "totalRooms": 10,
  "availableRooms": 10
}
```

---

#### Update Hotel (Hotel Manager)
```http
PUT /api/hotels/{hotelId}
Authorization: Bearer <MANAGER_TOKEN>
```
```json
{
  "availableRooms": 15
}
```

---

#### Delete Hotel (Admin)
```http
DELETE /api/hotels/{hotelId}
Authorization: Bearer <ADMIN_TOKEN>
```

---

### 📅 Booking APIs

#### Create Booking (User)
```http
POST /api/bookings/{hotelId}
Authorization: Bearer <USER_TOKEN>
```
```json
{
  "checkInDate": "2026-02-20",
  "checkOutDate": "2026-02-22"
}
```
Response:
```json
{
  "bookingId": 1,
  "hotelId": 2,
  "checkInDate": "2026-02-20",
  "checkOutDate": "2026-02-22"
}
```

---

#### Get Booking Details
```http
GET /api/bookings/{bookingId}
Authorization: Bearer <USER_TOKEN>
```

---

#### Cancel Booking (Hotel Manager)
```http
DELETE /api/bookings/{bookingId}
Authorization: Bearer <MANAGER_TOKEN>
```

---

## ⚠️ Business Rules Enforced

- Check-in date must be future date
- Check-out date must be after check-in
- No overbooking allowed
- Customers cannot cancel bookings
- Only managers can cancel bookings

---

## 🧪 Testing Strategy

- Controller-level unit tests
- MockMvc + Mockito
- Security filters disabled during tests
- No real DB used in tests

Run tests:
```bash
./gradlew test
```

---

## ▶️ Run the Application

```bash
./gradlew clean bootRun
```

App runs on:
```
http://localhost:8081
```

---

## 📦 Build JAR

```bash
./gradlew clean bootJar
java -jar build/libs/stayease-0.0.1-SNAPSHOT.jar
```
---
<!--
## 👤 Author

**Pushpak A. Fasate**  
Java Backend Developer  
Spring Boot | REST APIs | MySQL
-->

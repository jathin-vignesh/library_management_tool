# Library Management Tool

This Library Management System (LMS) provides basic functionality for managing books, users, and borrow records in a library. It is built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, with JWT-based authentication and role-based access control.

---

## Features

- User authentication (login/register)
- Role-based access: **Admin** and **Student**
- Book management
- Borrowing and returning books
- JWT token authentication

---

## Roles & Operations

### **Admin**

Admins have full access to the system and can perform the following operations:

1. **Register Users**
   - Add students or other admins to the system.
   - Endpoint: `POST /auth/register` (student)  
     `POST /auth/register/admin` (admin)
   
2. **Book Management**
   - **Add a book:** `POST /admin/books/`  
     Add a new book with title, author, ISBN, and available copies.  
     If the ISBN already exists, it will return an error.
   - **Get all books:** `GET /admin/books/`  
     Retrieve a list of all books in the library.
   - **Update book details:** `PATCH /admin/books/{book_id}`  
     Modify book details like title, author, or available copies.
   - **Delete a book:** `DELETE /admin/books/{book_id}`  
     A book can only be deleted if there are no active borrow records.  
     Otherwise, it will return an error.

3. **User Management**
   - **Get all users:** `GET /admin/users/`  
     Retrieve a list of all students and admins.

4. **Borrow Records**
   - **Get all Borrow Records:** `GET /admin/borrowHist/`  
     Admins can view all borrow records.

---

### **Student**

Students can perform actions related to borrowing books:

1. **View Books**
   - **Get all books:** `GET /books/`  
     Retrieve a list of all available books.

2. **Borrow Books**
   - **Borrow a book:** `POST /borrow/{book_id}`  
     Borrow an available book. Cannot borrow more copies than are available.

3. **Return Books**
   - **Return a book:** `POST /return/{borrow_id}`  
     Return a borrowed book.

4. **View Borrow History**
   - **Get my borrow records:** `GET /borrow/my`  
     View a list of books currently borrowed and their return status.

---

## Authentication

- JWT token-based authentication.
- **Login:** `POST /auth/login`  
  - Use email as username and password to get an access token.
- Include token in headers to access protected routes:  

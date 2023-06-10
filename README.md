My Awesome ToDo API
--------------------

Introduction
------------
My Awesome ToDo API is a Django REST Framework API that allows users to authenticate, register, and manage their tasks.

Installation
------------
To install My Awesome ToDo API, follow these steps:

1. Clone the repository
2. Install the dependencies
3. Set up the database
4. Run the server

Usage
-----
To use My Awesome ToDo API, follow these steps:

1. Open your web browser
2. Go to the URL of the API
3. Enter your credentials
4. Start using the API

API Endpoints
-------------
Here are the available endpoints in My Awesome ToDo API:

| Endpoint | Description |
| -------- | ----------- |
| `POST /api/login/` | Authenticate and obtain a JWT token for accessing protected resources. |
| `POST /api/register/` | Register a new account. |
| `POST /api/add/` | Add a new task. |
| `GET /api/get/` | Retrieve all tasks associated with the authenticated user. |
| `PUT /api/update/` | Update a task. |
| `POST /api/complete/` | Toggle a task's completed status. |
| `DELETE /api/delete/` | Delete a task. |

---

### `POST /api/login/`

API Description:
This API allows users to authenticate and obtain a JWT token for accessing protected resources.

Parameters:
- `username` (string): The username of the user.
- `password` (string): The password of the user.

Response:
- HTTP 200 OK: The request was successful. Returns a JWT token and username.
- HTTP 401 Unauthorized: The provided credentials are invalid.
- HTTP 400 Bad Request: The request data is invalid.

---

### `POST /api/register/`

API Description:
This API allows users to register a new account.

Parameters:
- `username` (string): The desired username for the new account.
- `first_name` (string, optional): The first name of the user.
- `last_name` (string, optional): The last name of the user.
- `password` (string): The password for the new account.

Response:
- HTTP 201 Created: The user account was created successfully. Returns a success message.
- HTTP 400 Bad Request: The request data is invalid or the username is already taken. Returns detailed error information.

---

### `POST /api/add/`

API Description:
This API allows authenticated users to add a new task.

Required Permissions:
- The user must be authenticated.

Request Headers:
- `Authorization` (string): The JWT token obtained from the login API must be provided as the value of the Authorization header in the format `Bearer <token>`.

Parameters:
- `task` (string): The task description.
- `date` (string): The expected date of the task completion in format of YYYY-MM-DD.

Response:
- HTTP 201 Created: The task was created successfully. Returns a success message and the task ID.
- HTTP 400 Bad Request: The request data is invalid. Returns detailed error information.

---

### `GET /api/get/`

API Description:
This API allows authenticated users to retrieve all their tasks.

Required Permissions:
- The user must be authenticated.

Request Headers:
- `Authorization` (string): The JWT token obtained from the login API must be provided as the value of the Authorization header in the format `Bearer <token>`.

Response:
- HTTP 200 OK: The request was successful. Returns all tasks associated with the authenticated user.

---

### `PUT /api/update/`

API Description:
This API allows authenticated users to update a task.

Required Permissions:
- The user must be authenticated.

Parameters:
- `taskId` (integer): The ID of the task to be updated.
- `updatedTask` (string): The updated task description.
- `updatedDate` (string): The updated date of the task.

Response:
- HTTP 200 OK: The task was updated successfully. Returns a success message.
- HTTP 400 Bad Request: The request data is invalid or the specified task does not exist. Returns detailed error information.

---

### `POST /api/complete/`

API Description:
This API allows authenticated users to toggle a task's completed status.

Required Permissions:
- The user must be authenticated.

Request Headers:
- `Authorization` (string): The JWT token obtained from the login API must be provided as the value of the Authorization header in the format `Bearer <token>`.

Parameters:
- `taskId` (integer): The ID of the task to toggle its completed status.

Response:
- HTTP 200 OK: The task's completed status was toggled successfully. Returns a success message.
- HTTP 400 Bad Request: The request data is invalid or the specified task does not exist. Returns detailed error information.

---

### `DELETE /api/delete/`

API Description:
This API allows authenticated users to delete a task.

Required Permissions:
- The user must be authenticated.

Request Headers:
- `Authorization` (string): The JWT token obtained from the login API must be provided as the value of the Authorization header in the format `Bearer <token>`.

Parameters:
- `taskId` (integer): The ID of the task to be deleted.

Response:
- HTTP 200 OK: The task was deleted successfully. Returns a success message.
- HTTP 400 Bad Request: The request data is invalid or the specified task does not exist. Returns detailed error information.

---

Contributing
------------
To contribute to My Awesome ToDo API, follow these steps:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

License
-------
My Awesome ToDo API is released under the MIT License.

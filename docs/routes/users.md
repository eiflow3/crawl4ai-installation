## `routes/users.py`

This module contains the endpoints for the users collection.

### Endpoints

- **`GET /users`**
  - Returns a list of all users from the database.
  - Response Model: `List[User]`

  **Example Request:**
  ```bash
  curl -X GET http://localhost:8000/users
  ```

  **Example Response:**
  ```json
  [
    {
      "_id": "60d5ec49f72e6e4b28ef1b8f",
      "number": "+639970839783",
      "subscribed_lgus": [
        "Noveleta"
      ]
    }
  ]
  ```

- **`POST /users`**
  - Creates a new user. If a user with the same number already exists, the existing user document will be returned.
  - Request Body: `User`
  - Response Model: `User`

  **Example Request:**
  ```bash
  curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '
  {
    "number": "+639817582216",
    "subscribed_lgus": [
      "General Trias"
    ]
  }'
  ```

  **Example Response (New User Created - 201 Created):**
  ```json
  {
    "_id": "60d5ec49f72e6e4b28ef1b90",
    "number": "+639817582216",
    "subscribed_lgus": [
      "General Trias"
    ]
  }
  ```

  **Example Response (Existing User Returned - 200 OK):**
  ```json
  {
    "_id": "60d5ec49f72e6e4b28ef1b90",
    "number": "+639817582216",
    "subscribed_lgus": [
      "General Trias"
    ]
  }
  ```

- **`DELETE /users`**
  - **Summary:** Delete all documents in the Users collection.
  - **Description:** Deletes all documents from the `users` collection, but keeps the collection itself.
  - **Responses:**
    - `200 OK`: Returns a success message indicating all documents have been deleted.
    - `500 Internal Server Error`: If the database connection is not available or deleting documents fails.
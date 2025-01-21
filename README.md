# django-rest-framework
This project outlines the development of a REST API using Django REST Framework (DRF). The API adheres to the following general requirements:

    Data Format: JSON
    Database: PostgreSQL or SQLite
    Django Version: Latest stable release

Models

The API revolves around two core models:

    User
        email (CharField): A unique email address for user identification.
        json_web_token (CharField): A JSON Web Token (JWT) for authentication.

    Message
        title (CharField): The title of the message.
        body (TextField): The content of the message.
        user (ForeignKey): A foreign key relationship linking a message to its corresponding user.

Relationships

    A single User can have many Messages (One-to-Many relationship).
    Each Message belongs to a single User (Many-to-One relationship).

User Controller (Unauthenticated Methods)

    Create User
        Accepts an email address as input.
        Checks for existing email addresses to prevent duplicates.
        If the email is unique:
            Generates a JWT.
            Creates a new User instance with the provided email and JWT.
            Returns a success response with the created User's details (email and JWT).
        If the email already exists:
            Returns a response with an appropriate status code (e.g., 409 Conflict) indicating the error.

    Display Users (Optional Pagination)
        Retrieves all User objects from the database.
        Optionally implements pagination to limit the number of returned users per request.
        Returns a list of User objects (email and JWT) in JSON format.

Message Controller (Authenticated Methods)

Authentication

    All methods in this controller require authentication using valid JWTs.
    Implement a mechanism (e.g., JWT middleware) to verify JWTs in incoming requests.

    Create Message
        Requires a JWT from an authenticated user.
        Retrieves the user associated with the JWT.
        Accepts message title and body as input.
        Creates a new Message instance with the provided title, body, and the retrieved user as the foreign key.
        Returns a success response with the details of the created Message.

    Change Message
        Requires a JWT from an authenticated user.
        Retrieves the user associated with the JWT.
        Accepts a message ID as input.
        Verifies that the message belongs to the authenticated user (authorization check).
        Accepts updated message title and/or body as input (optional).
        Updates the corresponding Message instance with the provided changes.
        Returns a success response with the details of the updated Message.

    Display Message
        Requires a JWT from an authenticated user.
        Retrieves the user associated with the JWT.
        Accepts a message ID as input.
        Verifies that the message belongs to the authenticated user (authorization check).
        Retrieves the Message object with the specified ID.
        Returns a success response with the details of the retrieved Message.

    Display and Filter Messages (Optional Pagination)
        Requires a JWT from an authenticated user.
        Retrieves the user associated with the JWT.
        Optionally accepts filters (e.g., search query) to retrieve specific messages.
        Optionally implements pagination to limit the number of returned messages per request.
        Returns a list of Message objects (filtered and/or paginated) in JSON format.

Additional Considerations

    Error Handling: Implement robust error handling to gracefully handle potential exceptions (e.g., invalid input, database errors) and return appropriate error responses.
    Security: Prioritize security measures to protect user data and prevent unauthorized access. Consider JWT expiration, user permissions, and input validation.
    Testing: Write comprehensive unit tests to ensure the functionality of your API endpoints.
    Documentation: Provide clear API documentation using tools like DRF's built-in API schema generation or external tools like Swagger.

By following these guidelines and incorporating the best aspects of Response A and Response B, you can create a well-structured, secure, and user-friendly REST API using Django REST Framework.

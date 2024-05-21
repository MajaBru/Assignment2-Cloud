# Assignment2-Cloud
This project is a simple-ish website inspired by Reddit-like forum sites. Building on OpenStack (Chameleon Cloud) using Docker and DockerCompose.


# System Description

1. Dockerize the Web Server:

- Create a Docker image for your web server (Flask or FastAPI).
- Ensure it can be load-balanced.

2. Cache Layer:
- Use Redis as the caching layer (use the Redis Docker image from DockerHub).

3. Processing and Like-Batcher:
- Implement the processing layer to handle API requests.
- Create a like-batcher to accumulate likes and update the database in batches.

4. SQL Database:
- Use MySQL or PostgreSQL as your relational database (use the respective Docker image from DockerHub).

5. Docker-Compose Setup:
- Define all services in a docker-compose.yml file.


# Usage/Functionality

1. User and Post Management:
- Implement endpoints to create users, posts, and categories.
- Implement endpoints to like posts.

2. Frontend:
- Create HTML templates to display posts by category and user.
- Provide options to create new posts and like posts.

# Testing
1. Unit Tests:
- Write tests for the cache and processing layers.
- Use pytest to run tests and ensure they follow PEP-8 principles.
- Ensure commands like flake8 . and mypy . run without errors.


# Web/Front-End
1. Create Views:
- Main view showing posts by category with options to like and create new posts.
- User view showing user information and posts.

# Load Balancer
1. Nginx Load Balancer:
- Use Nginx as the load balancer.
- Configure it to distribute traffic among multiple instances of your web server.

# Cache
1. Integrate Redis:
- Set up Redis to cache frequently accessed data.
- Implement logic to check the cache before querying the database.

# Processing
1. REST API:
- Develop RESTful endpoints to handle post creation, retrieval by category, user creation, and liking posts.
- Ensure endpoints follow REST principles.

# Like-Batcher
1. Batch Likes:
- Implement a mechanism to batch likes and update the database in intervals or when a certain count is reached.

# Database
1. Schema Design:
- Design a relational database schema for users, posts, and likes.
Implement the schema using SQ

# Report
Documentation:
Document your system architecture, including diagrams.
Discuss the choices made during planning and development.
Include a brief “How to” guide for building and running the system

# Deliverables
Source Code:
- Ensure the source code is organized and includes all necessary components.
- Include the Docker and Docker-Compose configurations.



# Example Report Structure
1. Introduction
Brief overview of the project goals and technologies used.

2. System Description
Detailed description of each component (Flask app, MySQL database, Docker setup).

3. Usage and Functionality
Explanation of how to run the application and what functionalities it supports.

4. Testing
Description of the testing strategy and examples of test cases.

5. Conclusion
Summary of what was achieved, challenges faced, and future improvements.
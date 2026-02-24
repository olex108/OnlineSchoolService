# OnlineSchoolService

Template for courses store.
A Django REST Framework project integrated with PostgreSQL, Redis, and Celery, fully containerized using Docker.

## 🌍 Global Deployment Guide (How to Fork & Run)

If you want to deploy this project to your own remote server, using GitHub Actions, follow these steps:

### 1. Server Preparation

1. Install Docker & Docker Compose on your Ubuntu server:
`sudo apt update && sudo apt install docker.io docker-compose -y`

2. Create Project Directory: 
`mkdir ~/OnlineSchoolService && cd ~/OnlineSchoolService`

3. Environment Setup:
Create a .env file manually on the server and fill it with your production secrets (use .env.example as a template).
   
   ```bash
    BASE_URL=url_path_for_base_page

    SECRET_KEY=app_secret_key
    DEBUG=app_debug_state
   
    ALLOWED_HOSTS=list_of_hosts
    
    # Postgres database params
    NAME=name_of_database
    USER=name_of_db_user
    PASSWORD=password
    HOST=host
    PORT=port
    
    # Email address and app password for sending emails
    EMAIL_ADDRESS=email_adress_for_sending_emails
    APP_EMAIL_PASSWORD=secret_email_app_password
    
    # API keys
    STRIPE_API_KEY=API_KEY_for_Stripe_service
    
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```
   
4. Nginx Config:
Copy the nginx/ folder from the repository to ~/OnlineSchoolService/nginx/ on your server.

### 2. GitHub Configuration


1. Fork this repository to your GitHub account.

2. Go to Settings > Secrets and variables > Actions and add the following Repository Secrets:

   - `DOCKER_HUB_USERNAME`: Your Docker Hub ID.
   - `DOCKER_HUB_ACCESS_TOKEN`: Your Docker Hub PAT (with Write access).
   - `SERVER_IP`: Public IP of your remote server.
   - `SSH_USER`: Your server username.
   - `SSH_KEY`: Your Private SSH Key (content of id_rsa).

### 3. Automated CI/CD

1. Push any changes.

2. GitHub Actions will automatically:

- Run the test suite.
- Build the Docker image and push it to Docker Hub.
- Connect to your server via SSH, pull the new image, and restart the containers.

### 4. Post-Deployment (First Run Only)

After the first successful deployment, finalize the setup on the server:

```bash
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py createsuperuser
```

### 🛠 Custom Django Management Commands

The project includes custom management commands to quickly set up the application environment. These commands use data from JSON fixtures located in the data_fixtures/ directory.

Note: You can modify the initial data (courses, users, lessons) by editing the JSON files in data_fixtures/ before running the commands.

1. Initialize Moderators Group:
Creates the "Moderators" group with predefined permissions.

```bash
docker compose exec web python manage.py add_moderators_group
```

2. Load Initial Content:

Populates the database with initial courses, lessons, and user data from fixtures.

```bash
docker compose exec web python manage.py load_data
```

3. Generate Payment Mock Data:

Fills the database with sample payment records for testing the billing system.

```bash
docker compose exec web python manage.py add_payment_data
```


## 🚀 Getting Started (Local Development)

### Prerequisites
* [Docker](https://www.docker.com)
* [Docker Compose](https://docs.docker.com)

### Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/olex108/OnlineSchoolService.git
   ```
   
2. Create a .env file in the root directory and populate it with your settings:

    ```bash
    BASE_URL=url_path_for_base_page

    SECRET_KEY=app_secret_key
    DEBUG=app_debug_state
   
    ALLOWED_HOSTS=list_of_hosts
    
    # Postgres database params
    NAME=name_of_database
    USER=name_of_db_user
    PASSWORD=password
    HOST=host
    PORT=port
    
    # Email address and app password for sending emails
    EMAIL_ADDRESS=email_adress_for_sending_emails
    APP_EMAIL_PASSWORD=secret_email_app_password
    
    # API keys
    STRIPE_API_KEY=API_KEY_for_Stripe_service
    
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```

3. Build and Run the project:

    ```bash
    docker-compose up --build
    ```

This command will build the images, apply database migrations, and start all services. The API will be available at http://localhost:8000.

## 🛠 Service Verification

To ensure everything is running correctly, use docker-compose ps to check container statuses.

1. Web API (Django)

    Access: http://localhost:8000/

    Verification: Open the link in your browser. You should see the Django REST Framework browsable API.

2. Database (PostgreSQL)
    
   Verification: Run a health check to ensure the DB is ready:

   ```bash
   docker-compose exec db pg_isready  
   ```
   
3. Redis

Verification: Ping the Redis server to check connectivity:

  ```bash
  docker-compose exec redis redis-cli ping
  ```

Expected output: PONG
    
4. Celery (Worker & Beat)
Worker Check: View logs to confirm connection to the broker:

    ```bash
    docker-compose logs celery
    ```

Beat Check: Confirm the scheduler is active:

  ```bash
  docker-compose logs celery_beat
  ```

## 📂 Useful Commands

### Docker commands

1. Run services:

```bash
docker-compose up -d
```
2. Stop services: 

```bash
docker-compose down
```

3. Stop and remove volumes (Wipes Database): 

```bash
docker-compose down -v
```

4. View live logs: 

```bash
docker-compose logs -f
```

### Castom commands

1. Re-run Migrations: 

```bash
docker-compose exec web python manage.py migrate
```

2. Add group "Moderators" to your project: 

```bash
docker-compose exec web python manage.py add_moderators_group
```

3. Load data from fixtures to your project: 

```bash
docker-compose exec web python manage.py load_data
```

4. Add payment data to your project: 

```bash
docker-compose exec web python manage.py add_payment_data
```

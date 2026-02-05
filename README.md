# OnlineSchoolService

Template for courses store.
A Django REST Framework project integrated with PostgreSQL, Redis, and Celery, fully containerized using Docker.

## 🚀 Getting Started

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

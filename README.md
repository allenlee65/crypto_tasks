# Framework Structure

![image](https://github.com/user-attachments/assets/c04cdd1d-726b-4063-84ff-cb4273f89cae)

# Directory Structure

- `features/`: BDD feature files
- `steps/`: Step implementation files
- `utils/`: Utility classes and helpers
- `test_data/`: Test data files
- `config/`: Configuration files

# Installation

1. **Clone the repository:**  
   git clone [<repository-url.git>](https://github.com/allenlee65/crypto_tasks.git)  
   cd crypto_tasks
2. **Create virtual environment:**  
   python -m venv venv  
   venv\Scripts\activate
3. **Install dependencies:**  
   pip install -r requirements.txt

# Run Tests (Windows Command Prompt Terminal)

## Run all tests

>### behave

## Run only smoke tests

>### behave --tags @smoke

## Run only REST API tests

>### behave --tags @rest

## Run only WebSocket tests

>### behave --tags @websocket

## Run specific feature

>### behave features\candlestick

## Run with JSON format

>### behave --format json

## Run negative tests only

>### behave --tags @negative

# Allure Report

>### pip install allure-behave  
>
>### behave -f allure_behave.formatter:AllureFormatter -o reports/allure-report ./features  
>
>### allure serve reports/allure-report

<img width="1917" height="930" alt="Screenshot From 2025-07-16 17-47-41" src="https://github.com/user-attachments/assets/439d8cf5-5331-4c3c-a0a2-3e072c32faa2" />

# Build the Docker image
>
>### sudo docker build -t crypto-tasks

# Run all tests
>
>### sudo  docker run --rm crypto-tasks

# Run specific test types
>
>### sudo  docker run --rm crypto-tasks behave --tags @smoke
>
>### sudo  docker run --rm crypto-tasks behave --tags @rest
>
>### sudo  docker run --rm crypto-tasks behave --tags @websocket
>
>### sudo  docker run --rm crypto-tasks behave --tags @negative

# Run specific feature
>
>### sudo  docker run --rm crypto-tasks behave features/candlestick

# Run with JSON format
>
>### sudo  docker run --rm crypto-tasks behave --format json

# Generate Allure reports
>
>### sudo docker run --rm -v $(pwd)/reports:/app/reports crypto-tasks \
>
>### behave -f allure_behave.formatter:AllureFormatter -o reports/allure-report ./features

# If you have allure installed locally, serve the reports
>
>### allure serve reports/allure-report

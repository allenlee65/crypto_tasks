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
   git clone [<repository-url.git>  ](https://github.com/allenlee65/crypto_tasks.git)  
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
>### behave -f allure_behave.formatter:AllureFormatter -o reports/allure-report ./features  
>### allure serve reports/allure-report
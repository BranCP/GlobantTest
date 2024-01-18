# Globant Coding Challenge Project

The project aims to create a REST API that can load information from CSV files into a relational database. The project is implemented in Python and utilizes cloud services.

## Used Services
- AWS S3
- AWS RDS (PostgreSQL Database)

## Required Python Libraries
- boto3
- pandas
- flask
- sqlalchemy
- os

## Folder Structure
- **data_example:** This folder is intended for loading sample data for testing the project.
- **test_flask.py:** This file represents the main project.
- **data_download:** Folder for downloaded data.
- **sql_commands.sql:** SQL statements for reviewing the data.
- **config.py:** File to put your DB credentials and your AWS access keys

## Usage
```bash
1. To execute the code and keep the service running, run the following command:

python jupyther\test_flask.py

2. Once the project is running (i.e., after executing "python jupyther\test_flask.py"), you can test its functionality using Postman:
   - Install Postman: [Download Postman](https://www.postman.com/downloads/)
   - Launch a POST request to `http://localhost:5000/upload_data`

Within the request, the process requires a JSON payload with the following information:
   ```json
   {
     "message": "Process files",       // An initialization message
     "file": "hired_employees.csv",    // The file to be processed
     "table": "hired_employees"         // The name of the table where the information will be loaded
   }

```



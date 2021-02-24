import json
import pyodbc
import os


def lambda_handler(event, context):

    print("APP_ENV = " + os.environ.get('APP_ENV'))
    if os.environ.get('APP_ENV') == 'docker':
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=docker.for.win.localhost;DATABASE=APM"
                              ";PORT=1433;UID=sa;PWD=myPass123")
    else:
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=database-1.cgwlmviu6zts.us-east-2.rds"
                              ".amazonaws.com;DATABASE=apm;PORT=1433;UID=admin;PWD=myPass123")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM Products WHERE id = ?", event['pathParameters']["id"])
    cursor.commit()
    cursor.close()

    return {
        'statusCode': 204,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({})
    }

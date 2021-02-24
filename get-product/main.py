import json
import pyodbc
import os


def lambda_handler(event, context):
    product = {}

    print("APP_ENV = " + os.environ.get('APP_ENV'))
    if os.environ.get('APP_ENV') == 'docker':
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=docker.for.win.localhost;DATABASE=APM"
                              ";PORT=1433;UID=sa;PWD=myPass123")
    else:
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=database-1.cgwlmviu6zts.us-east-2.rds"
                              ".amazonaws.com;DATABASE=apm;PORT=1433;UID=admin;PWD=myPass123")

    cursor = conn.cursor()
    cursor.execute('SELECT id, productName, productCode, tags, releaseDate, price, categoryId, description, starRating, '
                   'imageUrl '
                   'FROM Products '
                   'WHERE id = ' + event['pathParameters']["id"])

    for row in cursor:
        product['id'] = str(row[0])
        product['productName'] = row[1]
        product['productCode'] = row[2]
        if row[3] is not None:
            product['tags'] = row[3].split("|")
        product['releaseDate'] = row[4]
        product['price'] = str(row[5])
        product['categoryId'] = str(row[6])
        product['description'] = row[7]
        product['starRating'] = str(row[8])
        product['imageUrl'] = row[9]

    cursor.close()

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(product)
    }

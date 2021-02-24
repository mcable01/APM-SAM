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

    body = event['body']
    json_acceptable_string = body.replace("'", "\"")
    data = json.loads(json_acceptable_string)

    # if data["productName"] is None:
    #     product_name = ""
    # else:
    #     product_name = data["productName"]

    product_name = data["productName"]
    product_code = data["productCode"]
    tags = '|'.join(data["tags"])
    # release_date = data["releaseDate"]
    # price = data["price"]
    description = data["description"]
    star_rating = data["starRating"]
    # image_url = data["imageUrl"]

    cursor: object = conn.cursor()
    # cursor.execute("INSERT INTO Products(productName, productCode, tags, releaseDate, price, description, starRating, "
    #                "imageUrl) values (?, ?, ?, ?, ?, ?, ?, ?)", product_name, product_code, tags, release_date, price,
    #                description, star_rating, image_url)
    cursor.execute("INSERT INTO Products(productName, productCode, tags, description, starRating) "
                   "values (?, ?, ?, ?, ?)", product_name, product_code, tags, description, star_rating)
    cursor.commit()
    cursor.close()

    return {
        'statusCode': 201,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({})
    }

import mysql.connector
from mysql.connector import Error
from flask import Flask, request, send_file

app = Flask(__name__)

def create_connection():
    """Create a database connection to MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            user='root',       # Replace with your MySQL username
            password='mysql_root', # Replace with your MySQL password
            database='survey_db'  # Replace with your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

def create_table(connection):
    """Create the feedback table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        surname VARCHAR(255),
        email VARCHAR(255),
        tel VARCHAR(20),
        age INT NULL,
        usage_duration VARCHAR(50),
        customer_type VARCHAR(50),
        network_speed VARCHAR(50),
        challenges TEXT,
        data_usage TEXT,
        satisfaction VARCHAR(50),
        recommendation VARCHAR(50),
        favorite_feature VARCHAR(100),
        improvements TEXT,
        comments TEXT
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'feedback' created successfully")
    except Error as e:
        print(f"Error creating table: '{e}'")

def insert_feedback(connection, feedback_data):
    """Insert feedback data into the table."""
    insert_query = """
    INSERT INTO feedback (
        name, surname, email, tel, age, usage_duration, customer_type,
        network_speed, challenges, data_usage, satisfaction, recommendation,
        favorite_feature, improvements, comments
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query, feedback_data)
        connection.commit()
        print("Feedback data inserted successfully")
    except Error as e:
        print(f"Error inserting data: '{e}'")

@app.route('/')
def survey():
    return send_file('survey.html')

@app.route('/survey.css')
def css():
    return send_file('survey.css')

@app.route('/images/<filename>')
def images(filename):
    return send_file(f'images/{filename}')

@app.route('/submit', methods=['POST'])
def submit():
    # Extract form data
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    tel = request.form.get('tel')
    age_str = request.form.get('age')
    age = int(age_str) if age_str else None
    usage_duration = request.form.get('usageDuration')
    customer_type = request.form.get('customerType')
    network_speed = request.form.get('networkSpeed')
    challenges = request.form.get('challenges')
    data_usage = ', '.join(request.form.getlist('dataUsage'))
    satisfaction = request.form.get('satisfaction')
    recommendation = request.form.get('recommendation')
    favorite_feature = request.form.get('favoriteFeature')
    improvements = ', '.join(request.form.getlist('improvements'))
    comments = request.form.get('comments')

    feedback_data = (name, surname, email, tel, age, usage_duration, customer_type, network_speed, challenges, data_usage, satisfaction, recommendation, favorite_feature, improvements, comments)

    connection = create_connection()
    if connection:
        create_table(connection)
        insert_feedback(connection, feedback_data)
        connection.close()
        return "Thank you for your feedback! Your data has been saved."
    else:
        return "Error connecting to database. Please try again later."

if __name__ == "__main__":
    app.run(debug=True)

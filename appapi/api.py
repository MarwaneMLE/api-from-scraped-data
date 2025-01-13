from flask import Flask, jsonify, render_template
import sqlite3
import requests
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer


app = Flask(__name__)



@app.route('/data', methods=['GET'])
def get_data():
    connection = sqlite3.connect("/home/marwane/mlops-projects/api-course/api-from-scraped-data/appapi/db.sqlite3")
    cursor = connection.cursor()
    
    # Fetch all rows from the database
    cursor.execute("SELECT * FROM article_table")
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries for better structure
    data = []
    for row in rows:
        # Assuming the columns in the table are: id, article, date, press_name
        data.append({
            'id': row[0],
            'article': row[1],
            'date': row[2],
            'press_name': row[3]
        })

    # Close the connection to the database
    connection.close()

    # Return the data as JSON
    return jsonify({'data': data})



# Endpoint to consume the data from the `/data` endpoint
@app.route('/consume_data', methods=['GET'])
def consume_data():
    # URL of the /data endpoint
    url = 'http://127.0.0.1:5000/data'  # Change to your actual Flask app URL if needed

    try:
        # Make a GET request to the /data endpoint
        response = requests.get(url)
        
        # If the request is successful (status code 200), process the response
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response

            # Print the fetched data in the console (or process it as needed)
            print("Fetched Data from /data endpoint:")
            for item in data['data']:
                row = [f"ID: {item['id']}, Article: {item['article']}, Date: {item['date']}, Press Name: {item['press_name']}"]
                #print(f"ID: {item['id']}, Article: {item['article']}, Date: {item['date']}, Press Name: {item['press_name']}")
                #blob = TextBlob(f"{row[1]}", pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
                #sentiment = blob
                #print(sentiment)
            # Return a response confirming the consumption
            #return render_template("index.html", sentiment=row)
            return jsonify({"message": "Data successfully consumed and printed to console"}), 200
        
        else:
            return jsonify({"error": "Failed to fetch data from /data"}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error while consuming data: {e}"}), 500
 
 
@app.route('/sentiment')
def your_view_function():
    response = requests.get('http://127.0.0.1:5000/data')  # Replace with actual endpoint

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response

        # Initialize a list to collect all rows
        rows = []

        # Process each item in the response
        for item in data['data']:
            # Only the article text will be added here
            row = [item['article']]
            rows.append(row)  # Add the article to the rows list

        # Perform sentiment analysis on each article
        sentiments_list = []
        for row in rows:
            article = row[0]  # Extract the article text from the list
            blob = TextBlob(article)  # Pass the article text to TextBlob

            # Get the sentiment analysis result (polarity and subjectivity)
            sentiment = blob.sentiment
            sentiments_list.append(sentiment[0])  # Add the sentiment to the list

        # Return the rows and sentiment to the template
        return render_template("index.html", sentiment=sentiments_list)
    else:
        # Handle error if status code is not 200
        return "Error fetching data", 500


'''
@app.route('/sentiment')
def your_view_function():
    response = requests.get('http://127.0.0.1:5000/data')  # Replace with actual endpoint

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response

        # Initialize a list to collect all rows
        rows = []

        # Process each item in the response
        for item in data['data']:
            #row = [f"ID: {item['id']}, Article: {item['article']}, Date: {item['date']}, Press Name: {item['press_name']}"]
            row = [item['article']]

            """row = [
            [
                f"ID: {item['id']}",
                f"Article: {item['article']}",
                f"Date: {item['date']}",
                f"Press Name: {item['press_name']}"
            ] for item in data ]"""
            rows.append(row)  # Add the formatted string to the rows list

        # Optionally, you can perform sentiment analysis here for each row if needed
        # e.g., Sentiment analysis can be added for each article using TextBlob or another library.
        sentiments_lis = []
        for i in range(2):
            article = rows[i]#[1]
            blob = TextBlob(article, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

        # Get the sentiment analysis result
            sent = blob.sentiment
        # Return the rows to the template
        return render_template("index.html", sentiment=sent)
    else:
        # Handle error if status code is not 200
        return "Error fetching data", 500
'''

if __name__ == '__main__':
    app.run(debug=True)


'''from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/data', methods=['GET'])
def get_data():
    connection = sqlite3.connect("/home/marwane/mlops-projects/api-course/api-from-scraped-data/appapi/db.sqlite3")
    cursor = connection.cursor()
    data = cursor.execute("SELECT * FROM article_table")
    
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run(debug=True)'''
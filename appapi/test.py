from flask import Flask, jsonify
import sqlite3, requests
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
import text

app = Flask(__name__)

# Initialize the Translator
#translator = Translator()

# Endpoint to fetch data from the database
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


# Endpoint to consume the data from the `/data` endpoint and analyze sentiment
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

            # Analyze sentiment of each article
            sentiment_results = []
            for item in data['data']:
                article = item['article']
                
                # Translate article to English for sentiment analysis
                #translated_article = translator.translate(article, src='fr', dest='en').text
                
                # Use TextBlob to analyze the sentiment of the article
                blob = textblob_fr(article)
                sentiment_score = blob.sentiment.polarity  # Range [-1, 1]
                
                # Add sentiment result to the response
                sentiment_results.append({
                    'id': item['id'],
                    'article': item['article'],
                    'sentiment_score': sentiment_score,
                    'sentiment': 'positive' if sentiment_score > 0 else 'negative' if sentiment_score < 0 else 'neutral'
                })
            
            # Return the sentiment results as JSON
            return jsonify({"sentiments": sentiment_results}), 200
        
        else:
            return jsonify({"error": "Failed to fetch data from /data"}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error while consuming data: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)

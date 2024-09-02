from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load and clean the data
try:
    df = pd.read_csv("Book_details.csv", encoding="unicode_escape")
    print("CSV Loaded Successfully.")

    # Debug: Print DataFrame information
    print("DataFrame Columns:", df.columns)
    print("Sample Data:\n", df.head())

    # Ensure required columns are present
    required_columns = ['title', 'author', 'description', 'keywords', 'rack']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Missing required columns in CSV")

    df = df.dropna(axis=1, how="all")  # Remove columns with all NaN values

    # Clean and standardize text data
    df['title'] = df['title'].str.lower().str.strip()
    df['description'] = df['description'].str.lower().str.strip()
    df['keywords'] = df['keywords'].str.lower().str.strip()
    df['rack'] = df['rack'].astype(str).str.strip().str.lower()  # Ensure consistency
    print("Data Cleaning Completed.")
except Exception as e:
    print(f"Error loading CSV: {e}")

@app.route('/')
def index():
    return "Welcome to the Bookfinder API. Use /search to find books."

@app.route('/search', methods=['GET'])
def search_books():
    try:
        query = request.args.get('query', '').strip().lower()
        rack_number = request.args.get('rack', '').strip().lower()

        print(f"Query received: '{query}', Rack Number: '{rack_number}'")

        # Initialize empty results DataFrame
        results = pd.DataFrame()

        # Check for rack filtering
        if rack_number:
            print(f"Filtering by rack: '{rack_number}'")
            if rack_number not in df['rack'].unique():
                print(f"Rack '{rack_number}' not found in the data.")
                return jsonify({"error": "Rack not found"}), 404
            else:
                results = df[df['rack'] == rack_number]

        # Filter based on query and/or rack number
        if query:
            if not results.empty:
                results = results[
                    (results['title'].str.contains(query)) | 
                    (results['description'].str.contains(query)) | 
                    (results['keywords'].str.contains(query)) | 
                    (results['rack'].str.contains(query))
                ]
            else:
                results = df[
                    (df['title'].str.contains(query)) | 
                    (df['description'].str.contains(query)) | 
                    (df['keywords'].str.contains(query)) | 
                    (df['rack'].str.contains(query))
                ]

        print(f"Results found: {len(results)}")

        # Convert results to list of dictionaries for JSON response
        results_list = results.to_dict(orient='records')

        if len(results_list) == 0:
            response = {
                "message": "No books found matching your query",
                "total_results": 0
            }
        else:
            response = {
                "books": results_list,
                "total_results": len(results_list)
            }

        return jsonify(response)

    except Exception as e:
        print(f"Error during search: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load precomputed data and cosine similarity from pickle files
with open('cleaned_movie_list.pkl', 'rb') as f:
    movies_df = pickle.load(f)

with open('genre_similarity.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

@app.route('/')
def home():
    return jsonify({"message": "Movie Recommendation Backend is running!"})

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    title = request.args.get('title').lower()  # Lowercase to match cleaned titles
    language = request.args.get('language', '')  # Optional language filter

    # Check if the movie exists in the dataset
    if title not in movies_df['Name_cleaned'].values:
        return jsonify({"error": "Movie not found"}), 404

    # Filter the dataset by language if a language filter is provided
    if language:
        filtered_df = movies_df[movies_df['Language'] == language].reset_index(drop=True)
    else:
        filtered_df = movies_df.reset_index(drop=True)

    # Check if the title exists in the filtered dataset
    filtered_idx = filtered_df[filtered_df['Name_cleaned'] == title].index
    if filtered_idx.empty:
        return jsonify({"error": f"Movie '{title}' not found in {language} language"}), 404

    # Get the correct index for the filtered DataFrame
    filtered_idx = filtered_idx[0]

    # Use the precomputed cosine similarity matrix to get similar movies
    sim_scores = list(enumerate(cosine_sim[filtered_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Exclude the movie itself from the recommendations
    sim_scores = [score for score in sim_scores if score[0] != filtered_idx]

    # Get the top 15 recommendations
    sim_scores = sim_scores[:15]
    movie_indices = [i[0] for i in sim_scores]

    # Check if there are recommendations available
    if not movie_indices:
        return jsonify({"error": "No recommendations available"}), 404

    # Get the IDs and Names of the recommended movies
    recommendations = filtered_df[['ID', 'Name']].iloc[movie_indices].to_dict('records')

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

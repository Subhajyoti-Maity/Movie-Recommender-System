import pandas as pd
import numpy as np
import ast
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import zipfile
from io import BytesIO

def download_tmdb_dataset():
    """Download TMDB dataset from multiple sources for more comprehensive coverage"""
    print("Downloading TMDB dataset...")
    
    # Multiple URLs for different TMDB dataset versions
    dataset_urls = [
        {
            "name": "TMDB 5000 Movies (Original)",
            "movies_url": "https://raw.githubusercontent.com/krishnaik06/Movie-Recommender-in-python/master/tmdb_5000_movies.csv",
            "credits_url": "https://raw.githubusercontent.com/krishnaik06/Movie-Recommender-in-python/master/tmdb_5000_credits.csv"
        },
        {
            "name": "TMDB Extended Dataset",
            "movies_url": "https://raw.githubusercontent.com/rounakbanik/movies/master/movies_metadata.csv",
            "credits_url": "https://raw.githubusercontent.com/rounakbanik/movies/master/credits.csv"
        }
    ]
    
    for dataset in dataset_urls:
        try:
            print(f"Trying to download {dataset['name']}...")
            
            # Download movies data
            print("Downloading movies data...")
            movies_response = requests.get(dataset['movies_url'])
            movies_response.raise_for_status()
            
            # Download credits data
            print("Downloading credits data...")
            credits_response = requests.get(dataset['credits_url'])
            credits_response.raise_for_status()
            
            # Save the files
            with open('tmdb_movies.csv', 'wb') as f:
                f.write(movies_response.content)
            
            with open('tmdb_credits.csv', 'wb') as f:
                f.write(credits_response.content)
                
            print(f"{dataset['name']} downloaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error downloading {dataset['name']}: {e}")
            continue
    
    print("All download attempts failed. Using fallback method...")
    return False

def convert(text):
    """Convert string representation of lists to actual lists"""
    L = []
    try:
        for i in ast.literal_eval(text):
            L.append(i['name']) 
        return L
    except:
        return []

def generate_model():
    """Generate the movie recommendation model"""
    print("Loading and processing data...")
    
    # Load the datasets
    movies = pd.read_csv('tmdb_movies.csv')
    credits = pd.read_csv('tmdb_credits.csv')
    
    print(f"Movies dataset shape: {movies.shape}")
    print(f"Credits dataset shape: {credits.shape}")
    
    # Merge the datasets
    movies = movies.merge(credits, on='title')
    print(f"After merge shape: {movies.shape}")
    
    # Select relevant columns
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    
    # Remove rows with missing values
    movies.dropna(inplace=True)
    print(f"After removing NaN values: {movies.shape}")
    
    # Convert string representations to lists
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert)
    movies['crew'] = movies['crew'].apply(convert)
    
    # Process overview text
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    
    # Create tags by combining all features
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    # Create new dataframe with processed data
    new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
    new['tags'] = new['tags'].apply(lambda x: " ".join(x))
    
    print("Creating feature vectors...")
    
    # Create feature vectors using CountVectorizer
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(new['tags']).toarray()
    
    print(f"Feature vector shape: {vector.shape}")
    
    # Calculate cosine similarity
    print("Calculating cosine similarity...")
    similarity = cosine_similarity(vector)
    
    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)
    
    # Save the model files
    print("Saving model files...")
    pickle.dump(new, open('model/movie_list.pkl', 'wb'))
    pickle.dump(similarity, open('model/similarity.pkl', 'wb'))
    
    print("Model files generated successfully!")
    print("Files saved:")
    print("- model/movie_list.pkl")
    print("- model/similarity.pkl")
    
    return True

def main():
    """Main function to generate the model"""
    print("Movie Recommender System - Model Generation")
    print("=" * 50)
    
    # Check if model files already exist
    if os.path.exists('model/movie_list.pkl') and os.path.exists('model/similarity.pkl'):
        print("Model files already exist!")
        return True
    
    # Download dataset if needed
    if not os.path.exists('tmdb_movies.csv') or not os.path.exists('tmdb_credits.csv'):
        if not download_tmdb_dataset():
            print("Failed to download dataset. Exiting.")
            return False
    
    # Generate the model
    if generate_model():
        print("\nModel generation completed successfully!")
        print("You can now run the Streamlit app with: streamlit run app.py")
        return True
    else:
        print("Model generation failed!")
        return False

if __name__ == "__main__":
    main()

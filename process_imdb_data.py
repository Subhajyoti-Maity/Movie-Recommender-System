import pandas as pd
import pickle
import os
import gzip
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def process_imdb_data():
    """Process the downloaded IMDB data"""
    print("Processing IMDB dataset...")
    
    try:
        # Read the IMDB data
        df = pd.read_csv('title.basics.tsv.gz', compression='gzip', sep='\t', low_memory=False)
        print(f"Loaded {len(df)} titles from IMDB")
        
        # Filter for movies only (titleType == 'movie')
        movies = df[df['titleType'] == 'movie'].copy()
        print(f"Found {len(movies)} movies")
        
        # Filter for movies with genres (to ensure quality)
        movies = movies[movies['genres'].notna()]
        print(f"Found {len(movies)} movies with genres")
        
        # Remove rows with missing titles
        movies = movies.dropna(subset=['primaryTitle'])
        print(f"After removing missing titles: {len(movies)} movies")
        
        # Take a sample for performance (first 10000 movies)
        if len(movies) > 10000:
            movies = movies.head(10000)
            print(f"Using sample of {len(movies)} movies for performance")
        
        # Create tags from available information
        def create_tags(row):
            tags = []
            
            # Add title words
            if pd.notna(row['primaryTitle']):
                tags.extend(str(row['primaryTitle']).lower().split())
            
            # Add genres
            if pd.notna(row['genres']):
                tags.extend(str(row['genres']).split(','))
            
            # Add start year if available
            if pd.notna(row['startYear']) and row['startYear'] != '\\N':
                tags.append(str(int(float(row['startYear']))))
            
            return ' '.join(tags)
        
        # Create tags for each movie
        movies['tags'] = movies.apply(create_tags, axis=1)
        
        # Create final dataframe
        final_movies = pd.DataFrame({
            'movie_id': movies['tconst'],
            'title': movies['primaryTitle'],
            'tags': movies['tags']
        })
        
        # Remove rows with empty tags
        final_movies = final_movies[final_movies['tags'].str.strip() != '']
        print(f"Final movies with tags: {len(final_movies)}")
        
        return final_movies
        
    except Exception as e:
        print(f"Error processing IMDB data: {e}")
        return None

def create_model_from_movies(movies_df):
    """Create the recommendation model from movies dataframe"""
    print("Creating recommendation model...")
    
    # Create feature vectors
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(movies_df['tags']).toarray()
    
    print(f"Feature vector shape: {vector.shape}")
    
    # Calculate cosine similarity
    print("Calculating cosine similarity...")
    similarity = cosine_similarity(vector)
    
    # Create model directory
    os.makedirs('model', exist_ok=True)
    
    # Save the model files
    print("Saving model files...")
    pickle.dump(movies_df, open('model/movie_list.pkl', 'wb'))
    pickle.dump(similarity, open('model/similarity.pkl', 'wb'))
    
    print("✅ Model created successfully!")
    print(f"Total movies in system: {len(movies_df)}")
    
    return True

def main():
    """Main function to process IMDB data and create model"""
    print("🎬 IMDB Data Processor")
    print("=" * 30)
    
    # Check if IMDB data exists
    if not os.path.exists('title.basics.tsv.gz'):
        print("IMDB data not found. Please run download_movies_data.py first.")
        return False
    
    # Process the data
    movies_df = process_imdb_data()
    if movies_df is None:
        print("Failed to process IMDB data.")
        return False
    
    # Create the model
    if create_model_from_movies(movies_df):
        print("\n🎉 IMDB movie recommender system created successfully!")
        print("You can now:")
        print("1. Run the Streamlit app: streamlit run app.py")
        print("2. Add custom movies: python add_custom_movies.py")
        print("3. Batch import movies: python batch_import_movies.py")
        return True
    
    return False

if __name__ == "__main__":
    main()

import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_existing_model():
    """Load existing model files"""
    try:
        with open('model/movie_list.pkl', 'rb') as f:
            movie_list = pickle.load(f)
        with open('model/similarity.pkl', 'rb') as f:
            similarity = pickle.load(f)
        return movie_list, similarity
    except FileNotFoundError:
        print("Model files not found. Please run generate_model.py first.")
        return None, None

def create_sample_csv():
    """Create a sample CSV file for batch import"""
    sample_data = {
        'title': ['The Shawshank Redemption', 'The Godfather', 'Pulp Fiction'],
        'overview': [
            'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
            'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.'
        ],
        'genres': ['Drama', 'Crime, Drama', 'Crime, Drama'],
        'keywords': ['prison, friendship, redemption', 'mafia, family, power', 'crime, violence, redemption'],
        'cast': ['Tim Robbins, Morgan Freeman', 'Marlon Brando, Al Pacino', 'John Travolta, Samuel L. Jackson'],
        'crew': ['Frank Darabont', 'Francis Ford Coppola', 'Quentin Tarantino']
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('sample_movies_import.csv', index=False)
    print("✅ Sample CSV file created: sample_movies_import.csv")
    print("Edit this file and then run the import script again.")

def import_movies_from_csv(csv_file):
    """Import movies from a CSV file"""
    try:
        df = pd.read_csv(csv_file)
        print(f"Found {len(df)} movies in {csv_file}")
        
        movies = []
        for _, row in df.iterrows():
            # Parse comma-separated values
            genres = [g.strip() for g in str(row['genres']).split(',')] if pd.notna(row['genres']) else []
            keywords = [k.strip() for k in str(row['keywords']).split(',')] if pd.notna(row['keywords']) else []
            cast = [c.strip() for c in str(row['cast']).split(',')] if pd.notna(row['cast']) else []
            crew = [c.strip() for c in str(row['crew']).split(',')] if pd.notna(row['crew']) else []
            
            movie = {
                'title': str(row['title']),
                'overview': str(row['overview']) if pd.notna(row['overview']) else '',
                'genres': genres,
                'keywords': keywords,
                'cast': cast,
                'crew': crew
            }
            movies.append(movie)
            
        return movies
        
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def update_model_with_new_movies(new_movies):
    """Update the model with new movies"""
    print("Loading existing model...")
    movie_list, similarity = load_existing_model()
    
    if movie_list is None:
        return False
    
    print(f"Current movies in system: {len(movie_list)}")
    
    # Convert new movies to the same format as existing ones
    for movie in new_movies:
        # Create tags by combining all features
        tags = []
        if movie['overview']:
            tags.extend(movie['overview'].split())
        tags.extend(movie['genres'])
        tags.extend(movie['keywords'])
        tags.extend(movie['cast'])
        tags.extend(movie['crew'])
        
        # Add to movie list
        new_row = pd.DataFrame([{
            'movie_id': f"custom_{len(movie_list) + 1}",
            'title': movie['title'],
            'tags': ' '.join(tags)
        }])
        
        movie_list = pd.concat([movie_list, new_row], ignore_index=True)
    
    print(f"Updated movies in system: {len(movie_list)}")
    
    # Recalculate similarity matrix
    print("Recalculating similarity matrix...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(movie_list['tags']).toarray()
    new_similarity = cosine_similarity(vector)
    
    # Save updated model
    print("Saving updated model...")
    pickle.dump(movie_list, open('model/movie_list.pkl', 'wb'))
    pickle.dump(new_similarity, open('model/similarity.pkl', 'wb'))
    
    print("Model updated successfully!")
    return True

def main():
    """Main function for batch import"""
    print("🎬 Batch Import Movies to Recommender System")
    print("=" * 50)
    
    # Check if model exists
    if not os.path.exists('model/movie_list.pkl'):
        print("Model files not found. Please run generate_model.py first.")
        return
    
    csv_file = input("Enter CSV file path (or 'sample' to create sample file): ").strip()
    
    if csv_file.lower() == 'sample':
        create_sample_csv()
        return
    
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return
    
    # Import movies from CSV
    movies = import_movies_from_csv(csv_file)
    if movies is None:
        return
    
    # Show preview
    print("\nPreview of movies to import:")
    for i, movie in enumerate(movies[:5]):  # Show first 5
        print(f"{i+1}. {movie['title']}")
    if len(movies) > 5:
        print(f"... and {len(movies) - 5} more")
    
    # Confirm import
    confirm = input(f"\nImport {len(movies)} movies? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Import cancelled.")
        return
    
    # Update model
    if update_model_with_new_movies(movies):
        print("🎉 Movies imported successfully!")
        print("You can now restart the Streamlit app to see the new movies.")
    else:
        print("❌ Failed to import movies.")

if __name__ == "__main__":
    main()

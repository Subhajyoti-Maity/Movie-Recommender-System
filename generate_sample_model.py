import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_sample_data():
    """Generate sample movie data for demonstration"""
    print("Generating sample movie data...")
    
    # Sample movie data with more realistic TMDB IDs
    sample_movies = [
        {
            'movie_id': 278,  # The Shawshank Redemption
            'title': 'The Shawshank Redemption',
            'overview': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'genres': ['Drama'],
            'keywords': ['prison', 'friendship', 'redemption'],
            'cast': ['Tim Robbins', 'Morgan Freeman'],
            'crew': ['Frank Darabont']
        },
        {
            'movie_id': 238,  # The Godfather
            'title': 'The Godfather',
            'overview': 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
            'genres': ['Crime', 'Drama'],
            'keywords': ['mafia', 'family', 'crime'],
            'cast': ['Marlon Brando', 'Al Pacino'],
            'crew': ['Francis Ford Coppola']
        },
        {
            'movie_id': 680,  # Pulp Fiction
            'title': 'Pulp Fiction',
            'overview': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
            'genres': ['Crime', 'Drama'],
            'keywords': ['crime', 'violence', 'redemption'],
            'cast': ['John Travolta', 'Samuel L. Jackson'],
            'crew': ['Quentin Tarantino']
        },
        {
            'movie_id': 155,  # The Dark Knight
            'title': 'The Dark Knight',
            'overview': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham.',
            'genres': ['Action', 'Crime', 'Drama'],
            'keywords': ['superhero', 'batman', 'joker'],
            'cast': ['Christian Bale', 'Heath Ledger'],
            'crew': ['Christopher Nolan']
        },
        {
            'movie_id': 550,  # Fight Club
            'title': 'Fight Club',
            'overview': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club.',
            'genres': ['Drama'],
            'keywords': ['fight club', 'underground', 'rebellion'],
            'cast': ['Brad Pitt', 'Edward Norton'],
            'crew': ['David Fincher']
        },
        {
            'movie_id': 27205,  # Inception
            'title': 'Inception',
            'overview': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task.',
            'genres': ['Action', 'Adventure', 'Sci-Fi'],
            'keywords': ['dreams', 'technology', 'heist'],
            'cast': ['Leonardo DiCaprio', 'Joseph Gordon-Levitt'],
            'crew': ['Christopher Nolan']
        },
        {
            'movie_id': 603,  # The Matrix
            'title': 'The Matrix',
            'overview': 'A computer programmer discovers that reality as he knows it is a simulation created by machines.',
            'genres': ['Action', 'Sci-Fi'],
            'keywords': ['matrix', 'simulation', 'reality'],
            'cast': ['Keanu Reeves', 'Laurence Fishburne'],
            'crew': ['Lana Wachowski', 'Lilly Wachowski']
        },
        {
            'movie_id': 769,  # Goodfellas
            'title': 'Goodfellas',
            'overview': 'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen.',
            'genres': ['Biography', 'Crime', 'Drama'],
            'keywords': ['mafia', 'organized crime', 'biography'],
            'cast': ['Robert De Niro', 'Ray Liotta'],
            'crew': ['Martin Scorsese']
        },
        {
            'movie_id': 274,  # The Silence of the Lambs
            'title': 'The Silence of the Lambs',
            'overview': 'A young FBI cadet must receive the help of an incarcerated and manipulative killer.',
            'genres': ['Crime', 'Drama', 'Thriller'],
            'keywords': ['fbi', 'serial killer', 'psychological'],
            'cast': ['Jodie Foster', 'Anthony Hopkins'],
            'crew': ['Jonathan Demme']
        },
        {
            'movie_id': 157336,  # Interstellar
            'title': 'Interstellar',
            'overview': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.',
            'genres': ['Adventure', 'Drama', 'Sci-Fi'],
            'keywords': ['space', 'wormhole', 'survival'],
            'cast': ['Matthew McConaughey', 'Anne Hathaway'],
            'crew': ['Christopher Nolan']
        }
    ]
    
    # Create DataFrame
    movies_df = pd.DataFrame(sample_movies)
    
    # Process the data similar to the original notebook
    movies_df['tags'] = (
        movies_df['overview'].apply(lambda x: x.split()) +
        movies_df['genres'] +
        movies_df['keywords'] +
        movies_df['cast'] +
        movies_df['crew']
    )
    
    # Join tags into a single string
    movies_df['tags'] = movies_df['tags'].apply(lambda x: ' '.join(x))
    
    # Select final columns
    final_df = movies_df[['movie_id', 'title', 'tags']]
    
    print(f"Generated {len(final_df)} sample movies")
    return final_df

def generate_model():
    """Generate the movie recommendation model"""
    print("Generating movie recommendation model...")
    
    # Get sample data
    movies = generate_sample_data()
    
    # Create feature vectors using CountVectorizer
    cv = CountVectorizer(max_features=100, stop_words='english')
    vector = cv.fit_transform(movies['tags']).toarray()
    
    print(f"Feature vector shape: {vector.shape}")
    
    # Calculate cosine similarity
    print("Calculating cosine similarity...")
    similarity = cosine_similarity(vector)
    
    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)
    
    # Save the model files
    print("Saving model files...")
    pickle.dump(movies, open('model/movie_list.pkl', 'wb'))
    pickle.dump(similarity, open('model/similarity.pkl', 'wb'))
    
    print("Model files generated successfully!")
    print("Files saved:")
    print("- model/movie_list.pkl")
    print("- model/similarity.pkl")
    
    return True

def main():
    """Main function to generate the sample model"""
    print("Movie Recommender System - Sample Model Generation")
    print("=" * 55)
    
    # Check if model files already exist
    if os.path.exists('model/movie_list.pkl') and os.path.exists('model/similarity.pkl'):
        print("Model files already exist!")
        return True
    
    # Generate the model
    if generate_model():
        print("\nSample model generation completed successfully!")
        print("You can now run the Streamlit app with: streamlit run app.py")
        return True
    else:
        print("Model generation failed!")
        return False

if __name__ == "__main__":
    main()

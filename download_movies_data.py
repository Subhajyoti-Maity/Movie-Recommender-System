import pandas as pd
import requests
import os
import zipfile
from io import BytesIO

def download_from_kaggle():
    """Download from Kaggle (requires kaggle CLI)"""
    try:
        import kaggle
        print("Downloading from Kaggle...")
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('rounakbanik/tmdb-movie-metadata', path='.', unzip=True)
        return True
    except ImportError:
        print("Kaggle package not installed. Install with: pip install kaggle")
        return False
    except Exception as e:
        print(f"Kaggle download failed: {e}")
        return False

def download_from_alternative_sources():
    """Try alternative movie data sources"""
    sources = [
        {
            "name": "MovieLens Dataset",
            "url": "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip",
            "filename": "ml-latest-small.zip"
        },
        {
            "name": "IMDB Dataset",
            "url": "https://datasets.imdbws.com/title.basics.tsv.gz",
            "filename": "title.basics.tsv.gz"
        }
    ]
    
    for source in sources:
        try:
            print(f"Trying {source['name']}...")
            response = requests.get(source['url'], stream=True)
            response.raise_for_status()
            
            with open(source['filename'], 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Downloaded {source['name']}")
            
            # Extract if it's a zip file
            if source['filename'].endswith('.zip'):
                with zipfile.ZipFile(source['filename'], 'r') as zip_ref:
                    zip_ref.extractall('.')
                print(f"✅ Extracted {source['filename']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to download {source['name']}: {e}")
            continue
    
    return False

def create_sample_dataset():
    """Create a sample dataset with popular movies"""
    print("Creating sample dataset with popular movies...")
    
    sample_movies = [
        {
            'title': 'The Shawshank Redemption',
            'overview': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'genres': ['Drama'],
            'keywords': ['prison', 'friendship', 'redemption', 'hope'],
            'cast': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton'],
            'crew': ['Frank Darabont', 'Stephen King']
        },
        {
            'title': 'The Godfather',
            'overview': 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
            'genres': ['Crime', 'Drama'],
            'keywords': ['mafia', 'family', 'power', 'crime'],
            'cast': ['Marlon Brando', 'Al Pacino', 'James Caan'],
            'crew': ['Francis Ford Coppola', 'Mario Puzo']
        },
        {
            'title': 'Pulp Fiction',
            'overview': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
            'genres': ['Crime', 'Drama'],
            'keywords': ['crime', 'violence', 'redemption', 'gangsters'],
            'cast': ['John Travolta', 'Samuel L. Jackson', 'Uma Thurman'],
            'crew': ['Quentin Tarantino']
        },
        {
            'title': 'The Dark Knight',
            'overview': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
            'genres': ['Action', 'Crime', 'Drama'],
            'keywords': ['batman', 'joker', 'gotham', 'justice'],
            'cast': ['Christian Bale', 'Heath Ledger', 'Aaron Eckhart'],
            'crew': ['Christopher Nolan', 'Jonathan Nolan']
        },
        {
            'title': 'Fight Club',
            'overview': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.',
            'genres': ['Drama'],
            'keywords': ['fight club', 'insomnia', 'underground', 'rebellion'],
            'cast': ['Brad Pitt', 'Edward Norton', 'Helena Bonham Carter'],
            'crew': ['David Fincher', 'Chuck Palahniuk']
        }
    ]
    
    # Convert to DataFrame format compatible with the model
    processed_movies = []
    for i, movie in enumerate(sample_movies):
        tags = []
        if movie['overview']:
            tags.extend(movie['overview'].split())
        tags.extend(movie['genres'])
        tags.extend(movie['keywords'])
        tags.extend(movie['cast'])
        tags.extend(movie['crew'])
        
        processed_movies.append({
            'movie_id': f"sample_{i+1}",
            'title': movie['title'],
            'tags': ' '.join(tags)
        })
    
    # Save as pickle file
    import pickle
    os.makedirs('model', exist_ok=True)
    
    df = pd.DataFrame(processed_movies)
    pickle.dump(df, open('model/movie_list.pkl', 'wb'))
    
    # Create similarity matrix
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(df['tags']).toarray()
    similarity = cosine_similarity(vector)
    
    pickle.dump(similarity, open('model/similarity.pkl', 'wb'))
    
    print("✅ Sample dataset created with 5 popular movies!")
    print("Files saved:")
    print("- model/movie_list.pkl")
    print("- model/similarity.pkl")
    
    return True

def main():
    """Main function to download movie data"""
    print("🎬 Movie Data Downloader")
    print("=" * 40)
    
    print("Attempting to download movie data from various sources...")
    
    # Try different download methods
    if download_from_kaggle():
        print("✅ Successfully downloaded from Kaggle!")
        return True
    
    if download_from_alternative_sources():
        print("✅ Successfully downloaded from alternative source!")
        return True
    
    print("❌ All download methods failed.")
    print("\nCreating sample dataset instead...")
    
    if create_sample_dataset():
        print("\n🎉 Sample dataset created successfully!")
        print("You can now run the Streamlit app and add more movies using:")
        print("- python add_custom_movies.py (for individual movies)")
        print("- python batch_import_movies.py (for batch import)")
        return True
    
    return False

if __name__ == "__main__":
    main()

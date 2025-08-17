# 🎬 Movie Recommender System

A **colorful and modern** content-based movie recommendation system built with Streamlit, featuring beautiful gradients, interactive UI elements, **advanced search functionality**, **guaranteed trailer links for ALL movies**, **enhanced streaming services**, **personal movie collections**, and intelligent movie suggestions based on cosine similarity.

## ✨ Features

- 🎨 **Beautiful Colorful UI** - Modern gradient backgrounds and stylish design
- 🔍 **Advanced Search System** - Real-time movie filtering and search capabilities
- 🎭 **Smart Recommendations** - Content-based filtering using movie features
- 🎬 **Guaranteed Trailer Links** - **EVERY movie now has trailer access** - direct YouTube links or smart search
- 📺 **Enhanced Streaming Services** - Accurate availability for Disney+, Netflix Originals, Hotstar, and more
- 🖼️ **Movie Posters** - Real-time poster fetching from multiple APIs with fallback images
- 🚀 **Interactive Interface** - Hover effects, smooth animations, and responsive design
- 📱 **Wide Layout** - Optimized for desktop and tablet viewing
- 🎯 **Easy to Use** - Enhanced search with dropdown selection and one-click recommendations
- 🔍 **Smart Filtering** - Instant search results as you type
- 🗑️ **Search Management** - Clear search functionality and helpful tips
- 🌍 **Multi-language Support** - Support for various languages and regions
- 📊 **Personal Collections** - **Complete control over watch history, watchlist, and favorites**
- 🎬 **Popular Movies Section** - Quick access to trending films with collection status
- 🔍 **Collection Search & Add** - Dedicated system to add any movie to your collections

## 🎬 **NEW: Guaranteed Trailer Links for ALL Movies**

- **100% Coverage**: **Every single movie now has guaranteed trailer access** - no more "no trailer available" messages!
- **Direct Links**: Popular movies get direct YouTube trailer links that open immediately
- **Smart Search**: All other movies get intelligent YouTube search URLs that filter for trailers only
- **Multiple Search Variations**: Different search terms for better results (official trailer, teaser, year-specific)
- **Embedded Viewing**: Watch trailers directly in the app or open on YouTube
- **No More Warnings**: Every movie shows trailer options instead of "no trailer available"

### 🎬 **Trailer System Features:**
- **Direct YouTube Integration**: Official trailer links for 100+ popular movies
- **Smart Fallbacks**: Intelligent search for any movie not in our direct database
- **Multiple Search Options**: Try different search terms for better results
- **Year-Specific Searches**: Include release year for more accurate trailer finding
- **Trailer Filtering**: YouTube search parameters that focus on video content only
- **Comprehensive Coverage**: Works for classic movies, new releases, indie films, and everything in between

### 🎬 **Trailer Coverage Includes:**
- **Classic Movies**: The Dark Knight, Inception, The Matrix, Pulp Fiction, The Godfather
- **Disney/Pixar**: Frozen, Toy Story, Finding Nemo, Moana, Coco, Zootopia, Encanto
- **Marvel Movies**: Avengers: Endgame, Iron Man, Captain America, Thor, Black Panther
- **Star Wars**: All main saga films and spin-offs
- **Recent Hits**: Joker, Parasite, La La Land, Get Out, A Quiet Place
- **Indian Movies**: RRR, Baahubali, KGF, Dangal, 3 Idiots
- **Action & Comedy**: Mad Max, John Wick, Deadpool, The Grand Budapest Hotel
- **And Much More**: Every movie in your database now has trailer access!

## 📊 **NEW: Enhanced Personal Collections System**

- **Complete User Control**: **No automatic additions** - you decide exactly what goes in your collections
- **Three Collection Types**: Watch History, Watchlist, and Favorites
- **Smart Search & Add**: Dedicated system to find and add any movie to your collections
- **Quick Add Popular Movies**: Dropdown with popular movie suggestions
- **Manual Search**: Type any movie name to add to collections
- **Collection Status Display**: See which movies are already in your collections
- **Easy Management**: Remove movies, clear entire collections, and manage your movie library

### 📊 **Collection Features:**
- **Watch History**: Track movies you've watched or trailers you've viewed
- **Watchlist**: Build a list of movies you want to watch later
- **Favorites**: Keep track of your all-time favorite movies
- **Smart Search**: Find movies by partial names, case-insensitive matching
- **Debug Information**: See available movies in your database
- **Collection Statistics**: Track how many movies are in each collection
- **No Default Options**: Collections start completely empty - you build them your way

## 📺 **Enhanced Streaming Services**

- **Accurate Availability**: Only shows services where movies are actually available
- **Disney+ Integration**: Smart detection of Disney/Pixar/Marvel/Star Wars content
- **Netflix Originals**: Automatic identification of Netflix-exclusive content
- **Hotstar (India)**: Dedicated support for Indian streaming platform
- **Multiple Platforms**: Netflix, Prime Video, HBO Max, Disney+, Hulu, Peacock
- **Search Tools**: Integration with JustWatch, Reelgood, Flixable, and Streaming Search

### 📺 **Streaming Service Features:**
- **Smart Detection**: Automatically identifies movie types and suggests appropriate platforms
- **Regional Support**: Hotstar for India, Disney+ for global users
- **No False Promises**: Only shows services with confirmed availability
- **External Search**: Links to comprehensive streaming availability checkers

## 🔍 Enhanced Search Features

- **Real-time Search**: Type to instantly filter movies
- **Smart Filtering**: Case-insensitive partial matching
- **Search Tips**: Helpful guidance for better search results
- **Clear Search**: Easy reset to see all movies again
- **Success Messages**: Shows count of matching movies
- **Fallback Options**: Always access to full movie list
- **Alphabetical Browsing**: Browse movies by starting letter
- **Popular Movies**: Quick access to trending and popular films

## 🎬 Sample Movies Included

The system comes with 10 popular movies for demonstration:
- The Shawshank Redemption
- The Godfather
- Pulp Fiction
- The Dark Knight
- Fight Club
- Inception
- The Matrix
- Goodfellas
- The Silence of the Lambs
- Interstellar

## 🛠️ Technology Stack

- **Frontend**: Streamlit (with custom CSS styling)
- **Backend**: Python 3.12+
- **Machine Learning**: Scikit-learn (CountVectorizer, Cosine Similarity)
- **Data Processing**: Pandas, NumPy
- **API Integration**: Multiple movie APIs with enhanced fallback systems
- **Styling**: Custom CSS with gradients and animations
- **Search Engine**: Custom Python-based filtering system
- **Trailer System**: **Guaranteed YouTube integration for ALL movies**
- **Streaming Services**: Smart platform detection and availability checking
- **Collection Management**: Session state management with user control

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for API calls and trailer access)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd movie-recommender-system-tmdb-dataset-main
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Model Files
```bash
python generate_sample_model.py
```

### 4. Run the Application
```bash
streamlit run app.py
```

## 🌐 Access the Application

Once running, open your browser and navigate to:
- **Local**: http://localhost:8501
- **Network**: http://[your-ip]:8501

## 🎯 How to Use

### 🔍 **Search & Select Movies**
1. **Search for Movies**: Type any part of a movie title in the search box
2. **See Instant Results**: Movies are filtered in real-time as you type
3. **Select from Results**: Choose from filtered movies or all available movies
4. **Clear Search**: Use the clear button to reset and see all movies again
5. **Browse Alphabetically**: Click letters to see movies starting with specific characters
6. **Popular Movies**: Click on popular movie buttons for instant selection

### 🎬 **Get Recommendations & Trailers**
1. **Choose a Movie**: Select from search results, dropdown, or popular movies
2. **Get Recommendations**: Click the "🎯 Show Recommendations" button
3. **Watch Trailers**: **Every movie now has guaranteed trailer access!**
   - **Direct Links**: Popular movies open trailers immediately on YouTube
   - **Smart Search**: Other movies get intelligent YouTube search results
   - **Multiple Options**: Try different search terms for better results
4. **View Results**: See 5 similar movies with titles, posters, and trailer links
5. **Explore**: Each recommendation shows movie details and visual elements

### 📊 **Manage Your Collections**
1. **Add Movies**: Use the "🔍 Add Movies" section in the right column
2. **Quick Add**: Select from popular movie dropdown
3. **Manual Search**: Type any movie name to add to collections
4. **Choose Collection**: Add to Watchlist, Favorites, or History
5. **View Status**: See which movies are already in your collections
6. **Manage**: Remove movies or clear entire collections

### 📺 **Find Streaming Options**
1. **Check Availability**: See which streaming platforms have the movie
2. **Direct Links**: Click platform buttons to go directly to the movie
3. **Search Tools**: Use external services to check comprehensive availability
4. **Regional Options**: Access platform-specific links for your region

### 💡 **Search Tips**
- Type partial titles: "Batman" finds all Batman movies
- Use keywords: "Star" finds Star Wars, Star Trek, etc.
- Search genres: "Avengers" finds Marvel movies
- Case doesn't matter: "dark knight" works the same as "Dark Knight"
- Browse by letter: Click alphabetical buttons for organized viewing
- **Collection Search**: Use the dedicated search system to add movies to your collections

## 🔧 How It Works

### Content-Based Filtering
The system analyzes movie features including:
- **Overview/Plot** - Story descriptions and themes
- **Genres** - Movie categories and styles
- **Keywords** - Important themes and topics
- **Cast** - Actors and performers
- **Crew** - Directors, writers, and producers

### Recommendation Algorithm
1. **Feature Extraction**: Convert text data to numerical vectors using CountVectorizer
2. **Similarity Calculation**: Compute cosine similarity between all movie pairs
3. **Ranking**: Sort movies by similarity scores
4. **Selection**: Return top 5 most similar movies

### **Enhanced Trailer System**
1. **Guaranteed Coverage**: **Every movie gets trailer access** - no exceptions!
2. **Direct Mapping**: 100+ movies with verified YouTube trailer URLs
3. **Smart Fallbacks**: For unmapped movies, provides intelligent YouTube search
4. **Multiple Search Variations**: Different search terms for better results
5. **Year-Specific Searches**: Include release year when available
6. **Embedded Viewing**: Shows both direct links and embedded players

### **Personal Collections Management**
1. **User Control**: **No automatic additions** - you decide what goes in collections
2. **Smart Search**: Find movies by partial names with case-insensitive matching
3. **Multiple Sources**: Search both main database and popular movies
4. **Collection Types**: Watch History, Watchlist, and Favorites
5. **Easy Management**: Add, remove, and clear collections as needed

### Streaming Service Detection
1. **Content Analysis**: Identifies Disney, Marvel, Netflix, and other content types
2. **Platform Mapping**: Maps movies to appropriate streaming services
3. **Availability Checking**: Only shows services with confirmed availability
4. **Regional Support**: Provides platform-specific links for different regions

### Search Algorithm
1. **Input Processing**: Clean and normalize search terms
2. **Pattern Matching**: Find movies containing search terms
3. **Real-time Filtering**: Update results as user types
4. **Smart Fallbacks**: Provide alternatives when no matches found

### Poster Fetching
- **Primary**: Fetch real posters from multiple movie APIs
- **Fallback**: Display colorful placeholder images if posters unavailable
- **Error Handling**: Graceful degradation for API failures

## 🎨 UI Features

- **Gradient Headers**: Rainbow-colored main title with movie emojis
- **Colorful Sections**: Different gradient backgrounds for each UI component
- **Interactive Elements**: Hover effects on buttons and movie cards
- **Responsive Design**: Adapts to different screen sizes
- **Smooth Animations**: Transform effects and transitions
- **Search Interface**: Modern search box with instant feedback
- **Success Messages**: Colorful notifications for search results
- **Helpful Tips**: User guidance and search suggestions
- **Trailer Buttons**: Eye-catching buttons for **guaranteed trailer access**
- **Streaming Service Grid**: Organized display of available platforms
- **Collection Management**: Dedicated interface for managing your movie collections
- **Popular Movies Grid**: Interactive buttons for quick movie selection

## 📁 Project Structure

```
movie-recommender-system-tmdb-dataset-main/
├── app.py                          # Main Streamlit application with ALL features
├── enhanced_movie_service.py       # Enhanced movie data service
├── generate_sample_model.py        # Script to generate sample model data
├── generate_model.py               # Script for full TMDB dataset (optional)
├── requirements.txt                # Python dependencies
├── model/                          # Generated model files
│   ├── movie_list.pkl             # Movie data and features
│   └── similarity.pkl             # Cosine similarity matrix
├── notebook86c26b4f17.ipynb       # Original Jupyter notebook
├── Procfile                        # Deployment configuration
├── Dockerfile                      # Docker containerization
└── README.md                       # This file
```

## 🔮 Future Enhancements

- [x] **Advanced Search System** - Real-time movie filtering ✅
- [x] **Enhanced UI/UX** - Better search interface and user experience ✅
- [x] **Guaranteed Trailer Links** - **EVERY movie now has trailer access** ✅
- [x] **Enhanced Streaming Services** - Smart platform detection ✅
- [x] **Personal Collections** - **Complete user control over collections** ✅
- [x] **Alphabetical Browsing** - Letter-based movie organization ✅
- [x] **Popular Movies Section** - Quick access to trending films ✅
- [x] **Collection Search & Add** - Dedicated system for managing collections ✅
- [x] **Multiple Trailer Search Options** - Different search terms for better results ✅
- [ ] **User Authentication** - Personal recommendation profiles
- [ ] **Rating System** - User feedback integration
- [ ] **More Movies** - Expand to full TMDB dataset
- [ ] **Advanced Filtering** - Genre, year, rating preferences
- [ ] **Export Features** - Save recommendations to file
- [ ] **Mobile Optimization** - Better mobile experience
- [ ] **Search History** - Remember recent searches
- [ ] **Voice Search** - Speech-to-text movie search
- [ ] **Trailer Recommendations** - Suggest similar trailers
- [ ] **Streaming Price Comparison** - Cost analysis across platforms

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill existing Streamlit processes
   taskkill /f /im streamlit.exe
   ```

2. **Model Files Missing**
   ```bash
   # Regenerate model files
   python generate_sample_model.py
   ```

3. **Search Not Working**
   - Ensure you're typing in the search box
   - Check that the app has loaded completely
   - Try refreshing the page if issues persist

4. **Trailer Links Not Working**
   - **Every movie now has guaranteed trailer access!**
   - Check internet connection
   - Ensure YouTube is accessible in your region
   - Try refreshing the page

5. **Streaming Services Not Showing**
   - Check if the movie is in our database
   - Use external search tools for comprehensive results
   - Some movies may not be available on streaming platforms

6. **Collections Not Working**
   - Use the dedicated "🔍 Add Movies" section in the right column
   - Try different search terms if movie not found
   - Check the debug info to see available movies

### Error Messages

- **"No such file or directory: 'model/movie_list.pkl'"** → Run `generate_sample_model.py`
- **"Port 8501 is already in use"** → Kill existing processes or use different port
- **"KeyError: 'poster_path'"** → API error, fallback to placeholder images
- **Search not responding** → Check internet connection and refresh page
- **"No movies found" in collections** → Try different search terms or check spelling

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample model
python generate_sample_model.py

# Run the app
streamlit run app.py

# Access at http://localhost:8501
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **TMDB** - For movie data and poster images
- **YouTube** - For **guaranteed trailer integration for ALL movies**
- **Streamlit** - For the amazing web app framework
- **Scikit-learn** - For machine learning algorithms
- **Community** - For inspiration and feedback

---

**🎬 Made with ❤️ and lots of 🎨 colors!**

*Enjoy discovering your next favorite movie with our **guaranteed trailer access for ALL movies**, enhanced search system, smart streaming recommendations, and complete control over your personal movie collections!*

## 🆕 **Latest Updates**

### **Version 2.0 - Complete Trailer Coverage**
- ✅ **Every movie now has guaranteed trailer access**
- ✅ **No more "no trailer available" messages**
- ✅ **Smart fallback system for all movies**
- ✅ **Multiple search variations for better results**

### **Version 1.5 - Enhanced Collections**
- ✅ **Complete user control over collections**
- ✅ **No automatic additions - you decide everything**
- ✅ **Smart search system for adding movies**
- ✅ **Dedicated collection management interface**

### **Version 1.0 - Core Features**
- ✅ **Advanced search and filtering**
- ✅ **Content-based recommendations**
- ✅ **Enhanced streaming service detection**
- ✅ **Beautiful modern UI design**

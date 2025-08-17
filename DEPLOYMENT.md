# 🚀 Deployment Guide

## 🌐 **Streamlit Cloud (Recommended)**

### 1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit: Movie Recommender System"
git push origin main
```

### 2. **Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set the path to your app: `app.py`
6. Click "Deploy!"

## 🐳 **Docker Deployment**

### 1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. **Build and Run**
```bash
docker build -t movie-recommender .
docker run -p 8501:8501 movie-recommender
```

## ☁️ **Heroku Deployment**

### 1. **Create Procfile**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### 2. **Deploy**
```bash
heroku create your-app-name
git push heroku main
```

## 📱 **Local Development**

### 1. **Clone and Setup**
```bash
git clone <your-repo-url>
cd movie-recommender-system-tmdb-dataset-main
pip install -r requirements.txt
python generate_sample_model.py
streamlit run app.py
```

### 2. **Access at**: http://localhost:8501

## 🔧 **Environment Variables**

Create a `.env` file for local development:
```env
TMDB_API_KEY=your_api_key_here
```

## 📊 **Performance Tips**

- **Model Files**: Include `model/*.pkl` in your repo for faster startup
- **Caching**: Use `@st.cache_data` for expensive operations
- **API Limits**: Implement rate limiting for TMDB API calls

## 🚨 **Important Notes**

- **API Keys**: Never commit API keys to public repositories
- **Model Size**: Large model files may slow down deployment
- **Dependencies**: Ensure all requirements are compatible with deployment platform

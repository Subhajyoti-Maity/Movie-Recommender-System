# 🎬 Adding More Movies to Your Recommender System

This guide explains how to add more movies to your movie recommender system.

## 🚀 Quick Start Options

### Option 1: Download Larger Dataset (Recommended)
Run the enhanced model generator to get more movies from TMDB:

```bash
python generate_model.py
```

This will download a more comprehensive dataset with thousands of additional movies.

### Option 2: Add Custom Movies One by One
Use the interactive script to add movies manually:

```bash
python add_custom_movies.py
```

Follow the prompts to enter:
- Movie title
- Overview/description
- Genres (comma-separated)
- Keywords (comma-separated)
- Cast members (comma-separated)
- Crew members (comma-separated)

### Option 3: Batch Import from CSV
Import multiple movies at once from a CSV file:

```bash
python batch_import_movies.py
```

Type `sample` when prompted to create a sample CSV file with the correct format.

## 📁 CSV Format for Batch Import

Your CSV should have these columns:
- `title`: Movie title
- `overview`: Movie description
- `genres`: Comma-separated genres
- `keywords`: Comma-separated keywords
- `cast`: Comma-separated cast members
- `crew`: Comma-separated crew members

Example:
```csv
title,overview,genres,keywords,cast,crew
The Shawshank Redemption,Two imprisoned men bond over years...,Drama,prison friendship redemption,Tim Robbins Morgan Freeman,Frank Darabont
```

## 🔧 After Adding Movies

1. **Restart the Streamlit app** to see new movies:
   ```bash
   streamlit run app.py
   ```

2. **Verify new movies** appear in the dropdown menu

3. **Test recommendations** with the new movies

## 📊 Current System Status

- **Original movies**: ~5000 from TMDB dataset
- **Enhanced dataset**: Up to 45,000+ movies (when using extended dataset)
- **Custom movies**: Unlimited (added manually or via CSV)

## 🎯 Tips for Better Recommendations

- **Be specific with genres**: Use detailed genre combinations
- **Include key cast/crew**: Major actors and directors help with recommendations
- **Add relevant keywords**: Include themes, settings, and plot elements
- **Quality over quantity**: Better movie descriptions lead to better recommendations

## 🚨 Important Notes

- Adding movies requires regenerating the similarity matrix
- The process may take a few minutes for large datasets
- Always backup your model files before major changes
- New movies are integrated seamlessly with existing ones

## 🆘 Troubleshooting

**"Model files not found"**: Run `python generate_model.py` first
**"Import failed"**: Check CSV format and ensure all required columns exist
**"App not showing new movies"**: Restart the Streamlit application

---

Happy movie recommending! 🎭🍿

# activate Python virtual environment
echo "[Starting Fastapi kor-recipe-recommender]"
source kor-recipe/Scripts/activate
cd ndjango-django/recipe-recommender2

# Run the Fastapi development server
uvicorn main:app --port=6000

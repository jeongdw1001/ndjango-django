# activate Python virtual environment
echo "[Starting Flask photo predict]"
source photo-predict/Scripts/activate
cd ndjango-django/photo_predict
# Set environment variables
# export PYTHONDONTWRITEBYTECODE=1
# export PYTHONUNBUFFERED=1
# export FLASK_APP="photo_predict.py"
# export FLASK_ENV="production"
# echo $FLASK_APP

# Run the Flask development server
# flask run -h "0.0.0.0" -p 7000
python photo_predict.py

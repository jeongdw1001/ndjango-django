# activate Python virtual environment
echo "[Starting Django main app]"
source main/Scripts/activate
# Run the Django development server
cd ndjango-django/ndjango
echo "http://127.0.0.1:8000/"
python manage.py runserver
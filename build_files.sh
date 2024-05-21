echo "BUILD START"

# Use python3 instead of python3.11 if the latter is not available
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear

# Verify that the static files were collected
echo "BUILD END"

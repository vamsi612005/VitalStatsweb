echo "BUILD START"

# Use python3 instead of python3.11 if the latter is not available
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear

# Verify that the static files were collected
if [ -d "staticfiles_build" ]; then
  echo "Static files collected successfully."
else
  echo "Error: staticfiles_build directory not found."
  exit 1
fi

echo "BUILD END"

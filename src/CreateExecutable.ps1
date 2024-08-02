# Install all necessary requirements on your environment
pip install -r requirements.txt

# Run PyInstaller to create the executable
pyinstaller --onefile --icon=img/jobfinder-logo.ico --distpath .. JobFinder.py

# Check if the .spec file exists and delete it
if (Test-Path "JobFinder.spec") {
    Remove-Item "JobFinder.spec"
}

# Check if the build folder exists and delete it
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
@echo off
echo Installing GeoLoader...

:: Set the installation directory
set INSTALL_DIR=%USERPROFILE%\GeoLoader

:: Install dependencies using Chocolatey (ensure Chocolatey is installed)
echo Installing dependencies...
choco install -y git python3 cmake

:: Clone the GeoLoader repository
echo Cloning GeoLoader repository...
git clone https://github.com/entity12208/GeoLoader.git %INSTALL_DIR%

:: Navigate to the GeoLoader directory
cd %INSTALL_DIR%

:: Set up Python virtual environment
echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Install Python dependencies
pip install -r requirements.txt

:: Build GeoLoader
echo Building GeoLoader...
call build.bat

echo GeoLoader installation complete. You can now run GeoLoader or create mods.
pause

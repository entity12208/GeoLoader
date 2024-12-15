# GeoLoader CLI Documentation
GeoLoader is a Command Line Interface (CLI) tool designed to help create and manage Geometry Dash mods. It supports Windows, Linux, and macOS and provides features to simplify mod creation and building.

## Features
* Create Mods: Generate mod templates with all necessary files.
* Install Mods: Install mods for Geometry Dash with platform-specific install procedures.
* Build Mods: Compile .gloader files to integrate mods with the game.
## Installation
### Requirements
* Python 3.x or C++ for mod development.
* Geometry Dash installed.
### Running GeoLoader
1. Clone the repository:
`git clone https://github.com/entity12208/GeoLoader.git`
2. Navigate to the directory:
`cd GeoLoader`
3. For Linux/MacOS:
`./install.sh`
3. For Windows:
`install.bat`
## Command Usage
**geoloader new**
Creates a new mod template.
This will prompt you for information such as the mod name, developer name, and description. It will generate the following files:
/src/
  main.cpp
mod.json
about.md
/build/

**geoloader build**
Builds the mod into a .gloader file that can be loaded into Geometry Dash.
This will compile your mod and output a .gloader file in the /build/ directory.

**geoloader install**
Installs the mod to Geometry Dash.
This command will copy the necessary files to the correct location for Geometry Dash to load the mod.

## Contributing
Feel free to submit pull requests, report issues, or improve the documentation.

## License
GeoLoader is licensed under the BSL 1.0 License. For more details, see [LICENSE](https://github.com/entity12208/GeoLoader/LICENSE).

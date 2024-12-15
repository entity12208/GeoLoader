import json
import os

def load_config():
    with open('config.json') as f:
        return json.load(f)

def create_mod_template(mod_name):
    base_path = f"mods/{mod_name}"
    os.makedirs(base_path, exist_ok=True)
    os.makedirs(f"{base_path}/src", exist_ok=True)
    os.makedirs(f"{base_path}/build", exist_ok=True)

    with open(f"{base_path}/src/main.cpp", 'w') as f:
        f.write("// Main code for the project\n")

    with open(f"{base_path}/mod.json", 'w') as f:
        f.write(json.dumps({
            "name": mod_name,
            "version": "1.0.0",
            "description": "A new mod for GeoLoader",
            "author": "Your Name",
            "geoLoaderVersion": "1.0.0",
            "gdVersion": "2.11"
        }, indent=4))

    with open(f"{base_path}/about.md", 'w') as f:
        f.write(f"# {mod_name}\n\nDescription of your mod.\n")

    print(f"Mod template for {mod_name} created successfully.")

def main():
    config = load_config()
    print(f"GeoLoader version: {config['version']}")

    mod_name = input("Enter the name of the new mod: ")
    create_mod_template(mod_name)

if __name__ == "__main__":
    main()

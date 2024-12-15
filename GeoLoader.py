import json
import os
import subprocess
import platform
import shutil
import requests
import zipfile

def load_config(profile="default"):
    try:
        with open(f'config_{profile}.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Profile '{profile}' not found, loading default configuration.")
        return json.load(open('config.json'))

def save_config(profile="default", config_data=None):
    if config_data is None:
        config_data = load_config(profile)
    with open(f'config_{profile}.json', 'w') as f:
        json.dump(config_data, f, indent=4)

def create_mod_template(mod_name, profile="default"):
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

    with open(f"{base_path}/{mod_name}.gloader", 'w') as f:
        f.write(json.dumps({
            "modName": mod_name,
            "sourceFiles": ["src/main.cpp"],
            "outputFile": f"build/{mod_name}.dll"
        }, indent=4))

    print(f"Mod template for {mod_name} created successfully.")

def build_mod(mod_name, profile="default"):
    config = load_config(profile)
    mod_path = f"mods/{mod_name}"
    gloader_file = f"{mod_path}/{mod_name}.gloader"

    if not os.path.exists(gloader_file):
        print(f"{gloader_file} does not exist.")
        return

    with open(gloader_file) as f:
        mod_config = json.load(f)

    source_files = mod_config["sourceFiles"]
    output_file = mod_config["outputFile"]

    compiler = "g++"
    if platform.system() == "Windows":
        compiler = "cl"

    source_paths = " ".join([f"{mod_path}/{src}" for src in source_files])
    compile_cmd = f"{compiler} {source_paths} -o {mod_path}/{output_file}"

    try:
        subprocess.check_call(compile_cmd, shell=True)
        print(f"Build successful! Output: {mod_path}/{output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")

def update(profile="default"):
    print("Checking for updates...")
    repo_url = "https://api.github.com/repos/entity12208/GeoLoader/releases/latest"
    response = requests.get(repo_url)
    latest_release = response.json()

    version = latest_release['tag_name']
    download_url = latest_release['assets'][0]['browser_download_url']

    print(f"Updating GeoLoader to version {version}...")

    # Download the new version
    r = requests.get(download_url, stream=True)
    with open("geoloader_update.zip", "wb") as f:
        shutil.copyfileobj(r.raw, f)

    # Extract the files
    with zipfile.ZipFile("geoloader_update.zip", "r") as zip_ref:
        zip_ref.extractall("geoloader_update")

    # Replace old files
    for root, dirs, files in os.walk("geoloader_update"):
        for file in files:
            shutil.move(os.path.join(root, file), os.path.join(".", file))

    # Clean up
    shutil.rmtree("geoloader_update")
    os.remove("geoloader_update.zip")
    print("Update completed successfully!")

def uninstall(profile="default"):
    print("Uninstalling GeoLoader...")

    # Remove GeoLoader files
    files_to_remove = ['geoloader.py', 'geoloader_update.zip', 'geoloader']
    for file in files_to_remove:
        if os.path.exists(file):
            if os.path.isdir(file):
                shutil.rmtree(file)
            else:
                os.remove(file)

    # Remove the profile config
    if os.path.exists(f'config_{profile}.json'):
        os.remove(f'config_{profile}.json')

    print("GeoLoader has been uninstalled.")

def list_profiles():
    print("Available profiles:")
    for filename in os.listdir("."):
        if filename.startswith("config_") and filename.endswith(".json"):
            profile_name = filename[7:-5]
            print(f"- {profile_name}")

def switch_profile():
    profiles = [filename[7:-5] for filename in os.listdir(".") if filename.startswith("config_") and filename.endswith(".json")]
    if not profiles:
        print("No profiles available.")
        return None
    print("Available profiles:")
    for i, profile in enumerate(profiles, start=1):
        print(f"{i}. {profile}")
    
    try:
        choice = int(input("Select a profile by number: "))
        return profiles[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None

def main():
    action = input("Enter 'create' to create a new mod template, 'build' to build an existing mod, 'update' to update, 'uninstall' to uninstall, 'list' to list profiles or 'switch' to switch profiles: ").strip().lower()

    if action == 'create':
        mod_name = input("Enter the name of the new mod: ")
        profile = input("Enter profile (default or switch profile): ")
        create_mod_template(mod_name, profile)
    elif action == 'build':
        mod_name = input("Enter the name of the mod to build: ")
        profile = input("Enter profile (default or switch profile): ")
        build_mod(mod_name, profile)
    elif action == 'update':
        profile = input("Enter profile (default or switch profile): ")
        update(profile)
    elif action == 'uninstall':
        profile = input("Enter profile (default or switch profile): ")
        uninstall(profile)
    elif action == 'list':
        list_profiles()
    elif action == 'switch':
        profile = switch_profile()
        if profile:
            print(f"Switched to profile: {profile}")
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()

import json
import os
import subprocess
import platform
import requests

def load_config(profile="default"):
    """Load configuration for the given profile or default."""
    config_file = f'config_{profile}.json'
    if not os.path.exists(config_file):
        print(f"Profile '{profile}' not found, loading default configuration.")
        config_file = 'config.json'
    with open(config_file) as f:
        return json.load(f)

def save_config(profile="default", config_data=None):
    """Save the current configuration to a profile."""
    if config_data is None:
        config_data = load_config(profile)
    with open(f'config_{profile}.json', 'w') as f:
        json.dump(config_data, f, indent=4)

def create_mod_template(mod_name):
    """Create a template for a new mod."""
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

def build_mod(mod_name):
    """Compile and build the mod from source."""
    config = load_config()
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

def update_from_release():
    """Update GeoLoader from the latest release."""
    release_info = load_config().get("releaseInfo", {})
    if not release_info:
        print("No release information found.")
        return

    version = release_info.get("version", "unknown")
    release_notes = release_info.get("releaseNotes", "No release notes available.")
    print(f"Updating GeoLoader to version {version}...\nRelease Notes: {release_notes}")

    # Pull from the release's assets (e.g., zip, tar)
    download_url = release_info.get("downloadUrl")
    if download_url:
        try:
            response = requests.get(download_url)
            with open(f"GeoLoader-{version}.zip", 'wb') as f:
                f.write(response.content)
            print(f"Downloaded release to GeoLoader-{version}.zip")
            # You can also add logic here to extract and replace files.
        except requests.RequestException as e:
            print(f"Error downloading release: {e}")
    else:
        print("No download URL found in release info.")

def update_to_latest_commit():
    """Update GeoLoader to the latest commit."""
    print("Updating to the latest commit...")
    try:
        subprocess.check_call("git pull", shell=True)
        print("Successfully updated to the latest commit.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update: {e}")

def check_for_updates():
    """Check for updates from the repository's latest release."""
    repo_url = "https://api.github.com/repos/entity12208/GeoLoader/releases/latest"
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        release = response.json()

        version = release["tag_name"]
        pre_release = release.get("prerelease", False)
        release_notes = release.get("body", "No release notes.")
        download_url = release["assets"][0]["browser_download_url"]  # Assuming the first asset is the release file.

        print(f"Latest version: {version} - {'Pre-release' if pre_release else 'Stable'}")
        print(f"Release Notes: {release_notes}")
        return {
            "version": version,
            "releaseNotes": release_notes,
            "downloadUrl": download_url
        }

    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
        return {}

def main():
    """Main program entry point."""
    print("GeoLoader CLI")

    profile = input("Enter profile name (default if none): ").strip()
    if not profile:
        profile = "default"

    config = load_config(profile)
    print(f"GeoLoader version: {config['version']}")

    action = input("Enter 'create' to create a new mod template, 'build' to build an existing mod, 'update' to update GeoLoader: ").strip().lower()

    if action == 'create':
        mod_name = input("Enter the name of the new mod: ")
        create_mod_template(mod_name)
    elif action == 'build':
        mod_name = input("Enter the name of the mod to build: ")
        build_mod(mod_name)
    elif action == 'update':
        update_choice = input("Do you want to update to the latest release or the latest commit? (release/commit): ").strip().lower()
        if update_choice == "release":
            update_info = check_for_updates()
            if update_info:
                save_config(profile, {"releaseInfo": update_info})
                update_from_release()
        elif update_choice == "commit":
            update_to_latest_commit()
        else:
            print("Invalid option.")
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()

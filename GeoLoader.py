import json
import os
import subprocess
import platform

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

    with open(f"{base_path}/{mod_name}.gloader", 'w') as f:
        f.write(json.dumps({
            "modName": mod_name,
            "sourceFiles": ["src/main.cpp"],
            "outputFile": f"build/{mod_name}.dll"
        }, indent=4))

    print(f"Mod template for {mod_name} created successfully.")

def build_mod(mod_name):
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

def main():
    config = load_config()
    print(f"GeoLoader version: {config['version']}")

    action = input("Enter 'create' to create a new mod template or 'build' to build an existing mod: ").strip().lower()

    if action == 'create':
        mod_name = input("Enter the name of the new mod: ")
        create_mod_template(mod_name)
    elif action == 'build':
        mod_name = input("Enter the name of the mod to build: ")
        build_mod(mod_name)
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()

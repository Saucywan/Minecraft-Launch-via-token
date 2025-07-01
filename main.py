import minecraft_launcher_lib
import subprocess
import requests
import uuid

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

# --- USER SETTINGS ---
# -VERSION-
latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]
norm_version = "1.8.9"
all_installed_versions = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)

custom_version = []
if all_installed_versions is not None:
    if all_installed_versions:
        for idx in range(len(all_installed_versions)):
            if all_installed_versions[idx].get("complianceLevel") == 0:
                custom_version.append(all_installed_versions[idx])

# Get the user to select a version
if custom_version:
    print("Available versions:")
    for idx, version in enumerate(custom_version):
        print(f"{idx + 1}: {version['id']}")
    selected_index = int(input("Select a version by number (default is latest): ")) - 1
    if selected_index < 0 or selected_index >= len(custom_version):
        version = latest_version
    else:
        version = custom_version[selected_index]["id"]
if not custom_version:
    print("No custom versions found, using latest version.")
    version = latest_version

print("Selected version:", version)
# ---

# -Player Access Token-
access_token = input("Player's Access Token: ")  # The access token
# --- END OF SETTINGS ---


def add_dashes(uuid_hex: str) -> str:
    return str(uuid.UUID(hex=uuid_hex))


def get_profile(access_token: str):
    url = "https://api.minecraftservices.com/minecraft/profile"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        raise Exception("Minecraft profile not found. Does this account own Minecraft?")
    elif resp.status_code != 200:
        raise Exception(f"Error retrieving profile: {resp.status_code} - {resp.text}")
    return resp.json()


# Get user profile from token
profile = get_profile(access_token)
username = profile["name"]
puuid = add_dashes(profile["id"])

# Install the specified Minecraft version
minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)

# Launch options
options = {
    "username": username,
    "uuid": puuid,
    "token": access_token
}

# Build and run launch command
minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
subprocess.run(minecraft_command, cwd=minecraft_directory)

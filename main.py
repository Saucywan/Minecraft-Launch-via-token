import minecraft_launcher_lib
import subprocess
import requests
import uuid


# --- USER SETTINGS ---
# -VERSION-
# latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]
# or just use the version number
version = "1.8.9"  # The version to launch
# ---

# -Player Username-
username = "" # The player's username
# ---

# -Player Access Token-
access_token = ""  # The access token

# --- END OF SETTINGS ---



def add_dashes(uuid_hex: str) -> str:
    return str(uuid.UUID(hex=uuid_hex))

def get_uuid(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    resp = requests.get(url)
    if resp.status_code == 404:
        raise Exception(f"User '{username}' not found")
    data = resp.json()
    return data.get("id")

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)

puuid = add_dashes(get_uuid(username))
options = {
    "username": username,
    "uuid": puuid,
    "token": access_token
}

minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)

# Start Minecraft
subprocess.run(minecraft_command, cwd=minecraft_directory)


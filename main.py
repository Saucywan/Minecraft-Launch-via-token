import minecraft_launcher_lib
import subprocess

# latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]
# or just use the version number
version = "1.8.9"  # The version to launch

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)

username = "" # The player's username
uuid = "xx-xx-xx-xx"  # Get from namemc.com - with dash's
access_token = ""  # The access token

options = {
    "username": username,
    "uuid": uuid,
    "token": access_token
}

minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)

# Start Minecraft
subprocess.run(minecraft_command, cwd=minecraft_directory)


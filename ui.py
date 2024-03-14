# ui.py

# Starter code for assignment 2 in ICS 32 Programming
# with Software Libraries in Python

# Replace the following placeholders with your information.

# Nicole Utama
# nutama@uci.edu
# 20267081

from pathlib import Path
from Profile import *
import ds_client as dsc
import OpenWeather as weather
import Last_FM as fm

profile = Profile()
DSU_PORT = 3021
WEATHER_DEV_API_KEY = "37678f5231ba3e6702a5bf80a140f947"
FM_DEV_API_KEY = "c0a60fb3ace4ff1ea2748e5319a9ee72"

def c_command(directoryPath, file_name):
    """
    The function that creates the user's new DSU file.
    """
    path = Path(directoryPath)
    filepath = f"{directoryPath}" + f"\\{file_name}.dsu"
    p = Path(filepath)
    if p.exists():
        print("File already exists. Opening now.\n")
        o_command(directoryPath, file_name)
    else:
        new_user = input("Please enter a username for this file.\n")
        while " " in new_user:
            new_user = input("Username cannot have whitespace. Please try again.")
        profile.username = new_user
        psswd = input("Please enter a password for this file.\n")
        while " " in psswd:
            psswd = input("Password cannot have whitespace. Please try again.")
        profile.password = psswd
        new_bio = input("Please type a short bio for this file.\n")
        profile.bio = new_bio
        new_file = open(p, "x")
        profile.dsuserver = str(input("What server would you like to save to?\n"))
        profile.save_profile(filepath)
        print(f"{filepath} created\n")


def o_command(path, filename):
    """
    The command that opens existing DSU files.
    """
    filepath = f"{path}" + f"\\{filename}.dsu"
    p = Path(filepath)
    file = open(p, "r")
    print(f"{filepath} successfully opened.\n")


def p_command(option, path, filename):
    """
    The function that prints things from a user's opened DSU file.
    """
    filepath = f"{path}" + f"\\{filename}.dsu"
    # profile.save_profile(filepath)
    profile.load_profile(str(filepath))
    post_list = profile._posts
    if option == "-usr":
        print(profile.username)
    elif option == "-pwd":
        print(profile.password)
    elif option == "-bio":
        print(profile.bio)
    elif option == "-posts":
        if len(post_list) > 0:
            for i in range(0, len(post_list)):
                current_post = post_list[i]["entry"]
                print(f"post id {i}: {current_post}")
        else:
            print("No posts.")
    elif option == "-post":
        ids = input("What post would you like to print? Please enter integers only.\n")
        try:
            print(profile._posts[int(ids)]['entry'])
        except IndexError or ValueError:
            ids = input("Invalid. Please try again.\n")
        finally:
            confirm = input("Do you want to post this online? (y/n)\n")
            if confirm.lower() == "y":
                post_online(path, filename, profile._posts[int(ids)])
            else:
                print("Online posting cancelled.")
    elif option == "-all":
        print("Username: " + profile.username)
        print("Password: " + profile.password)
        print("Bio: " + profile.bio)
        for i in range(0, len(post_list)):
            current_post = post_list[i]["entry"]
            print(f"post id {i}: {current_post}")


def e_command(option, path, filename):
    """
    The function that lets the user edit things in their DSU file.
    """
    filepath = f"{path}" + f"/{filename}.dsu"
    p = Path(filepath)
    profile.load_profile(filepath)
    if option == "-usr":
        print("If you change the username, you must change the password too to continue posting online.")
        cont_confirmation = input("Are you sure you want to proceed? (y/n)")
        if cont_confirmation.lower() == "y":
            new_user = input("What do you want to change the username to?\n")
            while " " in new_user:
                new_user = input("Username cannot have whitespace. Please try again.\n")
            profile.username = new_user
            profile.save_profile(filepath)
            print(f"Successfully changed username to {profile.username}.\n")
        else:
            print("Username not changed.")
    elif option == "-pwd":
        print("If you change the password, you must also change the username to continue posting online.")
        cont_confirmation = input("Are you sure you want to proceed? (y/n)\n")
        if cont_confirmation.lower() == "y":
            new_pwd = input("What do you want to change the password to?\n")
            while " " in new_pwd:
                new_pwd = input("Password cannot have whitespace. Please try again.\n")
            profile.save_profile(filepath)
            profile.password = new_pwd
            profile.save_profile(filepath)
            print(f"Successfully changed password to {profile.password}.\n")
        else:
            print("Password not changed.\n")
    elif option == "-bio":
        new_bio = input("What do you want to change the bio to?\n")
        profile.bio = new_bio
        profile.save_profile(filepath)
        print(f"Successfully changed bio to {profile.bio}.\n")
    elif option == "-addpost":
        print("New options available! The dev has now added keywords.")
        print("@weather - access OpenWeather API to tell everyone the weather in your area!")
        print("Note: A valid US zip code is required for this functionality.")
        print("@lastfm - access LastFM API to show everyone your favorite tracks!")
        print("Note: A LastFM account is required for this functionality.")
        new_entry = input("Please type your new post.\n")
        new_post = Post(new_entry)
        profile.add_post(new_post)
        profile.save_profile(filepath)
        print("Would you like to post this online?\n")
        user_choice = input("(y/n)\n").lower()
        if user_choice == "y":
            post_online(path, filename, new_post)
        else:
            print("Post not shared online.\n")
        print("Post successfully added.\n")
    elif option == "-delpost":
        del_id = input("What post id do you want to get rid of?\n")
        profile.del_post(int(del_id))
        profile.save_profile(filepath)
        print("Post successfully deleted.\n")

def ui_api_bridge(message: str) -> str:
    """
    A function to help bridge the UI
    and API modules. Handles transclusion
    and passing parameters to functions.
    """
    if "@weather" in message and "@lastfm" in message:
        zipcode = input("Please input a valid US zipcode.\n")
        fm_user = input("Please input your LastFM username.\n")
        openweather = weather.OpenWeather(zipcode, "US")
        last_fm = fm.LastFM(fm_user)
        api_key_w_yn = input("Do you have an API key for OpenWeather? (y/n)\n").lower()
        if api_key_w_yn in ["y", "yes"]:
            user_w_api_key = input("Please input an API key.\n")
            openweather.set_apikey(user_w_api_key)
            openweather.load_data()
        else:
            print("That's fine. Using default API key now.\n")
            openweather.set_apikey(WEATHER_DEV_API_KEY)
            openweather.load_data()
        api_key_fm_yn = input("Do you have an API key for LastFM? (y/n)\n").lower()
        if api_key_fm_yn in ["y", "yes"]:
            user_fm_api_key = input("Please input an API key.\n")
            last_fm.set_apikey(user_fm_api_key)
            last_fm.load_data()
        else:
            print("That's fine. Using default API key now.\n")
            last_fm.set_apikey(FM_DEV_API_KEY)
            last_fm.load_data()
        transcluded_msg1 = openweather.transclude(message)
        transcluded_msg = last_fm.transclude(transcluded_msg1)

    elif "@weather" in message:
        zipcode = input("Please input a valid US zipcode.\n")
        api_key_yn = input("Do you have an API key for OpenWeather? (y/n)\n").lower()
        if api_key_yn in ["y", "yes"]:
            user_w_api_key = input("Please input an API key.\n")
            openweather = weather.OpenWeather(zipcode, "US")
            openweather.set_apikey(user_w_api_key)
            openweather.load_data()
        else:
            print("That's fine. Using default API key now.\n")
            openweather = weather.OpenWeather(zipcode, "US")
            openweather.set_apikey(WEATHER_DEV_API_KEY)
            openweather.load_data()
        transcluded_msg = openweather.transclude(message)
    elif "@lastfm" in message:
        fm_user = input("Please input your LastFM username.\n")
        api_key_yn = input("Do you have an API key for LastFM? (y/n)\n").lower()
        if api_key_yn in ["y", "yes"]:
            user_fm_api_key = input("Please input an API key.\n")
            last_fm = fm.LastFM(fm_user)
            last_fm.set_apikey(user_fm_api_key)
            last_fm.load_data()
        else:
            print("That's fine. Using default API key now.\n")
            last_fm = fm.LastFM(fm_user)
            last_fm.set_apikey(FM_DEV_API_KEY)
            last_fm.load_data()
        transcluded_msg = last_fm.transclude(message)

    return transcluded_msg

def post_online(path, filename, post: str):
    """
    The function that calls ds_client and allows
    the user to post online.
    """
    filepath = f"{path}" + f"\\{filename}.dsu"
    profile.load_profile(str(filepath))
    current_user = profile.username
    current_pwd = profile.password
    simul_post = input("Do you want to include your bio with this post? (y/n)\n").lower()
    transcluded_post = ui_api_bridge(str(post['entry']))
    if simul_post == "y":
        current_bio = profile.bio
        server = profile.dsuserver
        dsc.send(server, DSU_PORT, current_user, current_pwd, transcluded_post, current_bio)
    else:
        dsc.send(server, DSU_PORT, current_user, current_pwd, transcluded_post)

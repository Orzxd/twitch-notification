import requests
import time
import webbrowser
import random
from inputimeout import inputimeout, TimeoutOccurred

# input the streamers you want to check whether he/she is live
streamer_name_list = ['underground_dv', 'yeung_sonson']

# list for whether the webpage is opened; 0 = not opened
web_open_list = {streamer_name: 0 for streamer_name in streamer_name_list}

# twitch api call https://dev.twitch.tv/docs/api
client_id = '  '  # input your client id
client_secret = '' # input your client secret

# https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-client-credentials-flow
body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}


def get_twitch_data(streamer_name):
    try:
        headers = {
            'Client-ID': client_id,
            'Authorization': 'Bearer ' + client_secret
        }
        print('Using old token!')
        print(headers)
    except:
        print("Generating new token...")
        r = requests.post('https://id.twitch.tv/oauth2/token', body)

        # data output
        keys = r.json()

        print(keys)

        headers = {
            'Client-ID': client_id,
            'Authorization': 'Bearer ' + keys['access_token']
        }

        print(headers)

    # Example Request #1 - https://dev.twitch.tv/docs/api/reference#get-streams
    stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name,
                          headers=headers)
    stream_data = stream.json()
    # print(stream_data)
    return stream_data


def check_live(streamer_name, stream_data=None):
    is_live = False
    if len(stream_data['data']) == 1:
        print(streamer_name + ' is live: ' + stream_data['data'][0]['title'] + ' playing ' +
              stream_data['data'][0][
                  'game_name'])
        print("")
        print("")
        is_live = True
        # webpage is only opened 1 time.
        if web_open_list[streamer_name] == 0:
            webbrowser.open(f'https://www.twitch.tv/{streamer_name}', new=2, autoraise=True)
            web_open_list[streamer_name] += 1

    if len(stream_data['data']) == 0:
        print(streamer_name + ' is not live')
        print("")
        print("")

    return is_live


def run_checking():
    while True:
        i = False
        for streamer_name in streamer_name_list:
            print(f"...  checking {streamer_name}   ...")
            twitch_data = get_twitch_data(streamer_name)
            live_check = check_live(streamer_name, twitch_data)

            if live_check:
                i = True

        if i:
            try:
                exit_input = inputimeout('Do you want to continue? Y/N    input = ', timeout=10)
                if exit_input == 'N' or exit_input == 'n':
                    break
            except TimeoutOccurred:
                print("...  time out , continuing  ...")
                pass

        ran_time = random.randint(1, 5)
        change_to_sec = ran_time * 60
        print(f'Please wait for {ran_time} min')
        time.sleep(change_to_sec)


run_checking()

import requests
import argparse
from habitica import HabiticaAPI

BASE_URL = "https://habitica.com/api/v3"

def get_auth():
    client_key = "93c29c04-03b3-416f-bc6f-0edbfd806238-HabiticaCLI"
    auth_cfg = 'auth.cfg'

    with open(auth_cfg, 'r') as auth_file:
        user_id = auth_file.readline()
        user_id = user_id.split('=')[1].strip()

        api_key = auth_file.readline()
        api_key = api_key.split('=')[1].strip()

    auth_headers = {'x-api-user': user_id, 'x-api-key': api_key, 'x-client': client_key}
    return auth_headers

def print_daily(daily):
    task_name = daily["text"]
    streak = daily["streak"]
    if daily["completed"]:
        output = "[x] {task_name} ({streak} days in a row)".format(
            task_name=task_name, streak=streak)
    else:
        output = "[ ] {task_name} ({streak} days in a row)".format(
            task_name=task_name, streak=streak)

    print(output)

def print_habit(habit):
    print(habit["text"])
    if habit["up"]:
        print(" --{} ↑".format(habit["counterUp"]))

    if habit["down"]:
        print(" --{} ↓".format(habit["counterDown"]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A CLI for Habitica")
    subparsers = parser.add_subparsers(dest="command")
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("filter", nargs="?")

    args = parser.parse_args()
    hbt_api = HabiticaAPI(get_auth())

    if (args.command == "list"):
        if (args.filter == "dailys" or args.filter == "dailies"):
            query_params = {'type': 'dailys'}
            tasks = hbt_api.make_request("tasks/user", query_params)
            
            for t in tasks:
                print_daily(t)

        elif (args.filter == "habits"):
            query_params = {'type': 'habits'}
            tasks = hbt_api.make_request("tasks/user", query_params)

            for t in tasks:
                print_habit(t)

        else:
            tasks = hbt_api.make_request("tasks/user")

            habits = [x for x in tasks if x["type"] == "habit"]
            dailies = [x for x in tasks if x["type"] == "daily"]

            print("==DAILIES==")
            for d in dailies:
                print_daily(d)


            print("==HABITS==")
            for h in habits:
                print_habit(h)

        
    
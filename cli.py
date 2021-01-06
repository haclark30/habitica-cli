import requests
import argparse
import os
import re
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

def setup_parser():
    parser = argparse.ArgumentParser(description="A CLI for Habitica")
    subparsers = parser.add_subparsers(dest="command")

    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("filter", nargs="?", choices=["habits", "dailys", "dailies"])

    parser_up = subparsers.add_parser("up")
    parser_up.add_argument("task")
    parser_up.add_argument("-n", "--num", type=int, default=1)

    subparsers.add_parser("status")
    return parser


def run_command(parser, hbt_api):
    args = parser.parse_args()

    if (args.command == "list"):
        run_list_command(args, hbt_api)
    elif (args.command == "status"):
        run_status_command(hbt_api)
    elif (args.command == "up"):
        run_up_command(args, hbt_api)


def run_status_command(hbt_api):
    user = hbt_api.make_request("user")
    profile = user['profile']
    stats = user['stats']

    print(profile['name'])
    print('-' * 20)
    print("Level {} {}".format(stats['lvl'], stats['class'].capitalize()))
    print('-' * 20)

    print("HP: {}/{}".format(stats['hp'], stats['maxHealth']))
    print("XP: {}/{}".format(stats['exp'], stats['toNextLevel']))
    print("MP: {}/{}".format(stats['mp'], stats['maxMP']))

def run_list_command(args, hbt_api):
    if (args.filter == "dailys" or args.filter == "dailies"):
        query_params = {'type': 'dailys'}
        tasks = hbt_api.make_request("tasks/user", params=query_params)

        for t in tasks:
            print_daily(t)

    elif (args.filter == "habits"):
        query_params = {'type': 'habits'}
        tasks = hbt_api.make_request("tasks/user", params=query_params)

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

def run_up_command(args, hbt_api):
    tasks = hbt_api.make_request("tasks/user")
    matching_tasks = find_matching_tasks(args, tasks)
            
    if len(matching_tasks) == 0:
        print('no tasks matching "{}" found'.format(args.task))
    elif len(matching_tasks) == 1:
        task = matching_tasks[0]
        for _ in range(args.num):
            score_task(hbt_api, task, 'up')
        print("scored {} up {} time(s)".format(task['text'], args.num))
    else:
        print('found multiple matching tasks')

def find_matching_tasks(args, tasks):
    matching_tasks = []
    search_string = "^{}.*".format(args.task)

    for t in tasks:
        if re.search(search_string, t['text'], re.IGNORECASE):
            matching_tasks.append(t)
    return matching_tasks


def score_task(hbt_api, task, direction):
    uri = "tasks/{}/score/{}".format(task['id'], direction)
    return hbt_api.make_request(uri, method='post')

def main():
    # setup parser and Habitica API
    parser = setup_parser()
    hbt_api = HabiticaAPI(get_auth())

    # run the command
    run_command(parser, hbt_api)

if __name__ == "__main__":
    main()

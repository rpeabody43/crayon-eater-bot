from datetime import datetime, time
import pytz
import re
from os.path import isfile, join, dirname
import json

dir = dirname(__file__)

class SetEncoder (json.JSONEncoder):
    def default (self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

# old hall list can't be trusted while school's not in session
def during_school_day () -> bool:
    tz = pytz.timezone('America/New_York')
    now = datetime.now(tz)
    if now.weekday() >= 5: return False
    time_rn = now.time()
    return time(9, 0, 0, 0, tz) < time_rn  < time(15, 0, 0, 0, tz)


def write (to_increment: set[str], leaderboard: dict):

    if not during_school_day(): return

    today = datetime.now(pytz.timezone('America/New_York')).strftime('%d-%m-%Y')
    
    daily_post_path = join(dir, 'gdocs', 'dailypost.txt')
    # if the date at the top of the post is not today, don't run
    # kinda janky but it works
    with open (daily_post_path, 'r') as f:
        daily_post = f.read()
        rgx = '([0-1]?[0-2])\/([0-3]?[0-9])\/202.'
        dp_date_search = re.search(rgx, daily_post)
        if dp_date_search is not None:
            dp_date_str = dp_date_search.group()
            print(dp_date_str)

            first_slash = dp_date_str.index('/')
            second_slash = dp_date_str[first_slash+1:].index('/') + first_slash+1
            dp_date = datetime(
                year=int(dp_date_str[second_slash+1:]),
                month=int(dp_date_str[:first_slash]),
                day=int(dp_date_str[first_slash+1:second_slash])
                )

            if dp_date.strftime('%d-%m-%Y') != today:
                print('Post not updated today')
                return

    tmp_filepath = join(dir, 'tmp', f'{today}.json')
    cached_leaderboard_path = join(dir, 'tmp', 'leaderboard.json')
    
    # essentially checking whether we've already updated today
    if isfile(tmp_filepath): 
        with open (cached_leaderboard_path, 'r') as f:
            leaderboard = json.loads(f.read())
        with open (tmp_filepath, 'r') as f:
            to_increment = to_increment.union(
                set(
                    json.loads(f.read())
                    )
                )
    # we know it's the first time today updating the leaderboard
    # so set the 'cache' to be used later so values are only incremented once per day 
    else: 
        with open(cached_leaderboard_path, 'w') as f:
            f.write(json.dumps(leaderboard, indent=4))
    # we want to update which teachers are out today no matter what
    print(len(to_increment))
    with open (tmp_filepath, 'w') as f:
        f.write(json.dumps(to_increment, cls=SetEncoder))

    for teacher in to_increment:
        leaderboard[teacher] += 1
    
    with open (join(dir, 'leaderboard.json'), 'w') as f:
        f.write(json.dumps(leaderboard, indent=4))
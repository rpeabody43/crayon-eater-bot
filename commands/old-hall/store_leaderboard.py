from datetime import datetime, time
import pytz
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
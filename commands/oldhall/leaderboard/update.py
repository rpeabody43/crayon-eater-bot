import json
from os.path import join, dirname

from .store_leaderboard import write
from .gdocs import get_teachers

dir = dirname(__file__)
leaderboard_path = join(dir, 'leaderboard.json')

def which_teacher (lastname: str, entry: str) -> str | None:
    entry = entry.upper()
    lastname = lastname.upper()
    match lastname:
        case "COLEMAN":
            # both colemans teach math
            if 'KATELYN' in entry or 'MS' in entry:
                return "Coleman, Katelyn"
            if 'MATT' in entry or 'MR' in entry:
                return "Coleman, Matt"
        case "TORO":
            if 'KEVIN' in entry or 'MR' in entry or 'HISTORY' in entry or 'SOC STUDIES' in entry:
                return 'Toro, Kevin'
            if 'CHRISTINA' in entry or 'MS' in entry or 'SPANISH' in entry:
                return 'Toro, Christina'
        case "LEE":
            if 'ALLISON' in entry or 'ENGLISH' in entry:
                return 'Lee, Allison'
            if 'ALYSSA' in entry or 'SPANISH' in entry:
                return 'Lee, Alyssa'
        case _:
            return None


def fmt () -> dict:
    leaderboard: dict
    with open(leaderboard_path, 'r') as f:
        leaderboard = json.loads(f.read())


    leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)}
    leaderboard_values = list(leaderboard.values())
    ret = {}
    i = 0
    while i < len(leaderboard.keys()) and leaderboard_values[i] > 0:
        teacher = list(leaderboard.keys())[i]
        ret[teacher] = leaderboard[teacher]
        i += 1
    
    return ret

def update():
    old_hall_entries = get_teachers()
    leaderboard: dict = {}
    try:
        with open (leaderboard_path, 'r') as f:
            leaderboard = json.loads(f.read())
    except FileNotFoundError:
        with open (join(dir, 'blank_leaderboard.json'), 'r') as f:
            leaderboard = json.loads(f.read())
        with open (leaderboard_path, 'w') as f:
            f.write(json.dumps(leaderboard, indent=4))
        print ('Leaderboard does not exist, replaced with blank template')
    names = leaderboard.keys()
    
    to_increment = set()

    for entry in old_hall_entries:
        entry = entry.upper().replace('\u2019', '')
        for name in names:
            lastname = name[:name.index(',')].upper().replace('\u2019', '')
            # print(lastname)
            if lastname in entry:
                if lastname in ['COLEMAN', 'TORO', 'LEE']:
                    specific_teacher = which_teacher(lastname, entry)
                    if specific_teacher != None: to_increment.add(specific_teacher)
                else:
                    to_increment.add(name)
    
    print(to_increment)
    print(f'{len(to_increment)} out today')
    write(to_increment, leaderboard)


if __name__  == '__main__':
    update()
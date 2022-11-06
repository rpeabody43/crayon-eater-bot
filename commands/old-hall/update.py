import json
from os.path import join, dirname

from bot_command.store_leaderboard import write
from gdocs import get_teachers

dir = dirname(__file__)

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


def main():
    old_hall_entries = get_teachers()
    leaderboard: dict = {}
    with open (join(dir, 'leaderboard.json'), 'r') as f:
        leaderboard = json.loads(f.read())
    names = leaderboard.keys()
    
    to_increment = set()

    for entry in old_hall_entries:
        entry = entry.upper()
        for name in names:
            lastname = name[:name.index(',')].upper()
            # print(lastname)
            if lastname in entry:
                if lastname in ['COLEMAN', 'TORO', 'LEE']:
                    specific_teacher = which_teacher(lastname, entry)
                    if specific_teacher != None: to_increment.add(specific_teacher)
                else:
                    to_increment.add(name)
    
    print(to_increment)
    print(len(to_increment))
    write(to_increment, leaderboard)


if __name__  == '__main__':
    main()
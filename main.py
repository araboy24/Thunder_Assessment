import math


def get_shot_zone(x, y):
    dist = math.dist([x, y], [0, 0])
    if dist < 22:
        return '2PT'
    elif y <= 7.8 and abs(x) >= 22:
        return 'C3'
    elif dist >= 23.75:
        return 'NC3'
    else:
        return '2PT'


def get_distribution(team):
    counts = {}
    for d in team:
        if d[0] in counts.keys():
            counts[d[0]] += 1
        else:
            counts[d[0]] = 1
    for k, v in counts.items():
        counts[k] = round(v / len(team) * 100, 3)
    return counts


def get_efg(team, zone):
    total_shots = 0
    total_made = 0
    total_threes_made = 0
    for d in team:
        if d[0] != zone:
            continue
        total_shots += 1
        if d[1]:
            total_made += 1
            if zone in ['NC3', 'C3']:
                total_threes_made += 1
    return round((total_made + 0.5 * total_threes_made) / total_shots * 100, 3)


def get_results(team_a, team_b):
    print("Results")
    print("Team A Distribution:")
    for k, v in get_distribution(team_a).items():
        print(f'\t{k}: {v}%')
    print("\nTeam B Distribution:")
    for k, v in get_distribution(team_b).items():
        print(f'\t{k}: {v}%')

    print("\nTeam A eFG%:")
    print(f"\t2PT: {get_efg(team_a, '2PT')}%")
    print(f"\tNC3: {get_efg(team_a, 'NC3')}%")
    print(f"\tC3: {get_efg(team_a, 'C3')}%")

    print("\nTeam B eFG%:")
    print(f"\t2PT: {get_efg(team_b, '2PT')}%")
    print(f"\tNC3: {get_efg(team_b, 'NC3')}%")
    print(f"\tC3: {get_efg(team_b, 'C3')}%")


team_a = []
team_b = []

with open('shots_data.csv', 'r') as f:
    f.readline()  # Skip header
    for line in f:
        line_spl = line.split(',')
        team = 'A' if line_spl[0] == 'Team A' else 'B'
        x = float(line_spl[1].strip())
        y = float(line_spl[2].strip())
        is_made = line_spl[3].strip() == '1'
        shot_zone = get_shot_zone(x, y)
        if team == 'A':
            team_a.append([shot_zone, is_made])
        else:
            team_b.append([shot_zone, is_made])

    get_results(team_a, team_b)

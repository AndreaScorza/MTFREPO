
def importTasks(filepath : str, id : int):
    researcher_starting_point = (int(id / 100) % 3) * 3
    cluster = (int((id + 1)/2) + researcher_starting_point) % 10
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    headers_locations = {int(lines[i].split()[1]): i for i in range(len(lines)) if lines[i].startswith('id:')}
    starting_line = headers_locations[cluster] + 1
    return [line.split(maxsplit=2)[2] for line in  lines[starting_line : starting_line + 5]]

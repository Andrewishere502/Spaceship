def get_lines():
    with open("/Users/21berntson_a/Documents/Programming/Python/Spaceship/settings.txt", "r") as file:
        lines = file.readlines()
    return lines


def remove_meaningless_lines(lines):
    """Remove lines that are comments or are
    just a return character. Modifies lines.
    """
    i = 0
    while True:
        line = lines[i]

        if (line[0] == "#"
            or line == "\n"):

            lines.pop(i)

        else:

            # removes inline comments
            if "#" in line:
                comment_starts = line.index("#")
                lines[i] = line[:comment_starts]
            
            # removes \n characters
            if line[-1] == "\n":
                line = line[:-1]
                line = line.strip()
                lines[i] = line

            i += 1
        
        if i == len(lines):
            break
    return


def parse_prefs(lines):
    """Return a dict with the settings specified in settings."""
    settings = {}
    for line in lines:
        setting, pref = line.split(" = ")

        # check if pref is a bool
        if pref.lower() == "true":
            pref = True
        elif pref.lower() == "false":
            pref = False
        elif pref[0] == "'" and pref[-1] == "'":
            pref = str(pref)[1:-1]  # get rid of the ' '
        else:  # pref is an int or float
            try:
                if "." in pref:
                    pref = float(pref)
                else:
                    pref = int(pref)
            except ValueError:
                raise ValueError("{} is not a valid float or int.".format(pref))

        # add preference to settings
        settings.update({setting: pref})
    return settings


def get_settings():
    lines = get_lines()
    remove_meaningless_lines(lines)
    settings = parse_prefs(lines)
    return settings


def get_path():
    lines = get_lines()
    remove_meaningless_lines(lines)
    path = lines[0].split(" = ")[1]
    path = path[1:-1]  # remove ''
    return path


if __name__ == "__main__":
    settings = get_settings()
    print(settings)
    path = get_path()
    print(path)

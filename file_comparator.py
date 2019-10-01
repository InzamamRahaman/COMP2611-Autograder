
def create_file_representation(path):
    representation = []
    with open(path, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                line = line.lower()
                contents = line.split()
                representation.append(contents)
    return representation


def comprator(path1, path2):
    r1 = create_file_representation(path1)
    r2 = create_file_representation(path2)
    return r1 == r2

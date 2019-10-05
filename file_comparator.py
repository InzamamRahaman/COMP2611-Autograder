
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
    print(r1)
    print('-----------')
    print(r2)
    count = 0
    for x, y in zip(r1, r2):
        if x == y:
            count += 1
    score = float(count) / len(r2)
    return score

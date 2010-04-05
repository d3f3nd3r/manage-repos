import re

REPO_FILE_PATH='/home/d3f3nd3r/projects/python/manage-repos/repos'

def parse_repo_file(path):
    r_args = re.compile('(?P<arg>\w*)=\'(?P<value>[\w\-/@.:]*\')')

    repo_file = open(path, 'r')

    arg_values = []
    for line in repo_file.readlines():
        arg_value = r_args.search(line)
        if arg_value is not None:
            arg_values.append(arg_value.groupdict())

    print(arg_values)


def main():
    parse_repo_file(REPO_FILE_PATH)


if __name__ == '__main__':
    main()

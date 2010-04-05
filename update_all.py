import re, os
from mercurial import hg, ui, commands


REPO_FILE_PATH='/home/d3f3nd3r/projects/python/manage-repos/repos'

def parse_repo_file(path):
    r_args = re.compile('(?P<arg>\w*)=\'(?P<value>[\w\-/@.:]*\')')
    r_begin_of_entry = re.compile('^[\-]*$')
        
    repo_file = open(path, 'r')

    arg_values = []
    
    for line in repo_file.readlines():

        if r_begin_of_entry.search(line) is not None:
            arg_values.append(dict())
        else:
            arg_value = r_args.search(line)
            if arg_value is not None:
                arg_dict = arg_value.groupdict()
                arg_values[-1].setdefault(arg_dict['arg'], arg_dict['value'])
                
    return arg_values


class MecurialRepo():
    def __init__(self, name, path, url, username):
        r_url = re.compile('default = (?P<url>[\w\-/@.:]*)')
        self.name = name
        self.path = path

        hgrc_file = open(os.path.join(self.path, '.hg', 'hgrc'))
        for line in hgrc_file.readlines():
            url = r_url.search(line)
            if url is not None:
                self.url = url.groupdict()['url']
        
        if self.url is None:
            raise ValueError("MecurialRepo "+self.name+" no repo url found")

        self.username = username

    def update(self):
        pass

    
def main():
    parse_repo_file(REPO_FILE_PATH)


if __name__ == '__main__':
    main()

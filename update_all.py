import re, os
from mercurial import hg, ui, commands


REPO_FILE_PATH='/home/d3f3nd3r/.updateallrepos'

def parse_repo_file(path):
    r_args = re.compile('(?P<arg>\w*)=\'(?P<value>[\w\-/@.:]*)\'')
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

def init_repos(repo_configs):
    repos = []


    for repo_config in repo_configs:

        try:
            repo_type = repo_config.pop('type')
            if repo_type == 'mecurial':
                repos.append(MecurialRepo(**repo_config))
                print('Added new Mercurial Repo')

            if repo_type == 'svn':
                repos.append(SVNRepo(**repo_config))
                print('Added new SVN Repo')
        except KeyError:
            print('KeyError')
            
    return repos

class BaseRepo(object):
    def __init__(self, name, path, username=None):
        self.name = name
        self.path = path
        self.username = username

    def update(self):
        pass

import pysvn
class SVNRepo(BaseRepo):
    def __init__(self, name, path, username=None):
        super(SVNRepo , self).__init__(name, path, username)
        self.client = pysvn.Client()

    def update(self):
        self.client.update(self.path)
        

class MecurialRepo(BaseRepo):
    def __init__(self, name, path, username=None):
        super(MecurialRepo , self).__init__(name, path, username)
        self.type = 'mercurial'

        r_url = re.compile('default = (?P<url>[\w\-/@.:]*)')

        hgrc_file = open(os.path.join(self.path, '.hg', 'hgrc'))

        for line in hgrc_file.readlines():
            url = r_url.search(line)
            if url is not None:
                self.url = url.groupdict()['url']
        
        if self.url is None:
            raise ValueError("MecurialRepo "+self.name+" no repo url found")

        self.ui = ui.ui()
        self.repo = hg.repository(self.ui, self.path)

    def update(self):
        commands.pull(self.ui, self.repo, self.url)
        commands.update(self.ui, self.repo)

    def __str__(self):
        return '%s: %s' %(self.type, self.name)

    
def main():
    repo_configs = parse_repo_file(REPO_FILE_PATH)
    
    repos = init_repos(repo_configs)

    for repo in repos:
        print("Updating "+repo.name)
        repo.update()

        
if __name__ == '__main__':
    main()

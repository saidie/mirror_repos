
import os

from mirror_repos import host

class Target:
    def __init__(self, options):
        self.host = options['host']
        self.dest = options['dest']
        self.source = options['source']

    def run(self):
        h = host.HostManager().get_host(self.host)
        reposs = h.repositories(self.source)
        for repos in reposs:
            repo_dir = os.path.join(self.dest, repos['full_name'])
            if not os.path.isdir(repo_dir):
                os.makedirs(repo_dir)
                os.system("cd '%s' && git init --bare" % repo_dir)
                os.system("cd '%s' && git remote add upstream '%s'" % (repo_dir, repos['ssh_url']))
            os.system("cd '%s' && git fetch -p upstream" % repo_dir)


import os
import urllib.parse
import urllib.request
import configparser
import json
import re

class Base:
    def __init__(self, options):
        password_mgr = urllib.request.HTTPPasswordMgrWithPriorAuth()
        password_mgr.add_password(
            None, self.top_level_url(),
            options['username'], options['password'], True
        )
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        self.opener = urllib.request.build_opener(handler)

    def do_request(self, url, params=None):
        return self.opener.open(url, params)

class Github(Base):
    def __init__(self, options):
        Base.__init__(self, options)

    def top_level_url(self):
        return 'https://api.github.com'

    def repositories(self, source):
        url = os.path.join('https://api.github.com/users/%s/repos' % source)
        response = self.do_request(url)
        headers = dict(response.getheaders())
        repos = json.loads(str(response.read(), 'utf-8'))
        while 'Link' in headers:
            links = re.findall(r'<([^>]*)>; rel="([^"]*)"', headers['Link'])
            links = dict([(l[1], l[0]) for l in links])
            if 'next' not in links:
                break
            response = self.do_request(links['next'])
            headers = dict(response.getheaders())
            repos += json.loads(str(response.read(), 'utf-8'))
        return [self.make_repo(repo) for repo in repos if not repo['fork']]

    def make_repo(self, repo):
        return { 'full_name': repo['full_name'], 'ssh_url': repo['ssh_url'] }

class Bitbucket(Base):
    def __init__(self, options):
        Base.__init__(self, options)

    def top_level_url(self):
        return 'https://api.bitbucket.org'

    def repositories(self, source):
        url = os.path.join('https://api.bitbucket.org/2.0/repositories', source)
        response = json.loads(str(self.do_request(url).read(), 'utf-8'))
        repos = response['values']
        while 'next' in response:
            response = json.loads(str(self.do_request(response['next']).read(), 'utf-8'))
            repos += response['values']
        return [self.make_repo(repo) for repo in repos if 'parent' not in repo]

    def make_repo(self, repo):
        ssh_url = [link['href'] for link in repo['links']['clone'] if link['name'] == 'ssh'][0]
        return { 'full_name': repo['full_name'], 'ssh_url': ssh_url }

class HostManager:
    instance = None
    def __new__(cls):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

        self.hosts = {}
        for section in config.sections():
            options = dict(config.items(section))
            self.hosts[section] = produce(section, options)

    def get_host(self, hostname):
        return self.hosts[hostname]

def produce(host, args):
    if host == "github.com":
        return Github(args)
    elif host == "bitbucket.org":
        return Bitbucket(args)
    return None

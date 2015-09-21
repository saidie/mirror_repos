# mirror_repos

A script to mirror git repositories on github.com/bitbucket.org to local.
It can mirror private repositories which are accessible with your credentials.

## Requirements

- Python 3.5 or upper
- `git` executable

## Configuration

For now, your credentials are required to access github.com/bitbucket.org via GitHub/Bitbucket RESTful APIs.
Put the credentials to `config/host.cfg`.

Target repositroeis to be mirrored should be described in `config/target.cfg`.
A section describes a source, in which indicates a specific user or orgarniation (team), of repositories and their backup destination.

```config
[my_github_repos]
Host = github.com
Dest = /path/to/backup
Source = saidie # username or organization name

[my_bitbucket_repos]
Host = bitbucket.org
Dest = /path/to/backup
Source = saidie # username or team name
```

In above example, repositories of user `saidie` are backed-up to `/path/to/backup/github.com/saidie/{repository_name}` and `/path/to/backup/bitbucket.org/saidie/{repository_name}`.

## Execution

Run `bin/mirror_repos.py`.

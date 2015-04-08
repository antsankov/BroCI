import git, os, shutil

# See http://www.masnun.com/2012/01/22/fetching-remote-git-repo-with-python-in-a-few-lines-of-codes.html
def setup_repo(REMOTE_URL):
    DIR_NAME = 'REPO'
    #this is for a pull
    if os.path.isdir(DIR_NAME):
        repo = git.Repo(DIR_NAME)
        origin = repo.remotes.origin
        origin.pull(origin.refs[0].remote_head)

    #this is if we need to remake the directory
    else:
        os.mkdir(DIR_NAME)
        repo = git.Repo.init(DIR_NAME)
        origin = repo.create_remote('origin',REMOTE_URL)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

    local = DIR_NAME + '/local.bro'
    repo_scripts = DIR_NAME + '/scripts/ '

    #copy the local file from the pulled repo to the local on the system
    shutil.copy(local,'/usr/local/bro/share/bro/site')
    #move the scripts to the proper direcotry as well
    #use instead of shutil, because copytree sucks.
    os.system("cp "+ repo_scripts + '/usr/local/bro/share/bro/policy/scripts')


def update_repo(REMOTE_URL):
    repo = git.Repo.init(REMOTE_URL)
    o = repo.remotes.origin
    o.pull()

"""Scheduled collection is allowed to publish only news data and rendered desks."""
import subprocess
import re

ALLOWED = {'data/news.json', 'docs/data/news.json', 'docs/index.html',
           'docs/ko/index.html', 'docs/updates/index.html', 'docs/ko/updates/index.html',
           'docs/tools/dps/index.html', 'docs/ko/tools/dps/index.html',
           'docs/search-index.json', 'docs/sitemap.xml'}

def allowed_path(path):
    return path in ALLOWED or bool(re.fullmatch(r'docs/(?:ko/)?updates/(?:na|kr)-[a-zA-Z0-9_-]{1,64}/index\.html',path))

def check():
    changed = set(subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], text=True).splitlines())
    changed.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],text=True).splitlines())
    unexpected = {path for path in changed if not allowed_path(path)}
    if unexpected:
        raise SystemExit('Unexpected generated changes; aborting automated publication: '+', '.join(sorted(unexpected)))
    print('News-only publication check passed.')

if __name__=='__main__':check()

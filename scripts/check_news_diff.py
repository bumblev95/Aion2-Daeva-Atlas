"""Scheduled collection is allowed to publish only news data and rendered desks."""
import subprocess

ALLOWED = {'data/news.json', 'docs/data/news.json', 'docs/index.html',
           'docs/ko/index.html', 'docs/updates/index.html', 'docs/ko/updates/index.html'}
changed = set(subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines())
unexpected = changed - ALLOWED
if unexpected:
    raise SystemExit('Unexpected generated changes; aborting automated publication: '+', '.join(sorted(unexpected)))
print('News-only publication check passed.')

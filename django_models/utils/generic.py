import codecs
import fnmatch
import os
import re
from unipath import Path


def find_path(pattern, path, last_folder_only=False, ignored_dirs=''):
    ignored_dirs = ignored_dirs.split(',')
    result = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))

    if not result:
        return ''

    final_path = Path(result[0]).ancestor(1)
    relative_path = final_path.replace(str(path), '')

    if last_folder_only:
        return relative_path.split('/')[-1]
    return relative_path[1:] if relative_path.startswith('/') else relative_path


def get_version_from_changes(project_root=''):
    default_version = '0.0.0'
    current_version = ''
    changes = os.path.join(project_root, "CHANGES.rst")
    pattern = r'^(?P<version>[0-9]+.[0-9]+(.[0-9]+)?)'
    if not os.path.exists(changes):
        return default_version

    with codecs.open(changes, encoding='utf-8') as changes:
        for line in changes:
            match = re.match(pattern, line)
            if match:
                current_version = match.group("version")
                break
    return current_version or default_version

from pathlib import Path
import invoke.context
from invoke import task


@task
def release(c: invoke.context.Context, version: str, main_branch: str = "main", dev_branch: str = "dev"):
    """"""
    if version not in ["minor", "major", "patch"]:
        print("Version can be either major, minor or patch.")
        return

    import tomllib
    data = tomllib.loads(Path("pyproject.toml").read_text())
    old_version = data.get("project", {}).get("version")
    _major, _minor, _patch = [int(part) for part in old_version.split(".")]

    if version == "patch":
        _patch = _patch + 1
    elif version == "minor":
        _minor = _minor + 1
        _patch = 0
    elif version == "major":
        _major = _major + 1
        _minor = 0
        _patch = 0

    c.run(f"git checkout {dev_branch}") # Just to fail early in case the dev branch does not exist
    c.run(f"git checkout -b release-{_major}.{_minor}.{_patch} {dev_branch}")
    c.run(f"sed -i 's/\"{old_version}\"/\"{_major}.{_minor}.{_patch}\"/g' pyproject.toml")
    c.run(f"sed -i 's/\"{old_version}\"/\"{_major}.{_minor}.{_patch}\"/g' docs/conf.py")
    print(f"Update the readme for version {_major}.{_minor}.{_patch}.")
    print(f"Run 'uv lock --upgrade'.")
    input("Press enter when ready.")
    c.run(f"git add -u")
    c.run(f'git commit -m "Update changelog version {_major}.{_minor}.{_patch}"')
    c.run(f"git push --set-upstream origin release-{_major}.{_minor}.{_patch}")
    c.run(f"git checkout {main_branch}")
    c.run(f"git pull")
    c.run(f"git merge --no-ff release-{_major}.{_minor}.{_patch}")
    c.run(f'git tag -a {_major}.{_minor}.{_patch} -m "Release {_major}.{_minor}.{_patch}"')
    c.run(f"git push")
    c.run(f"git checkout {dev_branch}")
    c.run(f"git merge --no-ff release-{_major}.{_minor}.{_patch}")
    c.run(f"git push")
    c.run(f"git branch -d release-{_major}.{_minor}.{_patch}")
    c.run(f"git push origin --tags")

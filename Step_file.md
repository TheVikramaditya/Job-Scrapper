How to create tags

    git tag -a v1.0 -m "Version 1.0 Release"

    git push origin v1.0

    git tag

    git checkout tag_name

    git checkout v1.0

How to push pull

    git branch -m main master
    git fetch origin
    git branch -u origin/master master
    git remote set-head origin -a
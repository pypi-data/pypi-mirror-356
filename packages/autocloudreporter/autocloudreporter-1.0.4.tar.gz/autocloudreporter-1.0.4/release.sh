#!/bin/bash

baddeps=""
# check deps
python3 -m build.__init__ || baddeps="python3-build"
if [ -n "${baddeps}" ]; then
    echo "${baddeps} must be installed!"
    exit 1
fi

if [ "$#" != "1" ]; then
    echo "Must pass release version!"
    exit 1
fi

version=$1
name=autocloudreporter
sed -i -e "s,version=\".*\",version=\"${version}\", g" setup.py
sed -i -e "s,__version__ = \".*\",__version__ = \"${version}\", g" ${name}.py
git add setup.py ${name}.py
git commit -s -m "Release ${version}"
git push
git tag -a -m "Release ${version}" ${version}
git push origin ${version}
python3 -m build .
twine upload -r pypi dist/${name}-${version}*

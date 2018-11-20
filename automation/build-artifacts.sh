#!/bin/bash -xe
[[ -d exported-artifacts ]] \
|| mkdir -p exported-artifacts

[[ -d tmp.repos ]] \
|| mkdir -p tmp.repos


autoreconf -ivf
./configure
make dist

if [ -e /etc/fedora-release ]; then
	dnf builddep --spec ovirt-iso-uploader.spec
else
	yum-builddep ovirt-iso-uploader.spec
fi

rpmbuild \
    -D "_topdir $PWD/tmp.repos" \
    -ta ovirt-iso-uploader-*.tar.gz

mv *.tar.gz exported-artifacts
find \
    "$PWD/tmp.repos" \
    -iname \*.rpm \
    -exec mv {} exported-artifacts/ \;

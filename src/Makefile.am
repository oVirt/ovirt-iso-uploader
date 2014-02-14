#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

include $(top_srcdir)/build/python.inc

MAINTAINERCLEANFILES = \
	$(srcdir)/Makefile.in \
	$(NULL)

EXTRA_DIST = \
	config.py.in \
	isodomain.xml \
	$(NULL)

CLEANFILES = \
	config.py \
	$(NULL)

SUBDIRS = \
	logrotate.d \
	$(NULL)

dist_ovirtisouploaderlib_PYTHON = \
	__init__.py \
	__main__.py \
	$(NULL)

nodist_ovirtisouploaderlib_PYTHON = \
	config.py \
	$(NULL)

dist_man_MANS = \
	ovirt-iso-uploader.8 \
	engine-iso-uploader.8 \
	$(NULL)

dist_engineconfig_DATA = \
	isouploader.conf \
	$(NULL)

confddir=$(engineconfigdir)/isouploader.conf.d

config.py: config.py.in
	$(SED) \
	-e 's|@localstatedir[@]|$(localstatedir)|g' \
	-e 's|@PACKAGE_NAME[@]|$(PACKAGE_NAME)|g' < $< > $@

all-local: \
	python-syntax-check \
	$(NULL)

clean-local: \
	python-clean \
	$(NULL)

install-data-hook:
	$(MKDIR_P) "$(DESTDIR)$(confddir)"
	$(MKDIR_P) "$(DESTDIR)$(bindir)"
	$(MKDIR_P) "$(DESTDIR)$(localstatedir)/log/ovirt-engine/$(PACKAGE_NAME)"
	chmod a+x "$(DESTDIR)$(ovirtisouploaderlibdir)/__main__.py"
	chmod 640 "$(DESTDIR)$(engineconfigdir)/isouploader.conf"
	rm -f "$(DESTDIR)$(bindir)/ovirt-iso-uploader"
	rm -f "$(DESTDIR)$(bindir)/engine-iso-uploader"
	$(LN_S) "$(ovirtisouploaderlibdir)/__main__.py" "$(DESTDIR)$(bindir)/ovirt-iso-uploader"
	$(LN_S) ovirt-iso-uploader "$(DESTDIR)$(bindir)/engine-iso-uploader"

uninstall-hook:
	rm -f "$(DESTDIR)$(bindir)/ovirt-iso-uploader"
	rm -f "$(DESTDIR)$(bindir)/engine-iso-uploader"

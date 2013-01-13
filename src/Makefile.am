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
	$(srcdir)/Makefile.in

EXTRA_DIST = isodomain.xml

dist_ovirtisouploaderlib_PYTHON = \
	__init__.py \
	__main__.py

dist_man_MANS = \
	engine-iso-uploader.8

dist_engineconfig_DATA = \
	isouploader.conf

all-local: \
	python-syntax-check

clean-local: \
	python-clean

install-data-hook:
	$(MKDIR_P) "$(DESTDIR)$(bindir)"
	chmod a+x "$(DESTDIR)$(ovirtisouploaderlibdir)/__main__.py"
	rm -f "$(DESTDIR)$(bindir)/engine-iso-uploader"
	$(LN_S) "$(ovirtisouploaderlibdir)/__main__.py" "$(DESTDIR)$(bindir)/engine-iso-uploader"

uninstall-hook:
	rm -f "$(DESTDIR)$(bindir)/engine-iso-uploader"
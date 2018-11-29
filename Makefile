VERSION=1.5
RELEASE=3

TOPDIR  =$(shell rpm --eval '%{_topdir}')
SRCDIR  =$(shell rpm --define '_topdir $(TOPDIR)' --eval '%{_sourcedir}')
SPECDIR =$(shell rpm --define '_topdir $(TOPDIR)' --eval '%{_specdir}')
RPMDIR  =$(shell rpm --define '_topdir $(TOPDIR)' --eval '%{_rpmdir}')
ARCH    =$(shell uname -m)

BUNDLE  =$(VERSION)-$(RELEASE)_release.tar.gz
DKMSRPM =mhvtl-dkms-$(VERSION)-$(RELEASE).noarch.rpm
RPM     =mhvtl-$(VERSION)-$(RELEASE).$(ARCH).rpm

.PHONY: all
all: $(RPM) $(DKMSRPM)

%.rpm: $(RPMDIR)/noarch/%.rpm
	cp $(<) $(@)

%.rpm: $(RPMDIR)/$(ARCH)/%.rpm
	cp $(<) $(@)

$(RPMDIR)/noarch/$(DKMSRPM): $(SPECDIR)/mhvtl-dkms.spec $(SRCDIR)/$(BUNDLE)
	rpmbuild -bb \
		--define '_topdir $(TOPDIR)' \
		--define '_srcdir $(SRCDIR)' \
		--define '_specdir $(SPECDIR)' \
		--define 'version $(VERSION)' \
		--define 'release $(RELEASE)' \
		$(<)

$(RPMDIR)/$(ARCH)/$(RPM): $(SPECDIR)/mhvtl.spec $(SRCDIR)/$(BUNDLE)
	rpmbuild -bb \
		--define '_topdir $(TOPDIR)' \
		--define '_srcdir $(SRCDIR)' \
		--define '_specdir $(SPECDIR)' \
		--define 'version $(VERSION)' \
		--define 'release $(RELEASE)' \
		--target $(ARCH) \
		$(<)

$(SPECDIR)/%.spec: %.spec
	mkdir -p $(SPECDIR)
	cp $(<) $(@)

$(SRCDIR)/%.tar.gz: %.tar.gz
	mkdir -p $(SRCDIR)
	cp $(<) $(@)

$(BUNDLE):
	wget https://github.com/markh794/mhvtl/archive/$(@)

.PHONY: clean
clean:
	rm -rf $(SPECDIR)/mhvtl.* $(SRCDIR)/$(BUNDLE) *.rpm *.tar.gz

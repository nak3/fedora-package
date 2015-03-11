PACKAGE = rubygem-rhc
VERSION = 1.35.1
RELEASE = 1
TMPREPOS = tmp.repos
TMPREVIEW = tmp.review
FC_VERSION = fc21
F_VERSION = f21
DOWNLOAD_LINK = https://github.com/openshift/rhc/archive/552a5668e0f9ce1c7a870534aed066124d6e3f9d/$(PACKAGE)-$(VERSION).tar.gz
DOWNLOAD_LINK2 = http://rubygems.org/downloads/rhc-$(VERSION).gem

all: srpm

test:
	@echo "hello"

wget:
	wget $(DOWNLOAD_LINK)
	wget $(DOWNLOAD_LINK2)

scp:
	scp $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm fedorapeople:/home/fedora/kenjiro/public_html/copr/
#	scp $(PACKAGE).spec fedorapeople:/home/fedora/kenjiro/public_html/copr

srpm:   wget
	mkdir -p $(TMPREPOS)/{SPECS,RPMS,SRPMS,SOURCES}
	cp $(PACKAGE)-$(VERSION).tar.gz $(TMPREPOS)/SOURCES/$(PACKAGE)-$(VERSION).tar.gz
	cp rhc-$(VERSION).gem $(TMPREPOS)/SOURCES/rhc-$(VERSION).gem
	rpmbuild --define="_source_filedigest_algorithm md5" --define="_topdir `pwd`/$(TMPREPOS)" -bs $(PACKAGE).spec
	@echo
	@echo "srpm available at '$(TMPREPOS)'"
	@echo

rpm:    srpm
	rpmbuild --define="_topdir `pwd`/$(TMPREPOS)" --rebuild "$(TMPREPOS)"/SRPMS/*.src.rpm
	@echo
	@echo "rpm(s) available at '$(TMPREPOS)'"
	@echo

rpmlint:
	rpmlint $(PACKAGE).spec $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm tmp.repos/RPMS/x86_64/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).x86_64.rpm

kojibuild:
	koji build --scratch $(F_VERSION) $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm

fedora-review:
	mkdir -p $(TMPREVIEW)
	cd $(TMPREVIEW)
	fedora-review --rpm-spec --name $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm

clean:
	rm -f $(PACKAGE)-$(VERSION).tar.gz
	rm -rf $(PACKAGE)-$(VERSION)

clean-local:
	rm -fr "$(TMPREPOS)"
	rm -fr "$(TMPREVIEW)"

clean-all: clean clean-local

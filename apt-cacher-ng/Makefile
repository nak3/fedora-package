PACKAGE = apt-cacher-ng
VERSION = 0.7.27
RELEASE = 1
UPSTREAM_RELEASE = 1
TMPREPOS = tmp.repos
TMPREVIEW = tmp.review
FC_VERSION = fc20
F_VERSION = f20

all: srpm

test:
	@echo "hello"

wget:
	wget http://ftp.debian.org/debian/pool/main/a/$(PACKAGE)/$(PACKAGE)_$(VERSION).orig.tar.xz
	wget http://ftp.debian.org/debian/pool/main/a/$(PACKAGE)/$(PACKAGE)_$(VERSION)-$(UPSTREAM_RELEASE).debian.tar.xz

scp:
	scp tmp.repos/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm fedorapeople:/home/fedora/kenjiro/public_html/pkgreview/$(PACKAGE)/
	scp $(PACKAGE).spec fedorapeople:/home/fedora/kenjiro/public_html/pkgreview/$(PACKAGE)/

srpm:	wget
	mkdir -p $(TMPREPOS)/{SPECS,RPMS,SRPMS,SOURCES}
	cp $(PACKAGE)_$(VERSION).orig.tar.xz $(TMPREPOS)/SOURCES/$(PACKAGE)_$(VERSION).orig.tar.xz
	cp $(PACKAGE)_$(VERSION)-$(UPSTREAM_RELEASE).debian.tar.xz $(TMPREPOS)/SOURCES/$(PACKAGE)_$(VERSION)-$(RELEASE).debian.tar.xz
	#cp $(PACKAGE)_$(VERSION)-$(UPSTREAM_RELEASE).debian.tar.xz $(TMPREPOS)/SOURCES/$(PACKAGE)_$(VERSION).debian.tar.xz
	cp $(PACKAGE).service $(TMPREPOS)/SOURCES/
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
	rpmlint $(PACKAGE).spec tmp.repos/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm tmp.repos/RPMS/x86_64/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).x86_64.rpm

kojibuild:
	koji build --scratch $(F_VERSION) $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm

fedora-review:
	mkdir -p $(TMPREVIEW)
	cd $(TMPREVIEW)
	fedora-review --rpm-spec --name $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm

clean-all: clean clean-local

clean:
	rm -f $(PACKAGE)_$(VERSION)-1.debian.tar.xz
	rm -f $(PACKAGE)_$(VERSION).orig.tar.xz

clean-local:
	rm -fr "$(TMPREPOS)"

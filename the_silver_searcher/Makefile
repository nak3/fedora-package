PACKAGE = the_silver_searcher
VERSION = 0.25.0
RELEASE = 1
#EXTRA_DIST = .gitignore
TMPREPOS = tmp.repos
TMPREVIEW = tmp.review
FC_VERSION = fc20
F_VERSION = f20

commit =      7e212a4cbf01fa0c8275f05eaa2b2807bd127c11
shortcommit = 7e212a4

all: srpm

test:
	@echo "hello"

wget:
	wget https://codeload.github.com/ggreer/$(PACKAGE)/tar.gz/$(commit)
	mv $(commit) $(PACKAGE)-$(VERSION).tar.gz

scp:
	scp $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm fedorapeople:/home/fedora/kenjiro/public_html/pkgreview/$(PACKAGE)/
	scp $(PACKAGE).spec fedorapeople:/home/fedora/kenjiro/public_html/pkgreview/$(PACKAGE)/


# $(PACKAGE)-$(VERSION):
# 	cp -r $(PACKAGE) $(PACKAGE)-$(VERSION)

srpm:   wget
	mkdir -p $(TMPREPOS)/{SPECS,RPMS,SRPMS,SOURCES}
	cp $(PACKAGE)-$(VERSION).tar.gz $(TMPREPOS)/SOURCES/$(VERSION)-$(shortcommit).tar.gz
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

PACKAGE = openshift-sdn
VERSION = 0.4
RELEASE = 1
TMPREPOS = tmp.repos
TMPREVIEW = tmp.review
FC_VERSION = fc21
F_VERSION = f21
DOWNLOAD_LINK = https://github.com/openshift/openshift-sdn/archive/70d604e44c9ddb50b7ff3879c10d04ccf160de7c/openshift-sdn-0.4.tar.gz

all: srpm

test:
	@echo "hello"

wget:
	wget $(DOWNLOAD_LINK)

scp:
	scp $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm fedorapeople:/home/fedora/kenjiro/public_html/copr/
#	scp $(PACKAGE).spec fedorapeople:/home/fedora/kenjiro/public_html/copr

srpm:   wget
	mkdir -p $(TMPREPOS)/{SPECS,RPMS,SRPMS,SOURCES}
	cp $(PACKAGE)-$(VERSION).tar.gz $(TMPREPOS)/SOURCES/$(PACKAGE)-$(VERSION).tar.gz
#	----
#	tar xvf $(PACKAGE)-$(VERSION).tar.gz
#	cp -r rel-eng openshift-sdn-667d4aee179d89c377bf8557cb41c741307fcb4e/
#	tar cvf openshift-sdn-0.1.tar.gz openshift-sdn-667d4aee179d89c377bf8557cb41c741307fcb4e
#	cp $(PACKAGE)-$(VERSION).tar.gz $(TMPREPOS)/SOURCES/$(PACKAGE)-$(VERSION).tar.gz
#	----
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

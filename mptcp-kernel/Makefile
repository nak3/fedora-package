PACKAGE = kernel
VERSION = 3.14.15
LINUX_VERSION = 3.14
RELEASE = 309
TMPREPOS = tmp.repos
F_VERSION = f21
FC_VERSION = fc21

commit = dcdf730ddc79ff114da05c96fc7ce7bcab4e1952
shortcommit = dcdf730dd

all: srpm

test:
	echo $(shortcommit)

wget:
	wget https://codeload.github.com/multipath-tcp/mptcp/tar.gz/$(commit)
	mv $(commit) $(VERSION)-$(shortcommit).tar.gz
	tar xvf $(VERSION)-$(shortcommit).tar.gz
	mv mptcp-$(commit) linux-3.14
	tar -Jcvf linux-3.14.tar.xz linux-3.14

scp:
	scp tmp.repos/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).mptcp.$(FC_VERSION).src.rpm fedorapeople:/home/fedora/kenjiro/public_html/copr

srpm:	wget
	mkdir -p $(TMPREPOS)/{SPECS,RPMS,SRPMS,SOURCES}
	cp linux-3.14.tar.xz $(TMPREPOS)/SOURCES/
	cp originals/* $(TMPREPOS)/SOURCES/
	cp materials/config-x86_64-generic $(TMPREPOS)/SOURCES/
	rpmbuild --define="_source_filedigest_algorithm md5" --define="_topdir `pwd`/$(TMPREPOS)" -bs $(PACKAGE).spec
	@echo
	@echo "srpm available at '$(TMPREPOS)'"
	@echo

rpm:
	rpmbuild --define="_topdir `pwd`/$(TMPREPOS)" --rebuild "$(TMPREPOS)"/SRPMS/*.src.rpm
	@echo
	@echo "rpm(s) available at '$(TMPREPOS)'"
	@echo

kojibuild:
	koji build --scratch $(F_VERSION) $(TMPREPOS)/SRPMS/$(PACKAGE)-$(VERSION)-$(RELEASE).$(FC_VERSION).src.rpm

clean-all: clean clean-local

clean:
	rm -f $(VERSION)-$(shortcommit).tar.gz
	rm -f linux-$(LINUX_VERSION).tar.xz
	rm -rf linux-$(LINUX_VERSION)

clean-local:
	rm -fr "$(TMPREPOS)"

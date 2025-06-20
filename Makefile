# -*- mode: makefile-gmake; coding: utf-8 -*-
DESTDIR ?= ~

all:

package:
	ian build -c

install:
	python3 setup.py install \
	    --prefix=$(DESTDIR)/usr/ \
		--root=/ \
		--single-version-externally-managed \
	    --no-compile \
	    --install-layout=deb

.PHONY: clean
clean:
	find -name "*.pyc" -print -delete
	find -name __pycache__ -print -delete
	$(RM) -r build mdevtk.egg-info


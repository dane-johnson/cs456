.PHONY: clean
%.tar.gz: % %/Makefile
	cd $< && make clean
	tar -cvzf $@ $<
clean:
	rm -f *.tar.gz

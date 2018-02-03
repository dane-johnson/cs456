%:
	[ ! -e builds ] && mkdir builds || :
	cd ./proj$@ && pdflatex report.tex
	mv ./proj$@/report.pdf ./builds

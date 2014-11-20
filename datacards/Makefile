SHELL = bash

.PHONY : upload download

upload :
	rsync -aiHP ./* belknap@login.hep.wisc.edu:/afs/hep.wisc.edu/home/belknap/DblHLimits_611/src/datacards/

download :
	rsync -aiHP belknap@login.hep.wisc.edu:/afs/hep.wisc.edu/home/belknap/DblHLimits_611/src/datacards/* ./


.PHONY : download_root

download_root :
	rsync -aiHP belknap@login06.hep.wisc.edu:/nfs_scratch/belknap/data/samples/ ./root_files/

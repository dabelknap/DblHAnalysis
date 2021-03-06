CHANNEL=all

ROOTDIR = ./root_files
NTUPDIR = ./ntuples

SAMPLE_NAMES := $(notdir $(shell ls $(ROOTDIR)))

SAMPLE_PATHS := $(addprefix $(ROOTDIR), $(SAMPLE_NAMES))
NTUPLES := $(addprefix $(NTUPDIR)/, $(addsuffix .h5, $(SAMPLE_NAMES)))

.PHONY : download_root

download_root :
	mkdir -p ./root_files
	rsync -aiHP belknap@login06.hep.wisc.edu:/nfs_scratch/belknap/data/samples/ ./root_files/

ntuples : $(NTUPLES)

$(NTUPDIR)/%.h5 : $(ROOTDIR)/%
	python analyze4l.py $< $@ $(CHANNEL)

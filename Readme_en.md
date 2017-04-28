# MMPOSTagger

## A basic POS Tagger for Tibetan.

It currently only uses [Monlam Dictionary](http://monlamit.com/content/monlam-grand-tibetan-dictionary)'s POS Tags converted into [UD Tags](http://universaldependencies.org/u/pos/) (a repo about the POS mappings coming soon!)

## Installation and Usage:

##### Usage
 - Either clone or download the .zip
 - Put in `input` the files to POS-tag
 - run [POS_Tagger.py](POS_Tagger.py)

##### Dependencies
 - [PyTib](https://github.com/Esukhia/PyTib) for segmenting the input files in words, prior to POS Tagging.

Note: It has been copied in `dependencies` to allow to run the project after downloading the .zip file.

## Todo: 
 - add the Monlam features in the structure (tags in the dictionary that are not POS)
 - use monlam_verbs.json for the verbs
 - implement the SOAS POS Tags(from [Tibetan in Digital Communication](https://www.soas.ac.uk/cia/tibetanstudies/tibetan-in-digital-communications/) project) and use them as a first choice (falling back on Monlam where there is no POS)


Copyright [Buddhist Digital Resource Center](https://www.tbrc.org/), 2017, MIT License
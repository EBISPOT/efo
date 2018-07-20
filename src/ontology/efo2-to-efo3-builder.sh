
# convert efo-edit.owl to OWL functional syntax 

../../bin/robot convert -i efo-edit.owl --format ofn -o efo-edit.owl.tmp

mv efo-edit.owl.tmp efo-edit.owl

# download all the latest files we import

#python ../../bin/efoutils.py

#../../bin/robot unmerge \
#    --input build/efo-3-edit.owl --input build/full_imports/cl.owl \
#    unmerge --input build/full_imports/bto.owl \
#    unmerge --input build/full_imports/cl.owl \

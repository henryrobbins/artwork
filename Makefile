# Compile all work
work:
	cd template && python template.py
	cd dissolve && python dissolve.py
	cd mod && python mod.py
	cd drunk_walk && python drunk_walk.py
	cd partition && python partition.py
	cd clip && python clip.py
	cd channel && python channel.py
	cd resolution && python resolution.py
	cd stewart && python stewart.py
	cd steal_your_face && python steal_your_face.py
	cd weierstrass && python weierstrass.py
# cd conway && python conway.py
# TODO: uncomment this after testing

# Create archive directory
.PHONY: archive
archive:
	python archive.py

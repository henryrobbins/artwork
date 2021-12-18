# Compile all work
work:
	cd dissolve && python src.py
	cd mod && python src.py
	cd drunk_walk && python src.py
	cd partition && python src.py
	cd clip && python src.py
	cd channel && python src.py
	cd resolution && python src.py
	cd stewart && python src.py
	cd steal_your_face && python src.py
	cd weierstrass && python src.py
	cd conway && python src.py

# Create archive directory
web-archive:
	python web_archive.py

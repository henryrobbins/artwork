# Compile all netpbm works
netpbm-works:
	cd netpbm && make netpbm-works

# Compile all animation works
animation-works:
	cd animation && make animation-works

# Compile all ascii works
ascii-works:
	cd ascii && make ascii-works

# Compile all works
all-works: netpbm-works animation-works ascii-works

# Create archive directory
.PHONY: archive
archive:
	python archive.py
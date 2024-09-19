REPO=thraxil
APP=sebastian
MAX_COMPLEXITY=4

all: test

flake.lock: flake.nix
	nix flake update

include *.mk

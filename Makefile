all:
	./generate.py trams > src/trams.js
	yarn build
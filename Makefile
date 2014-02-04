.PHONY: docs server bootstrap deploy

docs:
	./build_docs.sh master docs/dev
	./build_docs.sh release-0.12 docs/0.12
	./build_docs.sh release-0.11 docs/0.11
	./build_docs.sh release-0.10 docs/0.10
	./build_docs.sh release-0.9 docs/0.9
	cd docs; ln -fs 0.12 stable

bootstrap:
	wget -O /tmp/bootstrap.zip http://twitter.github.com/bootstrap/assets/bootstrap.zip
	unzip -d static/ /tmp/bootstrap.zip

server:
	./server restart

deploy:
	ssh marc@bottlepy.org 'cd bottlepy.org && git pull && make server && make docs'


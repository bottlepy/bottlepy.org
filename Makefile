.PHONY: docs server

server:
	./server restart

docs:
	./build_docs.sh master docs/dev
	./build_docs.sh release-0.10 docs/0.10
	./build_docs.sh release-0.9 docs/0.9

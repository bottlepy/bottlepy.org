.PHONY: docs server bootstrap deploy

docs:
	./build_docs.sh patch-py313-multipart docs/dev
	./build_docs.sh release-0.12 docs/0.12
	#./build_docs.sh release-0.11 docs/0.11
	#./build_docs.sh release-0.10 docs/0.10
	#./build_docs.sh release-0.9 docs/0.9
	cd docs; ln -fs 0.12 stable

deploy: docs
	rsync -av docs/ root@defnull.de:/srv/stack/nginx/vhost/bottlepy.org/docs/


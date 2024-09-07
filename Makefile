.PHONY: docs server bootstrap deploy

docs:
	./build_docs.sh master htdocs/docs/dev
	./build_docs.sh release-0.13 htdocs/docs/0.13
	./build_docs.sh release-0.12 htdocs/docs/0.12
	#./build_docs.sh release-0.11 htdocs/htdocs/docs/0.11
	#./build_docs.sh release-0.10 docs/0.10
	#./build_docs.sh release-0.9 htdocs/docs/0.9
	cd htdocs/docs; ln -fs --no-dereference 0.13 stable

deploy: docs
	rsync -av htdocs/ root@bottlepy.org:/srv/stack/nginx/vhost/bottlepy.org/


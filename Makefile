.PHONY: setup lint test run demo docker
setup:
	pip install -r requirements.txt
lint:
	flake8 .
test:
	pytest --maxfail=1 --disable-warnings -q
run:
	python review.py --range HEAD~1..HEAD --output report.md
docker:
	docker build -t aicrl:local .
demo: setup lint test run

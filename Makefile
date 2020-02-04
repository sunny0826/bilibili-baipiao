.PHONY: run build

run: export COOKIES = $(BILIBILI_COOKIES)
run: export SENDER = $(EMAIL_SENDER)
run: export RECEIVER = $(EMAIL_RECEIVER)
run: export PASS = $(EMAIL_PASS)

build:
	pip install .

run: build
	baipiao
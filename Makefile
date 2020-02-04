.PHONY: run build

run: export COOKIES = $(PLUGIN_BILIBILI_COOKIES)
run: export SENDER = $(PLUGIN_EMAIL_SENDER)
run: export RECEIVER = $(PLUGIN_EMAIL_RECEIVER)
run: export PASS = $(PLUGIN_EMAIL_PASS)

build:
	pip install .

run: build
	baipiao
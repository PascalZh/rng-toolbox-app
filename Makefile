UI_SRC=src/generated/random_toolbox_main_window.py

all: $(UI_SRC)

$(UI_SRC): src/generated/%.py : src/%.ui
	pyuic5 -o $@ $<
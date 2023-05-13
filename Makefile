VENV		:= test -d venv || python3 -m venv venv
INSTALL	:= . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

install:venv
	@echo "Installing..."
	@$(INSTALL)
	@echo "Installation done."

venv:
	@echo "Creating venv..."
	@$(VENV)
	@echo "Creation done."

.PHONY: install venv

PACKAGE_NAME=my_deployment_package.zip
LIB_DIR=./libraries

.PHONY: all clean build

all: clean build

build:
	pip3 install --target $(LIB_DIR) -r requirements.txt

	cd $(LIB_DIR) && zip -r ../$(PACKAGE_NAME) .

	zip -r $(PACKAGE_NAME) . \
		-x "$(LIB_DIR)/*" \
		-x "main.py" \
		-x "./$(LIB_DIR)/*" \
		-x "./main.py" \
		-x "makefile" \
		-x "./makefile"

clean:
	rm -rf $(LIB_DIR)
	rm -f $(PACKAGE_NAME)

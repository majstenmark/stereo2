PATH_TO_FX=./bin/javafx-sdk-11.0.2/lib/

build: src
	mkdir -p build
	javac --module-path ${PATH_TO_FX} --add-modules=javafx.controls src/*.java -d build

prod:
	make build; java -cp 'build:.' --module-path ${PATH_TO_FX} --add-modules=javafx.controls App prod
usb:
	make build; java -cp 'build:.' --module-path ${PATH_TO_FX} --add-modules=javafx.controls App usb

mock:
	make build; java -cp 'build:.' --module-path ${PATH_TO_FX} --add-modules=javafx.controls App mock
slave:
	make build; java -cp 'build:.' --module-path ${PATH_TO_FX} --add-modules=javafx.controls App slave
axis:
	make build; java -cp 'build:.' --module-path ${PATH_TO_FX} --add-modules=javafx.controls App axis
all-master:
	make build; java -cp 'build:.' --module-path ${PATH_TO_FX} --add-modules=javafx.controls App all-master

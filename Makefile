LIB_DIR = clib

default: pytransciever

pytransciever: setup.py pytransciever.pyx $(LIB_DIR)/libtransciever.a
	python3 setup.py build_ext --inplace && rm -f pytransciever.c && rm -Rf build

$(LIB_DIR)/libtransciever.a:
	make -C $(LIB_DIR) libtransciever.a

clean:
	make -C $(LIB_DIR) clean
	rm *.so

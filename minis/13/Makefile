run: matrix_pow.so main.py
	python main.py

matrix_pow.so: matrix_pow.c
	$(CC) $(shell python-config --includes) -O3 matrix_pow.c -shared -fPIC -o matrix_pow.so

.PHONY: run

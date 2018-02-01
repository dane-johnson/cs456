.PHONY = all test benchmark
DEPS = sorts.h list.h
OBJ = sorts.o generator.o

all: benchmark test

benchmark: benchmark.o $(OBJ)
	gcc -o $@ $^

test: test.c $(OBJ)
	gcc -g -o $@ $^

%.o: %.c $(DEPS)
	gcc -c -o $@ $<

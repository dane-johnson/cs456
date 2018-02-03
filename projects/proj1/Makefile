.PHONY = all test benchmark
CFLAGS = -g
DEPS = sorts.h list.h
OBJ = sorts.o generator.o

all: benchmark test

benchmark: benchmark.c $(OBJ)
	gcc $(CFLAGS) -o $@ $^
clean:
	rm -f *.o benchmark test

test: test.c $(OBJ)
	gcc $(CFLAGS) -o $@ $^

%.o: %.c $(DEPS)
	gcc $(CFLAGS) -c -o $@ $<

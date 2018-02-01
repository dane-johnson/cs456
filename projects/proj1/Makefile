.PHONY = test
DEPS = sorts.h list.h
OBJ = sorts.o generator.o

test: test.c $(OBJ)
	gcc -g -o $@ $^

%.o: %.c $(DEPS)
	gcc -c -o $@ $<

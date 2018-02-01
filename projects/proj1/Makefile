.PHONY = test
DEPS = sorts.h list.h
OBJ = sorts.o generator.o

test: $(OBJ) test.o
	gcc -o $@ $^

%.o: %.c $(DEPS)
	gcc -c -o $@ $<

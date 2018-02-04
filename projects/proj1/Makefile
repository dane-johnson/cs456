.PHONY = all
CFLAGS = 
DEPS = sorts.h list.h
OBJ = sorts.o generator.o
EXE = benchmark test quicksort_array

all: $(EXE)

clean:
	rm -f *.o benchmark test

%.o: %.c $(DEPS)
	gcc $(CFLAGS) -c -o $@ $<

$(EXE): %: %.c $(OBJ)
	gcc $(CFLAGS) -o $@ $^

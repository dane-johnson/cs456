.PHONY = all
CFLAGS = -g 
DEPS = sorts.h list.h
OBJ = sorts.o generator.o
EXE = benchmark test quicksort_array mergesort_array quicksort_list mergesort_list

all: $(EXE)

clean:
	rm -f *.o $(EXE)

%.o: %.c $(DEPS)
	gcc $(CFLAGS) -c -o $@ $<

$(EXE): %: %.c $(OBJ)
	gcc $(CFLAGS) -o $@ $^

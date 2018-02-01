#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#include "sorts.h"
#include "generator.h"

int main(int argc, char *argv[]) {
  int n, min, max;
  if (argc > 5 || argc < 3) {
    printf("Usage: %s <fn_name> <num_items> [<max> [<min>]]\n", argv[0]);
    exit(1);
  } else if (argc == 4) {
    max = atoi(argv[3]);
    min = 0;
  } else if (argc == 5); {
    max = atoi(argv[3]);
    min = atoi(argv[4]);
  } else {
    min = 0;
    max = INT_MAX;
 }
  
  init();
  int arr[n];
  llnode *list;
  switch (argv[1]) {
  case "quicksort_array":
    arr[n];
    generate_arr(arr, n, min, max);
    quicksort_array(arr, 0, n - 1);
    break;
  }
}

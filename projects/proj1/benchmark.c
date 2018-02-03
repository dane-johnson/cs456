#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>

#include "list.h"
#include "sorts.h"
#include "generator.h"

void find_tail(llnode **tail) {
  llnode *curr = *tail;
  while (curr->next != NULL) {
    curr = curr->next;
  }
  *tail = curr;
}

int main(int argc, char *argv[]) {
  int n, min, max;
  if (argc > 5 || argc < 3) {
    printf("Usage: %s <fn_name> <num_items> [<max> [<min>]]\n", argv[0]);
    exit(1);
  } else if (argc == 4) {
    max = atoi(argv[3]);
    min = 0;
  } else if (argc == 5) {
    max = atoi(argv[3]);
    min = atoi(argv[4]);
  } else {
    min = 0;
    max = INT_MAX;
  }

  n = atoi(argv[2]);
  
  init();
  int arr[n];
  llnode *list, *tail;
  if (strcmp(argv[1], "quicksort_arr") == 0) {
    generate_arr(arr, n, min, max);
    quicksort_array(arr, 0, n - 1);
  } else if (strcmp(argv[1], "quicksort_list") == 0) {
    generate_list(&list, n, min, max);
    tail = list;
    find_tail(&tail);
    quicksort_list(list, list, tail);
  } else if (strcmp(argv[1], "mergesort_array") == 0) {
    generate_arr(arr, n, min, max);
    mergesort_array(arr, n);
  } else if (strcmp(argv[1], "mergesort_list") == 0) {
    generate_list(&list, n, min, max);
    tail = list;
    find_tail(&tail);
    mergesort_list(&list);
  }
}

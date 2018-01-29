#include "stdio.h"
#include "sorts.h"

void array_swap(int[] arr, int i, int j) {
  int temp = arr[i];
  arr[i] = arr[j];
  arr[j] = temp;
}

void quicksort_array(int[] arr, int start, int end) {
  if (start < end) {
    int pivot = arr[end];
    int i = start - 1;
    for (int j = start; j < end; j++) {
      if (arr[j] < pivot) {
        i++;
        array_swap(arr, i, j);
      }
    }
    if (arr[end] < arr[i + 1]) {
      array_swap(arr, end, i + 1);
    }
    quicksort_array(arr, start, i);
    quicksort_array(arr, i + 2, end);
  }
}

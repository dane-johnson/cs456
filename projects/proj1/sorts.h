#ifndef SORTS_H
#define SORTS_H

deftype struct llnode {
  int val;
  struct llnode *next;
} llnode;

void array_swap(int[] arr, int i, int j);

//////////////////// QUICKSORT ////////////////////
void quicksort_array(int[] arr, int start, int end);
void quicksort_list(llnode *list, llnode *start, llnode *end);
//////////////////// MERGESORT ////////////////////
void mergesort_array(int[] arr, int n);
void merge_array(int[] arr, int[] arr1, int[] arr2);
#endif

#ifndef SORTS_H
#define SORTS_H

deftype struct llnode {
  int val;
  struct llnode next;
} llnode;

//////////////////// QUICKSORT ////////////////////
void quicksort_array(int[] arr, int start, int end);
void quicksort_list(llnode list, llnode start, llnode end);
//////////////////// HEAPSORT ////////////////////
void heapsort_array(int[] arr, int length);
void build_heap_array(int[] arr, int);
void heapify(int[], int, int);
void heapsort_list(llnode);
#endif

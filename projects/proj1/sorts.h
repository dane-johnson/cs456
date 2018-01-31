#ifndef SORTS_H_
#define SORTS_H_

typedef struct llnode {
  int val;
  struct llnode *next;
} llnode;

void array_swap(int arr[], int i, int j);
void list_swap(llnode *a, llnode *b);

//////////////////// QUICKSORT ////////////////////
void quicksort_array(int arr[], int start, int end);
void quicksort_list(llnode *list, llnode *start, llnode *tail);
//////////////////// MERGESORT ////////////////////
void mergesort_array(int arr[], int n);
void merge_array(int arr[], int arr1[], int arr2[]);
#endif // SORTS_H_

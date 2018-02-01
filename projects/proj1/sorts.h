#ifndef SORTS_H_
#define SORTS_H_

void array_swap(int arr[], int i, int j);
void list_swap(llnode *a, llnode *b);

//////////////////// QUICKSORT ////////////////////
void quicksort_array(int arr[], int start, int end);
void quicksort_list(llnode *list, llnode *start, llnode *tail);
//////////////////// MERGESORT ////////////////////
void mergesort_array(int arr[], int n);
void merge_array(int arr[], int arr1[], int arr2[], int n1, int n2);
void mergesort_list(llnode **list);
void merge_list(llnode **list, llnode *list1, llnode *list2);
#endif // SORTS_H_

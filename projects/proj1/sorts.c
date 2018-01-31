#include "stdio.h"
#include "stdlib.h"
#include "sorts.h"

void array_swap(int arr[], int i, int j) {
  int temp = arr[i];
  arr[i] = arr[j];
  arr[j] = temp;
}

void list_swap(llnode *a, llnode *b) {
  int temp = a->val;
  a->val = b->val;
  b->val = temp;
}

//////////////////// QUICKSORT ////////////////////

void quicksort_array(int arr[], int start, int end) {
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

void quicksort_list(llnode *list, llnode *head, llnode *tail) {
  if (head != NULL && tail != NULL && head != tail) {
    int pivot = tail->val;
    llnode* mid = head;
    llnode* curr = head;
    llnode* last = NULL;

    while (curr != tail) {
      if (curr->val < pivot) {
        list_swap(curr, mid);
        last = mid;
        mid = mid->next;
      }
      curr = curr->next;
    }

    if (tail->val < mid->val) {
      list_swap(tail, mid);
    }
    
    quicksort_list(list, head,  last);
    quicksort_list(list, mid->next, tail);
  }
}

//////////////////// MERGESORT ////////////////////

void mergesort_array(int arr[], int n) {
  if (n > 1) {
    int n1 = n / 2;
    int n2 = n / 2 + n % 2;
    int arr1[n1];
    int arr2[n2];
  }
}
void merge_array(int arr[], int arr1[], int arr2[]);




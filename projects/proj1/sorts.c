#include <stdio.h>
#include <stdlib.h>

#include "list.h"
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
    if (mid != tail) {
      quicksort_list(list, mid->next, tail);
    }
  }
}

//////////////////// MERGESORT ////////////////////

void copyarr(int dest[], int src[], int n) {
  for (int i = 0; i < n; i++) {
    dest[i] = src[i];
  }
}

void mergesort_array(int arr[], int n) {
  if (n > 1) {
    int n1 = n / 2;
    int n2 = (n / 2) + (n % 2);
    int arr1[n1];
    int arr2[n2];
    copyarr(arr1, arr, n1);
    copyarr(arr2, arr + n1, n2);
    mergesort_array(arr1, n1);
    mergesort_array(arr2, n2);
    merge_array(arr, arr1, arr2, n1, n2);
  }
}

void merge_array(int arr[], int arr1[], int arr2[], int n1, int n2){
  int i = 0;
  int j = 0;
  while (i < n1 || j < n2) {
    if (i == n1) {
      arr[i + j] = arr2[j];
      j++;
    } else if (j == n2) {
      arr[i + j] = arr1[i];
      i++;
    } else if (arr1[i] > arr2[j]) {
      arr[i + j] = arr2[j];
      j++;
    } else {
      arr[i + j] = arr1[i];
      i++;
    }
  }
}

void split_list(llnode *list, llnode **list1, llnode **list2) {
  llnode *curr = list;
  llnode *mid = list;
  while (curr->next != NULL) {
    curr = curr->next;
    if (curr->next != NULL) {
      curr = curr->next;
      mid = mid->next;
    }
  }
  // list 2 will point to the first node after the middle
  *list2 = mid->next;
  // Break the list into 2 lists
  mid->next = NULL;
  *list1 = list;
}

void mergesort_list(llnode **list) {
  if ((*list)->next != NULL) {
    llnode *list1, *list2;
    split_list(*list, &list1, &list2);
    mergesort_list(&list1);
    mergesort_list(&list2);
    merge_list(list, list1, list2);
  }
}

void merge_list(llnode **list, llnode *list1, llnode *list2) {
  llnode *curr;
  if (list1->val < list2->val){
    curr = list1;
    list1 = list1->next;
  } else {
    curr = list2;
    list2 = list2->next;
  }
  *list = curr;
  while (list1 != NULL || list2 != NULL) {
    if (list1 == NULL) {
      curr->next = list2;
      list2 = list2->next;
      curr = curr->next;
    } else if (list2 == NULL) {
      curr->next = list1;
      list1 = list1->next;
      curr = curr->next;
    } else if (list1->val > list2->val) {
      curr->next = list2;
      list2 = list2->next;
      curr = curr->next;
    } else {
      curr->next = list1;
      list1 = list1->next;
      curr = curr->next;
    }
  }
  curr->next = NULL;
}

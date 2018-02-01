#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "list.h"
#include "generator.h"
#include "sorts.h"

void main() {
  printf("Testing generate_arr...\n");
  int arr[10];
  generate_arr(arr, 10, 2, 3);
  assert(arr[0] >= 2 && arr[0] <= 3);
  printf("Done\n");

  printf("Testing generate_list...\n");
  llnode* head;
  generate_list(&head, 1, 2, 3);
  assert(head->val >= 2 && head->val <= 3);
  assert(head->next == NULL);
  printf("Done\n");

  printf("Testing quicksort_array...\n");
  int arr1[3] = { 3, 2, 1 };
  quicksort_array(arr1, 0, 2);
  assert(arr1[0] == 1 && arr1[2] == 3);
  printf("Done\n");

  printf("Testing quicksort_list\n");
  llnode *nodes = (llnode*)calloc(3, sizeof(llnode));
  nodes[0].val = 3;
  nodes[1].val = 2;
  nodes[2].val = 1;
  nodes[0].next = &nodes[1];
  nodes[1].next = &nodes[2];
  nodes[2].next = NULL;
  quicksort_list(nodes, nodes, &nodes[2]);
  assert(nodes[0].val == 1 && nodes[2].val == 3);
  printf("Done\n");

  printf("Testing mergesort_array...\n");
  int arr2[3] = { 3, 2, 1 };
  mergesort_array(arr2, 3);
  assert(arr2[0] == 1 && arr2[2] == 3);
  printf("Done\n");

  printf("Testing mergesort_list\n");
  llnode *nodes1 = (llnode*)calloc(3, sizeof(llnode));
  nodes1[0].val = 3;
  nodes1[1].val = 2;
  nodes1[2].val = 1;
  nodes1[0].next = &nodes1[1];
  nodes1[1].next = &nodes1[2];
  nodes1[2].next = NULL;
  mergesort_list(&nodes1);
  assert(nodes1[0].val == 1 && nodes1[0].next->next->val == 3);
  printf("Done\n");
}

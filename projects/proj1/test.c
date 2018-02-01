#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "list.h"
#include "generator.h"

void main() {
  printf("Testing generate_arr...\n");
  int arr[1];
  generate_arr(arr, 1, 2, 3);
  assert(arr[0] >= 2 && arr[0] <= 3);
  printf("Done\n");

  printf("Testing generate_list...\n");
  llnode* head;
  generate_list(&head, 1, 2, 3);
  assert(head->val >= 2 && head->val <= 3);
  assert(head->next == NULL);
  printf("Done\n");
}

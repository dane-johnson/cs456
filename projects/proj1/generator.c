#include <time.h>
#include <stdlib.h>

#include "list.h"
#include "generator.h"

void init() {
  srand(time(NULL));
}

void generate_arr(int arr[], int n,  int min, int max) {
  for (int i = 0; i < n; i++) {
    int next_num = rand() % (max - min) + max;
    arr[i] = next_num;
  }
}

void generate_list(llnode** head, int n, int min, int max) {
  llnode *curr = (llnode*)malloc(sizeof(llnode));
  int next_num = rand() % (max - min) + max;
  curr->val = next_num;
  *head = curr;
  for (int i = 0; i < n - 1; i++) {
    curr = curr->next;
    curr = (llnode*)malloc(sizeof(llnode));
    next_num =  rand() % (max - min) + max;
  }
  curr->next = NULL;
}

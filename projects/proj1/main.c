#include <stdio.h>
#include <stdlib.h>

#include "list.h"
#include "sorts.h"

#define BUF_SIZE 255
#define NEW_NODE (llnode*)malloc(sizeof(llnode))

void read_file_into_list(FILE *fin, llnode **list) {
  llnode *curr = NEW_NODE;
  *list = curr;
  char str[BUF_SIZE];
  fgets(str, BUF_SIZE, fin);
  curr->val = atoi(str);
  while (fgets(str, BUF_SIZE, fin)) {
    curr->next = NEW_NODE;
    curr = curr->next;
    curr->val = atoi(str);
  }
  curr->next = NULL;
}

int count_file_size(FILE *fin) {
  int lines = 0;
  int ch;
  while (EOF != (ch=getc(fin))) {
    if (ch=="\n") {
      lines++;
    }
  }
  rewind(fin);
  return lines;
}

void read_file_into_array(FILE *fin, int arr[], int n) {
  char str[BUF_SIZE];
  for (int i = 0; i < n, i++) {
    fgets(str, BUF_SIZE, fin);
    arr[i] = atoi(str);
  }
}

int main(int argc, char *argv[]) {
  
}

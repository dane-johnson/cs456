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
    if (ch == '\n') {
      lines++;
    }
  }
  rewind(fin);
  return lines;
}

void read_file_into_array(FILE *fin, int arr[], int n) {
  char str[BUF_SIZE];
  for (int i = 0; i < n; i++) {
    fgets(str, BUF_SIZE, fin);
    arr[i] = atoi(str);
  }
}

void print_list_into_file(FILE *fout, llnode *list) {
  while(list->next) {
    fprintf(fout, "%d\n", list->val);
    list = list->next;
  }
}

void print_array_into_file(FILE *fout, int arr[], int n) {
  for (int i = 0; i < n; i++) {
    fprintf(fout, "%d\n", arr[i]);
  }
}

void usage(char *invocation) {
  printf("Usage: %s <infile>\n", invocation);
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    usage(argv[0]);
    exit(1);
  }
  FILE *fin = fopen(argv[1], "r");
  int n = count_file_size(fin);
  int arr[n];
  read_file_into_array(fin, arr, n);
  fclose(fin);
  quicksort_array(arr, 0, n - 1);
  char outfile[BUF_SIZE];
  sprintf(outfile, "quicksortarray-%s", argv[1]);
  FILE *fout =fopen(outfile, "w");
  print_array_into_file(fout, arr, n);
  fclose(fout);
}

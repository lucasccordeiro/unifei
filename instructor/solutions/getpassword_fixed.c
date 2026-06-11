/* Lab 2, file 4 — fix.
 * fgets never writes more than sizeof(buf) bytes, and we strip the
 * trailing newline before comparing.
 *
 * esbmc getpassword_fixed.c  =>  VERIFICATION SUCCESSFUL
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int getPassword(void)
{
  char buf[8];
  if (!fgets(buf, sizeof(buf), stdin))
    return 1;
  buf[strcspn(buf, "\n")] = '\0';
  return strcmp(buf, "SMT");
}

int main(void)
{
  int x = getPassword();
  if (x) {
    printf("Access Denied\n");
    exit(0);
  }
  printf("Access Granted\n");
  return 0;
}

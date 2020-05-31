# ReMe Part
## General information
You might have noticed that antivirus dosen't like the ReMe.dll. This already give a hint about the structure of the secound flag. After
the InitialCheck function of the first part there is a lot of quite complicted looking code. You might notice the `"THIS_IS_CSCG_NOT_A_MALWARE!"`
string here. If we run strings on the ReMe.dll file we see a lot of diffrent readable strings including the `"THIS_IS_CSCG_NOT_A_MALWARE!"` string,
however after that we only get short and non readable strings wich are probably false positives.

## Reversing
First we get the bytes of the InitialCheck function and store them in a byte array.
````
byte[] InitialCheckBytes = typeof(Program).GetMethod("InitialCheck", BindingFlags.Static | BindingFlags.NonPublic).GetMethodBody().GetILAsByteArray();
````
Then we read and store the complete current file (ReMe.dll) in a diffrent byte array.
````
byte[] fileBytes = File.ReadAllBytes(Assembly.GetExecutingAssembly().Location);
````
Now we get the position of the `"THIS_IS_CSCG_NOT_A_MALWARE!"` string inside the file and the copy all bytes after this string into a new array, 
using the follwing code.
````
int[] positions = fileBytes.Locate(Encoding.ASCII.GetBytes("THIS_IS_CSCG_NOT_A_MALWARE!"));
MemoryStream memoryStream = new MemoryStream(fileBytes);
memoryStream.Seek((long)(positions[0] + Encoding.ASCII.GetBytes("THIS_IS_CSCG_NOT_A_MALWARE!").Length), SeekOrigin.Begin);
byte[] encryptedCode = new byte[memoryStream.Length - memoryStream.Position];
memoryStream.Read(encryptedCode, 0, encryptedCode.Length);
````
The next line of code is long but we can break it down what it does. If we refactore it, it looks like this.
````
decryptedCode = Program.AES_Decrypt(encryptedCode, initialCheckBytes)
checkFunction = Assembly.Load(decryptedCode).GetTypes()[0].GetMethod("Check", BindingFlags.Static | BindingFlags.Public)

checkFunction.Invoke(null, new object[]
			{
				args
			});
````
First we decrypt the end of the file using the bytes of the initialCheck methode. We load the result as a new Programm and get a function
called Check from it. We then invoke that function with args as an argument.

So there is acctually a encrypted second program at the end of the file that is decrypted and run from the main methode of the first.
Maleware uses this trick to hide the payload, so the antivirus thought this is also a virus.

To get the check methode to reverse it we can patch the code in to write the decrypted bytes a file to disk, instead of loading it as
a assembly. We can open this file again with dnSpy and find a Check function inside the Inner class.

Here we split the secound argument at every `_` and check if the diffrent parts are correct. We can pice these checks together to get the parts 
`CSCG{n0w_u_know_st4t1c_and_` and
`_dotNet_R3333` of the flag.
The missing part of the flag is hashed using MD5 and compared to `b72f3bd391ba731a35708bfd8cd8a68f`. We have to bruteforce the hash to find
the missing part, but it's probaly not that long and complicated. We can use a side [crackstation](like https://crackstation.net/) to get
the result `dynamic`.

So your hole flag is CSCG{n0w_u_know_st4t1c_and_dynamic_dotNet_R3333}.

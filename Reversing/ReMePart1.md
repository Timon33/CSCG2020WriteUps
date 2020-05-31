# ReMe Part 1
## General information
Using the file command we can see that the main file of the challange is .Net assembly for Windows.
````
ReMe.dll: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows
````
That means reversing is quite easy because we can use a .net reflector like dnSpy to get the source code in a language like C#. This file 
contains both flags for part 1 and 2, so lets start with the first.

## Reversing
In Main we first call a function InitialCheck with args from main. Here we check some diffrent things, like if a Debugger is present, but
we can reverse this flag staticly so we don't need to worry about that. To get to the part of the code that prints the first flag we need to
pass the following check:
````
bool flag5 = args[0] != StringEncryption.Decrypt("D/T9XRgUcKDjgXEldEzeEsVjIcqUTl7047pPaw7DZ9I=");
			if (flag5)
			{
				Console.WriteLine("Nope");
				Environment.Exit(-1);
			}
			else
			{
				Console.WriteLine("There you go. Thats the first of the two flags! CSCG{{{0}}}", args[0]);
			}
````
So we have to know the result of the decrypt function given this encrypted string.

The hole Decrypt function looks like this.

````
public static string Decrypt(string cipherText)
		{
			string password = "A_Wise_Man_Once_Told_Me_Obfuscation_Is_Useless_Anyway";
			cipherText = cipherText.Replace(" ", "+");
			byte[] array = Convert.FromBase64String(cipherText);
			using (Aes aes = Aes.Create())
			{
				Rfc2898DeriveBytes rfc2898DeriveBytes = new Rfc2898DeriveBytes(password, new byte[]
				{
					73,
					118,
					97,
					110,
					32,
					77,
					101,
					100,
					118,
					101,
					100,
					101,
					118
				});
				aes.Key = rfc2898DeriveBytes.GetBytes(32);
				aes.IV = rfc2898DeriveBytes.GetBytes(16);
				using (MemoryStream memoryStream = new MemoryStream())
				{
					using (CryptoStream cryptoStream = new CryptoStream(memoryStream, aes.CreateDecryptor(), CryptoStreamMode.Write))
					{
						cryptoStream.Write(array, 0, array.Length);
						cryptoStream.Close();
					}
					cipherText = Encoding.Unicode.GetString(memoryStream.ToArray());
				}
			}
			return cipherText;
		}
````
As we can see we are delaing with AES. We can copy the function and the call to it and print the result. We execute it and get the output CanIHazFlag?. So your first flag is CSCG{CanIHazFlag?}.

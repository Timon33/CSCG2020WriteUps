#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <stdbool.h>

static const char alphabet[] =
"abcdefghijklmnopqrstuvwxyz"
"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"0123456789 !#$%&'()*+-./:;<=>?@";

static const int alphabetSize = sizeof(alphabet);

void algorithm(unsigned int s)
{	
	unsigned int prev = 0xffffffff;
	unsigned int temp = 0;

	for(int i = 0; i < 32; i++)
	{
		bool x = ((s >> i) & 1) == (prev & 1);

		prev = prev >> 1;

#ifdef DEBUG
		printf("shifted: %x\n", prev);
		printf("%d\n", (s >> i));
#endif
		if(!x)
		{
			prev = prev ^ 0xedb88320;
		}

#ifdef DEBUG
        printf("end: %x\n", prev);
#endif
	}

	if(prev == 0xf40e845e)
	{
		printf("result: %x\n", s);
	}
}

void bruteforce()
{
	for(int i = 0; i < alphabetSize; i++)
	{
		for(int j = 0; j < alphabetSize; j++)
		{
			for(int k = 0; k < alphabetSize; k++)
			{
				for(int l = 0; l < alphabetSize; l++)
				{
					int input = alphabet[i] | (alphabet[j] << 8) | (alphabet[k] << 16) | (alphabet[l] << 24);
					//printf("%x\n", input);
					algorithm(input);
				}
			}
		}
	}
}


int main(int argc, char *argv[])
{
	bruteforce();
}
#include <stdio.h>

struct arrWrap
{
	int arr[10];
};

struct arrWrap fun()
{
		struct arrWrap x;
		
		for(int i=0; i<10; i++)
		{
			x.arr[i] = i * 10;
		}
		
		return x;
}

int main()
{
	struct arrWrap x = fun();
	int i;
	
	for (i = 0; i < 10; i++)
	{
		printf("%d ", x.arr[i]);
	}
	printf("\n");
	return 0;

}
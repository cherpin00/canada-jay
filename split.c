#include <stdio.h>
 #include <string.h>
 #include <stdlib.h>
 #include <sys/stat.h>
 
long int get_file_size(FILE *fp){
		if (fp == NULL){
		printf("File could not be found");
		return(-1);
	}
	
	fseek(fp, 0L, SEEK_END);
	long int res = ftell(fp);
}
 
int main(int argc, char **argv)
{	
	int num_parts = 1;
	char input_stream[20];
	char str_1[30] = "split -b %d test";
	
	//this will be changed to be calculated from the amount of locations input
	printf("Input the number of parts: ");
	fgets(input_stream, 20, stdin);
	input_stream[strcspn(input_stream,"\n")] = 0;
	num_parts = atoi(input_stream);
	
	FILE *fp = fopen("test","r");
	int long res = get_file_size(fp);
	int remaining = res % num_parts;
	printf(" This is the file size %ld \n", res);
	fclose(fp);
	
	//If there is a remainder, I increase the bytes in each file by one
	int part_size = res/num_parts;
	if(remaining > 0){
		part_size++;
	}
	
	//This formats the string with the number for the system function
	char string_format_container[100];
	sprintf(string_format_container, str_1, part_size);
	printf("%s\n", string_format_container);
	
	//Linux has a command line function called split that splits the file for you if you specify the size. I call that here
	system(string_format_container);
	//once i create the files, I move them to their own locations
	system("mv xaa split1");
	system("mv xab split2");
	system("mv xac split3");
	//to recombine I use the system cat function
	system("cat split1/xaa split2/xab split3/xac > output_file.txt");
	return 0;
 }
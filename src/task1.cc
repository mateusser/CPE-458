#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <iostream>

#define BLOCKSIZE 4096

#define ERROR_DISK_NOT_FOUND -404

using namespace std;

/* This function opens a regular file and designates the first nBytes of it as space for the emulated disk.
 * nBytes should be an integral number of the block size. If nBytes > 0 and there is already a file by the given filename,
 * that file’s content may be overwritten. If nBytes is 0, an existing disk is opened, and should not be overwritten.
 * There is no requirement to maintain integrity of any file content beyond nBytes.
 * The return value is -1 on failure or a disk number on success.
 */
int mountDisk(char *filename, int nBytes);

/* This function unmounts the open disk (identified by ‘disk’). */
int unmountDisk(int disk);

/* readBlock() reads an entire block of BLOCKSIZE bytes from the open disk (identified by ‘disk’) and copies the result into a local buffer, 
 * block (which must be at least of BLOCKSIZE bytes). The bNum is a logical block number, 
 * which must be translated into a byte offset within the disk. The translation from logical to physical block is straightforward: 
 * bNum=0 is the very first byte of the file. bNum=1 is BLOCKSIZE bytes into the disk, bNum=n is n*BLOCKSIZE bytes into the disk. 
 * On success, it returns 0. -1 or smaller is returned if disk is not available (hasn’t been opened) or any other failures. 
 * readBlock will also perform the decryption operation. You should define your own error code system.
 */
int readBlock(int disk, int bNum, void *block);

/* writeBlock() takes disk number ‘disk’ and logical block number ‘bNum’ and encrypts and then 
 * writes the content of the buffer ‘block’ to that location. ‘block’ must be integral with BLOCKSIZE. Just as in readBlock(), 
 * writeBlock() must translate the logical block bNum to the correct byte position in the file. 
 * On success, it returns 0. -1 or smaller is returned if disk is not available (i.e. hasn’t been opened) or any other failures. 
 * You should define your own error code system.
 */
int writeBlock(int disk, int bNum, void *block);

vector<FILE *> disks;
int diskNumber = 0;

int main(int argc, char *argv[]){

	char *testBlock = (char *) calloc(BLOCKSIZE, sizeof(char));
	sprintf(testBlock, "Hello World!");
	char *output  = (char *) calloc(BLOCKSIZE, sizeof(char));

/*	cout << mountDisk("file1.dsk", 3) << endl;
	cout << writeBlock(0, 0, (void *) testBlock) << endl;
	cout << readBlock(0, 0, (void *) output) << endl;
	cout << output << endl;
	cout << unmountDisk(0) << endl;*/

	printf("Hello World!");

	free(testBlock);
	free(output);

	return 0;
}

int mountDisk(char *filename, int nBytes){
	FILE *fp = fopen(filename, "r+");

	if(fp == NULL || nBytes < 0)
		return -1;

	void *zeros = calloc(BLOCKSIZE, nBytes);

	fwrite(zeros, BLOCKSIZE, nBytes, fp);
	disks.push_back(fp);
	rewind(fp);

	free(zeros);

	return diskNumber++;
}

int unmountDisk(int disk){	
	if (disk >= disks.size()) {
		return ERROR_DISK_NOT_FOUND;
	}

	return fclose(disks[disk]);
}

int readBlock(int disk, int bNum, void *block){
		if (disk >= disks.size()) {
		return ERROR_DISK_NOT_FOUND;
	}

	FILE *fp = disks[disk];

	fseek(fp, bNum * BLOCKSIZE, SEEK_SET);
	fread(block, BLOCKSIZE, 1, fp);

	//TODO decrypt

	rewind(fp);

	return 0;
}

int writeBlock(int disk, int bNum, void *block){
	if (disk >= disks.size()) {
		return ERROR_DISK_NOT_FOUND;
	}

	FILE *fp = disks[disk];

	//TODO encrypt

	fseek(fp, bNum * BLOCKSIZE, SEEK_SET);
	fwrite(block, BLOCKSIZE, 1, fp);
	rewind(fp);

	return 0;
}

BIN=./bin/lab4
PATH=./src/

all: task1

task1: $(PATH)task1.cc
	@g++ -o $(BIN) $(PATH)task1.cc -lm -Wall

clean:
	@rm -rf bin
	@mkdir bin

run:
	@touch file1.dsk	
	@$(BIN)
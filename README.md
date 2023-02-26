# Batch processing with multiprogramming

This is a small program that simulates batch processing with multiprogramming (visual simulation only). Python 3.11.1 and Tkinter was used.

How does this work? The program creates a new batch with five processes by default. Each batch contains five processes (That's the configuration, that can change).

So now, two new functions were added in this program (since this is based on the program called "Batch Processing").

What are the functions?

* Interrupt button: This function interrupts a running process, then sends it to the end of that same batch to continue with another (This process can be executed again).
* Error button: This function terminates a running process (Terminated by error). First, the operation to be solved is automatically assigned the word "Error". After that, this is sent to the "Finished processes" screen to continue with another one.
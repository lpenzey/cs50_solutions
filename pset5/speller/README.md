# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

An invented word to denote a lung disease caused by breathing in very fine ash or dust. Also the longest word in our dictionary at 45 characters. 

## According to its man page, what does `getrusage` do?

Get resource usage: it returns resource usage measure for "get who" which is a;ways RUSAGE_SELF in speller.c This returns usage statistic such as the sum of resources used by all threads in the process. 

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

We do this becuase passing large structs by value is slow and memory intensive, potentially causing a stack overflow. 

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

`for (int c = fgetc(file); c != EOF; c = fgetc(file))`
The for loop above iterates through each character in the file by getting the next character using `fgetc(file)`. It means to get character from stream, the stream in this case being the file we're searching. It does this until the end of file (`c != EOF;`). 

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

It's important to use `fgetc` instead of `fscanf` because scanning for strings means you look for a whitespace to know where the word ends. Since some words end in punctuation (such as an apostrophe) it's better to scan by character. 

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

I think they were declared as constants so that they wouldn't be modified by our code. 

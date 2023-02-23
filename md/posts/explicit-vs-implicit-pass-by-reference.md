In programming, many of the online discussions involving the terms 'pass by reference' and 'pass by value' are muddy and silly.

Look at the utter confusion and miscommunication in this thread:
https://stackoverflow.com/questions/518000/is-javascript-a-pass-by-reference-or-pass-by-value-language/

You may be able to wade through the confusion and experimentally prove the behavior is as you expect, and that's great. But shouldn't we be able to communicate this sort of idea more clearly?

The people saying, "It's pass by value! It's just that the value is a reference!" clearly don't understand what is being asked.

The terms people should probably be using when asking this specific kind of question are 'explicit pass by reference' and 'implicit pass by reference'.

Pass by value is not special in any way, *it is the default*. It should be assumed. If I refer to a symbol, and the reference evaluates/collapses to the value associated with that symbol ... that's to be expected.

What the people asking these sorts of questions care about is when code looks like it could be either pass by value or pass by reference, depending on language specifics.
An ambiguity arises from switching between several programming languages and having to ask "If I pass this symbol into a new function/context/namespace, is the computer going to copy the value in memory that the symbol refers to into a new memory allocation isolated from the original (or at least function as if it had)? Or is the new local symbol going to simply point to the existing memory that the original symbol refers to, effectively aliasing/referencing/pointing to the original memory?"

A concrete code based example:
In C, there is no implicit pass by reference.
If you have a symbol 'a' and you call `f(a)`, that new function local symbol (whatever the parameter is named in the function definition, 'x' for example) will simply represent the primitive value of the symbol 'a' with no further connection to the previous symbol.
If 'a' represents an int that is set to 42 at the time of the call to 'f', then the new symbol will represent an allocation of memory 32 bits in size (on amd64) that is pre-set to 42 in binary (at some level; obviously there are levels where you could argue this is not what's "really" happening, but then again, most sequential programs are not "really" happening either because of out of order execution at the CPU level). If 'a' is a struct, an array, or a union etc., the new symbol will represent the value the original symbol represents at the time of the function call, just like with the int. This is because the language will implicitly copy the memory starting at the memory address of the struct the symbol represents until it reaches the memory address of pointer_value + sizeof(StructType). In both situations, a new memory allocation is performed (specifically on the stack) and the new symbol has no connection to what the original symbol represents after its initialization. Clearly, pass by value.
However, if you don't want to copy the entire arbitrary block of memory 'a' represents but merely refer to it, you can *explicitly* pass the underlying memory address associated with the symbol by referencing the symbol `f(&a)`. You then have to *explicitly* dereference the new symbol to refer to or mutate the value that the original symbol represented in the new function context `*x = 0`. Again, it is clearly pass by value (specifically a value of type 'size_t') because it is clear what value we are passing. What is happening is explicit in the notation of the code itself.

In other programming languages, what happens when passing a symbol into a new context is not as clear and is often not represented in the code itself at all.

In Python (I know because I just tested it), a simple int passed as a parameter will behave as it does in C: copy the memory into a new allocation isolated from the original. But, if I create a class with an int member and pass a symbol representing an instance of said class to a function as a parameter, Python, in terms of what C does, performs an *implicit* pass by reference and *implicitly* dereferences that reference when I try to refer to or mutate that new function local symbol.

This is the question people are really asking when they are asking if a particular programming language is "pass by value" or "pass by reference": "Is it like C where the computer will only act on the original memory when I explicitly instruct it to? Or is it like Python where the computer will act on the original memory implicitly?"

So, again, I think people should instead ask if the language in question is 'explicit pass by reference' or 'implicit pass by reference'.

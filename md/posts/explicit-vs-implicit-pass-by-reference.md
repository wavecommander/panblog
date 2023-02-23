% Explicit vs. Implicit 'Pass by reference'
22 Feb 2023
T3

# This sucks
# I don't recommend reading it
# It is so minute and lame
# I regret spending the time writing it
# It is truly 'Tier 3'

# Still here? Why?

In programming, many of the online discussions involving the terms 'pass by reference' and 'pass by value' are muddy and silly.

Look at the utter confusion and miscommunication in [this thread on StackOverflow](https://stackoverflow.com/questions/518000/is-javascript-a-pass-by-reference-or-pass-by-value-language/)

You may be able to wade through the confusion and experimentally prove the behavior is as you expect, and that's great.
But, shouldn't we be able to communicate this sort of idea more clearly?

The people saying, "It's pass by value! It's just that the value is a reference!" don't seem to understand what is being asked, or they do and are more concerned with being faithful to rigid definitions rather than have the other person understand what is going on.

The terms people should probably be using when asking this specific kind of question are '*explicit* pass by reference' and '*implicit* pass by reference'.

What the people asking these sorts of questions care about is when code looks like it could be either 'pass by value' or 'pass by reference', depending on language specifics which they are not familiar with (not the formal definition of 'pass by reference', but what they think it means which I am defining as '*implicit* pass by reference').

*I'm going to use the word 'symbol', but you can substitute it with 'identifier' if you like*

An ambiguity arises from switching between several programming languages and having to ask "If I pass this symbol into a new function/context/namespace, is the computer going to copy the value in memory that the symbol refers to into a new memory allocation isolated from the original (or at least function as if it had)? Or is the new local symbol going to simply point to the existing memory that the original symbol refers to, effectively aliasing/referencing/pointing to the original memory?"

## Concrete Examples

### C

This is going to be rather simplified as I am not a C language spec expert.

In C, by the terms I am trying to define, there is no *implicit* pass by reference.

If you have a symbol 'a' and you invoke `f(a)`, that new function local symbol ('x' in this example) will simply represent the same value that the symbol 'a' represents in the calling context at the time of the invocation with no further connection to the previous symbol.

```c
#include <stdio.h>

void f(int x) {
    x = 0;
}

int main() {
    int a = 42;
    printf("a: %d\n", a);

    f(a);
    printf("a: %d\n", a);
}
```
Output:
```
a: 42
a: 42
```

At the time of the call to `f(int)`, the new symbol 'x' represents a new stack allocation that is `sizeof(int)` words in size that is initialized to 42 in binary (at least at some level. Obviously there are levels where you could argue this is not what is "really" happening. Then again, most programs are not "really" happening as they are written because of compiler/interpreter optimizations and out of order execution at the CPU level).

If 'b' is a struct or a union, the new symbol will still represent the value the original symbol represents at the time of the function call just like with the `int`. This is because the language will implicitly copy the memory starting at the underlying memory address associated with the symbol until it reaches the memory address of `&b + sizeof(b)`.

```c
#include <stdio.h>

struct MyStruct {
    int a;
};

void f(struct MyStruct x) {
    x.a = 0;
}

int main() {
    struct MyStruct ms = {42};
    printf("ms.a: %d\n", ms.a);

    f(ms);
    printf("ms.a: %d\n", ms.a);
}
```
Output:
```
ms.a: 42
ms.a: 42
```

In both situations, a new stack allocation is performed and the new symbol has no connection to what the original symbol represents after its initialization. Clearly, pass by value.

However, if you don't want to copy the entire arbitrary block of memory the represents but merely refer to it, you can *explicitly* pass the underlying memory address associated with the symbol by referencing the symbol: `f(&a)`.

```c
#include <stdio.h>

void f(int *x) {
    *x = 0;
}

int main() {
    int a = 42;
    printf("a: %d\n", a);

    f(&a);
    printf("a: %d\n", a);
}
```
Output:
```
a: 42
a: 0
```

You then have to *explicitly* dereference the new symbol to refer to or mutate the value that the original symbol represented in the new function context: `*x = 0`. Again, it is clearly pass by value. And, it is *explicit* pass by reference because what value we are passing is clearly notated in the code itself.

The same is true if we modified the struct example above to *explictly* reference the struct represented by the symbol `ms`:

```c
#include <stdio.h>

struct MyStruct {
    int a;
};

void f(struct MyStruct *x) {
    x->a = 0;
}

int main() {
    struct MyStruct ms = {42};
    printf("ms.a: %d\n", ms.a);

    f(&ms);
    printf("ms.a: %d\n", ms.a);
}
```
Output:
```
ms.a: 42
ms.a: 0
```

The only place where it may be unclear for people learning C is when working with arrays.

#### Arrays

```c
#include <stdio.h>

void f(int arr[], int sz) {
    if (sz >= 1) {
        arr[0] = 0;
    }
}

int main() {
    int my_array[1] = {42};

    printf("my_array: %p\n", my_array);
    printf("my_array[0]: %d\n\n", my_array[0]);

    f(my_array, sizeof(my_array) / sizeof(int));

    printf("my_array: %p\n", my_array);
    printf("my_array[0]: %d\n\n", my_array[0]);

    printf("&(my_array[0]): %p\n", &(my_array[0]));
    printf("my_array == &(my_array[0]) : %s",
            my_array == &(my_array[0]) ? "True" : "False");
}
```

Output:
```
my_array: 0x16b246d1c
my_array[0]: 42

my_array: 0x16b246d1c
my_array[0]: 0

&(my_array[0]): 0x16b246d1c
my_array == &(my_array[0]) : True
```

It may look as though passing the symbol of an array as a function parameter should result in the value the symbol represents being copied into the new context, and it does. Those that are learning just need to learn that arrays are pointers and array access notation is an alternate way of pointer dereferencing.

This is still not *implicit* pass by reference by my definition because it is explicit in the notation that you are working with an array.

In other programming languages, what happens when passing a symbol into a new context is often not represented in the code notation itself at all.

### Python

In Python, a simple int passed as a parameter will behave as it does in C: copy the memory into a new allocation isolated from the original.

```python
def f(x: int):
    x = 0

a = 42
print(f'a: {a}')

f(a)
print(f'a: {a}')
```
Output:
```
a: 42
a: 42
```

But, if I create a class with an int member and pass a symbol representing an instance of said class to a function as a parameter, the original symbol now represents the value as it was mutated in the function context.

```python
class MyClass:
    def __init__(self, val: int):
        self.a = val

def f(x: MyClass):
    x.a = 0

mc = MyClass(42)
print(f'mc.a: {mc.a}')

f(mc)
print(f'mc.a: {mc.a}')
```
Output:
```
mc.a: 42
mc.a: 0
```

A similar behavior happens when applying this pattern to JavaScript objects.

Python (and JavaScript), in terms of what C does and my own terms, performs an *implicit* pass by reference and *implicitly* dereferences that reference when I try to refer to or mutate that new function local symbol.

This is the question people are really asking when they are asking if a particular programming language is 'pass by value' or 'pass by reference': "Is it like C where the computer will only act on the original memory when I explicitly instruct it to? Or is it like Python/JS where the computer will act on the original memory implicitly?"

Now, part of the allure of these languages is the simplicity that comes with not having to explicitly write what to do with a variable in terms of memory. And that's great. I definitely think that Python and JavaScript are fine for having made that design decision.

These language specifics are things that people will just have to learn when they are picking them up, but when using terms that describe multiple programming languages, it may be easier if we didn't use terms that only really apply to languages and paradigms that few people use anymore.

### Recommendation

Consider using *explicit* and *implicit* pass by reference in future discussions to avoid a quagmire of arguing over reified terms that are easily misunderstood by those that may be a bit newer.

# Now get off of this page and do something good

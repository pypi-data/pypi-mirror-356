# Python Optimizations

## [Optimized Scope](http://docs.python.org/3/glossary.html#term-optimized-scope)

A scope where target local variable names are reliably known to the compiler when the code is compiled, allowing
optimization of read and write access to these names. Note: most interpreter optimizations are
applied to all scopes, only those relying on a known set of local and nonlocal variable names are restricted to
optimized scopes.

The following local namespaces are optimized in this fashion:
- functions
- generators
- coroutines
- comprehensions
- generator expressions

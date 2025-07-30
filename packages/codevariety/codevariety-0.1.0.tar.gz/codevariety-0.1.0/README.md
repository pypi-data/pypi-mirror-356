# CodeVariety

This package contains several unrelated modules:
- SmartSet
- PRNG
- PySVN
- DebugTracer

## SmartSet
SmartSet is a hybrid data structure.
It contains these features:
- Performance close to a set
- All native set functions and operators
- Ability to sort data with .sort()
- Once the SmartSet is altered in any way after sorting, it resorts back to set-like behavior (unordered)
- Contains several math functions: .mean(), .sum(), .min(), .max(), and .normalize()
- '+' operator works same as '|' and .union() method

## Debug_Tracer
This is an easy-to-use debug tracer.
Simply put .start() before any function (main if the entire program), and .stop() at the end.
The output is color coded for good readability. 

## PRNG
This is a clone of the python random library.
It does not contain every feature, but it has some of the key features. 
Some of the features are:
- Produces random int or float
- Can provide upper and lower bounds for random numbers
- Produces random letters (upper and lower case)
- Has .shuffle() and .choice() functions

## pysvn
This is a small library (will expand in the future) for interacting with SVN via python.
It has the following functions:
- checkout()
- commit()
- export()
- log()

While the first three are straight forward in terms of their use, log() will return all files 
modified by a specified user on either a single date or a given date range.
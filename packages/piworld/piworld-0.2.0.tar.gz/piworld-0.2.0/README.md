# Welcome to PiWorld! (current version 0.2.0)

**PiWorld** is a small Python library (mainly intended as a personal project) which houses a couple pi-related commands.

Here, pi is stored as a **string** as an alternative to floating-point limits (where pi's value is only accurate up to the 15th decimal).

## Current Commands

The library currently has 8 commands:

- `pi10` → returns pi up to the 10th decimal  
- `pi20` → returns pi up to the 20th decimal  
- `pi50` → returns pi up to the 50th decimal  
- `pi100` → returns pi up to the 100th decimal  
- `pi200` → returns pi up to the 200th decimal  
- `pi500` → returns pi up to the 500th decimal
- `pidigit(n)` → returns the nth decimal of pi (if n == 0, the functions returns 3, for the digit before the decimals)
- `pislice(length, size)` → slices pi into a "length" sized string, then divides it into chunks with "size" characters

(More coming soon)

---

## Example Usage

The embedded constants can be used as follows:

```python
import piworld

print(piworld.pi10)   # Output: 3.1415926535
print(piworld.pi20)   # Output: 3.14159265358979323846
print(piworld.pi50)   # Output: 3.14159265358979323846264338327950288419716939937510
print(piworld.pi100)  # Output: 3.1415926535.....21170679
print(piworld.pi200)  # Output: 3.1415926535.....93038196
print(piworld.pi500)  # Output: 3.1415926535.....01194912
```

In addition to that, the two remaining functions work like so:

```python
from piworld import pidigit, pislice

"""pidigit(n) returns the nth digit of pi, unless n is 0, 
which returns 3 for the digit before the decimals instead"""

print(pidigit(0)) # returns 3
print(pidigit(1)) # returns 1
print(pidigit(2)) # returns 4
print(pidigit(3)) # returns 1
print(pidigit(4)) # returns 5

"""pislice(length, size) returns the decimals of pi up to the set 'length',
then chunks it into slices containing 'size' characters each
notice how when 'size' isn't divisible by 'length', the remaining digits are set at the end"""

print(pislice(10, 2)) # returns 14 14 92 65 35
print(pislice(15, 3)) # returns 141 592 653 589 793
print(pislice(18, 4)) # returns 1415 9265 3589 7932 38
print(pislice(23, 5)) # returns 14159 26535 89793 23846 264
```

---

## PiWorld GitHub Repository

Yo can find the GitHub repository for PiWorld over at https://github.com/seif-kz/piworld

---

## PLEASE NOTE

This is not meant to be a fully practical library with groundbreaking use —  
it is simply a fun little project serving as my own introduction to **PyPI** and **GitHub**.

This project might be getting some sparse updates here and there, but nothing major.

---

## Contact

TBA

~ Seif

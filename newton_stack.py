from fractions import Fraction
from operator import *
import math
import copy
import sys

def lsb(num, n=4):
	num = copy.deepcopy(num)
	bits = []
	b=Fraction(2)**Fraction(int(math.log2(num)))
	while b>(1/2**15) and num:
		q, num = divmod(num, b)
		bits += [q]
		b /= 2
	return int("".join(map(str, bits)).zfill(5)[-5:], 2)

def test_lsb():
	cases = [(2, 1), (7, 1), (1,8), (1,9), (1,7), (2801, 7)]
	for i in cases:
		print(str(i) + ": " + lsb(Fraction(*i)))

def run(code):
	stack = []
	pop = lambda: stack.pop() if stack else 0

	gen_op = lambda op, n=2: lambda: stack.append(op(*[pop() for i in range(n)]))

	commands = {
		10: pop, #pop
		11: lambda: stack.extend([pop()]*2), #duplicate
		12: lambda: stack.extend([pop(), pop()][::-1]), #swap
		13: lambda: stack.insert(0, pop()), #rotate
		14: lambda: stack.append(pop(0)), #unrotate
		15: stack.reverse, #reverse
		15: gen_op(add),
		16: gen_op(sub),
		17: gen_op(mul),
		18: gen_op(truediv),
		19: gen_op(pow),
		20: gen_op(mod),
		21: gen_op(lambda a: Fraction(math.log(a)), 1),
		22: gen_op(lambda a: Fraction(math.exp(a)), 1),
		23: gen_op(not_, 1),
		24: gen_op(lt),
		25: lambda: print(chr(int(pop()))),
		26: gen_op(lambda: "\n", 0),
		27: gen_op(lambda: " ", 0)
	}

	for radicand, tolerance, base in code:
		radicand, tolerance, base = Fraction(radicand), Fraction(tolerance), Fraction(base)
		x=radicand

		number = ""

		while abs(x*x - radicand) > tolerance:
			x-=(x**base-radicand)/(base*x**(base-1))
			command = lsb(x)

			print(x)
			print(command)

			if command < 10:
				number += str(command)
			else:
				if number:
					stack.append(Fraction(int(number)))
					number = []

				if command in commands:
					commands[command]()
	print(stack)
def main():
	with open(sys.argv[1]) as source:
		code = [i.split() for i in source.read().split("\n")][:-1]
		run(code)

if __name__=='__main__':
	main()

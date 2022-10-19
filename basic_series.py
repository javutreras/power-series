import math
from power_series import PowerSeries
from fractions import Fraction

def zero() -> PowerSeries:
    return PowerSeries(lambda n:0, order=None)

def geometric() -> PowerSeries:
    return PowerSeries(lambda n:1)

def exponential(a: int = 1) -> PowerSeries:
    return PowerSeries(lambda n: Fraction(a**n, math.factorial(n)))

def sine(a: int = 1) -> PowerSeries:
    return PowerSeries(lambda n: (1*(n%4==1)-1*(n%4==3))*Fraction(a**n, math.factorial(n)), order=1)

def cosine(a: int = 1) -> PowerSeries:
    return PowerSeries(lambda n: (1*(n%4==0)-1*(n%4==2))*Fraction(a**n, math.factorial(n)))

def sineh(a: int = 1) -> PowerSeries:
    return PowerSeries(lambda n: 1*(n%2==1)*Fraction(a**n, math.factorial(n)), order=1)

def cosineh(a: int = 1) -> PowerSeries:
    return PowerSeries(lambda n: 1*(n%2==0)*Fraction(a**n, math.factorial(n)))

def monomial(degree: int, coef :int = 1) -> PowerSeries:
    if coef == 0:
        return zero()
    return PowerSeries(lambda n: coef*(n==degree), order=degree)
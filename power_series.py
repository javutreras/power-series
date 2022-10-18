from fractions import Fraction
from typing import Callable


class PowerSeries:
    def __init__(self, coefs: Callable[[int], Fraction], order: int = 0) -> None:
        self.formula = coefs
        if not order or order >= 0:
            self.find_order()

    def coef(self, n: int) -> Fraction:
        """Return coefficient of z^n in power series expansion.

        Args:
            n (int): degree of target monomial.

        Returns:
            Fraction: coefficient of target monomial.
        """
        if self.order == None or n < self.order:
            return Fraction(0)
        else:
            return self.formula(n)

    def find_order(self) -> None:
        for i in range(11):
            if self.coef(i) != 0:
                self.order = i
                return
        self.order = None
        return

    def term(self, n: int) -> str:
        if n == 0:
            return '%s' % (self.coef(n),)
        elif n == 1:
            return '(%s)z' % (self.coef(n),)
        else:
            return '(%s)z^%s' % (self.coef(n), n)

    def print(self, length: int = 5) -> str:
        if not self.order:
            return '0'
        terms = [self.term(i + self.order)
                 for i in range(length) if self.coef(i + self.order) != 0]
        if not terms:
            return '0'
        else:
            return ' + '.join(terms)

    def negative(self) -> 'PowerSeries':
        """Obtain additive inverse of self.

        Returns:
            PowerSeries: self with changed sign.
        """
        return PowerSeries(lambda n: -self.coef(n), order=self.order)

    def plus(self, other: 'PowerSeries') -> 'PowerSeries':
        """Sum a given power series to self.

        Args:
            other (PowerSeries): power series to add.

        Returns:
            PowerSeries: self plus other.
        """
        if self.order == None:
            sum_order = other.order
        elif other.order == None:
            sum_order = self.order
        else:
            sum_order = min(self.order, other.order)
        return PowerSeries(lambda n: self.coef(n) + other.coef(n), order=sum_order)

    def minus(self, other: 'PowerSeries') -> 'PowerSeries':
        """Substract a given power series from self.

        Args:
            other (PowerSeries): power series to substract.

        Returns:
            PowerSeries: self minus other.
        """
        return self.plus(other.negative())

    def times_nth(self, other: 'PowerSeries', n: int) -> Fraction:
        """Return the coefficient of z^n in expansion of self*other.

        Args:
            other (PowerSeries): power series to multiply by.
            n (int): degree of target monomial.

        Returns:
            Fraction: coefficient of target monomial in product.
        """
        if self.order == None or other.order == None:
            return Fraction(0)
        terms = [self.coef(i) * other.coef(n-i)
                 for i in range(self.order, other.order + n + 1)]
        return sum(terms)

    def times(self, other: 'PowerSeries') -> 'PowerSeries':
        """Multiply a given power series with self.

        Args:
            other (PowerSeries): power seris to multiply.

        Returns:
            PowerSeries: self times other.
        """
        if self.order == None or other.order == None:
            return PowerSeries(lambda n: 0, order=None)
        return PowerSeries(lambda n: self.times_nth(other, n), order=self.order + other.order)

    def divide_nth(self, other: 'PowerSeries', n: int) -> 'PowerSeries':
        if other.order == None:
            raise ValueError('Division by zero')

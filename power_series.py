from fractions import Fraction
from typing import Callable


class PowerSeries:
    def __init__(self, coefficient_formula: Callable[[int], Fraction], order: int = 0) -> None:
        self.formula = coefficient_formula
        self.order = order
        if not self.order or self.order >= 0:
            self.get_order()

    def __call__(self, n: int) -> Fraction:
        """Return coefficient of z^n in power series expansion.

        Args:
            n (int): degree of target monomial.

        Returns:
            Fraction: coefficient of target monomial.
        """
        if self.order == None or n < self.order:
            return Fraction(0)
        else:
            return Fraction(self.formula(n))

    def get_order(self) -> None:
        for i in range(11):
            if self(i) != 0:
                self.order = i
                return
        self.order = None
        return

    def term(self, n: int) -> str:
        if n == 0:
            return '%s' % (self(n),)
        elif n == 1:
            return '(%s)z' % (self(n),)
        else:
            return '(%s)z^%s' % (self(n), n)

    def __str__(self, length: int = 5) -> str:
        if self.order == None:
            return '0'
        terms = [self.term(i + self.order)
                 for i in range(length) if self(i + self.order) != 0]
        if not terms:
            return '0'
        else:
            return ' + '.join(terms)

    def __neg__(self) -> 'PowerSeries':
        """Obtain additive inverse of self.

        Returns:
            PowerSeries: self with changed sign.
        """
        return PowerSeries(lambda n: -self(n), order=self.order)

    def __add__(self, other: 'PowerSeries') -> 'PowerSeries':
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
        return PowerSeries(lambda n: self(n) + other(n), order=sum_order)

    def __sub__(self, other: 'PowerSeries') -> 'PowerSeries':
        """Substract a given power series from self.

        Args:
            other (PowerSeries): power series to substract.

        Returns:
            PowerSeries: self minus other.
        """
        return self + (-other)

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
        terms = [self(i) * other(n-i)
                 for i in range(self.order, - other.order + n + 1)]
        return sum(terms)

    def __mul__(self, other: 'PowerSeries') -> 'PowerSeries':
        """Multiply a given power series with self.

        Args:
            other (PowerSeries): power seris to multiply.

        Returns:
            PowerSeries: self times other.
        """
        if self.order == None or other.order == None:
            return PowerSeries(lambda n: 0, order=None)
        return PowerSeries(lambda n: self.times_nth(other, n), order=self.order + other.order)

    def invertible_factor(self) -> 'PowerSeries':
        if self.order == None:
            raise ValueError('Zero not invertible')
        return self * PowerSeries(lambda n : 1*(n==-self.order), order=-self.order)

    def inverse_nth(self, n: int) -> Fraction:
        if self.order == None:
            raise ValueError('Division by zero')
        inv_factor = self.invertible_factor()
        if n == 0:
            return 1 / inv_factor(0)
        else:
            terms = [self.inverse_nth(i)*inv_factor(n-i) for i in range(n)]
            return - sum(terms) / inv_factor(0)

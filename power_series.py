from fractions import Fraction
from typing import Callable


class PowerSeries:
    """This class implements Laurent power series with rational coefficients.

    Each series Sigma(c_n*z^n) is represented by its coefficients function n -> c_n.
    The four basic arithmetic operations are supported between PowerSeries objects.
    A PowerSeries object can be called: Obj(n) returns the coefficient c_n as a Fraction object.
    The string representation of a PowerSeries, str(Obj), consists of the first self.length terms of the series as a text string.

    Args:
        coefficient_formula (Callable[[int], Fraction]): the function n -> c_n that defines the coefficients of the power series.
        order (int, optional): the order of the power series at zero. Defaults to 0. Is mandatory for series of negative order.

    Attributes:
        formula (Callable[[int], Fraction]): the function n -> c_n that defines the coefficients of the power series.
        order (int | None): the order of the power series at zero. The zero series has order None.
        length (int): the number of terms to output on the string representation of the series. Defaults of 5.

    Methods:
        set_length: change the value of self.length.
        get_order: internal - determine self.order during __init__.
        term: internal - build each term for string representation.
        times_nth: internal - build one term for multiplication of series.
        invertible_factor: internal - factor out powers of z to get an invertible series.
        inverse_nth: internal - build one term for computing inverse.
        inverse: return inverse power series.
    """
    def __init__(self, coefficient_formula: Callable[[int], Fraction], order: int = 0) -> None:
        self.formula = coefficient_formula
        self.order = order
        self.length = 5
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

    def set_length(self, n: int) -> None:
        """Set number of terms displayed when printing this power series. Default is 5.

        Args:
            n (int): number of terms to display.
        """
        self.length = n
        return

    def get_order(self) -> None:
        """Internal method to determine the order of the power series. After a number of zeroes (default: 11) it assumes the series is the zero series.
        """
        for i in range(11):
            if self(i) != 0:
                self.order = i
                return
        self.order = None
        return

    def term(self, n: int) -> str:
        """Return string of the form (c_n)z^n, the monomial of degree n in the series.

        Args:
            n (int): degree of the monomial.

        Returns:
            str: monomial as a string.
        """
        if n == 0:
            return '%s' % (self(n),)
        elif n == 1:
            return '(%s)z' % (self(n),)
        else:
            return '(%s)z^%s' % (self(n), n)

    def __str__(self) -> str:
        """Outputs first self.length terms of the power series as a string.

        Returns:
            str: first terms of the series.
        """
        if self.order == None:
            return '0'
        terms = [self.term(i + self.order)
                 for i in range(self.length) if self(i + self.order) != 0]
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
            other (PowerSeries): power series to multiply.

        Returns:
            PowerSeries: self times other.
        """
        if self.order == None or other.order == None:
            return PowerSeries(lambda n: 0, order=None)
        return PowerSeries(lambda n: self.times_nth(other, n), order=self.order + other.order)

    def invertible_factor(self) -> 'PowerSeries':
        """Returns series with the term z^(order) factored out; the invertible part of the preparation factorisation.

        Raises:
            ValueError: if the series is the zero series.

        Returns:
            PowerSeries: original series divided by z^(order).
        """
        if self.order == None:
            raise ValueError('Zero not invertible')
        return self * PowerSeries(lambda n : 1*(n==-self.order), order=-self.order)

    def inverse_nth(self, n: int) -> Fraction:
        """Returns nth coefficient of the inverse of series divided by z^(order). Internal method needed to compute the inverse.

        Args:
            n (int): degree of the monomial to which the target coefficient belongs.

        Raises:
            ValueError: if the series is the zero series.

        Returns:
            Fraction: coefficient of term of degree n of target series.
        """
        if self.order == None:
            raise ValueError('Division by zero')
        inv_factor = self.invertible_factor()
        if n == 0:
            return 1 / inv_factor(0)
        else:
            terms = [self.inverse_nth(i)*inv_factor(n-i) for i in range(n)]
            return - sum(terms) / inv_factor(0)
    
    def inverse(self) -> 'PowerSeries':
        """Returns the inverse of the power series.

        Raises:
            ValueError: if the series is the zero series.

        Returns:
            PowerSeries: inverse of the original series.
        """
        if self.order == None:
            raise ValueError('Division by zero')
        return PowerSeries(lambda n: self.inverse_nth(n)) * PowerSeries(lambda n:1*(n==-self.order), -self.order)
    
    def __truediv__(self, other: 'PowerSeries') -> 'PowerSeries':
        """Divide self by a given series.

        Args:
            other (PowerSeries): power series to divide by.

        Returns:
            PowerSeries: division of self by other.
        """
        return self * other.inverse()

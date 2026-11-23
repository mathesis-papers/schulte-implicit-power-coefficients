import json
from collections import defaultdict
from fractions import Fraction
from math import comb


def multiply(left, right, degree):
    product = [0] * (degree + 1)
    for left_degree, left_value in enumerate(left[:degree + 1]):
        for right_degree, right_value in enumerate(right[:degree - left_degree + 1]):
            product[left_degree + right_degree] += left_value * right_value
    return product


def reciprocal(series, degree):
    assert series[0] == 1
    result = [1] + [0] * degree
    for current_degree in range(1, degree + 1):
        result[current_degree] = -sum(
            series[index] * result[current_degree - index]
            for index in range(1, min(len(series) - 1, current_degree) + 1)
        )
    return result


def power(series, exponent, degree):
    if exponent < 0:
        return power(reciprocal(series, degree), -exponent, degree)
    result = [1] + [0] * degree
    base = series[:degree + 1]
    while exponent:
        if exponent % 2:
            result = multiply(result, base, degree)
        exponent //= 2
        if exponent:
            base = multiply(base, base, degree)
    return result


def native_series(arity_limit, parameter, degree):
    series = [1] + [0] * degree
    for current_degree in range(1, degree + 1):
        series[current_degree] = sum(
            power(series, step * parameter, current_degree - step)[current_degree - step]
            for step in range(1, min(arity_limit, current_degree) + 1)
        )
    return series


def generalized_binomial(upper, lower):
    if lower < 0:
        return 0
    if upper >= 0:
        return comb(upper, lower) if lower <= upper else 0
    return (-1) ** lower * comb(lower - upper - 1, lower)


def polynomial_coefficient(arity_limit, exponent, degree):
    return power([1] * (arity_limit + 1), exponent, degree)[degree]


def alternating_coefficient(arity_limit, exponent, degree):
    assert arity_limit in (2, 3)
    return sum(
        (-(arity_limit - 1)) ** index * generalized_binomial(exponent, index)
        * generalized_binomial(arity_limit * exponent - 2 * index, degree - index)
        for index in range(degree + 1)
    )


def coefficient_formula(arity_limit, parameter, exponent, degree):
    if degree == 0:
        return Fraction(1)
    total = parameter * degree + exponent
    series_power = power([1] * (arity_limit + 1), total - 1, degree - 1)
    derivative = list(range(1, arity_limit + 1))
    return Fraction(exponent, degree) * multiply(derivative, series_power, degree - 1)[degree - 1]


def logarithm(series, degree):
    derivative = [(index + 1) * series[index + 1] for index in range(degree)]
    quotient = multiply(derivative, reciprocal(series, degree - 1), degree - 1)
    return [Fraction(0)] + [Fraction(quotient[index - 1], index) for index in range(1, degree + 1)]


def compose(series, argument, degree):
    result = [0] * (degree + 1)
    for coefficient in reversed(series[:degree + 1]):
        result = multiply(result, argument, degree)
        result[0] += coefficient
    return result


def paths(arity_limit, parameter, roots, degree):
    length = parameter * degree + roots - 1
    counts = {roots - 1: 1}
    for current_step in range(length):
        following = defaultdict(int)
        remaining = length - current_step - 1
        for height, count in counts.items():
            for step_type in range(arity_limit + 1):
                next_height = height + parameter * step_type - 1
                if 0 <= next_height <= remaining:
                    following[next_height] += count
        counts = following
    return counts.get(0, 0)


def binomial_square_log(series, first_parameter, second_parameter, degree):
    result = [Fraction(0)] * (degree + 1)
    for outer in range(1, degree + 1):
        for inner in range(min(outer, degree - outer) + 1):
            shift = outer + inner
            coefficients = power(series, first_parameter * outer + second_parameter * inner, degree - shift)
            for index, value in enumerate(coefficients):
                result[shift + index] += Fraction(comb(outer, inner) ** 2 * value, outer)
    return result


def adjacent_binomial_log(series, degree):
    result = [Fraction(0)] * (degree + 1)
    for outer in range(1, degree // 2 + 1):
        base = multiply(power(series, outer, degree - 2 * outer),
                        power([1, -1], -2 * outer, degree - 2 * outer), degree - 2 * outer)
        for inner in range(min(outer - 1, degree - 2 * outer) + 1):
            shift = 2 * outer + inner
            for index, value in enumerate(base[:degree - shift + 1]):
                result[shift + index] += Fraction(comb(outer - 1, inner) * comb(outer, inner) * value, outer)
    return result


def main():
    counts = defaultdict(int)
    for arity_limit in (2, 3):
        for parameter in range(9):
            series = native_series(arity_limit, parameter, 18)
            for exponent in range(1, 8):
                coefficients = power(series, exponent, 18)
                for degree in range(19):
                    total = parameter * degree + exponent
                    direct = polynomial_coefficient(arity_limit, total, degree)
                    assert direct == alternating_coefficient(arity_limit, total, degree)
                    assert coefficients[degree] == Fraction(exponent * direct, total)
                    counts['positive_power_coefficients'] += 1
            if parameter:
                coefficients = logarithm(series, 18)
                for degree in range(1, 19):
                    assert coefficients[degree] == Fraction(polynomial_coefficient(arity_limit, parameter * degree, degree), parameter * degree)
                    counts['positive_logarithmic_coefficients'] += 1
            for lower_parameter in range(parameter + 1):
                argument = [0] + power(series, parameter - lower_parameter, 17)
                lower_series = native_series(arity_limit, lower_parameter, 18)
                assert compose(lower_series, argument, 18) == series
                counts['positive_composition_identities'] += 1
        for parameter in range(1, 5):
            series = native_series(arity_limit, parameter, 8)
            for roots in range(1, 6):
                coefficients = power(series, roots, 8)
                for degree in range(9):
                    assert paths(arity_limit, parameter, roots, degree) == coefficients[degree]
                    counts['positive_path_counts'] += 1
    for exponent in range(31):
        for degree in range(3 * exponent + 5):
            assert polynomial_coefficient(3, exponent, degree) == alternating_coefficient(3, exponent, degree)
            counts['quadrinomial_coefficients'] += 1
    for parameter in range(9):
        coefficients = native_series(3, parameter, 5)
        expected = [1, 1, parameter + 1,
                    Fraction(3 * parameter ** 2 + 5 * parameter + 2, 2),
                    Fraction(8 * parameter ** 3 + 18 * parameter ** 2 + 13 * parameter, 3),
                    Fraction(125 * parameter ** 4 + 350 * parameter ** 3 + 355 * parameter ** 2 + 34 * parameter, 24)]
        assert coefficients == expected
        counts['quadrinomial_row_polynomials'] += 6
        coefficients = native_series(2, parameter, 5)
        expected = [1, 1, parameter + 1,
                    Fraction(parameter * (3 * parameter + 5), 2),
                    Fraction(parameter * (8 * parameter ** 2 + 18 * parameter + 1), 3),
                    Fraction(parameter * (125 * parameter ** 3 + 350 * parameter ** 2 + 55 * parameter - 26), 24)]
        assert coefficients == expected
        counts['trinomial_row_polynomials'] += 6
    for arity_limit in range(1, 7):
        for parameter in range(-3, 4):
            series = native_series(arity_limit, parameter, 12)
            for exponent in range(-4, 5):
                coefficients = power(series, exponent, 12)
                for degree in range(13):
                    assert coefficients[degree] == coefficient_formula(arity_limit, parameter, exponent, degree)
                    counts['integer_parameter_coefficients'] += 1
                    if degree:
                        total = parameter * degree + exponent
                        if total:
                            assert coefficients[degree] == Fraction(exponent, total) * polynomial_coefficient(arity_limit, total, degree)
                            if arity_limit in (2, 3):
                                assert coefficients[degree] == Fraction(exponent, total) * alternating_coefficient(arity_limit, total, degree)
                                counts['signed_alternating_coefficients'] += 1
                        else:
                            expected = Fraction(exponent, degree) * (1 - (arity_limit + 1) * (degree % (arity_limit + 1) == 0))
                            assert coefficients[degree] == expected
                            counts['zero_denominator_coefficients'] += 1
            log_series = logarithm(series, 12)
            for degree in range(1, 13):
                if parameter:
                    expected = Fraction(polynomial_coefficient(arity_limit, parameter * degree, degree), parameter * degree)
                else:
                    expected = Fraction(1 - (arity_limit + 1) * (degree % (arity_limit + 1) == 0), degree)
                assert log_series[degree] == expected
                counts['integer_logarithmic_coefficients'] += 1
            for lower_parameter in range(-3, 4):
                argument = [0] + power(series, parameter - lower_parameter, 11)
                lower_series = native_series(arity_limit, lower_parameter, 12)
                assert compose(lower_series, argument, 12) == series
                counts['integer_composition_identities'] += 1
            inverse_argument = [0] + power([1] * (arity_limit + 1), -parameter, 11)
            assert compose(series, inverse_argument, 12) == [1] * (arity_limit + 1) + [0] * (12 - arity_limit)
            counts['reversion_identities'] += 1
        for parameter in range(1, 4):
            series = native_series(arity_limit, parameter, 6)
            for roots in range(1, 4):
                coefficients = power(series, roots, 6)
                for degree in range(7):
                    assert paths(arity_limit, parameter, roots, degree) == coefficients[degree]
                    counts['general_arity_path_counts'] += 1
    for parameter in range(-2, 6):
        series = native_series(3, parameter, 12)
        assert binomial_square_log(series, parameter - 1, parameter, 12) == logarithm(series, 12)
        counts['hanna_binomial_square_logarithms'] += 12
    for first_parameter in range(-2, 4):
        for second_parameter in range(-2, 4):
            exponents = (first_parameter + 1,
                         first_parameter + second_parameter + 1,
                         2 * first_parameter + second_parameter + 2)
            series = [1] + [0] * 12
            for degree in range(1, 13):
                series[degree] = sum(
                    power(series, exponent, degree - shift)[degree - shift]
                    for shift, exponent in enumerate(exponents, start=1) if shift <= degree
                )
            assert binomial_square_log(series, first_parameter, second_parameter, 12) == logarithm(series, 12)
            counts['hanna_two_parameter_logarithms'] += 12
    series = native_series(3, 1, 12)
    expected = logarithm(multiply([1, -1], series, 12), 12)
    assert adjacent_binomial_log(series, 12) == expected
    counts['hanna_adjacent_binomial_logarithms'] += 12
    for first in range(9):
        for second in range(9):
            numerator = [comb(first, index) * comb(second, index) for index in range(min(first, second) + 1)]
            expanded = multiply(numerator, power([1, -1], -(first + second + 1), 18), 18)
            for degree in range(19):
                assert expanded[degree] == comb(first + degree, degree) * comb(second + degree, degree)
                counts['binomial_product_transform'] += 1
    for exponent in range(21):
        row = power([1, 1, 1, 1], exponent, 3 * exponent + 4)
        assert sum(row) == 4 ** exponent
        if exponent:
            assert sum((-1) ** degree * value for degree, value in enumerate(row)) == 0
        assert row[:3 * exponent + 1] == list(reversed(row[:3 * exponent + 1]))
        assert all(value > 0 for value in row[:3 * exponent + 1])
        counts['quadrinomial_row_properties'] += 1
        for degree, value in enumerate(row):
            positive = sum(generalized_binomial(exponent, index) * generalized_binomial(exponent, degree - 2 * index)
                           for index in range(degree // 2 + 1))
            assert value == positive
            counts['quadrinomial_positive_sum'] += 1
            if exponent:
                inclusion = sum((-1) ** index * generalized_binomial(exponent, index)
                                * generalized_binomial(exponent + degree - 4 * index - 1, degree - 4 * index)
                                for index in range(degree // 4 + 1))
                assert value == inclusion
                counts['quadrinomial_inclusion_exclusion'] += 1
    for arity_limit in range(1, 7):
        for parameter in range(1, 5):
            degree = 16
            native = native_series(arity_limit, parameter, degree)
            root = [0] * (degree + 1)
            for index in range((degree - 1) // parameter + 1):
                root[1 + parameter * index] = native[index]
            polynomial_argument = [0] * (degree + 1)
            for index in range(min(arity_limit, degree // parameter) + 1):
                polynomial_argument[parameter * index] = 1
            inverse_argument = [0] + reciprocal(polynomial_argument, degree - 1)
            identity = [0, 1] + [0] * (degree - 1)
            assert compose(root, inverse_argument, degree) == identity
            assert compose(inverse_argument, root, degree) == identity
            counts['sparse_reversion_identities'] += 1
    assert native_series(3, -1, 4) == [1, 1, 0, 0, -1]
    counts['negative_parameter_example'] += 1
    print(json.dumps({
        'status': 'pass', 'arithmetic': 'exact integers and rational numbers',
        'coverage': dict(sorted(counts.items())), 'total_comparisons': sum(counts.values()),
        'ranges': {
            'positive_power_coefficients': 'd=2,3; n=0..8; m=1..7; k=0..18',
            'positive_logarithmic_coefficients': 'd=2,3; n=1..8; k=1..18',
            'positive_path_counts': 'd=2,3; n=1..4; m=1..5; k=0..8',
            'positive_composition_identities': 'd=2,3; 0<=a<=n<=8; degrees 0..18',
            'quadrinomial_coefficients': 'N=0..30; k=0..3N+4',
            'quadrinomial_row_polynomials': 'n=0..8; k=0..5',
            'trinomial_row_polynomials': 'n=0..8; k=0..5',
            'integer_parameter_coefficients': 'd=1..6; n=-3..3; m=-4..4; k=0..12',
            'signed_alternating_coefficients': 'd=2,3; n=-3..3; m=-4..4; k=1..12; nk+m!=0',
            'zero_denominator_coefficients': 'd=1..6; n=-3..3; m=-4..4; k=1..12; nk+m=0',
            'integer_logarithmic_coefficients': 'd=1..6; n=-3..3; k=1..12',
            'integer_composition_identities': 'd=1..6; n,a=-3..3; degrees 0..12',
            'reversion_identities': 'd=1..6; n=-3..3; degrees 0..12',
            'general_arity_path_counts': 'd=1..6; n,m=1..3; k=0..6',
            'hanna_binomial_square_logarithms': 'd=3; n=-2..5; k=1..12',
            'hanna_adjacent_binomial_logarithms': 'd=3; n=1; k=1..12',
            'hanna_two_parameter_logarithms': 'p,q=-2..3; k=1..12',
            'binomial_product_transform': 'a,b=0..8; degrees 0..18',
            'quadrinomial_row_properties': 'N=0..20; support, positivity, symmetry and evaluations at 1,-1',
            'quadrinomial_positive_sum': 'N=0..20; k=0..3N+4',
            'quadrinomial_inclusion_exclusion': 'N=1..20; k=0..3N+4',
            'sparse_reversion_identities': 'd=1..6; n=1..4; both compositions through degree 16',
            'negative_parameter_example': 'd=3; n=-1; degrees 0..4',
        },
        'interpretation': 'Finite comparisons supplement the written proofs of the all-index identities.',
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

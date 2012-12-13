# test_nielsen.py - unit tests for nielsen.py
#
# Copyright 2012 Jeffrey Finkelstein
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for the :mod:`nielsen` module.

.. codeauthor:: Jeffrey Finkelstein <jeffrey.finkelstein@gmail.com>

"""
from nielsen import FreeGroup
from nielsen import freely_reduced
from nielsen import halves
from nielsen import strip_identities
from nielsen import Word


def test_repr():
    q = Word('q')
    assert 'q' in repr(q)
    F = FreeGroup({q}, q)
    assert 'q' in repr(F)


def test_equality():
    assert Word('a') == Word('a')
    assert Word('a') != Word('b')


def test_add():
    assert Word('a') + Word('a') == Word(['a', 'a'])
    assert Word('a') + Word('b') + Word('a') == Word(['a', 'b', 'a'])


def test_length():
    assert len(Word('a')) == 1
    assert len(Word('a') + Word('b')) == 2


def test_identity():
    generators = frozenset(Word(c) for c in 'abe')
    identity = Word('e')
    F = FreeGroup(generators, identity)
    assert identity == F.inverse(identity)


def test_strip_identities():
    generators = frozenset(Word(c) for c in 'abe')
    e = identity = Word('e')
    F = FreeGroup(generators, identity)
    a = Word('a')
    b = Word('b')
    assert strip_identities(F, e) == e
    assert strip_identities(F, e + e + e) == e
    assert strip_identities(F, a + e) == a
    assert strip_identities(F, a + e + e) == a
    assert strip_identities(F, e + a + e) == a
    assert strip_identities(F, e + a + e + b) == a + b


def test_freely_reduced():
    generators = frozenset(Word(c) for c in 'abcde')
    e = identity = Word('e')
    F = FreeGroup(generators, identity)
    a = Word('a')
    b = Word('b')
    a_inv = F.inverse(a)
    b_inv = F.inverse(b)
    assert freely_reduced(F, a + a_inv) == identity
    assert freely_reduced(F, a + b + b_inv + a_inv) == identity
    assert freely_reduced(F, a + a + b + b_inv + a_inv) == a
    assert freely_reduced(F, a + e + b) == a + b


def test_missing_identity():
    generators = frozenset(Word(c) for c in 'abcd')
    e = identity = Word('e')
    F = FreeGroup(generators, identity)
    assert e == F.identity
    assert F.inverse(e) == e


def test_inverse():
    a, b, c, e = (Word(c) for c in 'abce')
    F = FreeGroup({a, b, c, e}, e)
    abc = a + b + c
    abc_inv = F.inverse(abc)
    assert freely_reduced(F, abc + abc_inv) == e


def test_power():
    a, b, c, e = (Word(c) for c in 'abce')
    F = FreeGroup({a, b, c, e}, e)
    for x in (a, b, c, e):
        assert F.power(x, 0) == e
        assert F.power(x, 1) == x
        assert freely_reduced(F, x + F.power(x, -1)) == e
        assert F.power(x, 2) == x + x
        assert F.power(x, 3) == x + x + x


def test_starts_and_ends_with():
    a, b, c = (Word(c) for c in 'abc')
    abc = a + b + c
    assert abc.startswith(a + b)
    assert not abc.endswith(a + b)
    assert abc.endswith(b + c)
    assert not abc.startswith(b + c)


def test_halves():
    a, b = Word('a'), Word('b')
    ab, ba = a + b, b + a
    l, r = halves(ab + ba)
    assert l == ab
    assert r == ba


def test_nielsen_reduced():
    a, b, c, d, e = (Word(c) for c in 'abcde')
    F = FreeGroup({a, b, c, d, e}, e)
    # TODO Here put some example set, U, with a known Nielsen reduced form, V.
    #U = {a + b + c, a + F.inverse(b) + c + F.inverse(b), c + c + F.inverse(a)}
    #V = nielsen_reduced(F, U)
    #assert generates(V, U)

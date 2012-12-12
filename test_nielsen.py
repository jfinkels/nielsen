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
from nielsen import strip_identities
from nielsen import Word


def test_equality():
    assert Word('a') == Word('a')
    assert Word('a') != Word('b')


def test_add():
    assert Word('a') + Word('a') == Word(['a', 'a'])
    assert Word('a') + Word('b') + Word('a') == Word(['a', 'b', 'a'])


def test_length():
    generators = frozenset(Word(c) for c in 'abe')
    identity = Word('e')
    F = FreeGroup(generators, identity)
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

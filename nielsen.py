# nielsen.py - implementation of the Nielsen reduction for free groups
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
"""Provides an implementation of the Nielsen reduction for free groups.

The implementation is adapted from the pseudocode given in `The Nielsen
Reduction and P-Complete Problems in Free Groups`__.

.. codeauthor:: Jeffrey Finkelstein <jeffrey.finkelstein@gmail.com>

.. nielsen_: http://dx.doi.org/10.1016/0304-3975(84)90024-0

__ nielsen_

"""
from functools import reduce
import itertools
import operator as op


class FreeGroup:
    """Represents a free group on a finite set of generators.

    Words in the free group are given as instances of :class:`Word`.

    """

    def __init__(self, generators, identity):
        """Creates a new free group on the specified set of generators.

        `generators` must be a :class:`frozenset` of instances of
        :class:`Word`, each having length one.

        `identity` is the instance of :class:`Word`, again of length one, which
        represents the identity in this free group. If `identity` is not
        already in `generators`, it will be added in this object's
        representation of the set of generators.

        This constructor generates new :class:`Word` instances, each of length
        one, which represent the inverses of `generators`, so do not include
        the inverses of `generators` in that set. These inverses are available
        using the :meth:`inverses` and :meth:`inverse` methods.

        """
        self.generators = generators
        self._identity = identity
        if self._identity not in self.generators:
            self.generators |= frozenset((self._identity, ))
        self._generate_inverses()
        self._generators_by_label = {x.label: x for x in self._inverses}

    def __repr__(self):
        return '<Group {}>'.format(repr(self.generators))

    def _generate_inverses(self):
        """Creates one group element for each inverse and assigns mappings from
        group elements to their inverses in the :attr:`_inverses` dictionary.

        """
        # First, create a new element which represents the inverse of each
        # element in the group.
        self._inverses = {x: Word(x.label + '^{-1}') for x in self.generators}
        # Next, force the inverse of the identity to be itself.
        self._inverses[self._identity] = self._identity
        # Finally, ensure that each of the inverses map to their inverses as
        # well.
        self._inverses.update({v: k for k, v in self._inverses.items()})

    @property
    def identity(self):
        """Returns the identity element of this group as an instance of
        :class:`Word` of length one.

        """
        return self._identity

    # @property
    # def inverses(self):
    #     """Returns the mapping from group elements to their inverses."""
    #     return self._inverses

    def inverse(self, word):
        """Returns the inverse of `word` as an instance of :class:`Word`."""
        if len(word) == 1:
            return self._inverses[word]
        return sum(self.inverse(self._generators_by_label[x.label])
                   for x in reversed(word))

    def power(self, word, exp):
        """Returns the :class:`Word` which results from raising `word` to the
        `exp` power.

        """
        if exp < 0:
            return self.power(self.inverse(word), -exp)
        if exp == 0:
            return self.identity
        if exp == 1:
            return word
        half = exp // 2
        return self.power(word, half) + self.power(word, exp - half)


class Word:
    """Represents a (not necessarily freely reduced) word in a free group.

    Instances of this class are immutable.

    The free group structure is given entirely by an instance of
    :class:`FreeGroup` which contains the underlying set of the free group
    (given as words of length one) and the corresponding inverses.

    The word which an instance of this class represents is not necessarily
    freely reduced, so its representation may contain adjacent inverses.

    This class overrides the :meth:`__eq__` and :meth:`__ne__` comparisons so
    that

        Word('a') + Word('b') == Word('a') + Word('b')

    """

    def __init__(self, label):
        """Instantiates a new element of a free group with the specified
        identifying label.

        `label` must be a :class:`str` or :class:`unicode`. The label for each
        element in a group must be unique.

        """
        if isinstance(label, list):
            self._word = label
        else:
            self._word = [label]

    def __repr__(self):
        return '<Word {}>'.format(repr(self._word))

    def __str__(self):
        return '<Word {}>'.format(str(self._word))

    def __add__(self, other):
        """Returns the concatenation of this word with `other`.

        No cancellation of adjacent inverses is performed in this method; for
        such functionality, see :func:`freely_reduced`.

        """
        return Word(self._word + other._word)

    def __eq__(self, other):
        return self._word == other._word

    def __ne__(self, other):
        return self._word != other._word

    def __hash__(self):
        return hash(''.join(self._word))

    def __len__(self):
        return len(self._word)

    def __getitem__(self, key):
        return Word(self._word[key])

    def __iter__(self):
        return iter(Word(c) for c in self._word)

    def __reversed__(self):
        return reversed(self._word)

    @property
    def label(self):
        """Returns the string representation of this word.

        This raises an :exc:`Exception` if the length of this word is not one.

        """
        if len(self._word) != 1:
            raise Exception
        return self._word[0]

    def startswith(self, prefix):
        """Returns ``True`` if and only if `prefix` is a prefix of this word.

        """
        return ''.join(self._word).startswith(prefix)

    def endswith(self, suffix):
        """Returns ``True`` if and only if `suffix` is a suffix of this word.

        """
        return ''.join(self._word).endswith(suffix)


def halves(word):
    """Returns the pair containing the :class:`Word` instances which result
    from splitting `word` at its midpoint.

    Pre-condition: the length of `word` must be even.

    """
    midpoint = len(word) // 2
    return (word[:midpoint], word[midpoint:])
    

def strip_identities(F, word):
    """Returns a new word equivalent to `word` but with superfluous identities
    removed.

    If the word equals the identity, the identity in `F` will be returned.

    """
    new_symbols = reduce(op.add, (c for c in word if c != F.identity))
    if len(new_symbols) == 0:
        return F.identity
    print('returning', new_symbols)
    return new_symbols


# TODO the reference for this is String matching and algorithmic problems in
# free groups by J. Avenhaus and K. Madlener in Revista Colombiana de
# Matematicas, Volume 14, Issue 1, 1980:
# http://www.scm.org.co/aplicaciones/revista/revistas.php?modulo=MasInformacion&ver=412
#
# That reference has a more efficient algorithm, but it is hard to obtain.
def freely_reduced(F, word):
    """Returns a new :class:`Word` instance which represents the freely reduced
    word which is equivalent to `word` in the free group `F`.

    In the free group *F* we have that for every word *w* there is a unique
    freely reduced word *v* such that *w* is equivalent to *v* (in the sense of
    cancelling adjacent inverses).

    """
    modified = True
    while modified:
        modified = False
        for i in range(len(word) - 1):
            if F.inverse(word[i]) == word[i + 1]:
                word = word[:i] + word[i + 2:]
                modified = True
                break
    if len(word) == 0:
        return F.identity
    return strip_identities(F, word)


def nielsen_reduced(F, U):
    """Returns a set *V* such that the subgroup generated by *U* equals the
    subgroup generated by *V* (that is *<U> = <V>*) and *V* is Nielsen-reduced.

    `F` is an instance of :class:`FreeGroup` and `U` is an iterable of
    instances of :class:`Word` in the given free group.

    Pre-condition: at least one of the elements in `U` is not the identity of
    the free group `F`.

    Implementation note: this function computes the Nielsen reduction of `U` by
    adapting the implementation given in `The Nielsen Reduction and P-Complete
    Problems in Free Groups`__.

    .. nielsen_: http://dx.doi.org/10.1016/0304-3975(84)90024-0

    __ nielsen_

    """
    # Phase 1: eliminate words which are equivalent to the identity, then take
    # only the shorter of each word and its inverse.
    #
    # The set `V` will eventually contain the Nielsen reduced set, and it will
    # be returned at the end of this function.
    V = {min(v, F.inverse(v), key=lambda w: len(w))
         for v in (freely_reduced(u) for u in U) if v != F.identity}
    found_half = True
    while found_half:
        found_half = False
        # Phase 2: eliminate words when the concatenation of the word with
        # another yields a word which is equivalent to a shorter word,
        # including the inverses of either the left or right word.
        found_shorter = True
        while found_shorter:
            found_shorter = False
            # Iterate over each pair of distinct words and each combination of
            # inverses of those words.
            for u_i, u_j in itertools.permutations(V, 2):
                for e_i, e_j in itertools.product((1, -1), repeat=2):
                    # If the freely reduced concatenation is shorter than the
                    # left word, replace the longer word with the shorter one.
                    v = freely_reduced(F.power(u_i, e_i) + F.power(u_j, e_j))
                    if len(v) < len(u_i):
                        found_shorter = True
                        V.remove(u_i)
                        if v != F.identity:
                            V.add(min(v, F.inverse(v)))
        # Phase 3: find the shortest string u_j which can be decomposed into a
        # prefix and suffix of equal length which can be described by a
        # concatenation of shorter strings.
        #
        # TODO transform this code into a min() statement somehow?
        (u_j, u_k, p, p_inv, c, c_inv) = (None, ) * 6
        for u_j_candidate in V:
            # Since we are looking for the word u_j with the shortest length,
            # ignore any candidates which are larger than the current shortest
            # u_j.
            if u_j is not None and len(u_j_candidate) > len(u_j):
                continue
            # Also ignore words which do not have even length.
            if len(u_j_candidate) % 2 != 0:
                continue
            # Split the word into two halves, p and q.
            p_candidate, q_inv = halves(u_j_candidate)
            q = F.inverse(q_inv)
            for u_k_candidate in (w for w in V if w != u_j_candidate):
                # If another word u_k in V starts with q or ends with
                # inverse(q), store the current candidate u_j, along with some
                # extra information needed for after the loop over candidates
                # for u_j.
                if u_k_candidate.startswith(q):
                    u_j = u_j_candidate
                    u_k = u_k_candidate
                    p = p_candidate
                    p_inv = F.inverse(p)
                    c_inv = u_k_candidate[len(q):]
                    c = F.inverse(c_inv)
                    break
                elif u_k_candidate.endswith(q_inv):
                    u_j = u_j_candidate
                    u_k = u_k_candidate
                    p = p_candidate
                    p_inv = F.inverse(p)
                    c = u_k_candidate[:-len(q_inv)]
                    c_inv = F.inverse(c)
                    break
        # If `u_j` has been set, then so have `p`, `c`, and `c_inv`. In this
        # case we can replace `u_k` with a shorter string. We set `found_half`
        # to `True` because Phase 2 must run again, since the change we make
        # here may cause `V` to violate one of the properties required of
        # a Nielsen reduced set.
        #
        # In the case that no word `u_j` exists which satisfies the properties
        # in the previous loop, we exit from the main loop and return from the
        # function.
        if u_j is not None:
            found_half = True
            V.remove(u_k)
            V.add(min(p + c_inv, c + p_inv))
    return V

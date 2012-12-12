# Nielsen transformation for free groups #

This package contains an implementation of both free groups and the Nielsen
transformation.

## Copyright license ##

Copyright 2012 Jeffrey Finkelstein.

The code in this package is licensed under the GNU GPL version 3 or later. For
more information, see `LICENSE`.

## Installing ##

This application requires [Python][0] version 3 or later.

[0]: http://www.python.org/

## Testing ##

Running the unit tests requires [nose][1]. To install `nose`, run

    pip install nose

[1]: https://nose.readthedocs.org/en/latest/

## Using ##

Here is an example of creating and using words in a free group; words you
create must have string labels of length one:

    >>> from nielsen import Word
    >>> a = Word('a')
    >>> b = Word('b')
    >>> ab = a + b
    >>> ab
    <Word ['a', 'b']>
    >>> ab + ab
    <Word ['a', 'b', 'a', 'b']>

Words with the same component compare equal if they consist of the same
generators in the same order:

    >>> from nielsen import Word
    >>> Word('a') == Word('b')
    False
    >>> Word('a') + Word('b') == Word('a') + Word('b')
    True

Here is an example of creating and using a free group:

    >>> from nielsen import Word
    >>> from nielsen import FreeGroup
    >>> a, b, e = (Word(c) for c in 'abe')
    >>> # Here, the word "e" represents the identity in the free group.
    ... F = FreeGroup({a, b, e}, e)
    >>> F
    <Group {<Word ['a']>, <Word ['b']>, <Word ['e']>}>
    >>> F.identity
    <Word ['e']>
    >>> # Inverses are created for each of the generators
    ... F.inverse(a)
    <Word ['a^{-1}']>
    >>> # Concatenating words does not automatically cancel adjacent inverses
    ... a + b + F.inverse(b) + F.inverse(a)
    <Word ['a', 'b', 'b^{-1}', 'a^{-1}']>

Here is an example of computing the freely reduced word which is equivalent to
a given word:

    >>> from nielsen import Word
    >>> from nielsen import FreeGroup
    >>> from nielsen import freely_reduced
    >>> a, b, e = (Word(c) for c in 'abe')
    >>> F = FreeGroup({a, b, e}, e)
    >>> word = a + b + F.inverse(b) + F.inverse(a)
    >>> word
    <Word ['a', 'b', 'b^{-1}', 'a^{-1}']>
    >>> freely_reduced(F, word)
    <Word ['e']>
    >>> word = a + a + F.inverse(a) + b
    >>> word
    <Word ['a', 'a', 'a^{-1}', 'b']>
    >>> freely_reduced(F, word)
    <Word ['a', 'b']>

Here is an example of computing the Nielsen transformation of a set of words:

    TODO fill me in

## Contact ##

Jeffrey Finkelstein <jeffrey.finkelstein@gmail.com>

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : kv.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 01/19/2018
#
# Qinsheng Zhang modified based on Jacinle.
# Distributed under terms of the MIT license.

from jammy.utils.context import EmptyContext


class KVStoreBase:
    """The base class for all key-value stores."""

    def __init__(self, readonly: bool = False):
        """Initialize the KVStore.

        Args:
            readonly: If True, the KVStore is readonly.
        """
        self.__readonly = readonly

    @property
    def readonly(self):
        """Whether the KVStore is readonly."""
        return self.__readonly

    def has(self, key, **kwargs):
        return self._has(key, **kwargs)

    def get(self, key, default=None, **kwargs):
        return self._get(key, default=default, **kwargs)

    def put(self, key, value, replace: bool = True, **kwargs):
        """Put the value of the key. If the key already exists, the value will be replaced if replace is True.

        Args:
            key: the key.
            value: the value.
            replace: whether to replace the value if the key already exists.
        """
        assert not self.readonly, "KVStore is readonly: {}.".format(self)
        return self._put(key, value, replace=replace, **kwargs)

    def update(self, key, value, **kwargs):
        """Update the value of the key. If the key does not exist, the value will be put.

        Args:
            key: the key.
            value: the value.
        """
        kwargs["replace"] = True
        self.put(key, value, **kwargs)

    def erase(self, key, **kwargs):
        """Erase the key from the KVStore.

        Args:
            key: the key.
        """
        assert not self.readonly, "KVStore is readonly: {}.".format(self)
        return self._erase(key, **kwargs)

    def transaction(self, *args, **kwargs):
        """Create a transaction context."""
        return self._transaction(*args, **kwargs)

    def __contains__(self, key):
        return self.has(key)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)  # pylint: disable=no-member

    def __delitem__(self, key):
        return self.erase(key)

    def keys(self):
        return self._keys()

    def _has(self, key):
        raise NotImplementedError(
            "KVStore {} does not support has.".format(self.__class__.__name__)
        )

    def _get(self, key, default):
        raise NotImplementedError(
            "KVStore {} does not support get.".format(self.__class__.__name__)
        )

    def _put(self, key, value, replace):
        raise NotImplementedError(
            "KVStore {} does not support put.".format(self.__class__.__name__)
        )

    def _erase(self, key):
        raise NotImplementedError(
            "KVStore {} does not support erase.".format(self.__class__.__name__)
        )

    def _transaction(
        self, *args, **kwargs
    ):  # pylint: disable=unused-argument,no-self-use
        return EmptyContext()

    def _keys(self):
        raise NotImplementedError(
            "KVStore {} does not support keys access.".format(self.__class__.__name__)
        )

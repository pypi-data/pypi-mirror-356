# ===----------------------------------------------------------------------=== #
# Copyright (c) 2025, Modular Inc. All rights reserved.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions:
# https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===----------------------------------------------------------------------=== #
"""Utility classes for using objects as keys in data structures."""

from collections.abc import MutableMapping, MutableSet


# From https://stackoverflow.com/questions/16994307/identityset-in-python
class IdentitySet(MutableSet):
    """Set that uses object `id` as keys to support unhashable types."""

    def __init__(self, iterable=()):
        self.map = {}  # id -> object
        self |= iterable  # add elements from iterable to the set (union)

    def __len__(self):
        return len(self.map)

    def __iter__(self):
        return iter(self.map.values())

    def __contains__(self, x):
        return id(x) in self.map

    def add(self, value):
        """Add an element."""
        self.map[id(value)] = value

    def discard(self, value):
        """Remove an element.  Do not raise an exception if absent."""
        self.map.pop(id(value), None)

    def __repr__(self):
        if not self:
            return f"{self.__class__.__name__}()"
        return f"{self.__class__.__name__}({list(self)!r})"


class IdentityMap(MutableMapping):
    """Map that uses object `id` as keys to support unhashable types."""

    def __init__(self):
        self.key_map = {}  # id -> object
        self.value_map = {}  # id -> Value

    def __getitem__(self, key):
        return self.value_map[id(key)]

    def __setitem__(self, key, value):
        self.key_map[id(key)] = key
        self.value_map[id(key)] = value

    def __delitem__(self, key):
        del self.key_map[id(key)]
        del self.value_map[id(key)]

    def __iter__(self):
        return iter(self.key_map.values())

    def __len__(self):
        return len(self.key_map)

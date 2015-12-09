# Fork: https://github.com/fabioz/u-msgpack-python
#
# u-msgpack-python v1.6 - vsergeev at gmail
# https://github.com/vsergeev/u-msgpack-python
#
# u-msgpack-python is a lightweight MessagePack serializer and deserializer
# module, compatible with both Python 2 and 3, as well CPython and PyPy
# implementations of Python. u-msgpack-python is fully compliant with the
# latest MessagePack specification.com/msgpack/msgpack/blob/master/spec.md). In
# particular, it supports the new binary, UTF-8 string, and application ext
# types.
#
# MIT License
#
# Copyright (c) 2013-2014 Ivan A. Sergeev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""
u-msgpack-python v1.6 - vsergeev at gmail
https://github.com/vsergeev/u-msgpack-python

u-msgpack-python is a lightweight MessagePack serializer and deserializer
module, compatible with both Python 2 and 3, as well CPython and PyPy
implementations of Python. u-msgpack-python is fully compliant with the
latest MessagePack specification.com/msgpack/msgpack/blob/master/spec.md). In
particular, it supports the new binary, UTF-8 string, and application ext
types.

License: MIT
"""

# Changes on 1.6.1 by Fabio Zadrozny: Did a number of performance enhancements.
version = (1, 6, 1)
"Module version tuple"

import struct
import sys


_struct_unpack = struct.unpack
_struct_pack = struct.pack

_PY2 = sys.version_info[0] < 3
_IS_PY3 = not _PY2

try:
    xrange
except NameError:
    xrange = range  # @ReservedAssignment

if _IS_PY3:
    _byte_type = bytes
    def _as_bytes(b):
        if b.__class__ == str:
            return b.encode('utf-8')
        return b

else:
    _byte_type = str
    
    def _as_bytes(b):
        if b.__class__ == unicode:
            return b.encode('utf-8')
        return b

################################################################################

# Extension type for application-specific types and data
class Ext:
    """
    The Ext class facilitates creating a serializable extension object to store
    an application-specific type and data byte array.
    """

    def __init__(self, type, data):
        """
        Construct a new Ext object.

        Args:
            type: application-specific type integer from 0 to 127
            data: application-specific data byte array

        Raises:
            TypeError:
                Specified ext type is outside of 0 to 127 range.

        Example:
        >>> foo = umsgpack_s.Ext(0x05, b"\x01\x02\x03")
        >>> umsgpack_s.packb({u"special stuff": foo, u"awesome": True})
        '\x82\xa7awesome\xc3\xadspecial stuff\xc7\x03\x05\x01\x02\x03'
        >>> bar = umsgpack_s.unpackb(_)
        >>> print(bar["special stuff"])
        Ext Object (Type: 0x05, Data: 01 02 03)
        >>>
        """
        # Application ext type should be 0 <= type <= 127
        if not type.__class__ == int or not (type >= 0 and type <= 127):
            raise TypeError("ext type out of range")

        # Check data is type bytes
        elif _IS_PY3 and not data.__class__ == bytes:
            raise TypeError("ext data is not type \'bytes\'")

        elif not _IS_PY3 and not data.__class__ == str:
            raise TypeError("ext data is not type \'str\'")

        self.type = type
        self.data = data

    def __eq__(self, other):
        """
        Compare this Ext object with another for equality.
        """
        return (isinstance(other, self.__class__) and
                self.type == other.type and
                self.data == other.data)

    def __ne__(self, other):
        """
        Compare this Ext object with another for inequality.
        """
        return not self.__eq__(other)

    def __str__(self):
        """
        String representation of this Ext object.
        """
        s = "Ext Object (Type: 0x%02x, Data: " % self.type
        for i in xrange(min(len(self.data), 8)):
            if i > 0:
                s += " "
            if isinstance(self.data[i], int):
                s += "%02x" % (self.data[i])
            else:
                s += "%02x" % ord(self.data[i])
        if len(self.data) > 8:
            s += " ..."
        s += ")"
        return s

################################################################################

# Base Exception classes
class PackException(Exception):
    "Base class for exceptions encountered during packing."
    pass
class UnpackException(Exception):
    "Base class for exceptions encountered during unpacking."
    pass

# Packing error
class UnsupportedTypeException(PackException):
    "Object type not supported for packing."
    pass

# Unpacking error
class InsufficientDataException(UnpackException):
    "Insufficient data to unpack the encoded object."
    pass
class InvalidStringException(UnpackException):
    "Invalid UTF-8 string encountered during unpacking."
    pass
class ReservedCodeException(UnpackException):
    "Reserved code encountered during unpacking."
    pass
class UnhashableKeyException(UnpackException):
    """
    Unhashable key encountered during map unpacking.
    The serialized map cannot be deserialized into a Python dictionary.
    """
    pass
class DuplicateKeyException(UnpackException):
    "Duplicate key encountered during map unpacking."
    pass

# Backwards compatibility
KeyNotPrimitiveException = UnhashableKeyException
KeyDuplicateException = DuplicateKeyException

################################################################################

# You may notice _struct_pack("B", x) instead of the simpler chr(x) in the code
# below. This is to allow for seamless Python 2 and 3 compatibility, as chr(x)
# has a str return type instead of bytes in Python 3, and _struct_pack(...) has
# the right return type in both versions.

def _pack_integer(x, write):
    if x < 0:
        if x >= -32:
            write(_struct_pack("b", x))
        elif x >= -2 ** (8 - 1):
            write(b"\xd0")
            write(_struct_pack("b", x))
        elif x >= -2 ** (16 - 1):
            write(b"\xd1")
            write(_struct_pack(">h", x))
        elif x >= -2 ** (32 - 1):
            write(b"\xd2")
            write(_struct_pack(">i", x))
        elif x >= -2 ** (64 - 1):
            write(b"\xd3")
            write(_struct_pack(">q", x))
        else:
            raise UnsupportedTypeException("huge signed int")
    else:
        if x <= 127:
            write(_struct_pack("B", x))
        elif x <= 2 ** 8 - 1:
            write(b"\xcc")
            write(_struct_pack("B", x))
        elif x <= 2 ** 16 - 1:
            write(b"\xcd")
            write(_struct_pack(">H", x))
        elif x <= 2 ** 32 - 1:
            write(b"\xce")
            write(_struct_pack(">I", x))
        elif x <= 2 ** 64 - 1:
            write(b"\xcf")
            write(_struct_pack(">Q", x))
        else:
            raise UnsupportedTypeException("huge unsigned int")

def _pack_nil(x, write):
    write(b"\xc0")

def _pack_boolean(x, write):
    write(b"\xc3" if x else b"\xc2")

# Auto-detect system float precision
if sys.float_info.mant_dig == 53:
    _float_size = 64

    def _pack_float(x, write):
        write(b"\xcb")
        write(_struct_pack(">d", x))
else:
    _float_size = 32

    def _pack_float(x, write):
        write(b"\xca")
        write(_struct_pack(">f", x))

def _pack_string(x, write):
    x = x.encode('utf-8')
    sz = len(x)

    if sz <= 31:
        write(_struct_pack("B", 0xa0 | sz))
        write(x)
    elif sz <= 2 ** 8 - 1:
        write(b"\xd9")
        write(_struct_pack("B", sz))
        write(x)
    elif sz <= 2 ** 16 - 1:
        write(b"\xda")
        write(_struct_pack(">H", sz))
        write(x)
    elif sz <= 2 ** 32 - 1:
        write(b"\xdb")
        write(_struct_pack(">I", sz))
        write(x)
    else:
        raise UnsupportedTypeException("huge string")

def _pack_binary(x, write):
    sz = len(x)
    if sz <= 2 ** 8 - 1:
        write(b"\xc4")
        write(_struct_pack("B", sz))
        write(x)
    elif sz <= 2 ** 16 - 1:
        write(b"\xc5")
        write(_struct_pack(">H", sz))
        write(x)
    elif sz <= 2 ** 32 - 1:
        write(b"\xc6")
        write(_struct_pack(">I", sz))
        write(x)
    else:
        raise UnsupportedTypeException("huge binary string")


def _pack_ext(x, write):
    sz = len(x.data)

    if sz == 1:
        write(b"\xd4")
        write(_struct_pack("B", x.type & 0xff))
        write(x.data)
    elif sz == 2:
        write(b"\xd5")
        write(_struct_pack("B", x.type & 0xff))
        write(x.data)
    elif sz == 4:
        write(b"\xd6")
        write(_struct_pack("B", x.type & 0xff))
        write(x.data)
    elif sz == 8:
        write(b"\xd7")
        write(_struct_pack("B", x.type & 0xff))
        write(x.data)
    elif sz == 16:
        write(b"\xd8")
        write(_struct_pack("B", x.type & 0xff))
        write(x.data)
    elif sz <= 2 ** 8 - 1:
        write(b"\xc7")
        write(_struct_pack("BB", sz, x.type & 0xff))
        write(x.data)
    elif sz <= 2 ** 16 - 1:
        write(b"\xc8")
        write(_struct_pack(">HB", sz, x.type & 0xff))
        write(x.data)
    elif sz <= 2 ** 32 - 1:
        write(b"\xc9")
        write(_struct_pack(">IB", sz, x.type & 0xff))
        write(x.data)
    else:
        raise UnsupportedTypeException("huge ext data")

def _pack_array(arr, write):
    sz = len(arr)

    if sz <= 15:
        write(_struct_pack("B", 0x90 | sz))
    elif sz <= 2 ** 16 - 1:
        write(b"\xdc")
        write(_struct_pack(">H", sz))
    elif sz <= 2 ** 32 - 1:
        write(b"\xdd")
        write(_struct_pack(">I", sz))
    else:
        raise UnsupportedTypeException("huge array")

    get = _pack_dispatch.__getitem__
    for x in arr:
        get(x.__class__)(x, write)

def _pack_array_(x, write):
    sz = len(x)

    if sz <= 15:
        write(_struct_pack("B", 0x90 | sz))
    elif sz <= 2 ** 16 - 1:
        write(b"\xdc")
        write(_struct_pack(">H", sz))
    elif sz <= 2 ** 32 - 1:
        write(b"\xdd")
        write(_struct_pack(">I", sz))
    else:
        raise UnsupportedTypeException("huge array")

    get = _pack_dispatch.__getitem__
    for e in x:
        get(e.__class__)(e, write)


if _IS_PY3:

    def _pack_map(x, write):
        sz = len(x)

        if sz <= 15:
            write(_struct_pack("B", 0x80 | sz))
        elif sz <= 2 ** 16 - 1:
            write(b"\xde")
            write(_struct_pack(">H", sz))
        elif sz <= 2 ** 32 - 1:
            write(b"\xdf")
            write(_struct_pack(">I", sz))
        else:
            raise UnsupportedTypeException("huge array")

        get = _pack_dispatch.__getitem__
        for k, v in x.items():
            get(k.__class__)(k, write)
            get(v.__class__)(v, write)
else:
    def _pack_map(x, write):
        sz = len(x)

        if sz <= 15:
            write(_struct_pack("B", 0x80 | sz))
        elif sz <= 2 ** 16 - 1:
            write(b"\xde")
            write(_struct_pack(">H", sz))
        elif sz <= 2 ** 32 - 1:
            write(b"\xdf")
            write(_struct_pack(">I", sz))
        else:
            raise UnsupportedTypeException("huge array")

        get = _pack_dispatch.__getitem__
        for k, v in x.iteritems():  # The only difference from the PY3 version is iteritems().
            get(k.__class__)(k, write)
            get(v.__class__)(v, write)


def packb(x):
    """
    Serialize a Python object into MessagePack bytes.

    Args:
        x: Python object

    Returns:
        A 'str' or 'bytes' containing the serialized bytes (depending on python version).

    Raises:
        UnsupportedType(PackException):
            Object type not supported for packing.

    Example:
    >>> umsgpack_s._packb({u"compact": True, u"schema": 0})
    '\x82\xa7compact\xc3\xa6schema\x00'
    >>>
    """

    # This is slower on py2.7 and 3.3 (on windows)
    # b = _BytesIO()
    # _packb(x, b.write)
    # return b.getvalue()

    lst = []
    try:
        _pack_dispatch[x.__class__](x, lst.append)
    except KeyError:
        raise UnsupportedTypeException("unsupported type: %s, %r" % (str(type(x)), x))
    return b''.join(lst)



################################################################################

def _unpack_integer(code, read_fn):
    if (ord(code) & 0xe0) == 0xe0:
        return _struct_unpack("b", code)[0]
    elif code == b'\xd0':
        return _struct_unpack("b", read_fn(1))[0]
    elif code == b'\xd1':
        return _struct_unpack(">h", read_fn(2))[0]
    elif code == b'\xd2':
        return _struct_unpack(">i", read_fn(4))[0]
    elif code == b'\xd3':
        return _struct_unpack(">q", read_fn(8))[0]
    elif (ord(code) & 0x80) == 0x00:
        return _struct_unpack("B", code)[0]
    elif code == b'\xcc':
        return _struct_unpack("B", read_fn(1))[0]
    elif code == b'\xcd':
        return _struct_unpack(">H", read_fn(2))[0]
    elif code == b'\xce':
        return _struct_unpack(">I", read_fn(4))[0]
    elif code == b'\xcf':
        return _struct_unpack(">Q", read_fn(8))[0]
    raise Exception("logic error, not int: 0x%02x" % ord(code))

def _unpack_reserved(code, read_fn):
    if code == b'\xc1':
        raise ReservedCodeException("encountered reserved code: 0x%02x" % ord(code))
    raise Exception("logic error, not reserved code: 0x%02x" % ord(code))

def _unpack_nil(code, read_fn):
    if code == b'\xc0':
        return None
    raise Exception("logic error, not nil: 0x%02x" % ord(code))

def _unpack_boolean(code, read_fn):
    if code == b'\xc2':
        return False
    elif code == b'\xc3':
        return True
    raise Exception("logic error, not boolean: 0x%02x" % ord(code))

def _unpack_float(code, read_fn):
    if code == b'\xca':
        return _struct_unpack(">f", read_fn(4))[0]
    elif code == b'\xcb':
        return _struct_unpack(">d", read_fn(8))[0]
    raise Exception("logic error, not float: 0x%02x" % ord(code))

def _unpack_string(code, read_fn):
    if (ord(code) & 0xe0) == 0xa0:
        length = ord(code) & ~0xe0
    elif code == b'\xd9':
        length = _struct_unpack("B", read_fn(1))[0]
    elif code == b'\xda':
        length = _struct_unpack(">H", read_fn(2))[0]
    elif code == b'\xdb':
        length = _struct_unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not string: 0x%02x" % ord(code))

    try:
        return bytes.decode(read_fn(length), 'utf-8')
    except UnicodeDecodeError:
        raise InvalidStringException("unpacked string is not utf-8")

def _unpack_binary(code, read_fn):
    if code == b'\xc4':
        length = _struct_unpack("B", read_fn(1))[0]
    elif code == b'\xc5':
        length = _struct_unpack(">H", read_fn(2))[0]
    elif code == b'\xc6':
        length = _struct_unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not binary: 0x%02x" % ord(code))

    return read_fn(length)

def _unpack_ext(code, read_fn):
    if code == b'\xd4':
        length = 1
    elif code == b'\xd5':
        length = 2
    elif code == b'\xd6':
        length = 4
    elif code == b'\xd7':
        length = 8
    elif code == b'\xd8':
        length = 16
    elif code == b'\xc7':
        length = _struct_unpack("B", read_fn(1))[0]
    elif code == b'\xc8':
        length = _struct_unpack(">H", read_fn(2))[0]
    elif code == b'\xc9':
        length = _struct_unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not ext: 0x%02x" % ord(code))

    return Ext(ord(read_fn(1)), read_fn(length))

def _unpack_array(code, read_fn):
    if (ord(code) & 0xf0) == 0x90:
        length = (ord(code) & ~0xf0)
    elif code == b'\xdc':
        length = _struct_unpack(">H", read_fn(2))[0]
    elif code == b'\xdd':
        length = _struct_unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not array: 0x%02x" % ord(code))


    # The code below was: return [_unpackb(read_fn) for _i in xrange(length)]
    # On Py 2.7 the code below was around 7% faster (mostly inlining some things).
    ret = []
    get = _unpack_dispatch_table.__getitem__
    append = ret.append
    while length > 0:
        length -= 1
        code = read_fn(1)
        append(get(code)(code, read_fn))
    return ret

def _unpack_map(code, read_fn):
    if (ord(code) & 0xf0) == 0x80:
        length = (ord(code) & ~0xf0)
    elif code == b'\xde':
        length = _struct_unpack(">H", read_fn(2))[0]
    elif code == b'\xdf':
        length = _struct_unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not map: 0x%02x" % ord(code))

    get = _unpack_dispatch_table.__getitem__

    d = {}
    setitem = d.__setitem__
    while length > 0:
        length -= 1
        key_code = read_fn(1)
        k = get(key_code)(key_code, read_fn)

        val_code = read_fn(1)
        setitem(k, get(val_code)(val_code, read_fn))
    return d

########################################
def _byte_reader(s):
    i = [0]
    len_s = len(s)
    def read_fn(n):
        j = i[0]
        if j + n > len_s:
            raise InsufficientDataException()
        substring = s[j:j + n]
        i[0] = j + n
        return substring
    return read_fn

def _unpackb(read_fn):
    code = read_fn(1)
    return _unpack_dispatch_table[code](code, read_fn)


def unpackb(s):
    """
    Deserialize MessagePack bytes into a Python object.

    Args:
        s: a 'str' containing the MessagePack serialized bytes in Py 2 or 'bytes' in Py3.

    Returns:
        A deserialized Python object.

    Raises:
        TypeError:
            Packed data is not type 'str'.
        InsufficientDataException(UnpackException):
            Insufficient data to unpack the encoded object.
        InvalidStringException(UnpackException):
            Invalid UTF-8 string encountered during unpacking.
        ReservedCodeException(UnpackException):
            Reserved code encountered during unpacking.
        UnhashableKeyException(UnpackException):
            Unhashable key encountered during map unpacking.
            The serialized map cannot be deserialized into a Python dictionary.
        DuplicateKeyException(UnpackException):
            Duplicate key encountered during map unpacking.

    Example:
    >>> umsgpack_s.unpackb(b'\x82\xa7compact\xc3\xa6schema\x00')
    {u'compact': True, u'schema': 0}
    >>>
    """
    if s.__class__ != _byte_type:
        raise TypeError("packed data is not type '%s'" % (_byte_type,))
    read_fn = _byte_reader(s)
    return _unpackb(read_fn)


loads = unpackb
dumps = packb

# Dispatch table built in __init for fast lookup of unpacking function.
_unpack_dispatch_table = {}

# Dispatch table built in __init for fast lookup of packing function.
_pack_dispatch = {}

################################################################################

def __init():

    # Fix uint
    for code in xrange(0, 0x7f + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_integer
    # Fix map
    for code in xrange(0x80, 0x8f + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_map
    # Fix array
    for code in xrange(0x90, 0x9f + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_array
    # Fix str
    for code in xrange(0xa0, 0xbf + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_string
    # Nil
    _unpack_dispatch_table[b'\xc0'] = _unpack_nil
    # Reserved
    _unpack_dispatch_table[b'\xc1'] = _unpack_reserved
    # Boolean
    _unpack_dispatch_table[b'\xc2'] = _unpack_boolean
    _unpack_dispatch_table[b'\xc3'] = _unpack_boolean
    # Bin
    for code in xrange(0xc4, 0xc6 + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_binary
    # Ext
    for code in xrange(0xc7, 0xc9 + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_ext
    # Float
    _unpack_dispatch_table[b'\xca'] = _unpack_float
    _unpack_dispatch_table[b'\xcb'] = _unpack_float
    # Uint
    for code in xrange(0xcc, 0xcf + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_integer
    # Int
    for code in xrange(0xd0, 0xd3 + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_integer
    # Fixext
    for code in xrange(0xd4, 0xd8 + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_ext
    # String
    for code in xrange(0xd9, 0xdb + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_string
    # Array
    _unpack_dispatch_table[b'\xdc'] = _unpack_array
    _unpack_dispatch_table[b'\xdd'] = _unpack_array
    # Map
    _unpack_dispatch_table[b'\xde'] = _unpack_map
    _unpack_dispatch_table[b'\xdf'] = _unpack_map
    # Negative fixint
    for code in xrange(0xe0, 0xff + 1):
        _unpack_dispatch_table[_struct_pack("B", code)] = _unpack_integer

    if not _IS_PY3:
        _pack_dispatch.update({
            bool: _pack_boolean,
            int:_pack_integer,
            long:_pack_integer,
            float: _pack_float,
            unicode: _pack_string,
            str:_pack_binary,
            list:_pack_array,
            tuple:_pack_array,
            dict:_pack_map,
            Ext:_pack_ext,
            None.__class__:_pack_nil
        })

    else:
        _pack_dispatch.update({
            bool: _pack_boolean,
            int:_pack_integer,
            float: _pack_float,
            str:_pack_string,
            bytes:_pack_binary,
            list:_pack_array,
            tuple:_pack_array,
            dict:_pack_map,
            Ext:_pack_ext,
            None.__class__:_pack_nil
        })


__init()

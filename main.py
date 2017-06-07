# coding: utf-8

from __future__ import absolute_import, unicode_literals

import sys
import warnings

import ruamel.yaml
from ruamel.yaml.error import *                                # NOQA

from ruamel.yaml.tokens import *                               # NOQA
from ruamel.yaml.events import *                               # NOQA
from ruamel.yaml.nodes import *                                # NOQA

from ruamel.yaml.loader import BaseLoader, SafeLoader, Loader, RoundTripLoader  # NOQA
from ruamel.yaml.dumper import BaseDumper, SafeDumper, Dumper, RoundTripDumper  # NOQA
from ruamel.yaml.compat import StringIO, BytesIO, with_metaclass, PY3
from ruamel.yaml.resolver import VersionedResolver, Resolver  # NOQA
from ruamel.yaml.representer import (BaseRepresenter, SafeRepresenter, Representer,
                                     RoundTripRepresenter)
from ruamel.yaml.constructor import (BaseConstructor, SafeConstructor, Constructor,
                                     RoundTripConstructor)
from ruamel.yaml.loader import Loader as UnsafeLoader

if False:  # MYPY
    from typing import List, Set, Dict, Union, Any                          # NOQA
    from ruamel.yaml.compat import StreamType, StreamTextType, VersionType  # NOQA

try:
    from _ruamel_yaml import CParser, CEmitter   # type: ignore
except:
    CParser = CEmitter = None

# import io

enforce = object()


# YAML is an acronym, i.e. spoken: rhymes with "camel". And thus a
# subset of abbreviations, which should all caps according to PEP8

class YAML(object):
    def __init__(self, _kw=enforce, typ=None, pure=False):
        # type: (Any, Any, Any) -> None
        """
        _kw: not used, forces keyword arguments in 2.7 (in 3 you can do (*, safe_load=..)
        typ: 'rt'/None -> RoundTripLoader/RoundTripDumper,  (default)
             'safe'    -> SafeLoader/SafeDumper,
             'unsafe'  -> normal/unsafe Loader/Dumper
             'base'    -> baseloader
        pure: if True only use Python modules
        """
        if _kw is not enforce:
            raise TypeError("{}.__init__() takes no positional argument but at least "
                            "one was given ({!r})".format(self.__class__.__name__, _kw))

        self.typ = 'rt' if typ is None else typ
        self.Resolver = ruamel.yaml.resolver.VersionedResolver
        self.allow_unicode = True
        self.Reader = None       # type: Any
        self.Scanner = None      # type: Any
        self.Serializer = None   # type: Any
        if self.typ == 'rt':
            # no optimized rt-dumper yet
            self.Emitter = ruamel.yaml.emitter.Emitter                       # type: Any
            self.Serializer = ruamel.yaml.serializer.Serializer              # type: Any
            self.Representer = ruamel.yaml.representer.RoundTripRepresenter  # type: Any
            self.Scanner = ruamel.yaml.scanner.RoundTripScanner              # type: Any
            # no optimized rt-parser yet
            self.Parser = ruamel.yaml.parser.RoundTripParser                 # type: Any
            self.Composer = ruamel.yaml.composer.Composer                    # type: Any
            self.Constructor = ruamel.yaml.constructor.RoundTripConstructor  # type: Any
        elif self.typ == 'safe':
            self.Emitter = ruamel.yaml.emitter.Emitter if pure or CEmitter is None \
                else CEmitter
            self.Representer = ruamel.yaml.representer.SafeRepresenter
            self.Parser = ruamel.yaml.parser.Parser if pure or CParser is None else CParser
            self.Composer = ruamel.yaml.composer.Composer
            self.Constructor = ruamel.yaml.constructor.SafeConstructor
        elif self.typ == 'base':
            self.Emitter = ruamel.yaml.emitter.Emitter
            self.Representer = ruamel.yaml.representer.BaseRepresenter
            self.Parser = ruamel.yaml.parser.Parser if pure or CParser is None else CParser
            self.Composer = ruamel.yaml.composer.Composer
            self.Constructor = ruamel.yaml.constructor.BaseConstructor
        elif self.typ == 'unsafe':
            self.Emitter = ruamel.yaml.emitter.Emitter
            self.Representer = ruamel.yaml.representer.Representer
            self.Parser = ruamel.yaml.parser.Parser if pure or CParser is None else CParser
            self.Composer = ruamel.yaml.composer.Composer
            self.Constructor = ruamel.yaml.constructor.Constructor
        self.stream = None
        self.canonical = None
        self.indent = None
        self.width = None
        self.line_break = None
        self.block_seq_indent = None
        self.top_level_colon_align = None
        self.prefix_colon = None
        self.version = None
        self.preserve_quotes = None
        self.allow_duplicate_keys = False  # duplicate keys in map, set
        self.encoding = None
        self.explicit_start = None
        self.explicit_end = None
        self.tags = None
        self.default_style = None
        self.default_flow_style = None

    @property
    def reader(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, self.Reader(None, loader=self))
        return getattr(self, attr)

    @property
    def scanner(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, self.Scanner(loader=self))
        return getattr(self, attr)

    @property
    def parser(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            if self.Parser is not CParser:
                setattr(self, attr, self.Parser(loader=self))
            else:
                if getattr(self, '_stream', None) is None:
                    # wait for the stream
                    return None
                else:
                    # if not hasattr(self._stream, 'read') and hasattr(self._stream, 'open'):
                    #     # pathlib.Path() instance
                    #     setattr(self, attr, CParser(self._stream))
                    # else:
                    setattr(self, attr, CParser(self._stream))  # type: ignore
                    # self._parser = self._composer = self
                    # print('scanner', self.loader.scanner)

        return getattr(self, attr)

    @property
    def composer(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, self.Composer(loader=self))
        return getattr(self, attr)

    @property
    def constructor(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            cnst = self.Constructor(preserve_quotes=self.preserve_quotes, loader=self)
            cnst.allow_duplicate_keys = self.allow_duplicate_keys
            setattr(self, attr, cnst)
        return getattr(self, attr)

    @property
    def resolver(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, self.Resolver(
                version=self.version, loader=self))
        return getattr(self, attr)

    @property
    def emitter(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            if self.Emitter is not CEmitter:
                setattr(self, attr, self.Emitter(
                    None, canonical=self.canonical,
                    indent=self.indent, width=self.width,
                    allow_unicode=self.allow_unicode, line_break=self.line_break,
                    block_seq_indent=self.block_seq_indent,
                    dumper=self))
            else:
                if getattr(self, '_stream', None) is None:
                    # wait for the stream
                    return None
                return None
        return getattr(self, attr)

    @property
    def serializer(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, self.Serializer(
                encoding=self.encoding,
                explicit_start=self.explicit_start, explicit_end=self.explicit_end,
                version=self.version, tags=self.tags, dumper=self))
        return getattr(self, attr)

    @property
    def representer(self):
        # type: () -> Any
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, self.Representer(
                default_style=self.default_style,
                default_flow_style=self.default_flow_style,
                dumper=self))
        return getattr(self, attr)

    # separate output resolver?

    def load(self, stream):
        # type: (StreamTextType) -> Any
        """
        at this point you either have the non-pure Parser (which has its own reader and
        scanner) or you have the pure Parser.
        If the pure Parser is set, then set the Reader and Scanner, if not already set.
        If either the Scanner or Reader are set, you cannot use the non-pure Parser,
            so reset it to the pure parser and set the Reader resp. Scanner if necessary
        """
        if not hasattr(stream, 'read') and hasattr(stream, 'open'):
            # pathlib.Path() instance
            with stream.open('r') as fp:  # type: ignore
                return self.load(fp)
        constructor, parser = self.get_constructor_parser(stream)
        try:
            return constructor.get_single_data()
        finally:
            parser.dispose()

    def load_all(self, stream, _kw=enforce):  # , skip=None):
        # type: (StreamTextType, Any) -> Any
        if _kw is not enforce:
            raise TypeError("{}.__init__() takes no positional argument but at least "
                            "one was given ({!r})".format(self.__class__.__name__, _kw))
        if not hasattr(stream, 'read') and hasattr(stream, 'open'):
            # pathlib.Path() instance
            with stream.open('r') as fp:  # type: ignore
                yield self.load_all(fp, _kw=enforce)
        # if skip is None:
        #     skip = []
        # elif isinstance(skip, int):
        #     skip = [skip]
        constructor, parser = self.get_constructor_parser(stream)
        try:
            while constructor.check_data():
                yield constructor.get_data()
        finally:
            parser.dispose()

    def get_constructor_parser(self, stream):
        # type: (StreamTextType) -> Any
        """
        the old cyaml needs special setup, and therefore the stream
        """
        if self.Parser is not CParser:
            if self.Reader is None:
                self.Reader = ruamel.yaml.reader.Reader
            if self.Scanner is None:
                self.Scanner = ruamel.yaml.scanner.Scanner
            self.reader.stream = stream
        else:
            if self.Reader is not None:
                if self.Scanner is None:
                    self.Scanner = ruamel.yaml.scanner.Scanner
                self.Parser = ruamel.yaml.parser.Parser
                self.reader.stream = stream
            elif self.Scanner is not None:
                if self.Reader is None:
                    self.Reader = ruamel.yaml.reader.Reader
                self.Parser = ruamel.yaml.parser.Parser
                self.reader.stream = stream
            else:
                # combined C level reader>scanner>parser
                # does some calls to the resolver, e.g. BaseResolver.descend_resolver
                # if you just initialise the CParser, to much of resolver.py
                # is actually used
                rslvr = self.Resolver
                if rslvr is ruamel.yaml.resolver.VersionedResolver:
                    rslvr = ruamel.yaml.resolver.Resolver

                class XLoader(self.Parser, self.Constructor, rslvr):  # type: ignore
                    def __init__(selfx, stream, version=None, preserve_quotes=None):
                        # type: (StreamTextType, VersionType, bool) -> None
                        CParser.__init__(selfx, stream)
                        selfx._parser = selfx._composer = selfx
                        self.Constructor.__init__(selfx, loader=selfx)
                        selfx.allow_duplicate_keys = self.allow_duplicate_keys
                        rslvr.__init__(selfx, loadumper=selfx)
                self._stream = stream
                loader = XLoader(stream)
                return loader, loader
        return self.constructor, self.parser

    def dump(self, data, stream=None):
        # type: (Any, StreamType) -> Any
        return self.dump_all([data], stream)

    def dump_all(self, documents, stream=None):
        # type: (Any, StreamType) -> Any
        """
        Serialize a sequence of Python objects into a YAML stream.
        If stream is None, return the produced string instead.
        """
        # The stream should have the methods `write` and possibly `flush`.
        if not hasattr(stream, 'write') and hasattr(stream, 'open'):
            # pathlib.Path() instance
            with stream.open('w') as fp:   # type: ignore
                return self.dump_all(documents, fp)
        getvalue = None
        if self.top_level_colon_align is True:
            tlca = max([len(str(x)) for x in documents[0]])  # type: Any
        else:
            tlca = self.top_level_colon_align
        if stream is None:
            if self.encoding is None:
                stream = StringIO()
            else:
                stream = BytesIO()
            getvalue = stream.getvalue
        serializer, representer, emitter = \
            self.get_serializer_representer_emitter(stream, tlca)
        try:
            self.serializer.open()
            for data in documents:
                try:
                    self.representer.represent(data)
                except AttributeError:
                    # print(dir(dumper._representer))
                    raise
            self.serializer.close()
        finally:
            try:
                self.emitter.dispose()
            except AttributeError:
                raise
                # self.dumper.dispose()  # cyaml
            delattr(self, "_serializer")
            delattr(self, "_emitter")
        if getvalue is not None:
            return getvalue()
        return None

    def get_serializer_representer_emitter(self, stream, tlca):
        # type: (StreamType, Any) -> Any
        # we have only .Serializer to deal with (vs .Reader & .Scanner), much simpler
        if self.Emitter is not CEmitter:
            if self.Serializer is None:
                self.Serializer = ruamel.yaml.serializer.Serializer
            self.emitter.stream = stream
            self.emitter.top_level_colon_align = tlca
            return self.serializer, self.representer, self.emitter
        if self.Serializer is not None:
            # cannot set serializer with CEmitter
            self.Emitter = ruamel.yaml.emitter.Emitter
            self.emitter.stream = stream
            self.emitter.top_level_colon_align = tlca
            return self.serializer, self.representer, self.emitter
        # C routines

        rslvr = ruamel.yaml.resolver.BaseResolver if self.typ == 'base' \
            else ruamel.yaml.resolver.Resolver

        class XDumper(CEmitter, self.Representer, rslvr):  # type: ignore
            def __init__(selfx, stream,
                         default_style=None, default_flow_style=None,
                         canonical=None, indent=None, width=None,
                         allow_unicode=None, line_break=None,
                         encoding=None, explicit_start=None, explicit_end=None,
                         version=None, tags=None, block_seq_indent=None,
                         top_level_colon_align=None, prefix_colon=None):
                # type: (StreamType, Any, Any, Any, bool, Union[None, int], Union[None, int], bool, Any, Any, Union[None, bool], Union[None, bool], Any, Any, Any, Any, Any) -> None   # NOQA
                CEmitter.__init__(selfx, stream, canonical=canonical,
                                  indent=indent, width=width, encoding=encoding,
                                  allow_unicode=allow_unicode, line_break=line_break,
                                  explicit_start=explicit_start,
                                  explicit_end=explicit_end,
                                  version=version, tags=tags)
                selfx._emitter = selfx._serializer = selfx._representer = selfx
                Representer.__init__(selfx, default_style=default_style,
                                     default_flow_style=default_flow_style)
                Resolver.__init__(selfx)
        self._stream = stream
        dumper = XDumper(stream)
        self._emitter = self._serializer = dumper
        return dumper, dumper, dumper

    # basic types
    def map(self, **kw):
        # type: (Any) -> Any
        if self.typ == 'rt':
            from ruamel.yaml.comments import CommentedMap
            return CommentedMap(**kw)
        else:
            return dict(**kw)

    def seq(self, *args):
        # type: (Any) -> Any
        if self.typ == 'rt':
            from ruamel.yaml.comments import CommentedSeq
            return CommentedSeq(*args)
        else:
            return list(*args)


########################################################################################

def scan(stream, Loader=Loader):
    # type: (StreamTextType, Any) -> Any
    """
    Scan a YAML stream and produce scanning tokens.
    """
    loader = Loader(stream)
    try:
        while loader.scanner.check_token():
            yield loader.scanner.get_token()
    finally:
        loader._parser.dispose()


def parse(stream, Loader=Loader):
    # type: (StreamTextType, Any) -> Any
    """
    Parse a YAML stream and produce parsing events.
    """
    loader = Loader(stream)
    try:
        while loader._parser.check_event():
            yield loader._parser.get_event()
    finally:
        loader._parser.dispose()


def compose(stream, Loader=Loader):
    # type: (StreamTextType, Any) -> Any
    """
    Parse the first YAML document in a stream
    and produce the corresponding representation tree.
    """
    loader = Loader(stream)
    try:
        return loader.get_single_node()
    finally:
        loader.dispose()


def compose_all(stream, Loader=Loader):
    # type: (StreamTextType, Any) -> Any
    """
    Parse all YAML documents in a stream
    and produce corresponding representation trees.
    """
    loader = Loader(stream)
    try:
        while loader.check_node():
            yield loader._composer.get_node()
    finally:
        loader._parser.dispose()


def load(stream, Loader=None, version=None, preserve_quotes=None):
    # type: (StreamTextType, Any, VersionType, Any) -> Any
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    if Loader is None:
        warnings.warn(UnsafeLoaderWarning.text, UnsafeLoaderWarning, stacklevel=2)
        Loader = UnsafeLoader
    loader = Loader(stream, version, preserve_quotes=preserve_quotes)
    try:
        return loader._constructor.get_single_data()
    finally:
        loader._parser.dispose()


def load_all(stream, Loader=None, version=None, preserve_quotes=None):
    # type: (StreamTextType, Any, VersionType, bool) -> Any
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    """
    if Loader is None:
        warnings.warn(UnsafeLoaderWarning.text, UnsafeLoaderWarning, stacklevel=2)
        Loader = UnsafeLoader
    loader = Loader(stream, version, preserve_quotes=preserve_quotes)
    try:
        while loader._constructor.check_data():
            yield loader._constructor.get_data()
    finally:
        loader._parser.dispose()


def safe_load(stream, version=None):
    # type: (StreamTextType, VersionType) -> Any
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    Resolve only basic YAML tags.
    """
    return load(stream, SafeLoader, version)


def safe_load_all(stream, version=None):
    # type: (StreamTextType, VersionType) -> Any
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    Resolve only basic YAML tags.
    """
    return load_all(stream, SafeLoader, version)


def round_trip_load(stream, version=None, preserve_quotes=None):
    # type: (StreamTextType, VersionType, bool) -> Any
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    Resolve only basic YAML tags.
    """
    return load(stream, RoundTripLoader, version, preserve_quotes=preserve_quotes)


def round_trip_load_all(stream, version=None, preserve_quotes=None):
    # type: (StreamTextType, VersionType, bool) -> Any
    """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    Resolve only basic YAML tags.
    """
    return load_all(stream, RoundTripLoader, version, preserve_quotes=preserve_quotes)


def emit(events, stream=None, Dumper=Dumper,
         canonical=None, indent=None, width=None,
         allow_unicode=None, line_break=None):
    # type: (Any, StreamType, Any, bool, Union[int, None], int, bool, Any) -> Any
    """
    Emit YAML parsing events into a stream.
    If stream is None, return the produced string instead.
    """
    getvalue = None
    if stream is None:
        stream = StringIO()
        getvalue = stream.getvalue
    dumper = Dumper(stream, canonical=canonical, indent=indent, width=width,
                    allow_unicode=allow_unicode, line_break=line_break)
    try:
        for event in events:
            dumper.emit(event)
    finally:
        try:
            dumper._emitter.dispose()
        except AttributeError:
            raise
            dumper.dispose()   # cyaml
    if getvalue is not None:
        return getvalue()

enc = None if PY3 else 'utf-8'


def serialize_all(nodes, stream=None, Dumper=Dumper,
                  canonical=None, indent=None, width=None,
                  allow_unicode=None, line_break=None,
                  encoding=enc, explicit_start=None, explicit_end=None,
                  version=None, tags=None):
    # type: (Any, StreamType, Any, Any, Union[None, int], Union[None, int], bool, Any, Any, Union[None, bool], Union[None, bool], VersionType, Any) -> Any # NOQA
    """
    Serialize a sequence of representation trees into a YAML stream.
    If stream is None, return the produced string instead.
    """
    getvalue = None
    if stream is None:
        if encoding is None:
            stream = StringIO()
        else:
            stream = BytesIO()
        getvalue = stream.getvalue
    dumper = Dumper(stream, canonical=canonical, indent=indent, width=width,
                    allow_unicode=allow_unicode, line_break=line_break,
                    encoding=encoding, version=version, tags=tags,
                    explicit_start=explicit_start, explicit_end=explicit_end)
    try:
        dumper._serializer.open()
        for node in nodes:
            dumper.serialize(node)
        dumper._serializer.close()
    finally:
        try:
            dumper._emitter.dispose()
        except AttributeError:
            raise
            dumper.dispose()   # cyaml
    if getvalue is not None:
        return getvalue()


def serialize(node, stream=None, Dumper=Dumper, **kwds):
    # type: (Any, StreamType, Any, Any) -> Any
    """
    Serialize a representation tree into a YAML stream.
    If stream is None, return the produced string instead.
    """
    return serialize_all([node], stream, Dumper=Dumper, **kwds)


def dump_all(documents, stream=None, Dumper=Dumper,
             default_style=None, default_flow_style=None,
             canonical=None, indent=None, width=None,
             allow_unicode=None, line_break=None,
             encoding=enc, explicit_start=None, explicit_end=None,
             version=None, tags=None, block_seq_indent=None,
             top_level_colon_align=None, prefix_colon=None):
    # type: (Any, StreamType, Any, Any, Any, bool, Union[None, int], Union[None, int], bool, Any, Any, Union[None, bool], Union[None, bool], Any, Any, Any, Any, Any) -> Union[None, str]   # NOQA
    """
    Serialize a sequence of Python objects into a YAML stream.
    If stream is None, return the produced string instead.
    """
    getvalue = None
    if top_level_colon_align is True:
        top_level_colon_align = max([len(str(x)) for x in documents[0]])
    if stream is None:
        if encoding is None:
            stream = StringIO()
        else:
            stream = BytesIO()
        getvalue = stream.getvalue
    dumper = Dumper(stream, default_style=default_style,
                    default_flow_style=default_flow_style,
                    canonical=canonical, indent=indent, width=width,
                    allow_unicode=allow_unicode, line_break=line_break,
                    encoding=encoding, explicit_start=explicit_start,
                    explicit_end=explicit_end, version=version,
                    tags=tags, block_seq_indent=block_seq_indent,
                    top_level_colon_align=top_level_colon_align, prefix_colon=prefix_colon,
                    )
    try:
        dumper._serializer.open()
        for data in documents:
            try:
                dumper._representer.represent(data)
            except AttributeError:
                # print(dir(dumper._representer))
                raise
        dumper._serializer.close()
    finally:
        try:
            dumper._emitter.dispose()
        except AttributeError:
            raise
            dumper.dispose()  # cyaml
    if getvalue is not None:
        return getvalue()
    return None


def dump(data, stream=None, Dumper=Dumper,
         default_style=None, default_flow_style=None,
         canonical=None, indent=None, width=None,
         allow_unicode=None, line_break=None,
         encoding=enc, explicit_start=None, explicit_end=None,
         version=None, tags=None, block_seq_indent=None):
    # type: (Any, StreamType, Any, Any, Any, bool, Union[None, int], Union[None, int], bool, Any, Any, Union[None, bool], Union[None, bool], VersionType, Any, Any) -> Union[None, str]   # NOQA
    """
    Serialize a Python object into a YAML stream.
    If stream is None, return the produced string instead.

    default_style ∈ None, '', '"', "'", '|', '>'

    """
    return dump_all([data], stream, Dumper=Dumper,
                    default_style=default_style,
                    default_flow_style=default_flow_style,
                    canonical=canonical,
                    indent=indent, width=width,
                    allow_unicode=allow_unicode,
                    line_break=line_break,
                    encoding=encoding, explicit_start=explicit_start,
                    explicit_end=explicit_end,
                    version=version, tags=tags, block_seq_indent=block_seq_indent)


def safe_dump_all(documents, stream=None, **kwds):
    # type: (Any, StreamType, Any) -> Union[None, str]
    """
    Serialize a sequence of Python objects into a YAML stream.
    Produce only basic YAML tags.
    If stream is None, return the produced string instead.
    """
    return dump_all(documents, stream, Dumper=SafeDumper, **kwds)


def safe_dump(data, stream=None, **kwds):
    # type: (Any, StreamType, Any) -> Union[None, str]
    """
    Serialize a Python object into a YAML stream.
    Produce only basic YAML tags.
    If stream is None, return the produced string instead.
    """
    return dump_all([data], stream, Dumper=SafeDumper, **kwds)


def round_trip_dump(data, stream=None, Dumper=RoundTripDumper,
                    default_style=None, default_flow_style=None,
                    canonical=None, indent=None, width=None,
                    allow_unicode=None, line_break=None,
                    encoding=enc, explicit_start=None, explicit_end=None,
                    version=None, tags=None, block_seq_indent=None,
                    top_level_colon_align=None, prefix_colon=None):
    # type: (Any, StreamType, Any, Any, Any, bool, Union[None, int], Union[None, int], bool, Any, Any, Union[None, bool], Union[None, bool], VersionType, Any, Any, Any, Any) -> Union[None, str]   # NOQA
    allow_unicode = True if allow_unicode is None else allow_unicode
    return dump_all([data], stream, Dumper=Dumper,
                    default_style=default_style,
                    default_flow_style=default_flow_style,
                    canonical=canonical,
                    indent=indent, width=width,
                    allow_unicode=allow_unicode,
                    line_break=line_break,
                    encoding=encoding, explicit_start=explicit_start,
                    explicit_end=explicit_end,
                    version=version, tags=tags, block_seq_indent=block_seq_indent,
                    top_level_colon_align=top_level_colon_align, prefix_colon=prefix_colon)


# Loader/Dumper are no longer composites, to get to the associated
# Resolver()/Representer(), etc., you need to instantiate the class

def add_implicit_resolver(tag, regexp, first=None, Loader=None, Dumper=None,
                          resolver=Resolver):
    # type: (Any, Any, Any, Any, Any, Any) -> None
    """
    Add an implicit scalar detector.
    If an implicit scalar value matches the given regexp,
    the corresponding tag is assigned to the scalar.
    first is a sequence of possible initial characters or None.
    """
    if Loader is None and Dumper is None:
        resolver.add_implicit_resolver(tag, regexp, first)
        return
    if Loader:
        if hasattr(Loader, 'add_implicit_resolver'):
            Loader.add_implicit_resolver(tag, regexp, first)
        elif issubclass(Loader, (BaseLoader, SafeLoader, ruamel.yaml.loader.Loader,
                                 RoundTripLoader)):
            Resolver.add_implicit_resolver(tag, regexp, first)
        else:
            raise NotImplementedError
    if Dumper:
        if hasattr(Dumper, 'add_implicit_resolver'):
            Dumper.add_implicit_resolver(tag, regexp, first)
        elif issubclass(Dumper, (BaseDumper, SafeDumper, ruamel.yaml.dumper.Dumper,
                                 RoundTripDumper)):
            Resolver.add_implicit_resolver(tag, regexp, first)
        else:
            raise NotImplementedError


# this code currently not tested
def add_path_resolver(tag, path, kind=None, Loader=None, Dumper=None,
                      resolver=Resolver):
    # type: (Any, Any, Any, Any, Any, Any) -> None
    """
    Add a path based resolver for the given tag.
    A path is a list of keys that forms a path
    to a node in the representation tree.
    Keys can be string values, integers, or None.
    """
    if Loader is None and Dumper is None:
        resolver.add_path_resolver(tag, path, kind)
        return
    if Loader:
        if hasattr(Loader, 'add_path_resolver'):
            Loader.add_path_resolver(tag, path, kind)
        elif issubclass(Loader, (BaseLoader, SafeLoader, ruamel.yaml.loader.Loader,
                                 RoundTripLoader)):
            Resolver.add_path_resolver(tag, path, kind)
        else:
            raise NotImplementedError
    if Dumper:
        if hasattr(Dumper, 'add_path_resolver'):
            Dumper.add_path_resolver(tag, path, kind)
        elif issubclass(Dumper, (BaseDumper, SafeDumper, ruamel.yaml.dumper.Dumper,
                                 RoundTripDumper)):
            Resolver.add_path_resolver(tag, path, kind)
        else:
            raise NotImplementedError


def add_constructor(tag, object_constructor, Loader=None, constructor=Constructor):
    # type: (Any, Any, Any, Any) -> None
    """
    Add an object constructor for the given tag.
    object_onstructor is a function that accepts a Loader instance
    and a node object and produces the corresponding Python object.
    """
    if Loader is None:
        constructor.add_constructor(tag, object_constructor)
    else:
        if hasattr(Loader, 'add_constructor'):
            Loader.add_constructor(tag, object_constructor)
            return
        if issubclass(Loader, BaseLoader):
            BaseConstructor.add_constructor(tag, object_constructor)
        elif issubclass(Loader, SafeLoader):
            SafeConstructor.add_constructor(tag, object_constructor)
        elif issubclass(Loader, Loader):
            Constructor.add_constructor(tag, object_constructor)
        elif issubclass(Loader, RoundTripLoader):
            RoundTripConstructor.add_constructor(tag, object_constructor)
        else:
            raise NotImplementedError


def add_multi_constructor(tag_prefix, multi_constructor, Loader=None,
                          constructor=Constructor):
    # type: (Any, Any, Any, Any) -> None
    """
    Add a multi-constructor for the given tag prefix.
    Multi-constructor is called for a node if its tag starts with tag_prefix.
    Multi-constructor accepts a Loader instance, a tag suffix,
    and a node object and produces the corresponding Python object.
    """
    if Loader is None:
        constructor.add_multi_constructor(tag_prefix, multi_constructor)
    else:
        if False and hasattr(Loader, 'add_multi_constructor'):
            Loader.add_multi_constructor(tag_prefix, constructor)
            return
        if issubclass(Loader, BaseLoader):
            BaseConstructor.add_multi_constructor(tag_prefix, multi_constructor)
        elif issubclass(Loader, SafeLoader):
            SafeConstructor.add_multi_constructor(tag_prefix, multi_constructor)
        elif issubclass(Loader, ruamel.yaml.loader.Loader):
            Constructor.add_multi_constructor(tag_prefix, multi_constructor)
        elif issubclass(Loader, RoundTripLoader):
            RoundTripConstructor.add_multi_constructor(tag_prefix, multi_constructor)
        else:
            raise NotImplementedError


def add_representer(data_type, object_representer, Dumper=None, representer=Representer):
    # type: (Any, Any, Any, Any) -> None
    """
    Add a representer for the given type.
    object_representer is a function accepting a Dumper instance
    and an instance of the given data type
    and producing the corresponding representation node.
    """
    if Dumper is None:
        representer.add_representer(data_type, object_representer)
    else:
        if hasattr(Dumper, 'add_representer'):
            Dumper.add_representer(data_type, object_representer)
            return
        if issubclass(Dumper, BaseDumper):
            BaseRepresenter.add_representer(data_type, object_representer)
        elif issubclass(Dumper, SafeDumper):
            SafeRepresenter.add_representer(data_type, object_representer)
        elif issubclass(Dumper, Dumper):
            Representer.add_representer(data_type, object_representer)
        elif issubclass(Dumper, RoundTripDumper):
            RoundTripRepresenter.add_representer(data_type, object_representer)
        else:
            raise NotImplementedError


# this code currently not tested
def add_multi_representer(data_type, multi_representer, Dumper=None, representer=Representer):
    # type: (Any, Any, Any, Any) -> None
    """
    Add a representer for the given type.
    multi_representer is a function accepting a Dumper instance
    and an instance of the given data type or subtype
    and producing the corresponding representation node.
    """
    if Dumper is None:
        representer.add_multi_representer(data_type, multi_representer)
    else:
        if hasattr(Dumper, 'add_multi_representer'):
            Dumper.add_multi_representer(data_type, multi_representer)
            return
        if issubclass(Dumper, BaseDumper):
            BaseRepresenter.add_multi_representer(data_type, multi_representer)
        elif issubclass(Dumper, SafeDumper):
            SafeRepresenter.add_multi_representer(data_type, multi_representer)
        elif issubclass(Dumper, Dumper):
            Representer.add_multi_representer(data_type, multi_representer)
        elif issubclass(Dumper, RoundTripDumper):
            RoundTripRepresenter.add_multi_representer(data_type, multi_representer)
        else:
            raise NotImplementedError


class YAMLObjectMetaclass(type):
    """
    The metaclass for YAMLObject.
    """
    def __init__(cls, name, bases, kwds):
        # type: (Any, Any, Any) -> None
        super(YAMLObjectMetaclass, cls).__init__(name, bases, kwds)
        if 'yaml_tag' in kwds and kwds['yaml_tag'] is not None:
            cls.yaml_constructor.add_constructor(cls.yaml_tag, cls.from_yaml)  # type: ignore
            cls.yaml_representer.add_representer(cls, cls.to_yaml)             # type: ignore


class YAMLObject(with_metaclass(YAMLObjectMetaclass)):  # type: ignore
    """
    An object that can dump itself to a YAML stream
    and load itself from a YAML stream.
    """
    __slots__ = ()  # no direct instantiation, so allow immutable subclasses

    yaml_constructor = Constructor
    yaml_representer = Representer

    yaml_tag = None  # type: Any
    yaml_flow_style = None  # type: Any

    @classmethod
    def from_yaml(cls, constructor, node):
        # type: (Any, Any) -> Any
        """
        Convert a representation node to a Python object.
        """
        return constructor.construct_yaml_object(node, cls)

    @classmethod
    def to_yaml(cls, representer, data):
        # type: (Any, Any) -> Any
        """
        Convert a Python object to a representation node.
        """
        return representer.represent_yaml_object(cls.yaml_tag, data, cls,
                                                 flow_style=cls.yaml_flow_style)

import pytest # type: ignore

from promnesia import Source


def test_minimal():
    '''
    Example of a smallest possible config, using a 'demo' source
    '''
    cfg = make('''
from promnesia import Source
from promnesia.sources import demo

SOURCES = [
    Source(demo.index),
]
''')
    assert len(cfg.sources) == 1
    assert all(isinstance(s, Source) for s in cfg.sources)
    # todo output dirs?
    index(cfg)


def test_sources_style():
    '''
    Testing 'styles' of specifying sources
    '''
    cfg = make('''
from promnesia import Source
from promnesia.sources import demo

SOURCES = [
    # you can pass arguments to index functions
    Source(demo.index, count=10, name='explicit name'),

    # or rely on the default argument!
    Source(demo.index, name='another name'),

    # or rely on default source name name (will be guessed as 'demo')
    Source(demo.index),

    # rely on default index function
    Source(demo),

    # no need for Source() either!
    demo,

    # I guess this is as simple as it possibly gets...
    # 'promnesia.sources.demo',

    # or, make it lazy
    lambda: Source(demo.index, name='lazy'),
]
    ''')

    srcs = cfg.sources
    assert all(isinstance(_, Source) for _ in cfg.sources)

    [s1, s2, s3, s4, s5, s6] = srcs
    index(cfg)
    # TODO assert on results count?


def test_no_sources():
    cfg = make('''
''')
    # raises because no SOURCES
    with pytest.raises(RuntimeError):
        cfg.sources


def test_empty_sources():
    cfg = make('''
SOURCES = []
    ''')
    # raises because empty SOURCES
    with pytest.raises(RuntimeError):
        cfg.sources


from pathlib import Path
from tempfile import TemporaryDirectory

from promnesia.config import import_config, Config


def make(body: str) -> Config:
    with TemporaryDirectory() as td:
        tdir = Path(td)
        cp = tdir / 'cfg.py'
        cp.write_text(body)
        return import_config(cp)


def index(cfg: Config):
    import promnesia.config as config
    from promnesia.__main__ import _do_index
    config.instance = cfg
    try:
        errors = list(_do_index())
        assert len(errors) == 0
    finally:
        config.reset()

import os
import tempfile

import pytest

from uhura.functional import uhura_reader, uhura_writer
from uhura.modes import fixture_builder_mode


def test_readers_attach_pickle_extension():
    @uhura_reader
    def readable_thing_1():
        return "hello"

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "good_output")
        input_path = os.path.join(temp_dir, "input")

        with fixture_builder_mode(known_good_path=output_path, input_path=input_path):
            readable_thing_1()
        assert os.path.exists(os.path.join(input_path, f"{readable_thing_1.__qualname__}.pkl"))


def test_writers_attach_pickle_extension():
    @uhura_writer
    def writable_thing_1(thing: str):
        pass

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "good_output")
        input_path = os.path.join(temp_dir, "input")

        with fixture_builder_mode(known_good_path=output_path, input_path=input_path):
            writable_thing_1("goodbye")
        assert os.path.exists(os.path.join(output_path, f"{writable_thing_1.__qualname__}.pkl"))


def test_writer_raises_if_ambiguous():
    with pytest.raises(ValueError):

        @uhura_writer
        def ambiguous_writable(thing: str, other_arg: str):
            pass

    with pytest.raises(ValueError):

        @uhura_writer(output_arg="not an argument")
        def ambiguous_writable(thing: str, other_arg):
            pass

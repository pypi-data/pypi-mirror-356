# Copyright (c) OpenMMLab. All rights reserved.
import pickle
from io import BytesIO
from typing import Any

from .base import BaseFileHandler


class PickleHandler(BaseFileHandler):

    str_like = False

    def load_from_fileobj(self, file: BytesIO, **kwargs):
        return pickle.load(file, **kwargs)

    def load_from_path(self, filepath, **kwargs):
        return super().load_from_path(filepath, mode="rb", **kwargs)

    def dump_to_str(self, obj, **kwargs):
        kwargs.setdefault("protocol", 2)
        return pickle.dumps(obj, **kwargs)

    def dump_to_fileobj(self, obj: Any, file: BytesIO, **kwargs):
        kwargs.setdefault("protocol", 2)
        pickle.dump(obj, file, **kwargs)

    def dump_to_path(self, obj, filepath, **kwargs):
        # super().dump_to_path(obj, filepath, mode="wb", **kwargs)
        with open(filepath, "wb") as f:
            pickle.dump(obj, f, **kwargs)

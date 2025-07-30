from __future__ import annotations

import io, hashlib, functools, os
from typing import Dict, Any, Optional, List, Tuple, Union
from tqdm.auto import tqdm

from .io_utils import FileTuple, iter_file_tuples

from sensory_transcription.client.core.io_utils import (
    AudioLike, build_multipart, sha1_any
)

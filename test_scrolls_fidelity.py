#!/usr/bin/env python3
"""Backward-compatible wrapper for the SCROLLS fidelity tests."""

import unittest

from tests.test_scrolls_fidelity import *  # noqa: F401,F403


if __name__ == "__main__":
    unittest.main()

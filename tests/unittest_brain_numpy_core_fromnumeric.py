# -*- encoding=utf-8 -*-
# Copyright (c) 2017-2018 hippo91 <guillaume.peillex@gmail.com>

# Licensed under the LGPL: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
# For details: https://github.com/PyCQA/astroid/blob/master/COPYING.LESSER
import unittest

try:
    import numpy  # pylint: disable=unused-import

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from astroid import builder, Uninferable


@unittest.skipUnless(HAS_NUMPY, "This test requires the numpy library.")
class BrainNumpyCoreFromNumericTest(unittest.TestCase):
    """
    Test the numpy core fromnumeric brain module
    """

    numpy_functions = (("sum", "[1, 2]"),)

    def _inferred_numpy_func_call(self, func_name, *func_args):
        node = builder.extract_node(
            """
        import numpy as np
        func = np.{:s}
        func({:s})
        """.format(
                func_name, ",".join(func_args)
            )
        )
        return node.infer()

    def test_numpy_function_calls_inferred_as_ndarray(self):
        """
        Test that calls to numpy functions are inferred as numpy.ndarray
        """
        licit_array_types = set([".ndarray", Uninferable])
        for func_ in self.numpy_functions:
            with self.subTest(typ=func_):
                inferred_values = set([v.pytype() for v in self._inferred_numpy_func_call(*func_)])
                self.assertTrue(
                    len(inferred_values) == 2,
                    msg="Too much inferred values {} for {:s}".format(inferred_values, func_[1]),
                )
                self.assertTrue(
                    inferred_values == licit_array_types,
                    msg="Illicit type for {:s} ({})".format(
                        func_[0], inferred_values),
                )


if __name__ == "__main__":
    unittest.main()

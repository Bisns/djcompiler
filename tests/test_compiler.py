import unittest
from unittest.mock import patch

from setuptools import Extension

from djcompiler import DjangoCompiler


class DjangoCompilerTests(unittest.TestCase):
    def test_ext_modules_accepts_unhashable_extensions(self):
        compiler = DjangoCompiler(ignored_dirs=["ignored"], ignored_files=["skip.py"])
        walk_result = [
            ("./", [], ["views.py", "helpers.pyx", "__init__.py", "0001_initial.py", "skip.py", "data.txt"]),
            ("./ignored", [], ["excluded.py"]),
        ]

        with patch.object(Extension, "__hash__", None), patch(
            "djcompiler.compiler.djcompiler.os.walk", return_value=walk_result
        ):
            modules = compiler.ext_modules()

        self.assertEqual(
            [(module.name, module.sources) for module in modules],
            [("views", ["./views.py"]), ("helpers", ["./helpers.pyx"])],
        )


if __name__ == "__main__":
    unittest.main()

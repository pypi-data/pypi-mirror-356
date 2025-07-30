import ast
import subprocess
from typing import Set

from flake8_all_not_strings import Plugin


def get_results(s: str) -> Set[str]:
    tree = ast.parse(s)
    plugin = Plugin(tree)
    return {'{}:{}: {}'.format(*r) for r in plugin.run()}


class TestFlake8AllNotStrings:
    def test_flake8_all_not_strings_in_flake8_command(self):
        result = str(subprocess.check_output(["flake8", "--version"]))
        assert "flake8_all_not_strings" in result

    def test_flake8_all_not_strings(self):
        assert get_results("") == set()
        assert get_results(
            "__all__ = [\nsomething,\nsomething_else, something_else_else]") ==\
            set(
            [
                "3:0: ANS100: 'something_else' import under __all__ is not a "
                "string.",
                "3:16: ANS100: 'something_else_else' import under __all__ "
                "is not a string.",
                "2:0: ANS100: 'something' import under __all__ is not a string."
            ]
        )

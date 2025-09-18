from pathlib import Path

from tools.php_syntax_check import check_php_syntax


def test_php_check_allows_missing_interpreter(tmp_path: Path):
    test_file = tmp_path / "dummy.php"
    test_file.write_text("<?php echo 'ok';")
    exit_code = check_php_syntax([tmp_path], allow_missing_php=True)
    assert exit_code == 0

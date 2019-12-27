"""Tests for strip_backend() function."""
from os import path as osp
from terraform_ci import strip_backend


def test_strip_backend(tmpdir):
    """Check that main.tf is copied."""
    original_tf_dir = tmpdir.mkdir("original")
    tf_file = original_tf_dir.join("main.tf")
    tf_file.write("")

    with strip_backend(str(original_tf_dir)) as tmp_tf_dir:
        assert osp.exists(
            osp.join(tmp_tf_dir, "main.tf")
        )

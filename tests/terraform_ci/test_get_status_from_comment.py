"""Tests for get_status_from_comment()."""
import pytest

from terraform_ci import get_status_from_comment


@pytest.mark.parametrize("comment, status", [
    (
        None,
        None
    ),
    (
        """""",
        None
    ),
    (
        """
        some
        comment
        """,
        None
    ),
    (
        """Module | Success | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+)"""
        """ Add | Change | Destroy
--- | --- | ---: | ---: | ---:
**cloudflare** | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) `True` | **1** | 0 | 0
**github** | ![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `False` | 0 | 0 | 0

# **cloudflare**

## stdout

```cloudflare plan```

## stderr

_no output_

# **github**

## stdout

```github plan```

## stderr

```some output```

<details><summary><i>metadata</i></summary>
<p>

```eyJjbG91ZGZsYXJlIjogeyJhZGQiOiAxLCAiY2hhbmdlIjogMCwgImRlc3Ryb3kiOiAwLCAic3RkZX"""
        """JyIjogIiIsICJzdWNjZXNzIjogdHJ1ZSwgInN0ZG91dCI6ICJjbG91ZGZsYXJlIHBsYW4i"""
        """fSwgImdpdGh1YiI6IHsiYWRkIjogMCwgImNoYW5nZSI6IDAsICJkZXN0cm95IjogMCwgIn"""
        """N0ZGVyciI6ICJzb21lIG91dHB1dCIsICJzdWNjZXNzIjogZmFsc2UsICJzdGRvdXQiOiAi"""
        """Z2l0aHViIHBsYW4ifX0=```
</p>
</details>
""",
        {
            'cloudflare': {
                'add': 1,
                'change': 0,
                'destroy': 0,
                'stderr': "",
                'success': True,
                'stdout': 'cloudflare plan'
            },
            'github': {
                'add': 0,
                'change': 0,
                'destroy': 0,
                'stderr': 'some output',
                'success': False,
                'stdout': 'github plan'
            }
        },
    )
])
def test_get_status_from_comment(comment, status):
    """Check that get_status_from_comment() returns expected status."""
    assert get_status_from_comment(comment) == status

"""render_comment() tests."""
# pylint: disable=line-too-long

# noinspection PyPackageRequirements
import pytest

from terraform_ci import render_comment


@pytest.mark.parametrize('status, expected_output', [
    (
        {
            'cloudflare': {
                'add': 1,
                'change': 0,
                'destroy': 0,
                'stderr': b'',
                'success': True,
                'stdout': 'cloudflare plan'
            },
            'github': {
                'add': 0,
                'change': 0,
                'destroy': 0,
                'stderr': b'some output',
                'success': False,
                'stdout': 'github plan'
            }
        },
        """Module | Success | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) Add | Change | Destroy
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

```eyJjbG91ZGZsYXJlIjogeyJhZGQiOiAxLCAiY2hhbmdlIjogMCwgImRlc3Ryb3kiOiAwLCAic3RkZXJyIjogIiIsICJzdWNjZXNzIjogdHJ1ZSwgInN0ZG91dCI6ICJjbG91ZGZsYXJlIHBsYW4ifSwgImdpdGh1YiI6IHsiYWRkIjogMCwgImNoYW5nZSI6IDAsICJkZXN0cm95IjogMCwgInN0ZGVyciI6ICJzb21lIG91dHB1dCIsICJzdWNjZXNzIjogZmFsc2UsICJzdGRvdXQiOiAiZ2l0aHViIHBsYW4ifX0=```
</p>
</details>
"""
    ),
    (
        {
            'cloudflare': {
                'success': True,
                'stderr': b'',
                'stdout': b'terraform init -no-color\n\nInitializing the backend...\n\nInitializing provider plugins...\n\nTerraform has been successfully initialized!\n\nYou may now begin working with Terraform. Try running "terraform plan" to see\nany changes that are required for your infrastructure. All Terraform commands\nshould now work.\n\nIf you ever set or change modules or backend configuration for Terraform,\nrerun this command to reinitialize your working directory. If you forget, other\ncommands will detect it and remind you to do so if necessary.\nterraform get -update=true -no-color\nterraform plan -var-file=../global_variables.tfvars -var-file=../../.env/terraform.tfvars -no-color\nRefreshing Terraform state in-memory prior to plan...\nThe refreshed state will be used to calculate this plan, but will not be\npersisted to local or remote state storage.\n\ncloudflare_record.verification_record_3: Refreshing state... (ID: 2ab0c155081745ca00effed5847e5ba7)\ncloudflare_record.verification_record_1: Refreshing state... (ID: d39e64e10fb40d45645e558a3fc33910)\ncloudflare_record.verification_record_5: Refreshing state... (ID: 1679568e8cced8adf4d02f12952c10d0)\ncloudflare_record.sites: Refreshing state... (ID: f109786dcdcbef13e22c6bf4e8c92136)\ncloudflare_record.calendar: Refreshing state... (ID: 2e0bddb67ce0b4802b74d0573beb459b)\ncloudflare_record.google_mail_record_3: Refreshing state... (ID: ad9665cff6cd17ab66950d99640b57dd)\ncloudflare_record.comodo_cert_console: Refreshing state... (ID: a8501534c477de0522ec92408465ef35)\ncloudflare_record.comodo_cert_recovery: Refreshing state... (ID: e27043dbc5ab0cbd6f570318279e8260)\ncloudflare_record.google_mail_record_4: Refreshing state... (ID: bd6ce59f27a11a6edf2bb5f38b5454b1)\ncloudflare_record.mail: Refreshing state... (ID: b00400644830377797feccccb75e14d3)\ncloudflare_record.google_mail_record_1: Refreshing state... (ID: ca5642b2c131e0b012af7ad3d275886b)\ncloudflare_record.comodo_cert_www: Refreshing state... (ID: 666671cb4a5820a1b88daa34e7c6a421)\ncloudflare_record.google_mail_record_2: Refreshing state... (ID: 2d82243bc95f8386c8ddeb7b0c083d98)\ncloudflare_zone.twindb-cie_com: Refreshing state... (ID: 02cffc58027ebabbe29614c6bf6e3716)\ncloudflare_record.drive: Refreshing state... (ID: 7f3e38c63ce7d169012edf79a01955f3)\ncloudflare_record.verification_record_2: Refreshing state... (ID: 2468d19b6567522466124658c3ae1a7d)\ncloudflare_record.google_mail_record_5: Refreshing state... (ID: 0332768712fb40e81ac5a10973019de2)\ncloudflare_record.comodo_cert_root: Refreshing state... (ID: 3a327cd3e905251ccb595f5c003c5160)\n\n------------------------------------------------------------------------\n\nNo changes. Infrastructure is up-to-date.\n\nThis means that Terraform did not detect any differences between your\nconfiguration and real physical resources that exist. As a result, no\nactions need to be performed.\n',
                'add': 0,
                'change': 0,
                'destroy': 0
            }
        },
        """Module | Success | Add | Change | Destroy
--- | --- | ---: | ---: | ---:
**cloudflare** | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) `True` | 0 | 0 | 0

# **cloudflare**

## stdout

```terraform init -no-color

Initializing the backend...

Initializing provider plugins...

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
terraform get -update=true -no-color
terraform plan -var-file=../global_variables.tfvars -var-file=../../.env/terraform.tfvars -no-color
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

cloudflare_record.verification_record_3: Refreshing state... (ID: 2ab0c155081745ca00effed5847e5ba7)
cloudflare_record.verification_record_1: Refreshing state... (ID: d39e64e10fb40d45645e558a3fc33910)
cloudflare_record.verification_record_5: Refreshing state... (ID: 1679568e8cced8adf4d02f12952c10d0)
cloudflare_record.sites: Refreshing state... (ID: f109786dcdcbef13e22c6bf4e8c92136)
cloudflare_record.calendar: Refreshing state... (ID: 2e0bddb67ce0b4802b74d0573beb459b)
cloudflare_record.google_mail_record_3: Refreshing state... (ID: ad9665cff6cd17ab66950d99640b57dd)
cloudflare_record.comodo_cert_console: Refreshing state... (ID: a8501534c477de0522ec92408465ef35)
cloudflare_record.comodo_cert_recovery: Refreshing state... (ID: e27043dbc5ab0cbd6f570318279e8260)
cloudflare_record.google_mail_record_4: Refreshing state... (ID: bd6ce59f27a11a6edf2bb5f38b5454b1)
cloudflare_record.mail: Refreshing state... (ID: b00400644830377797feccccb75e14d3)
cloudflare_record.google_mail_record_1: Refreshing state... (ID: ca5642b2c131e0b012af7ad3d275886b)
cloudflare_record.comodo_cert_www: Refreshing state... (ID: 666671cb4a5820a1b88daa34e7c6a421)
cloudflare_record.google_mail_record_2: Refreshing state... (ID: 2d82243bc95f8386c8ddeb7b0c083d98)
cloudflare_zone.twindb-cie_com: Refreshing state... (ID: 02cffc58027ebabbe29614c6bf6e3716)
cloudflare_record.drive: Refreshing state... (ID: 7f3e38c63ce7d169012edf79a01955f3)
cloudflare_record.verification_record_2: Refreshing state... (ID: 2468d19b6567522466124658c3ae1a7d)
cloudflare_record.google_mail_record_5: Refreshing state... (ID: 0332768712fb40e81ac5a10973019de2)
cloudflare_record.comodo_cert_root: Refreshing state... (ID: 3a327cd3e905251ccb595f5c003c5160)

------------------------------------------------------------------------

No changes. Infrastructure is up-to-date.

This means that Terraform did not detect any differences between your
configuration and real physical resources that exist. As a result, no
actions need to be performed.
```

## stderr

_no output_

<details><summary><i>metadata</i></summary>
<p>

```eyJjbG91ZGZsYXJlIjogeyJzdWNjZXNzIjogdHJ1ZSwgInN0ZGVyciI6ICIiLCAic3Rkb3V0IjogInRlcnJhZm9ybSBpbml0IC1uby1jb2xvclxuXG5Jbml0aWFsaXppbmcgdGhlIGJhY2tlbmQuLi5cblxuSW5pdGlhbGl6aW5nIHByb3ZpZGVyIHBsdWdpbnMuLi5cblxuVGVycmFmb3JtIGhhcyBiZWVuIHN1Y2Nlc3NmdWxseSBpbml0aWFsaXplZCFcblxuWW91IG1heSBub3cgYmVnaW4gd29ya2luZyB3aXRoIFRlcnJhZm9ybS4gVHJ5IHJ1bm5pbmcgXCJ0ZXJyYWZvcm0gcGxhblwiIHRvIHNlZVxuYW55IGNoYW5nZXMgdGhhdCBhcmUgcmVxdWlyZWQgZm9yIHlvdXIgaW5mcmFzdHJ1Y3R1cmUuIEFsbCBUZXJyYWZvcm0gY29tbWFuZHNcbnNob3VsZCBub3cgd29yay5cblxuSWYgeW91IGV2ZXIgc2V0IG9yIGNoYW5nZSBtb2R1bGVzIG9yIGJhY2tlbmQgY29uZmlndXJhdGlvbiBmb3IgVGVycmFmb3JtLFxucmVydW4gdGhpcyBjb21tYW5kIHRvIHJlaW5pdGlhbGl6ZSB5b3VyIHdvcmtpbmcgZGlyZWN0b3J5LiBJZiB5b3UgZm9yZ2V0LCBvdGhlclxuY29tbWFuZHMgd2lsbCBkZXRlY3QgaXQgYW5kIHJlbWluZCB5b3UgdG8gZG8gc28gaWYgbmVjZXNzYXJ5LlxudGVycmFmb3JtIGdldCAtdXBkYXRlPXRydWUgLW5vLWNvbG9yXG50ZXJyYWZvcm0gcGxhbiAtdmFyLWZpbGU9Li4vZ2xvYmFsX3ZhcmlhYmxlcy50ZnZhcnMgLXZhci1maWxlPS4uLy4uLy5lbnYvdGVycmFmb3JtLnRmdmFycyAtbm8tY29sb3JcblJlZnJlc2hpbmcgVGVycmFmb3JtIHN0YXRlIGluLW1lbW9yeSBwcmlvciB0byBwbGFuLi4uXG5UaGUgcmVmcmVzaGVkIHN0YXRlIHdpbGwgYmUgdXNlZCB0byBjYWxjdWxhdGUgdGhpcyBwbGFuLCBidXQgd2lsbCBub3QgYmVcbnBlcnNpc3RlZCB0byBsb2NhbCBvciByZW1vdGUgc3RhdGUgc3RvcmFnZS5cblxuY2xvdWRmbGFyZV9yZWNvcmQudmVyaWZpY2F0aW9uX3JlY29yZF8zOiBSZWZyZXNoaW5nIHN0YXRlLi4uIChJRDogMmFiMGMxNTUwODE3NDVjYTAwZWZmZWQ1ODQ3ZTViYTcpXG5jbG91ZGZsYXJlX3JlY29yZC52ZXJpZmljYXRpb25fcmVjb3JkXzE6IFJlZnJlc2hpbmcgc3RhdGUuLi4gKElEOiBkMzllNjRlMTBmYjQwZDQ1NjQ1ZTU1OGEzZmMzMzkxMClcbmNsb3VkZmxhcmVfcmVjb3JkLnZlcmlmaWNhdGlvbl9yZWNvcmRfNTogUmVmcmVzaGluZyBzdGF0ZS4uLiAoSUQ6IDE2Nzk1NjhlOGNjZWQ4YWRmNGQwMmYxMjk1MmMxMGQwKVxuY2xvdWRmbGFyZV9yZWNvcmQuc2l0ZXM6IFJlZnJlc2hpbmcgc3RhdGUuLi4gKElEOiBmMTA5Nzg2ZGNkY2JlZjEzZTIyYzZiZjRlOGM5MjEzNilcbmNsb3VkZmxhcmVfcmVjb3JkLmNhbGVuZGFyOiBSZWZyZXNoaW5nIHN0YXRlLi4uIChJRDogMmUwYmRkYjY3Y2UwYjQ4MDJiNzRkMDU3M2JlYjQ1OWIpXG5jbG91ZGZsYXJlX3JlY29yZC5nb29nbGVfbWFpbF9yZWNvcmRfMzogUmVmcmVzaGluZyBzdGF0ZS4uLiAoSUQ6IGFkOTY2NWNmZjZjZDE3YWI2Njk1MGQ5OTY0MGI1N2RkKVxuY2xvdWRmbGFyZV9yZWNvcmQuY29tb2RvX2NlcnRfY29uc29sZTogUmVmcmVzaGluZyBzdGF0ZS4uLiAoSUQ6IGE4NTAxNTM0YzQ3N2RlMDUyMmVjOTI0MDg0NjVlZjM1KVxuY2xvdWRmbGFyZV9yZWNvcmQuY29tb2RvX2NlcnRfcmVjb3Zlcnk6IFJlZnJlc2hpbmcgc3RhdGUuLi4gKElEOiBlMjcwNDNkYmM1YWIwY2JkNmY1NzAzMTgyNzllODI2MClcbmNsb3VkZmxhcmVfcmVjb3JkLmdvb2dsZV9tYWlsX3JlY29yZF80OiBSZWZyZXNoaW5nIHN0YXRlLi4uIChJRDogYmQ2Y2U1OWYyN2ExMWE2ZWRmMmJiNWYzOGI1NDU0YjEpXG5jbG91ZGZsYXJlX3JlY29yZC5tYWlsOiBSZWZyZXNoaW5nIHN0YXRlLi4uIChJRDogYjAwNDAwNjQ0ODMwMzc3Nzk3ZmVjY2NjYjc1ZTE0ZDMpXG5jbG91ZGZsYXJlX3JlY29yZC5nb29nbGVfbWFpbF9yZWNvcmRfMTogUmVmcmVzaGluZyBzdGF0ZS4uLiAoSUQ6IGNhNTY0MmIyYzEzMWUwYjAxMmFmN2FkM2QyNzU4ODZiKVxuY2xvdWRmbGFyZV9yZWNvcmQuY29tb2RvX2NlcnRfd3d3OiBSZWZyZXNoaW5nIHN0YXRlLi4uIChJRDogNjY2NjcxY2I0YTU4MjBhMWI4OGRhYTM0ZTdjNmE0MjEpXG5jbG91ZGZsYXJlX3JlY29yZC5nb29nbGVfbWFpbF9yZWNvcmRfMjogUmVmcmVzaGluZyBzdGF0ZS4uLiAoSUQ6IDJkODIyNDNiYzk1ZjgzODZjOGRkZWI3YjBjMDgzZDk4KVxuY2xvdWRmbGFyZV96b25lLnR3aW5kYi1jaWVfY29tOiBSZWZyZXNoaW5nIHN0YXRlLi4uIChJRDogMDJjZmZjNTgwMjdlYmFiYmUyOTYxNGM2YmY2ZTM3MTYpXG5jbG91ZGZsYXJlX3JlY29yZC5kcml2ZTogUmVmcmVzaGluZyBzdGF0ZS4uLiAoSUQ6IDdmM2UzOGM2M2NlN2QxNjkwMTJlZGY3OWEwMTk1NWYzKVxuY2xvdWRmbGFyZV9yZWNvcmQudmVyaWZpY2F0aW9uX3JlY29yZF8yOiBSZWZyZXNoaW5nIHN0YXRlLi4uIChJRDogMjQ2OGQxOWI2NTY3NTIyNDY2MTI0NjU4YzNhZTFhN2QpXG5jbG91ZGZsYXJlX3JlY29yZC5nb29nbGVfbWFpbF9yZWNvcmRfNTogUmVmcmVzaGluZyBzdGF0ZS4uLiAoSUQ6IDAzMzI3Njg3MTJmYjQwZTgxYWM1YTEwOTczMDE5ZGUyKVxuY2xvdWRmbGFyZV9yZWNvcmQuY29tb2RvX2NlcnRfcm9vdDogUmVmcmVzaGluZyBzdGF0ZS4uLiAoSUQ6IDNhMzI3Y2QzZTkwNTI1MWNjYjU5NWY1YzAwM2M1MTYwKVxuXG4tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cblxuTm8gY2hhbmdlcy4gSW5mcmFzdHJ1Y3R1cmUgaXMgdXAtdG8tZGF0ZS5cblxuVGhpcyBtZWFucyB0aGF0IFRlcnJhZm9ybSBkaWQgbm90IGRldGVjdCBhbnkgZGlmZmVyZW5jZXMgYmV0d2VlbiB5b3VyXG5jb25maWd1cmF0aW9uIGFuZCByZWFsIHBoeXNpY2FsIHJlc291cmNlcyB0aGF0IGV4aXN0LiBBcyBhIHJlc3VsdCwgbm9cbmFjdGlvbnMgbmVlZCB0byBiZSBwZXJmb3JtZWQuXG4iLCAiYWRkIjogMCwgImNoYW5nZSI6IDAsICJkZXN0cm95IjogMH19```
</p>
</details>
"""
    ),
    (
        {
            'cloudflare': {
                'success': True,
                'stderr': b'',
                'stdout': b'foo',
                'add': None,
                'change': None,
                'destroy': None
            }
        },
        """Module | Success | ![#FFFF00](https://placehold.it/15/FFFF00/000000?text=+) Add | ![#FFFF00](https://placehold.it/15/FFFF00/000000?text=+) Change | ![#FFFF00](https://placehold.it/15/FFFF00/000000?text=+) Destroy
--- | --- | ---: | ---: | ---:
**cloudflare** | ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) `True` | Unknown | Unknown | Unknown

# **cloudflare**

## stdout

```foo```

## stderr

_no output_

<details><summary><i>metadata</i></summary>
<p>

```eyJjbG91ZGZsYXJlIjogeyJzdWNjZXNzIjogdHJ1ZSwgInN0ZGVyciI6ICIiLCAic3Rkb3V0IjogImZvbyIsICJhZGQiOiBudWxsLCAiY2hhbmdlIjogbnVsbCwgImRlc3Ryb3kiOiBudWxsfX0=```
</p>
</details>
"""

    )
])
def test_render_comment(status, expected_output):
    """
    Check that output format is valid.
    """
    actual_output = render_comment(status)
    assert actual_output == expected_output

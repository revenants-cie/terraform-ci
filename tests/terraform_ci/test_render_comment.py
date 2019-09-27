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
"""

    )
])
def test_render_comment(status, expected_output):
    """
    Check that output format is valid.
    """
    actual_output = render_comment(status)
    assert actual_output == expected_output

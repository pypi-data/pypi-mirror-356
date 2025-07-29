<!-- speakeasy-ignore-start -->

<div align="center">
  <a href="https://novu.co?utm_source=github" target="_blank">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/2233092/213641039-220ac15f-f367-4d13-9eaf-56e79433b8c1.png">
    <img alt="Novu Logo" src="https://user-images.githubusercontent.com/2233092/213641043-3bbb3f21-3c53-4e67-afe5-755aeb222159.png" width="280"/>
  </picture>
  </a>
</div>

<br/>

<p align="center">
   <a href="https://www.producthunt.com/products/novu">
    <img src="https://img.shields.io/badge/Product%20Hunt-Golden%20Kitty%20Award%202023-yellow" alt="Product Hunt">
  </a>
  <a href="https://news.ycombinator.com/item?id=38419513"><img src="https://img.shields.io/badge/Hacker%20News-%231-%23FF6600" alt="Hacker News"></a>
  <a href="https://www.npmjs.com/package/@novu/node">
    <img src="https://img.shields.io/npm/dm/@novu/node" alt="npm downloads">
  </a>
</p>

<h1 align="center">The &lt;Inbox /&gt; infrastructure for modern products</h1>

<div align="center">
The notification platform that turns complex multi-channel delivery into a single <Inbox /> component. Built for developers, designed for growth, powered by open source.
</div>

<!-- speakeasy-ignore-end -->
  
# Python Novu SDK

[![PyPI](https://img.shields.io/pypi/v/novu-py?color=blue)](https://pypi.org/project/novu-py/)
[![codecov](https://codecov.io/gh/novuhq/novu-python/branch/main/graph/badge.svg?token=RON7F8QTZX)](https://codecov.io/gh/novuhq/novu-python)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/novu)
![PyPI - License](https://img.shields.io/pypi/l/novu)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
---
The Python [Novu](https://novu.co) SDK and package provides a fluent and expressive interface for interacting with [Novu's API](https://docs.novu.co/api-reference) and managing notifications.
<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=novu-py&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>
<br /><br />
<!-- Start Summary [summary] -->
## Summary

Novu API: Novu REST API. Please see https://docs.novu.co/api-reference for more details.

For more information about the API: [Novu Documentation](https://docs.novu.co)
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [Python Novu SDK](https://github.com/novuhq/novu-py/blob/master/#python-novu-sdk)
  * [SDK Installation](https://github.com/novuhq/novu-py/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/novuhq/novu-py/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/novuhq/novu-py/blob/master/#sdk-example-usage)
  * [Available Resources and Operations](https://github.com/novuhq/novu-py/blob/master/#available-resources-and-operations)
  * [Retries](https://github.com/novuhq/novu-py/blob/master/#retries)
  * [Error Handling](https://github.com/novuhq/novu-py/blob/master/#error-handling)
  * [Server Selection](https://github.com/novuhq/novu-py/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/novuhq/novu-py/blob/master/#custom-http-client)
  * [Authentication](https://github.com/novuhq/novu-py/blob/master/#authentication)
  * [Resource Management](https://github.com/novuhq/novu-py/blob/master/#resource-management)
  * [Debugging](https://github.com/novuhq/novu-py/blob/master/#debugging)
* [Development](https://github.com/novuhq/novu-py/blob/master/#development)
  * [Contributions](https://github.com/novuhq/novu-py/blob/master/#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install novu-py
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add novu-py
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from novu-py python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "novu-py",
# ]
# ///

from novu_py import Novu

sdk = Novu(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Trigger Notification Event

```python
# Synchronous Example
import novu_py
from novu_py import Novu


with Novu(
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.trigger(trigger_event_request_dto=novu_py.TriggerEventRequestDto(
        workflow_id="workflow_identifier",
        payload={
            "comment_id": "string",
            "post": {
                "text": "string",
            },
        },
        overrides=novu_py.Overrides(),
        to="SUBSCRIBER_ID",
    ))

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import novu_py
from novu_py import Novu

async def main():

    async with Novu(
        secret_key="YOUR_SECRET_KEY_HERE",
    ) as novu:

        res = await novu.trigger_async(trigger_event_request_dto=novu_py.TriggerEventRequestDto(
            workflow_id="workflow_identifier",
            payload={
                "comment_id": "string",
                "post": {
                    "text": "string",
                },
            },
            overrides=novu_py.Overrides(),
            to="SUBSCRIBER_ID",
        ))

        # Handle response
        print(res)

asyncio.run(main())
```

### Cancel Triggered Event

```python
# Synchronous Example
from novu_py import Novu


with Novu(
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.cancel(transaction_id="<id>")

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from novu_py import Novu

async def main():

    async with Novu(
        secret_key="YOUR_SECRET_KEY_HERE",
    ) as novu:

        res = await novu.cancel_async(transaction_id="<id>")

        # Handle response
        print(res)

asyncio.run(main())
```

### Broadcast Event to All

```python
# Synchronous Example
import novu_py
from novu_py import Novu


with Novu(
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.trigger_broadcast(trigger_event_to_all_request_dto=novu_py.TriggerEventToAllRequestDto(
        name="<value>",
        payload={
            "comment_id": "string",
            "post": {
                "text": "string",
            },
        },
        overrides=novu_py.TriggerEventToAllRequestDtoOverrides(
            **{
                "fcm": {
                    "data": {
                        "key": "value",
                    },
                },
            },
        ),
    ))

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import novu_py
from novu_py import Novu

async def main():

    async with Novu(
        secret_key="YOUR_SECRET_KEY_HERE",
    ) as novu:

        res = await novu.trigger_broadcast_async(trigger_event_to_all_request_dto=novu_py.TriggerEventToAllRequestDto(
            name="<value>",
            payload={
                "comment_id": "string",
                "post": {
                    "text": "string",
                },
            },
            overrides=novu_py.TriggerEventToAllRequestDtoOverrides(
                **{
                    "fcm": {
                        "data": {
                            "key": "value",
                        },
                    },
                },
            ),
        ))

        # Handle response
        print(res)

asyncio.run(main())
```

### Trigger Notification Events in Bulk

```python
# Synchronous Example
import novu_py
from novu_py import Novu


with Novu(
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.trigger_bulk(bulk_trigger_event_dto={
        "events": [
            novu_py.TriggerEventRequestDto(
                workflow_id="workflow_identifier",
                payload={
                    "comment_id": "string",
                    "post": {
                        "text": "string",
                    },
                },
                overrides=novu_py.Overrides(),
                to="SUBSCRIBER_ID",
            ),
            novu_py.TriggerEventRequestDto(
                workflow_id="workflow_identifier",
                payload={
                    "comment_id": "string",
                    "post": {
                        "text": "string",
                    },
                },
                overrides=novu_py.Overrides(),
                to="SUBSCRIBER_ID",
            ),
            novu_py.TriggerEventRequestDto(
                workflow_id="workflow_identifier",
                payload={
                    "comment_id": "string",
                    "post": {
                        "text": "string",
                    },
                },
                overrides=novu_py.Overrides(),
                to="SUBSCRIBER_ID",
            ),
        ],
    })

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import novu_py
from novu_py import Novu

async def main():

    async with Novu(
        secret_key="YOUR_SECRET_KEY_HERE",
    ) as novu:

        res = await novu.trigger_bulk_async(bulk_trigger_event_dto={
            "events": [
                novu_py.TriggerEventRequestDto(
                    workflow_id="workflow_identifier",
                    payload={
                        "comment_id": "string",
                        "post": {
                            "text": "string",
                        },
                    },
                    overrides=novu_py.Overrides(),
                    to="SUBSCRIBER_ID",
                ),
                novu_py.TriggerEventRequestDto(
                    workflow_id="workflow_identifier",
                    payload={
                        "comment_id": "string",
                        "post": {
                            "text": "string",
                        },
                    },
                    overrides=novu_py.Overrides(),
                    to="SUBSCRIBER_ID",
                ),
                novu_py.TriggerEventRequestDto(
                    workflow_id="workflow_identifier",
                    payload={
                        "comment_id": "string",
                        "post": {
                            "text": "string",
                        },
                    },
                    overrides=novu_py.Overrides(),
                    to="SUBSCRIBER_ID",
                ),
            ],
        })

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [environments](https://github.com/novuhq/novu-py/blob/master/docs/sdks/environments/README.md)

* [create](https://github.com/novuhq/novu-py/blob/master/docs/sdks/environments/README.md#create) - Create an environment
* [list](https://github.com/novuhq/novu-py/blob/master/docs/sdks/environments/README.md#list) - List all environments
* [update](https://github.com/novuhq/novu-py/blob/master/docs/sdks/environments/README.md#update) - Update an environment
* [delete](https://github.com/novuhq/novu-py/blob/master/docs/sdks/environments/README.md#delete) - Delete an environment

### [integrations](https://github.com/novuhq/novu-py/blob/master/docs/sdks/integrations/README.md)

* [list](https://github.com/novuhq/novu-py/blob/master/docs/sdks/integrations/README.md#list) - List all integrations
* [create](https://github.com/novuhq/novu-py/blob/master/docs/sdks/integrations/README.md#create) - Create an integration
* [update](https://github.com/novuhq/novu-py/blob/master/docs/sdks/integrations/README.md#update) - Update an integration
* [delete](https://github.com/novuhq/novu-py/blob/master/docs/sdks/integrations/README.md#delete) - Delete an integration
* [set_as_primary](https://github.com/novuhq/novu-py/blob/master/docs/sdks/integrations/README.md#set_as_primary) - Update integration as primary
* [list_active](https://github.com/novuhq/novu-py/blob/master/docs/sdks/integrations/README.md#list_active) - List active integrations

### [messages](https://github.com/novuhq/novu-py/blob/master/docs/sdks/messages/README.md)

* [retrieve](https://github.com/novuhq/novu-py/blob/master/docs/sdks/messages/README.md#retrieve) - List all messages
* [delete](https://github.com/novuhq/novu-py/blob/master/docs/sdks/messages/README.md#delete) - Delete a message
* [delete_by_transaction_id](https://github.com/novuhq/novu-py/blob/master/docs/sdks/messages/README.md#delete_by_transaction_id) - Delete messages by transactionId

### [notifications](https://github.com/novuhq/novu-py/blob/master/docs/sdks/notifications/README.md)

* [list](https://github.com/novuhq/novu-py/blob/master/docs/sdks/notifications/README.md#list) - List all events
* [retrieve](https://github.com/novuhq/novu-py/blob/master/docs/sdks/notifications/README.md#retrieve) - Retrieve an event

### [Novu SDK](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novu/README.md)

* [trigger](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novu/README.md#trigger) - Trigger event
* [cancel](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novu/README.md#cancel) - Cancel triggered event
* [trigger_broadcast](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novu/README.md#trigger_broadcast) - Broadcast event to all
* [trigger_bulk](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novu/README.md#trigger_bulk) - Bulk trigger event

### [subscribers](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscribers/README.md)

* [search](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscribers/README.md#search) - Search subscribers
* [create](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscribers/README.md#create) - Create a subscriber
* [retrieve](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscribers/README.md#retrieve) - Retrieve a subscriber
* [patch](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscribers/README.md#patch) - Update a subscriber
* [delete](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscribers/README.md#delete) - Delete a subscriber
* [create_bulk](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscribers/README.md#create_bulk) - Bulk create subscribers

#### [subscribers.credentials](https://github.com/novuhq/novu-py/blob/master/docs/sdks/credentials/README.md)

* [update](https://github.com/novuhq/novu-py/blob/master/docs/sdks/credentials/README.md#update) - Update provider credentials
* [append](https://github.com/novuhq/novu-py/blob/master/docs/sdks/credentials/README.md#append) - Upsert provider credentials
* [delete](https://github.com/novuhq/novu-py/blob/master/docs/sdks/credentials/README.md#delete) - Delete provider credentials

#### [subscribers.messages](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novumessages/README.md)

* [update_as_seen](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novumessages/README.md#update_as_seen) - Update notification action status
* [mark_all](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novumessages/README.md#mark_all) - Update all notifications state
* [mark_all_as](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novumessages/README.md#mark_all_as) - Update notifications state

#### [subscribers.notifications](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novunotifications/README.md)

* [feed](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novunotifications/README.md#feed) - Retrieve subscriber notifications
* [unseen_count](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novunotifications/README.md#unseen_count) - Retrieve unseen notifications count

#### [subscribers.preferences](https://github.com/novuhq/novu-py/blob/master/docs/sdks/preferences/README.md)

* [list](https://github.com/novuhq/novu-py/blob/master/docs/sdks/preferences/README.md#list) - Retrieve subscriber preferences
* [update](https://github.com/novuhq/novu-py/blob/master/docs/sdks/preferences/README.md#update) - Update subscriber preferences

#### [subscribers.properties](https://github.com/novuhq/novu-py/blob/master/docs/sdks/properties/README.md)

* [update_online_flag](https://github.com/novuhq/novu-py/blob/master/docs/sdks/properties/README.md#update_online_flag) - Update subscriber online status

#### [subscribers.topics](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novutopics/README.md)

* [list](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novutopics/README.md#list) - Retrieve subscriber subscriptions

### [topics](https://github.com/novuhq/novu-py/blob/master/docs/sdks/topics/README.md)

* [list](https://github.com/novuhq/novu-py/blob/master/docs/sdks/topics/README.md#list) - List all topics
* [create](https://github.com/novuhq/novu-py/blob/master/docs/sdks/topics/README.md#create) - Create a topic
* [get](https://github.com/novuhq/novu-py/blob/master/docs/sdks/topics/README.md#get) - Retrieve a topic
* [update](https://github.com/novuhq/novu-py/blob/master/docs/sdks/topics/README.md#update) - Update a topic
* [delete](https://github.com/novuhq/novu-py/blob/master/docs/sdks/topics/README.md#delete) - Delete a topic

#### [topics.subscribers](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novusubscribers/README.md)

* [retrieve](https://github.com/novuhq/novu-py/blob/master/docs/sdks/novusubscribers/README.md#retrieve) - Check topic subscriber

#### [topics.subscriptions](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscriptions/README.md)

* [list](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscriptions/README.md#list) - List topic subscriptions
* [create](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscriptions/README.md#create) - Create topic subscriptions
* [delete](https://github.com/novuhq/novu-py/blob/master/docs/sdks/subscriptions/README.md#delete) - Delete topic subscriptions

### [workflows](https://github.com/novuhq/novu-py/blob/master/docs/sdks/workflows/README.md)

* [create](https://github.com/novuhq/novu-py/blob/master/docs/sdks/workflows/README.md#create) - Create a workflow
* [list](https://github.com/novuhq/novu-py/blob/master/docs/sdks/workflows/README.md#list) - List all workflows
* [update](https://github.com/novuhq/novu-py/blob/master/docs/sdks/workflows/README.md#update) - Update a workflow
* [get](https://github.com/novuhq/novu-py/blob/master/docs/sdks/workflows/README.md#get) - Retrieve a workflow
* [delete](https://github.com/novuhq/novu-py/blob/master/docs/sdks/workflows/README.md#delete) - Delete a workflow
* [patch](https://github.com/novuhq/novu-py/blob/master/docs/sdks/workflows/README.md#patch) - Update a workflow
* [sync](https://github.com/novuhq/novu-py/blob/master/docs/sdks/workflows/README.md#sync) - Sync a workflow

#### [workflows.steps](https://github.com/novuhq/novu-py/blob/master/docs/sdks/steps/README.md)

* [retrieve](https://github.com/novuhq/novu-py/blob/master/docs/sdks/steps/README.md#retrieve) - Retrieve workflow step

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import novu_py
from novu_py import Novu
from novu_py.utils import BackoffStrategy, RetryConfig


with Novu(
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.trigger(trigger_event_request_dto=novu_py.TriggerEventRequestDto(
        workflow_id="workflow_identifier",
        payload={
            "comment_id": "string",
            "post": {
                "text": "string",
            },
        },
        overrides=novu_py.Overrides(),
        to="SUBSCRIBER_ID",
    ),
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import novu_py
from novu_py import Novu
from novu_py.utils import BackoffStrategy, RetryConfig


with Novu(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.trigger(trigger_event_request_dto=novu_py.TriggerEventRequestDto(
        workflow_id="workflow_identifier",
        payload={
            "comment_id": "string",
            "post": {
                "text": "string",
            },
        },
        overrides=novu_py.Overrides(),
        to="SUBSCRIBER_ID",
    ))

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `trigger_async` method may raise the following exceptions:

| Error Type                           | Status Code                       | Content Type     |
| ------------------------------------ | --------------------------------- | ---------------- |
| models.PayloadValidationExceptionDto | 400                               | application/json |
| models.ErrorDto                      | 414                               | application/json |
| models.ErrorDto                      | 401, 403, 404, 405, 409, 413, 415 | application/json |
| models.ValidationErrorDto            | 422                               | application/json |
| models.ErrorDto                      | 500                               | application/json |
| models.APIError                      | 4XX, 5XX                          | \*/\*            |

### Example

```python
import novu_py
from novu_py import Novu, models


with Novu(
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:
    res = None
    try:

        res = novu.trigger(trigger_event_request_dto=novu_py.TriggerEventRequestDto(
            workflow_id="workflow_identifier",
            payload={
                "comment_id": "string",
                "post": {
                    "text": "string",
                },
            },
            overrides=novu_py.Overrides(),
            to="SUBSCRIBER_ID",
        ))

        # Handle response
        print(res)

    except models.PayloadValidationExceptionDto as e:
        # handle e.data: models.PayloadValidationExceptionDtoData
        raise(e)
    except models.ErrorDto as e:
        # handle e.data: models.ErrorDtoData
        raise(e)
    except models.ErrorDto as e:
        # handle e.data: models.ErrorDtoData
        raise(e)
    except models.ValidationErrorDto as e:
        # handle e.data: models.ValidationErrorDtoData
        raise(e)
    except models.ErrorDto as e:
        # handle e.data: models.ErrorDtoData
        raise(e)
    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Index

You can override the default server globally by passing a server index to the `server_idx: int` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the indexes associated with the available servers:

| #   | Server                   | Description |
| --- | ------------------------ | ----------- |
| 0   | `https://api.novu.co`    |             |
| 1   | `https://eu.api.novu.co` |             |

#### Example

```python
import novu_py
from novu_py import Novu


with Novu(
    server_idx=1,
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.trigger(trigger_event_request_dto=novu_py.TriggerEventRequestDto(
        workflow_id="workflow_identifier",
        payload={
            "comment_id": "string",
            "post": {
                "text": "string",
            },
        },
        overrides=novu_py.Overrides(),
        to="SUBSCRIBER_ID",
    ))

    # Handle response
    print(res)

```

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import novu_py
from novu_py import Novu


with Novu(
    server_url="https://eu.api.novu.co",
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.trigger(trigger_event_request_dto=novu_py.TriggerEventRequestDto(
        workflow_id="workflow_identifier",
        payload={
            "comment_id": "string",
            "post": {
                "text": "string",
            },
        },
        overrides=novu_py.Overrides(),
        to="SUBSCRIBER_ID",
    ))

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from novu_py import Novu
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Novu(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from novu_py import Novu
from novu_py.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Novu(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name         | Type   | Scheme  | Environment Variable |
| ------------ | ------ | ------- | -------------------- |
| `secret_key` | apiKey | API key | `NOVU_SECRET_KEY`    |

To authenticate with the API the `secret_key` parameter must be set when initializing the SDK client instance. For example:
```python
import novu_py
from novu_py import Novu


with Novu(
    secret_key="YOUR_SECRET_KEY_HERE",
) as novu:

    res = novu.trigger(trigger_event_request_dto=novu_py.TriggerEventRequestDto(
        workflow_id="workflow_identifier",
        payload={
            "comment_id": "string",
            "post": {
                "text": "string",
            },
        },
        overrides=novu_py.Overrides(),
        to="SUBSCRIBER_ID",
    ))

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Novu` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from novu_py import Novu
def main():

    with Novu(
        secret_key="YOUR_SECRET_KEY_HERE",
    ) as novu:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Novu(
        secret_key="YOUR_SECRET_KEY_HERE",
    ) as novu:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from novu_py import Novu
import logging

logging.basicConfig(level=logging.DEBUG)
s = Novu(debug_logger=logging.getLogger("novu_py"))
```

You can also enable a default debug logger by setting an environment variable `NOVU_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=novu-py&utm_campaign=python)

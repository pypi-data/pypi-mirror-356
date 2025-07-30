# V1

## Boxes

Types:

```python
from gbox_sdk.types.v1 import (
    AndroidBox,
    CreateAndroidBox,
    CreateBoxConfig,
    CreateLinuxBox,
    LinuxBox,
    BoxCreateResponse,
    BoxRetrieveResponse,
    BoxListResponse,
    BoxExecuteCommandsResponse,
    BoxRunCodeResponse,
    BoxStartResponse,
    BoxStopResponse,
)
```

Methods:

- <code title="post /api/v1/boxes">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">create</a>(\*\*<a href="src/gbox_sdk/types/v1/box_create_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/box_create_response.py">BoxCreateResponse</a></code>
- <code title="get /api/v1/boxes/{id}">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">retrieve</a>(id) -> <a href="./src/gbox_sdk/types/v1/box_retrieve_response.py">BoxRetrieveResponse</a></code>
- <code title="get /api/v1/boxes">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">list</a>(\*\*<a href="src/gbox_sdk/types/v1/box_list_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/box_list_response.py">BoxListResponse</a></code>
- <code title="post /api/v1/boxes/android">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">create_android</a>(\*\*<a href="src/gbox_sdk/types/v1/box_create_android_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/android_box.py">AndroidBox</a></code>
- <code title="post /api/v1/boxes/linux">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">create_linux</a>(\*\*<a href="src/gbox_sdk/types/v1/box_create_linux_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/linux_box.py">LinuxBox</a></code>
- <code title="post /api/v1/boxes/{id}/commands">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">execute_commands</a>(id, \*\*<a href="src/gbox_sdk/types/v1/box_execute_commands_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/box_execute_commands_response.py">BoxExecuteCommandsResponse</a></code>
- <code title="post /api/v1/boxes/{id}/run-code">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">run_code</a>(id, \*\*<a href="src/gbox_sdk/types/v1/box_run_code_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/box_run_code_response.py">BoxRunCodeResponse</a></code>
- <code title="post /api/v1/boxes/{id}/start">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">start</a>(id) -> <a href="./src/gbox_sdk/types/v1/box_start_response.py">BoxStartResponse</a></code>
- <code title="post /api/v1/boxes/{id}/stop">client.v1.boxes.<a href="./src/gbox_sdk/resources/v1/boxes/boxes.py">stop</a>(id) -> <a href="./src/gbox_sdk/types/v1/box_stop_response.py">BoxStopResponse</a></code>

### Actions

Types:

```python
from gbox_sdk.types.v1.boxes import ActionResult, ActionScreenshotResponse
```

Methods:

- <code title="post /api/v1/boxes/{id}/actions/click">client.v1.boxes.actions.<a href="./src/gbox_sdk/resources/v1/boxes/actions.py">click</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/action_click_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/action_result.py">ActionResult</a></code>
- <code title="post /api/v1/boxes/{id}/actions/drag">client.v1.boxes.actions.<a href="./src/gbox_sdk/resources/v1/boxes/actions.py">drag</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/action_drag_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/action_result.py">ActionResult</a></code>
- <code title="post /api/v1/boxes/{id}/actions/move">client.v1.boxes.actions.<a href="./src/gbox_sdk/resources/v1/boxes/actions.py">move</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/action_move_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/action_result.py">ActionResult</a></code>
- <code title="post /api/v1/boxes/{id}/actions/press">client.v1.boxes.actions.<a href="./src/gbox_sdk/resources/v1/boxes/actions.py">press</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/action_press_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/action_result.py">ActionResult</a></code>
- <code title="post /api/v1/boxes/{id}/actions/screenshot">client.v1.boxes.actions.<a href="./src/gbox_sdk/resources/v1/boxes/actions.py">screenshot</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/action_screenshot_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/action_screenshot_response.py">ActionScreenshotResponse</a></code>
- <code title="post /api/v1/boxes/{id}/actions/scroll">client.v1.boxes.actions.<a href="./src/gbox_sdk/resources/v1/boxes/actions.py">scroll</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/action_scroll_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/action_result.py">ActionResult</a></code>
- <code title="post /api/v1/boxes/{id}/actions/touch">client.v1.boxes.actions.<a href="./src/gbox_sdk/resources/v1/boxes/actions.py">touch</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/action_touch_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/action_result.py">ActionResult</a></code>
- <code title="post /api/v1/boxes/{id}/actions/type">client.v1.boxes.actions.<a href="./src/gbox_sdk/resources/v1/boxes/actions.py">type</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/action_type_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/action_result.py">ActionResult</a></code>

### Fs

Types:

```python
from gbox_sdk.types.v1.boxes import FListResponse, FReadResponse, FWriteResponse
```

Methods:

- <code title="get /api/v1/boxes/{id}/fs/list">client.v1.boxes.fs.<a href="./src/gbox_sdk/resources/v1/boxes/fs.py">list</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/f_list_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/f_list_response.py">FListResponse</a></code>
- <code title="get /api/v1/boxes/{id}/fs/read">client.v1.boxes.fs.<a href="./src/gbox_sdk/resources/v1/boxes/fs.py">read</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/f_read_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/f_read_response.py">FReadResponse</a></code>
- <code title="post /api/v1/boxes/{id}/fs/write">client.v1.boxes.fs.<a href="./src/gbox_sdk/resources/v1/boxes/fs.py">write</a>(id, \*\*<a href="src/gbox_sdk/types/v1/boxes/f_write_params.py">params</a>) -> <a href="./src/gbox_sdk/types/v1/boxes/f_write_response.py">FWriteResponse</a></code>

### Browser

Types:

```python
from gbox_sdk.types.v1.boxes import BrowserCdpURLResponse, BrowserConnectURLResponse
```

Methods:

- <code title="get /api/v1/boxes/{id}/browser/connect-url/cdp">client.v1.boxes.browser.<a href="./src/gbox_sdk/resources/v1/boxes/browser.py">cdp_url</a>(id) -> str</code>
- <code title="get /api/v1/boxes/{id}/browser/connect-url">client.v1.boxes.browser.<a href="./src/gbox_sdk/resources/v1/boxes/browser.py">connect_url</a>(id) -> <a href="./src/gbox_sdk/types/v1/boxes/browser_connect_url_response.py">BrowserConnectURLResponse</a></code>


## Complete code
Get completions based on the current model, settings and code

### Request
| Property         | Value                   |
| ---------------- | ----------------------- |
| Method           | POST                    |
| Route            | `/v1/complete/gpt`      |
| Content-Type     | `application/json`      |


### Body parameters
| Parameter             | Type                                                                  | Description                                                                                                               |
| --------------------- |:---------------------------------------------------------------------:| :-------------------------------------------------------------------------------------------------------------------------|
| code                  | string                                                                | Code used to complete (full context)                                                                                  |
| filename              | string                                                                | Filename (ex. `test.py`)                                                                                                  |
| mode                  | string (supported values: `ONE_TOKEN`, `FULL_LINE`)                   | Completion mode                                                                                                           |
| offset                | int                                                                   | Cursor's offset when called completion                                                                                    |
| prefix                | string                                                                | Last token before space or another symbol, used for correct completion in IDEA (ex. for `find(va⎮)` must return `va`)     |
| model                 | string (supported one of models from config, default `best`)          | Completion model                                                                                                          |
| num_iterations        | int (default `10`)                                                    |                                                                                                                           |
| beam_size             | int (default `3`)                                                     |                                                                                                                           |
| diversity_groups      | int (default `1`)                                                     |                                                                                                                           |
| diversity_strength    | double (default `0.3`)                                                |                                                                                                                           |
| len_norm_base         | double (default `0.3`)                                                |                                                                                                                           |
| len_norm_pow          | double (default `2.0`)                                                |                                                                                                                           |
| group_answers         | boolean(default `false`)                                              |                                                                                                                           |
| top_n                 | int (default `5`)                                                     | Pass it if you want to set maximum amount of suggestions, otherwise set null                                              |
| group_top_n           | int (default `5`)                                                     |                                                                                                                           |
| only_full_lines       | boolean (default `true`)                                              |                                                                                                                           |

### Returns
1. 200 -- Success
1. 204 -- Request was canceled by server
1. 500 -- Internal server error

### Example
```json
{
  "code": "import num\nimport os",
  "prefix": "num",
  "offset": 10,
  "filename": "test.py",
  "mode": "FULL_LINE",
  "num_iterations": 10,
  "beam_size": 3,
  "diversity_groups": 3,
  "diversity_strength": 0.3,
  "top_n": 5,
  "only_full_lines": true
}
```
**Successful Response**
```json
{
  "completions": [
    "numpy as np",
    "numpy",
    "numpy # np"
  ]
}
```
**Unsuccessful Response**
```json
{
  "error": {
    "code": 500,
    "issue": {
      "message": "<EXCEPTION_MESSAGE>"
    },
    "message": "<API_EXCEPTION_CLASS>",
    "type": "<EXCEPTION_CLASS>"
  }
}
```

# Benchmarks

## Runtime durations

`max_sample = 50` and `num_workers = 2`

|          | create_save_quantized | create_quantized_model | default |
| :------- | :-------------------: | ---------------------: | ------: |
| Duration |         13.64         |                     15 |      29 |
|          |          14           |                   13.4 |      29 |

`max_sample = 100` and `num_workers = 2`

|          | create_save_quantized | create_quantized_model | default |
| :------- | :-------------------: | ---------------------: | ------: |
| Duration |         25.6          |                  28.13 |      60 |
|          |         27.8          |                  28.73 |      61 |

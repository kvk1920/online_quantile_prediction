# online_quantile_prediction

Prepare:
```shell
pip3 install -r requirements.txt
```

Run experiment:
```shell
python3 -m src run ficnn -uc ficnn_ds3
```

Run visualization:
```shell
python3 -m src visualize quantiles test_data3 ficnn_ds3 ficnn_ds3_q test_layout3
python3 -m src visualize crps test_data3 ficnn_ds3 ficnn_ds3_q test_layout3
```

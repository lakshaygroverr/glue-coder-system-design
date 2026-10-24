# Measured results (100 users, ramp 20/s, 25 s, Windows desktop)

| Setup | Median ms | Avg ms | Requests/s | Failures % | Requests |
|---|---|---|---|---|---|
| 1_one_worker | 5000 | 4888 | 13.1 | 94.9 | 315 |
| 2_ten_threads | 1300 | 1281 | 32.9 | 1.5 | 792 |
| 3_cached | 2 | 53 | 61.1 | 0.8 | 1474 |
| 4_three_servers_lb | 3 | 13 | 62.5 | 0.0 | 1510 |
| 5_lb_kill_8002 | 4 | 219 | 54.3 | 1.6 | 1309 |

Load balancer log when 8002 was killed: `server 8002 is down, skipping`

# FOD ARGUS laptop benchmarking

| Configuration | Status | Unit | Unique inputs | Observations | Mean ms | Median ms | P95 ms | Max ms | Throughput/s |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| crops | completed | frame | 30 | 30 | 32.943 | 29.431 | 52.130 | 60.518 | 30.355 |
| patchcore | completed | frame | 30 | 30 | 30.771 | 27.888 | 47.417 | 50.893 | 32.498 |
| fod | completed | crop | 28 | 28 | 29.872 | 28.937 | 36.017 | 46.455 | 33.476 |
| crack | completed | crop | 28 | 28 | 28.748 | 27.152 | 36.273 | 37.768 | 34.785 |
| coordinates | completed | detection | 18 | 18 | 0.021 | 0.022 | 0.026 | 0.026 | 46838.409 |
| thermal_sampling | completed | frame | 30 | 30 | 4.579 | 4.210 | 7.589 | 7.862 | 218.406 |
| thermal | completed | frame | 30 | 30 | 33.064 | 23.829 | 51.202 | 135.077 | 30.245 |
| Sequential 2 (skips crack on FOD detection) | completed | frame | 30 | 30 | 71.953 | 57.626 | 163.073 | 234.060 | 13.898 |
| Parallel | completed | frame | 30 | 30 | 88.826 | 80.055 | 184.630 | 242.217 | 11.258 |
| patchcore | completed | frame | 30 | 90 | 29.891 | 25.933 | 45.004 | 49.215 | 33.455 |
| fod | completed | crop | 28 | 84 | 32.135 | 25.681 | 51.366 | 53.099 | 31.119 |
| crack | completed | crop | 28 | 84 | 32.169 | 33.352 | 34.560 | 36.020 | 31.086 |
| coordinates | completed | detection | 18 | 54 | 0.021 | 0.021 | 0.024 | 0.026 | 47145.100 |
| thermal_sampling | completed | frame | 30 | 90 | 4.082 | 4.259 | 7.345 | 7.719 | 244.998 |
| thermal | completed | frame | 30 | 90 | 30.337 | 22.657 | 47.473 | 151.366 | 32.963 |
| Sequential 2 (skips crack on FOD detection) | completed | frame | 30 | 90 | 72.870 | 59.338 | 174.765 | 222.852 | 13.723 |
| Parallel | completed | frame | 30 | 90 | 87.342 | 72.356 | 189.063 | 236.972 | 11.449 |
| Sequential 1 (runs both models) | completed | frame | 30 | 30 | 95.662 | 75.048 | 229.020 | 301.182 | 10.453 |
| Sequential 1 (runs both models) | completed | frame | 30 | 90 | 99.185 | 80.431 | 234.196 | 306.702 | 10.082 |

Throughput = completed observations / sum of directly measured processing seconds.
Each row is one run; repetitions reuse the same unique inputs. Crop throughput is separate from frame throughput.
See status.json for failures and unprocessed counts. No camera, Jetson, accuracy or 5 mm claims.
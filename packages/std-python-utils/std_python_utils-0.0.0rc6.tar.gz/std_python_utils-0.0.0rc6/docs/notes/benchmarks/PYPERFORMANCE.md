Benchmarks with tag 'apps':
===========================

| Benchmark      | pynorm313 | py313                  | py314                  | py314free              |
|----------------|:---------:|:----------------------:|:----------------------:|:----------------------:|
| 2to3           | 195 ms    | 183 ms: 1.06x faster   | 177 ms: 1.10x faster   | not significant        |
| docutils       | 1.73 sec  | 1.69 sec: 1.02x faster | 1.84 sec: 1.07x slower | 1.88 sec: 1.09x slower |
| html5lib       | 48.1 ms   | 42.3 ms: 1.14x faster  | 39.8 ms: 1.21x faster  | 39.7 ms: 1.21x faster  |
| Geometric mean | (ref)     | 1.07x faster           | 1.08x faster           | 1.02x faster           |

Benchmarks with tag 'math':
===========================

| Benchmark      | pynorm313 | py313                 | py314                 | py314free             |
|----------------|:---------:|:---------------------:|:---------------------:|:---------------------:|
| float          | 49.7 ms   | 58.4 ms: 1.18x slower | not significant       | not significant       |
| nbody          | 60.8 ms   | 75.2 ms: 1.24x slower | 55.9 ms: 1.09x faster | 84.7 ms: 1.39x slower |
| pidigits       | 139 ms    | 163 ms: 1.17x slower  | 152 ms: 1.10x slower  | 157 ms: 1.13x slower  |
| Geometric mean | (ref)     | 1.19x slower          | 1.01x faster          | 1.16x slower          |

Benchmarks with tag 'regex':
============================

| Benchmark      | pynorm313 | py313                 | py314                 | py314free             |
|----------------|:---------:|:---------------------:|:---------------------:|:---------------------:|
| regex_compile  | 92.2 ms   | 86.3 ms: 1.07x faster | 75.4 ms: 1.22x faster | not significant       |
| regex_dna      | 123 ms    | 121 ms: 1.01x faster  | not significant       | 124 ms: 1.01x slower  |
| regex_v8       | 14.2 ms   | 14.9 ms: 1.05x slower | 14.4 ms: 1.01x slower | 15.0 ms: 1.05x slower |
| Geometric mean | (ref)     | 1.01x faster          | 1.04x faster          | 1.02x slower          |

Benchmark hidden because not significant (1): regex_effbot

Benchmarks with tag 'serialize':
================================

| Benchmark            | pynorm313 | py313                  | py314                  | py314free              |
|----------------------|:---------:|:----------------------:|:----------------------:|:----------------------:|
| json_dumps           | 6.24 ms   | not significant        | 6.75 ms: 1.08x slower  | 8.05 ms: 1.29x slower  |
| json_loads           | 14.1 us   | 16.4 us: 1.16x slower  | 16.3 us: 1.16x slower  | 17.4 us: 1.24x slower  |
| pickle               | 6.45 us   | 6.76 us: 1.05x slower  | 6.87 us: 1.06x slower  | 6.66 us: 1.03x slower  |
| pickle_dict          | 18.0 us   | 15.0 us: 1.20x faster  | 13.1 us: 1.37x faster  | 16.5 us: 1.09x faster  |
| pickle_list          | 2.82 us   | 2.39 us: 1.18x faster  | 2.24 us: 1.26x faster  | 2.50 us: 1.13x faster  |
| pickle_pure_python   | 232 us    | not significant        | 187 us: 1.24x faster   | 205 us: 1.13x faster   |
| tomli_loads          | 1.50 sec  | 1.47 sec: 1.02x faster | 1.24 sec: 1.20x faster | 1.44 sec: 1.04x faster |
| unpickle             | 8.03 us   | 8.40 us: 1.05x slower  | 8.60 us: 1.07x slower  | 9.42 us: 1.17x slower  |
| unpickle_list        | 2.48 us   | 2.52 us: 1.01x slower  | 2.78 us: 1.12x slower  | 3.08 us: 1.24x slower  |
| unpickle_pure_python | 140 us    | 134 us: 1.05x faster   | 112 us: 1.25x faster   | not significant        |
| xml_etree_parse      | 88.3 ms   | 150 ms: 1.70x slower   | 155 ms: 1.75x slower   | 161 ms: 1.82x slower   |
| xml_etree_iterparse  | 59.5 ms   | 83.7 ms: 1.41x slower  | 89.6 ms: 1.51x slower  | 74.9 ms: 1.26x slower  |
| xml_etree_generate   | 47.6 ms   | 53.5 ms: 1.12x slower  | 49.6 ms: 1.04x slower  | 56.5 ms: 1.19x slower  |
| xml_etree_process    | 34.8 ms   | 37.9 ms: 1.09x slower  | not significant        | 38.7 ms: 1.11x slower  |
| Geometric mean       | (ref)     | 1.07x slower           | 1.02x slower           | 1.12x slower           |

Benchmarks with tag 'startup':
==============================

| Benchmark              | pynorm313 | py313                 | py314                 | py314free             |
|------------------------|:---------:|:---------------------:|:---------------------:|:---------------------:|
| python_startup         | 9.42 ms   | 10.4 ms: 1.11x slower | 10.4 ms: 1.10x slower | 12.4 ms: 1.31x slower |
| python_startup_no_site | 6.69 ms   | 7.92 ms: 1.18x slower | 7.90 ms: 1.18x slower | 9.51 ms: 1.42x slower |
| Geometric mean         | (ref)     | 1.15x slower          | 1.14x slower          | 1.37x slower          |

Benchmarks with tag 'template':
===============================

| Benchmark       | pynorm313 | py313                 | py314                 | py314free             |
|-----------------|:---------:|:---------------------:|:---------------------:|:---------------------:|
| django_template | 26.1 ms   | 24.1 ms: 1.08x faster | 22.7 ms: 1.15x faster | not significant       |
| genshi_text     | 18.2 ms   | 16.2 ms: 1.12x faster | 13.9 ms: 1.31x faster | 16.4 ms: 1.11x faster |
| genshi_xml      | 39.7 ms   | 34.1 ms: 1.16x faster | 29.8 ms: 1.33x faster | not significant       |
| mako            | 6.37 ms   | 7.26 ms: 1.14x slower | not significant       | 10.3 ms: 1.62x slower |
| Geometric mean  | (ref)     | 1.06x faster          | 1.17x faster          | 1.09x slower          |

All benchmarks:
===============

| Benchmark                | pynorm313 | py313                  | py314                  | py314free              |
|--------------------------|:---------:|:----------------------:|:----------------------:|:----------------------:|
| 2to3                     | 195 ms    | 183 ms: 1.06x faster   | 177 ms: 1.10x faster   | not significant        |
| async_generators         | 257 ms    | 313 ms: 1.22x slower   | 283 ms: 1.10x slower   | 315 ms: 1.22x slower   |
| asyncio_websockets       | 264 ms    | 732 ms: 2.78x slower   | 739 ms: 2.80x slower   | 734 ms: 2.78x slower   |
| chaos                    | 41.3 ms   | not significant        | 36.3 ms: 1.14x faster  | 43.8 ms: 1.06x slower  |
| comprehensions           | 12.0 us   | not significant        | 9.47 us: 1.27x faster  | 10.7 us: 1.13x faster  |
| bench_mp_pool            | 5.59 ms   | 6.15 ms: 1.10x slower  | 32.1 ms: 5.74x slower  | 21.0 ms: 3.76x slower  |
| bench_thread_pool        | 884 us    | 822 us: 1.08x faster   | not significant        | 1.12 ms: 1.26x slower  |
| coroutines               | 13.2 ms   | 16.0 ms: 1.21x slower  | not significant        | 12.4 ms: 1.06x faster  |
| coverage                 | 48.0 ms   | not significant        | not significant        | 53.8 ms: 1.12x slower  |
| crypto_pyaes             | 45.0 ms   | 51.1 ms: 1.14x slower  | not significant        | 54.1 ms: 1.20x slower  |
| deepcopy                 | 276 us    | 255 us: 1.08x faster   | 155 us: 1.78x faster   | 191 us: 1.44x faster   |
| deepcopy_reduce          | 2.35 us   | 2.17 us: 1.08x faster  | 1.61 us: 1.45x faster  | 2.02 us: 1.16x faster  |
| deepcopy_memo            | 25.4 us   | 27.8 us: 1.10x slower  | 16.1 us: 1.58x faster  | 20.3 us: 1.25x faster  |
| deltablue                | 2.51 ms   | 2.00 ms: 1.25x faster  | 1.74 ms: 1.44x faster  | 2.73 ms: 1.09x slower  |
| django_template          | 26.1 ms   | 24.1 ms: 1.08x faster  | 22.7 ms: 1.15x faster  | not significant        |
| docutils                 | 1.73 sec  | 1.69 sec: 1.02x faster | 1.84 sec: 1.07x slower | 1.88 sec: 1.09x slower |
| fannkuch                 | 248 ms    | 289 ms: 1.17x slower   | not significant        | 289 ms: 1.16x slower   |
| float                    | 49.7 ms   | 58.4 ms: 1.18x slower  | not significant        | not significant        |
| create_gc_cycles         | 976 us    | 1.06 ms: 1.09x slower  | 1.17 ms: 1.20x slower  | 687 us: 1.42x faster   |
| gc_traversal             | 2.60 ms   | not significant        | not significant        | 1.08 ms: 2.41x faster  |
| generators               | 21.2 ms   | not significant        | 17.4 ms: 1.22x faster  | not significant        |
| genshi_text              | 18.2 ms   | 16.2 ms: 1.12x faster  | 13.9 ms: 1.31x faster  | 16.4 ms: 1.11x faster  |
| genshi_xml               | 39.7 ms   | 34.1 ms: 1.16x faster  | 29.8 ms: 1.33x faster  | not significant        |
| go                       | 109 ms    | 99.4 ms: 1.10x faster  | 74.5 ms: 1.47x faster  | 85.7 ms: 1.28x faster  |
| hexiom                   | 4.37 ms   | not significant        | 3.42 ms: 1.28x faster  | not significant        |
| html5lib                 | 48.1 ms   | 42.3 ms: 1.14x faster  | 39.8 ms: 1.21x faster  | 39.7 ms: 1.21x faster  |
| json_dumps               | 6.24 ms   | not significant        | 6.75 ms: 1.08x slower  | 8.05 ms: 1.29x slower  |
| json_loads               | 14.1 us   | 16.4 us: 1.16x slower  | 16.3 us: 1.16x slower  | 17.4 us: 1.24x slower  |
| logging_format           | 4.48 us   | 4.11 us: 1.09x faster  | 3.96 us: 1.13x faster  | 4.73 us: 1.06x slower  |
| logging_silent           | 61.0 ns   | 60.4 ns: 1.01x faster  | 52.6 ns: 1.16x faster  | 54.3 ns: 1.12x faster  |
| logging_simple           | 4.01 us   | not significant        | 3.61 us: 1.11x faster  | 4.22 us: 1.05x slower  |
| mako                     | 6.37 ms   | 7.26 ms: 1.14x slower  | not significant        | 10.3 ms: 1.62x slower  |
| mdp                      | 1.52 sec  | 1.56 sec: 1.03x slower | 1.58 sec: 1.04x slower | 1.70 sec: 1.12x slower |
| meteor_contest           | 79.8 ms   | not significant        | not significant        | 86.9 ms: 1.09x slower  |
| nbody                    | 60.8 ms   | 75.2 ms: 1.24x slower  | 55.9 ms: 1.09x faster  | 84.7 ms: 1.39x slower  |
| nqueens                  | 62.9 ms   | not significant        | 57.7 ms: 1.09x faster  | 68.5 ms: 1.09x slower  |
| pathlib                  | 11.3 ms   | not significant        | 9.73 ms: 1.16x faster  | 10.2 ms: 1.11x faster  |
| pickle                   | 6.45 us   | 6.76 us: 1.05x slower  | 6.87 us: 1.06x slower  | 6.66 us: 1.03x slower  |
| pickle_dict              | 18.0 us   | 15.0 us: 1.20x faster  | 13.1 us: 1.37x faster  | 16.5 us: 1.09x faster  |
| pickle_list              | 2.82 us   | 2.39 us: 1.18x faster  | 2.24 us: 1.26x faster  | 2.50 us: 1.13x faster  |
| pickle_pure_python       | 232 us    | not significant        | 187 us: 1.24x faster   | 205 us: 1.13x faster   |
| pidigits                 | 139 ms    | 163 ms: 1.17x slower   | 152 ms: 1.10x slower   | 157 ms: 1.13x slower   |
| pprint_safe_repr         | 530 ms    | 581 ms: 1.10x slower   | 476 ms: 1.11x faster   | not significant        |
| pprint_pformat           | 1.09 sec  | 1.19 sec: 1.09x slower | 957 ms: 1.14x faster   | not significant        |
| pyflate                  | 336 ms    | not significant        | 256 ms: 1.31x faster   | 308 ms: 1.09x faster   |
| python_startup           | 9.42 ms   | 10.4 ms: 1.11x slower  | 10.4 ms: 1.10x slower  | 12.4 ms: 1.31x slower  |
| python_startup_no_site   | 6.69 ms   | 7.92 ms: 1.18x slower  | 7.90 ms: 1.18x slower  | 9.51 ms: 1.42x slower  |
| raytrace                 | 183 ms    | 171 ms: 1.07x faster   | 166 ms: 1.10x faster   | 206 ms: 1.13x slower   |
| regex_compile            | 92.2 ms   | 86.3 ms: 1.07x faster  | 75.4 ms: 1.22x faster  | not significant        |
| regex_dna                | 123 ms    | 121 ms: 1.01x faster   | not significant        | 124 ms: 1.01x slower   |
| regex_v8                 | 14.2 ms   | 14.9 ms: 1.05x slower  | 14.4 ms: 1.01x slower  | 15.0 ms: 1.05x slower  |
| richards                 | 35.5 ms   | 28.9 ms: 1.23x faster  | 24.6 ms: 1.44x faster  | 29.7 ms: 1.20x faster  |
| richards_super           | 39.9 ms   | 32.1 ms: 1.24x faster  | 27.2 ms: 1.46x faster  | 37.0 ms: 1.08x faster  |
| scimark_fft              | 175 ms    | 195 ms: 1.12x slower   | not significant        | 227 ms: 1.30x slower   |
| scimark_lu               | 59.8 ms   | 56.5 ms: 1.06x faster  | not significant        | 65.2 ms: 1.09x slower  |
| scimark_monte_carlo      | 42.8 ms   | not significant        | 35.1 ms: 1.22x faster  | 46.9 ms: 1.10x slower  |
| scimark_sor              | 90.7 ms   | 80.1 ms: 1.13x faster  | 59.6 ms: 1.52x faster  | 75.5 ms: 1.20x faster  |
| scimark_sparse_mat_mult  | 2.47 ms   | not significant        | not significant        | 3.50 ms: 1.41x slower  |
| spectral_norm            | 55.3 ms   | 72.1 ms: 1.30x slower  | not significant        | 70.7 ms: 1.28x slower  |
| sqlglot_normalize        | 189 ms    | not significant        | 199 ms: 1.05x slower   | 208 ms: 1.10x slower   |
| sqlglot_optimize         | 36.1 ms   | not significant        | not significant        | 39.5 ms: 1.09x slower  |
| sqlglot_parse            | 851 us    | 805 us: 1.06x faster   | 774 us: 1.10x faster   | 942 us: 1.11x slower   |
| sqlglot_transpile        | 1.08 ms   | 1.03 ms: 1.05x faster  | 963 us: 1.12x faster   | 1.20 ms: 1.11x slower  |
| sqlite_synth             | 1.34 us   | 1.78 us: 1.33x slower  | 1.93 us: 1.44x slower  | 1.78 us: 1.34x slower  |
| sympy_expand             | 289 ms    | 287 ms: 1.01x faster   | 313 ms: 1.08x slower   | 329 ms: 1.14x slower   |
| sympy_integrate          | 13.3 ms   | 13.0 ms: 1.03x faster  | not significant        | 15.1 ms: 1.13x slower  |
| sympy_sum                | 89.6 ms   | 88.3 ms: 1.01x faster  | 95.2 ms: 1.06x slower  | 104 ms: 1.16x slower   |
| sympy_str                | 170 ms    | 168 ms: 1.01x faster   | not significant        | 190 ms: 1.12x slower   |
| telco                    | 4.47 ms   | 5.21 ms: 1.17x slower  | 4.86 ms: 1.09x slower  | 5.76 ms: 1.29x slower  |
| tomli_loads              | 1.50 sec  | 1.47 sec: 1.02x faster | 1.24 sec: 1.20x faster | 1.44 sec: 1.04x faster |
| typing_runtime_protocols | 107 us    | 104 us: 1.02x faster   | 101 us: 1.05x faster   | 126 us: 1.18x slower   |
| unpack_sequence          | 29.4 ns   | 33.5 ns: 1.14x slower  | 24.9 ns: 1.18x faster  | 35.6 ns: 1.21x slower  |
| unpickle                 | 8.03 us   | 8.40 us: 1.05x slower  | 8.60 us: 1.07x slower  | 9.42 us: 1.17x slower  |
| unpickle_list            | 2.48 us   | 2.52 us: 1.01x slower  | 2.78 us: 1.12x slower  | 3.08 us: 1.24x slower  |
| unpickle_pure_python     | 140 us    | 134 us: 1.05x faster   | 112 us: 1.25x faster   | not significant        |
| xml_etree_parse          | 88.3 ms   | 150 ms: 1.70x slower   | 155 ms: 1.75x slower   | 161 ms: 1.82x slower   |
| xml_etree_iterparse      | 59.5 ms   | 83.7 ms: 1.41x slower  | 89.6 ms: 1.51x slower  | 74.9 ms: 1.26x slower  |
| xml_etree_generate       | 47.6 ms   | 53.5 ms: 1.12x slower  | 49.6 ms: 1.04x slower  | 56.5 ms: 1.19x slower  |
| xml_etree_process        | 34.8 ms   | 37.9 ms: 1.09x slower  | not significant        | 38.7 ms: 1.11x slower  |
| Geometric mean           | (ref)     | 1.04x slower           | 1.03x faster           | 1.09x slower           |

Benchmark hidden because not significant (2): dulwich_log, regex_effbot
Ignored benchmarks (19) of pynorm313.json: async_tree_cpu_io_mixed, async_tree_cpu_io_mixed_tg, async_tree_eager, async_tree_eager_cpu_io_mixed, async_tree_eager_cpu_io_mixed_tg, async_tree_eager_io, async_tree_eager_io_tg, async_tree_eager_memoization, async_tree_eager_memoization_tg, async_tree_eager_tg, async_tree_io, async_tree_io_tg, async_tree_memoization, async_tree_memoization_tg, async_tree_none, async_tree_none_tg, chameleon, dask, tornado_http
Ignored benchmarks (21) of py313.json: async_tree_cpu_io_mixed, async_tree_cpu_io_mixed_tg, async_tree_eager, async_tree_eager_cpu_io_mixed, async_tree_eager_cpu_io_mixed_tg, async_tree_eager_io, async_tree_eager_io_tg, async_tree_eager_memoization, async_tree_eager_memoization_tg, async_tree_eager_tg, async_tree_io, async_tree_io_tg, async_tree_memoization, async_tree_memoization_tg, async_tree_none, async_tree_none_tg, asyncio_tcp, asyncio_tcp_ssl, chameleon, dask, tornado_http
Ignored benchmarks (3) of py314.json: asyncio_tcp, asyncio_tcp_ssl, dask

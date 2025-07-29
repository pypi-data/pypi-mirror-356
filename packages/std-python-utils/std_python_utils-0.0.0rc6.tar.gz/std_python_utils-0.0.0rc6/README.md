# std-utils
Standard Python Utils
# TODOS
```
final return schema: {'type': 'model', 'cls': <class 'src.std_utils.aws_utils.cdk.models.configs.ConstructConfig'>, '
schema': {'type': 'model-fields', 'fields': {'parent': {'type': 'model-field', 'schema': {'type': 'is-instance', '
cls': <class 'constructs.Construct'>}, 'metadata': {}}, 'id': {'type': 'model-field', 'schema': {'type': 'str'}, '
metadata': {}}, 'env': {'type': 'model-field', 'schema': {'type': 'is-instance', 'cls': <class '
aws_cdk.Environment'>}, 'metadata': {}}}, 'model_name': 'ConstructConfig', 'computed_fields': []}, 'custom_init':
True, 'root_model': False, 'config': {'title': 'ConstructConfig', 'extra_fields_behavior': 'forbid', '
revalidate_instances': 'always', 'validate_default': True, 'regex_engine': 'python-re', 'validation_error_cause':
True}, 'ref': 'src.std_utils.aws_utils.cdk.models.configs.ConstructConfig:788869520', 'metadata':
{'pydantic_js_functions': [<bound method BaseModel.__get_pydantic_json_schema
__ of <class 'src.std_utils.aws_utils.cdk.models.configs.ConstructConfig'>>]}}
```
## Benchmark reports
Benchmark reports are stored in [.reports/benchmarks](.reports/benchmarks)

### Reading CProfile data

- ncalls: Total number of calls to the function. If there are two numbers, that means the function recursed and the
  first is the total number of calls and the second is the number of primitive (non-recursive) calls.
- tottime: total time spent in the given function (excluding time made in calls to sub-functions)
- percall: tottime divided by ncalls
- cumtime: is the cumulative time spent in this and all subfunctions (from invocation till exit). This figure is
  accurate even for recursive functions.
- percall: cumtime divided by primitive calls

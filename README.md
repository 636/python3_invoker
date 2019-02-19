# Invoker Readme

invoker utility for DI(Injector) and context configuration.

## How to use

```sh
cd sample
invoker logging.yaml invoke_option.yaml \
  --config config_base.yaml \
  --config config_diff.yaml
```

## Invoke Options

```yaml
# invoke target qualified name
invoke: sample.sample_function
# invoke kargs
args:
  keyPath: test.abc
```

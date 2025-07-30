from typing import Any, TYPE_CHECKING
import math

if TYPE_CHECKING:
    import flaml.tune
    import flaml.tune.sample
    import hyperopt.pyll
    from hyperopt import hp
    from hyperopt.pyll import scope
    import optuna


def add_prefix(prefix: str, name: str, sep: str) -> str:
    return prefix + sep + name if prefix else name


def convert_to_hyperopt(param_cfg: Any, prefix: str = '', name: str = 'name', sep: str = '?') -> Any:
    if not isinstance(param_cfg, dict) and not isinstance(param_cfg, list):
        return param_cfg

    param_cfg = param_cfg.copy()

    if isinstance(param_cfg, dict):
        new_config = dict()
        if name in param_cfg.keys():
            name_value = param_cfg.pop(name)
            return {
                name: name_value,
                **convert_to_hyperopt(param_cfg, add_prefix(prefix, name_value, sep), name, sep)
            }

        for k, v in param_cfg.items():
            if isinstance(v, dict):
                if 'args' in v.keys():
                    new_config[k] = get_hyperopt_sampler(v['args'], v['sampler'], add_prefix(prefix, k, sep))
                else:
                    new_config[k] = convert_to_hyperopt(v, add_prefix(prefix, k, sep), name, sep)
            else:
                new_config[k] = convert_to_hyperopt(v, add_prefix(prefix, k, sep), name, sep)
        return new_config
    elif isinstance(param_cfg, list):
        new_config = list()
        for item in param_cfg:
            new_config.append(convert_to_hyperopt(item, prefix, name, sep))
        return hyperopt.hp.choice(prefix + sep + name, new_config)

    else:
        return param_cfg


def convert_to_optuna(trial: 'optuna.Trial', param_cfg: Any,
                      prefix: str = '', name: str = 'name', sep: str = '?') -> dict:
    param_cfg = param_cfg.copy()

    out = dict()

    if isinstance(param_cfg, dict):
        if name in param_cfg.keys():
            name_value = param_cfg.pop(name)
            return {
                name: name_value,
                **convert_to_optuna(trial, param_cfg, add_prefix(prefix, name_value, sep), name, sep)
            }

    for k, v in param_cfg.items():
        if isinstance(v, dict):
            if 'args' in v.keys():
                out[k] = get_optuna_sampler(v['args'], v['sampler'], add_prefix(prefix, k, sep), trial)
            else:
                out[k] = convert_to_optuna(trial, v, add_prefix(prefix, k, sep), name, sep)
        elif isinstance(v, list):
            selected = trial.suggest_categorical(add_prefix(prefix, k, sep), v)
            out[k] = convert_to_optuna(trial, selected, add_prefix(prefix, k, sep), name, sep)
        else:
            out[k] = v

    return out


def convert_to_flaml(param_cfg: Any, name: str = 'name') -> Any:
    if not isinstance(param_cfg, dict) and not isinstance(param_cfg, list):
        return param_cfg

    param_cfg = param_cfg.copy()

    if isinstance(param_cfg, dict):
        new_config = dict()
        if name in param_cfg.keys():
            name_value = param_cfg.pop(name)
            return {
                name: name_value,
                **convert_to_flaml(param_cfg, name)
            }

        for k, v in param_cfg.items():
            if isinstance(v, dict):
                if 'args' in v.keys():
                    new_config[k] = get_flaml_sampler(v['args'], v['sampler'])
                else:
                    new_config[k] = convert_to_flaml(v, name)
            else:
                new_config[k] = convert_to_flaml(v, name)
        return new_config
    elif isinstance(param_cfg, list):
        new_config = list()
        for item in param_cfg:
            new_config.append(convert_to_flaml(item, name))
        return flaml.tune.choice(new_config)

    else:
        return param_cfg


def get_sampler(
        package_name: str,
        arg: list,
        sampler: str,
        sample_name: str = "",
        trial: 'optuna.Trial' = None) -> Any:
    # match package_name:
    #     case "flaml":
    #         return get_flaml_sampler(arg, sampler)
    #     case "hyperopt":
    #         return get_hyperopt_sampler(arg, sampler, sample_name)
    #     case "optuna":
    #         return get_optuna_sampler(arg, sampler, sample_name, trial)
    #     case _:
    #         raise ValueError(f"Package {package_name} not supported")
    if package_name == "flaml":
        return get_flaml_sampler(arg, sampler)
    elif package_name == "hyperopt":
        return get_hyperopt_sampler(arg, sampler, sample_name)
    elif package_name == "optuna":
        return get_optuna_sampler(arg, sampler, sample_name, trial)
    else:
        raise ValueError(f"Package {package_name} not supported")


def get_flaml_sampler(arg: list, sampler: str) -> 'flaml.tune.sample.Domain':
    global flaml
    import flaml.tune
    # match sampler:
    #     case "uniform":
    #         return flaml.tune.uniform(*arg)
    #     case "loguniform":
    #         return flaml.tune.loguniform(*arg)
    #     case "quniform":
    #         return flaml.tune.quniform(*arg)
    #     case "qloguniform":
    #         return flaml.tune.qloguniform(*arg)
    #     case "uniformint":
    #         return flaml.tune.randint(*arg)
    #     case "quniformint":
    #         return flaml.tune.qrandint(*arg)
    #     case "loguniformint":
    #         return flaml.tune.lograndint(*arg)
    #     case "qloguniformint":
    #         return flaml.tune.qlograndint(*arg)
    #     case "choice":
    #         return flaml.tune.choice(arg)
    #     case _:
    #         raise ValueError(f"Sampler {sampler} not supported")
    if sampler == "uniform":
        return flaml.tune.uniform(*arg)
    elif sampler == "loguniform":
        return flaml.tune.loguniform(*arg)
    elif sampler == "quniform":
        return flaml.tune.quniform(*arg)
    elif sampler == "qloguniform":
        return flaml.tune.qloguniform(*arg)
    elif sampler == "uniformint":
        return flaml.tune.randint(*arg)
    elif sampler == "quniformint":
        return flaml.tune.qrandint(*arg)
    elif sampler == "loguniformint":
        return flaml.tune.lograndint(*arg)
    elif sampler == "qloguniformint":
        return flaml.tune.qlograndint(*arg)
    elif sampler == "choice":
        return flaml.tune.choice(arg)
    else:
        raise ValueError(f"Sampler {sampler} not supported")


def get_hyperopt_sampler(arg: list, sampler: str, sample_name: str) -> 'hyperopt.pyll.Apply':
    global hyperopt
    try:
        import hyperopt.pyll
        import hyperopt.hp
    except ImportError:
        raise ImportError("Hyperopt is not installed. Please install it using `pip install hyperopt`")
    # match sampler:
    #     case "uniform":
    #         return hp.uniform(sample_name, *arg)
    #     case "loguniform":
    #         return hp.loguniform(sample_name, *arg)
    #     case "quniform":
    #         return hp.quniform(sample_name, *arg)
    #     case "qloguniform":
    #         return hp.qloguniform(sample_name, *arg)
    #     case "uniformint":
    #         return hp.randint(sample_name, *arg)
    #     case "quniformint":
    #         return scope.int(hp.quniform(sample_name, *arg))
    #     case "loguniformint":
    #         return scope.int(hp.loguniform(sample_name, *arg))
    #     case "qloguniformint":
    #         return scope.int(hp.qloguniform(sample_name, *arg))
    #     case "choice":
    #         return hp.choice(sample_name, arg)
    #     case _:
    #         raise ValueError(f"Sampler {sampler} not supported")
    if sampler == "uniform":
        return hyperopt.hp.uniform(sample_name, *arg)
    elif sampler == "loguniform":
        return hyperopt.hp.loguniform(sample_name, math.log(arg[0]), math.log(arg[1]))
    elif sampler == "quniform":
        return hyperopt.hp.quniform(sample_name, *arg)
    elif sampler == "qloguniform":
        return hyperopt.hp.qloguniform(sample_name, math.log(arg[0]), math.log(arg[1]), arg[2])
    elif sampler == "uniformint":
        return hyperopt.hp.randint(sample_name, *arg)
    elif sampler == "quniformint":
        return hyperopt.pyll.scope.int(hyperopt.hp.quniform(sample_name, *arg))
    elif sampler == "loguniformint":
        return hyperopt.pyll.scope.int(hyperopt.hp.loguniform(sample_name, math.log(arg[0]), math.log(arg[1])))
    elif sampler == "qloguniformint":
        return hyperopt.pyll.scope.int(hyperopt.hp.qloguniform(sample_name, math.log(arg[0]), math.log(arg[1]), arg[2]))
    elif sampler == "choice":
        return hyperopt.hp.choice(sample_name, arg)
    else:
        raise ValueError(f"Sampler {sampler} not supported")


def get_optuna_sampler(arg: list,
                       sampler: str,
                       sample_name: str,
                       trial: 'optuna.Trial') -> Any:
    # match sampler:
    #     case "uniform":
    #         return trial.suggest_float(sample_name, *arg)
    #     case "loguniform":
    #         return trial.suggest_float(sample_name, *arg, log=True)
    #     case "quniform":
    #         return trial.suggest_float(sample_name, arg[0], arg[1], step=arg[2])
    #     case "qloguniform":
    #         return trial.suggest_float(sample_name, arg[0], arg[1], step=arg[2], log=True)
    #     case "uniformint":
    #         return trial.suggest_int(sample_name, *arg)
    #     case "quniformint":
    #         return trial.suggest_int(sample_name, arg[0], arg[1], step=arg[2])
    #     case "loguniformint":
    #         return trial.suggest_int(sample_name, arg[0], arg[1], log=True)
    #     case "qloguniformint":
    #         return trial.suggest_int(sample_name, arg[0], arg[1], step=arg[2], log=True)
    #     case "choice":
    #         return trial.suggest_categorical(sample_name, arg)
    #     case _:
    #         raise ValueError(f"Sampler {sampler} not supported")
    if sampler == "uniform":
        return trial.suggest_float(sample_name, *arg)
    elif sampler == "loguniform":
        return trial.suggest_float(sample_name, *arg, log=True)
    elif sampler == "quniform":
        return trial.suggest_float(sample_name, arg[0], arg[1], step=arg[2])
    elif sampler == "qloguniform":
        return round(trial.suggest_float(sample_name, arg[0], arg[1], log=True) / arg[2]) * arg[2]
    elif sampler == "uniformint":
        return trial.suggest_int(sample_name, *arg)
    elif sampler == "quniformint":
        return trial.suggest_int(sample_name, arg[0], arg[1], step=arg[2])
    elif sampler == "loguniformint":
        return trial.suggest_int(sample_name, arg[0], arg[1], log=True)
    elif sampler == "qloguniformint":
        return int(trial.suggest_int(sample_name, arg[0], arg[1], log=True) / arg[2]) * arg[2]
    elif sampler == "choice":
        return trial.suggest_categorical(sample_name, arg)
    else:
        raise ValueError(f"Sampler {sampler} not supported")


def get_estimator_class(estimator_name: str) -> Any:
    package = estimator_name.rsplit(".", 1)[0]
    try:
        exec(f"import {package}")
    except ImportError:
        return None
    return eval(estimator_name)


def _match_flaml_domain(domain: 'flaml.tune.sample.Domain') -> dict:
    """
    Match the FLAML domain to the definition used in this library.
    """
    domain_type = domain.__class__.__name__
    if domain_type == 'Categorical':
        return {"args": domain.categories, "sampler": "choice"}

    lower = domain.lower
    upper = domain.upper
    args = [lower, upper]

    sampler = domain.get_sampler()
    sampler_name = ''

    if sampler.__class__.__name__ == 'Quantized':
        sampler_name += 'q'
        args += [sampler.q]
        sampler = sampler.sampler

    sampler_name += sampler.__class__.__name__.lower()[1:]

    if domain_type == 'Integer':
        sampler_name += 'int'

    return {"args": args, "sampler": sampler_name}


def _transform_hyperopt(config: dict) -> dict:
    """
    Transform the configuration from Hyperopt format to the format used in this library.
    """
    # TODO: Implement this
    raise NotImplementedError


def _transform_flaml(config: Any) -> Any:
    """
    Transform the configuration from FLAML format to the format used in this library.
    """
    global flaml
    try:
        import flaml.tune
        import flaml.tune.sample
    except ImportError:
        raise ImportError("FLAML is not installed. Please install it using `pip install flaml`")

    try:
        import ray.tune.search.sample
        domain_class = ray.tune.search.sample.Domain
    except ImportError:
        domain_class = flaml.tune.sample.Domain

    if isinstance(config, dict):
        new_config = dict()
        for k, v in config.items():
            if isinstance(v, dict):
                new_config[k] = _transform_flaml(v)
            elif isinstance(v, domain_class):
                result = _match_flaml_domain(v)
                if isinstance(result['args'][0], dict):
                    new_config[k] = list()
                    for item in result['args']:
                        new_config[k].append(_transform_flaml(item))
                else:
                    new_config[k] = result
            else:
                new_config[k] = v
    else:
        return config

    return new_config


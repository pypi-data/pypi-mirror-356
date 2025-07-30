# Copyright (c) 2025-2025 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from collections import defaultdict

import yaml

from msprechecker.prechecker.register import PrecheckerBase, show_check_result, CheckResult, check_file_permission
from msprechecker.prechecker.utils import (
    parse_mindie_server_config,
    parse_ranktable_file,
    get_model_path_from_mindie_config,
    get_mindie_server_config,
    is_deepseek_model,
    read_csv_or_json,
    logger,
)
from msprechecker.prechecker.suggestions import DOMAIN, NOT_EMPTY_VALUE
from msprechecker.core.utils import ResultStatus
from msprechecker.core.utils.version import Version
from msprechecker.presets import get_default_rule
from msprechecker.core.utils.result import Result, Severity


class ConfigCheckerBase(PrecheckerBase):
    __checker_name__ = "Config"

    def __init__(self, domain):
        super().__init__()
        self.domain, self.config_path = domain, ""

    def action(self, env_key, env_value):
        if env_value == NOT_EMPTY_VALUE:
            return f"配置文件 {self.config_path} 中添加 {env_key} 字段"
        else:
            return f"配置文件 {self.config_path} 中修改 {env_key}={env_value}"

    def do_precheck(self, envs, additional_checks=None, **kwargs):
        if not self.config_path:
            return

        if not envs:
            logger.warning(f"Read config failed: {self.config_path!r}")
            return

        check_file_permission(self.config_path, domain="config", checker_name="file_perm")


class MindieConfigChecker(ConfigCheckerBase):
    __checker_name__ = "MindieConfig"

    def __init__(self):
        super().__init__(domain=DOMAIN.mindie_config)

    def collect_env(self, mindie_service_path=None, **kwargs):
        self.config_path = get_mindie_server_config(mindie_service_path)
        return parse_mindie_server_config(self.config_path)


class RankTableChecker(ConfigCheckerBase):
    __checker_name__ = "RankTable"

    def __init__(self):
        super().__init__(domain=DOMAIN.ranktable)

    def collect_env(self, ranktable_file=None, **kwargs):
        self.config_path = ranktable_file
        return parse_ranktable_file(self.config_path)


class ModelConfigChecker(ConfigCheckerBase):
    __checker_name__ = "ModelConfig"

    def __init__(self):
        super().__init__(domain=DOMAIN.model_config)

    def collect_env(self, mindie_service_path=None, **kwargs):
        weight_dir = kwargs.get("weight_dir")
        model_name = "deepseek"
        if not weight_dir:
            model_name, weight_dir = get_model_path_from_mindie_config(mindie_service_path=mindie_service_path)

        if not model_name or not weight_dir:
            return None

        model_config_path = os.path.join(weight_dir, "config.json")
        model_config = read_csv_or_json(model_config_path) if os.path.exists(model_config_path) else {}
        self.config_path = model_config_path
        logger.debug(f"ModelConfigCollecter model_name={model_name} model_config={model_config}")
        return {"model_name": model_name, "model_config": model_config}

    def do_precheck(self, envs, additional_checks=None, **kwargs):
        super().do_precheck(envs, additional_checks, **kwargs)

        if not envs:
            return

        model_name, model_config = envs.get("model_name"), envs.get("model_config")
        if not model_name or not model_config:
            return
        torch_dtype = model_config.get("torch_dtype")
        if torch_dtype is not None and torch_dtype != "float16":
            show_check_result(
                "ModelConfig", "torch_dtype", CheckResult.ERROR,
                action="请将 torch_dtype 设置为 float16",
                reason=f"当前 torch_dtype 为 {torch_dtype}，推荐为 float16",
            )
        model_transformers_version = model_config.get("transformers_version")
        if model_transformers_version:
            try:
                import transformers
                current_transformers_version = transformers.__version__
            except ImportError:
                show_check_result(
                    "ModelConfig", "transformers_version", CheckResult.ERROR,
                    action="请升级 transformers 库",
                    reason=f"模型要求 transformers>={model_transformers_version}，当前未安装",
                )
                return
            if Version(model_transformers_version) > Version(current_transformers_version):
                show_check_result(
                    "ModelConfig", "transformers_version", CheckResult.ERROR,
                    action="请升级 transformers 库",
                    reason=f"模型要求 transformers>={model_transformers_version}，当前为 {current_transformers_version}",
                )
        if not is_deepseek_model(model_name):
            return


class K8SCheckerBase(ConfigCheckerBase):
    PATH_SEPARATOR = "."
    output_title = "Config"

    def __init__(self, domain):
        super().__init__(domain=domain)

    @staticmethod
    def load_yaml(config_path):
        if config_path is None or not os.path.isfile(config_path):
            return {}
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}") from e

    @staticmethod
    def flatten_dict_leaves(result, data, parent_path: str = "", sep: str = PATH_SEPARATOR) -> None:
        if isinstance(data, dict):
            for key, value in data.items():
                path = f"{parent_path}{sep}{key}" if parent_path else key
                if key == "npuDeviceIds":
                    result[path] = value
                    continue
                K8SCheckerBase.flatten_dict_leaves(result, value, path, sep)
        elif isinstance(data, list):
            for idx, value in enumerate(data):
                path = f"{parent_path}[{idx}]" if parent_path else f"[{idx}]"
                K8SCheckerBase.flatten_dict_leaves(result, value, path, sep)
        else:
            result[parent_path] = data

    @staticmethod
    def extract_expected_nodes(result, data, parent_path: str = "", sep: str = PATH_SEPARATOR) -> None:
        if isinstance(data, dict):
            for key, value in data.items():
                path = f"{parent_path}{sep}{key}" if parent_path else key
                if isinstance(value, dict) and "expected" in value:
                    result[path] = value
                else:
                    K8SCheckerBase.extract_expected_nodes(result, value, path, sep)
        elif isinstance(data, list):
            for idx, value in enumerate(data):
                path = f"{parent_path}[{idx}]" if parent_path else f"[{idx}]"
                K8SCheckerBase.extract_expected_nodes(result, value, path, sep)
        else:
            raise OSError("Unexpected leaf node without 'expected' key.")

    def validate_expected(self, key: str, expected_info, actual_value, collected_data):
        if isinstance(expected_info, dict):
            return self._validate_single(key, expected_info, actual_value, collected_data)
        elif isinstance(expected_info, list):
            for expected_rule in expected_info:
                check_status, expected_value = self._validate_single(key, expected_rule, actual_value, collected_data)
                if not check_status:
                    return check_status, expected_value
            return check_status, actual_value
        else:
            raise ValueError(f"Unsupported expected type: {type(expected_info).__name__}")

    def do_precheck(self, envs, additional_checks=None, **kwargs):
        super().do_precheck(envs, additional_checks, **kwargs)

        if not envs:
            return

        log_level = kwargs.get("log_level", "error")

        level_to_severities = {
            'info': (Severity.LOW, Severity.MEDIUM, Severity.HIGH),
            'warning': (Severity.MEDIUM, Severity.HIGH),
            'error': (Severity.HIGH,)
        }

        min_severity_range = level_to_severities.get(log_level, (Severity.LOW, Severity.MEDIUM, Severity.HIGH))

        default_rule = get_default_rule(self.rule_type)
        if additional_checks:
            default_rule.update(additional_checks)
        expected_nodes = {}
        self.extract_expected_nodes(expected_nodes, default_rule)
        config_nodes = {}
        self.flatten_dict_leaves(config_nodes, envs)
        res = []
        for config_key, rule_node in expected_nodes.items():
            if "expected" not in rule_node:
                raise ValueError(f"Missing 'expected' key in node: {config_key}")

            actual_value = config_nodes.get(config_key)
            severity = Severity(rule_node.get("severity", "high"))
            reason = rule_node.get("reason", "no reason")
            expected_info = rule_node.get("expected")
            check_status, expected_value = self.validate_expected(config_key, expected_info, actual_value, config_nodes)
            if not check_status and severity in min_severity_range:
                res.append(
                    Result(
                        key=config_key,
                        actual=actual_value,
                        expected=expected_value,
                        status=ResultStatus(check_status, severity),
                        reason=reason
                    )
                )

        tree = self._build_tree(res)
        if not tree['children']:
            self.logger.info(
                f"- config: All {self.output_title.lower()} fields passed the checks "
                f"[Severity: {min_severity_range}]."
            )
            return
        output = [self.output_title]
        self._render_tree(tree, output, "", True, True)
        self.logger.info('\n'.join(output))

    def _validate_single(self, key: str, expected_rule: dict, actual_value, collected_data):
        from msprechecker.core.utils import MacroExpander, Compiler
        from msprechecker.core.validators import get_validator
        check_type = expected_rule.get("type")
        if check_type is None:
            raise ValueError(f"Missing 'type' in expected node for {key}")
        expected_value = expected_rule.get("value")
        expaned_value = MacroExpander(collected_data, key).expand(expected_value)
        expected_value = Compiler.compile(expaned_value)
        validator = get_validator(check_type)
        check_status = validator.validate(actual_value, expected_value)
        return check_status, expected_value

    def _build_tree(self, results) -> dict:
        root = {'children': defaultdict(dict), 'result': None}
        for result in results:
            if result.status:
                continue
            parts = result.key.split('.')
            node = root
            for part in parts[:-1]:
                if part not in node['children']:
                    node['children'][part] = {'children': defaultdict(dict), 'result': None}
                node = node['children'][part]
            leaf = parts[-1]
            if leaf not in node['children']:
                node['children'][leaf] = {'children': defaultdict(dict), 'result': result}
            else:
                node['children'][leaf]['result'] = result
        return root

    def _render_tree(self, node, output, prefix, is_last, is_root=False):
        if not is_root:
            if node.get('result'):
                result = node['result']
                output[-1] += f" {result.status}"
                if not result.status:
                    indent = prefix.replace("├──", "│  ").replace("└──", "   ")
                    output.append(f"{indent}├── actual: {self._fmt_value(result.actual)}")
                    if self.rule_type == "env":
                        output.append(f"{indent}├── expected: {self._fmt_value(result.expected)}")
                    output.append(f"{indent}└── reason: {result.reason}")
        children = node['children']
        child_keys = list(children.keys())
        for i, key in enumerate(child_keys):
            child = children[key]
            if not self._has_failed_descendant(child):
                continue
            last_child = i == len(child_keys) - 1
            connector = "└── " if last_child else "├── "
            output.append(f"{prefix}{connector}{key}")
            new_prefix = prefix + ("    " if last_child else "│   ")
            self._render_tree(child, output, new_prefix, last_child)

    def _has_failed_descendant(self, node):
        if node.get('result') and not node['result'].status:
            return True
        for child in node['children'].values():
            if self._has_failed_descendant(child):
                return True
        return False

    def _fmt_value(self, value):
        if value is None:
            return "<missing>"
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)


class UserConfigChecker(K8SCheckerBase):
    __checker_name__ = "UserConfig"
    output_title = "User Config"
    rule_type = "user_config"

    def __init__(self):
        super().__init__(domain=DOMAIN.user_config)

    def collect_env(self, user_config_path=None, **kwargs):
        self.config_path = user_config_path
        return read_csv_or_json(user_config_path) if user_config_path and os.path.exists(user_config_path) else {}


class MindIEEnvChecker(K8SCheckerBase):
    __checker_name__ = "MindIEEnv"
    output_title = "MindIE Env"
    rule_type = "env"

    def __init__(self):
        super().__init__(domain=DOMAIN.mindie_env)

    def collect_env(self, user_config_path=None, **kwargs):
        self.config_path = kwargs.get("mindie_env_config_path", None)
        return read_csv_or_json(self.config_path) if self.config_path and os.path.exists(self.config_path) else {}


mindie_config_checker = MindieConfigChecker()
ranktable_checker = RankTableChecker()
model_config_checker = ModelConfigChecker()
user_config_checker = UserConfigChecker()
mindie_env_checker = MindIEEnvChecker()

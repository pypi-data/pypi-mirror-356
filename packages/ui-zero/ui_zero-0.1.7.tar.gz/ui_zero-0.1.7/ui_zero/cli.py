#!/usr/bin/env python3
"""
UI-Zero command line interface

用法示例:
    # 使用默认测试用例文件
    ui-zero

    # 指定测试用例文件
    ui-zero --testcase test_case.json

    # 指定单个测试命令
    ui-zero --command "找到[假日乐消消]app，并打开"

    # 指定多个测试命令
    ui-zero --command "找到app" --command "点击按钮"
"""

import argparse
import json
import logging
import os
import sys
from typing import Any, Callable, Dict, List, Optional

import dotenv
import yaml

from .adb import ADBTool
from .agent import ActionOutput, AndroidAgent, take_action
from .env_config import ensure_env_config, setup_env_interactive, validate_env
from .localization import get_text

# 加载环境变量
dotenv.load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 禁用httpx的INFO日志
logging.getLogger("httpx").setLevel(logging.WARNING)


def list_available_devices() -> List[str]:
    """列出所有可用的Android设备"""
    try:
        adb_tool = ADBTool()
        devices = adb_tool.get_connected_devices()
        return devices
    except Exception as e:
        logger.error(get_text("device_list_error", e))
        return []


class StepRunner:
    """测试运行器，用于执行测试用例"""

    def __init__(self, agent: AndroidAgent):
        """
        初始化测试运行器

        Args:
            agent: AndroidAgent实例
        """
        self.agent = agent

    def run_step(
        self,
        step: str,
        screenshot_callback: Optional[Callable[[bytes], None]] = None,
        preaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
        postaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
        stream_resp_callback: Optional[Callable[[str, bool], None]] = None,
        timeout: Optional[int] = None,
    ) -> ActionOutput:
        """
        执行单个测试步骤

        Args:
            step: 测试步骤描述
            screenshot_callback: 截图回调函数
            preaction_callback: 动作前回调函数
            postaction_callback: 动作后回调函数
            stream_resp_callback: 流式响应回调函数
            timeout: 超时时间（毫秒）

        Returns:
            执行结果
        """
        logger.info(get_text("step_execution_log", step))

        try:
            # 执行步骤
            result = self.agent.run(
                step,
                max_iters=10,
                screenshot_callback=screenshot_callback,
                preaction_callback=preaction_callback,
                postaction_callback=postaction_callback,
                stream_resp_callback=stream_resp_callback,
                timeout=timeout,
            )

            return result
        except Exception as e:
            logger.error(get_text("step_execution_error", e))
            raise


def load_testcase_from_file(testcase_file: str) -> list:
    """从JSON文件加载测试用例"""
    try:
        with open(testcase_file, "r", encoding="utf-8") as f:
            testcases = json.load(f)
        if not isinstance(testcases, list):
            raise ValueError(get_text("testcase_format_error"))
        return testcases
    except FileNotFoundError:
        print(get_text("testcase_file_not_found", testcase_file))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(get_text("testcase_file_json_error", testcase_file, e))
        sys.exit(1)
    except Exception as e:
        print(get_text("testcase_file_load_error", e))
        sys.exit(1)


def load_yaml_config(yaml_file: str) -> Dict[str, Any]:
    """从YAML文件加载配置"""
    try:
        with open(yaml_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        if not isinstance(config, dict):
            raise ValueError(get_text("yaml_config_format_error"))
        return config
    except FileNotFoundError:
        print(get_text("yaml_config_file_not_found", yaml_file))
        sys.exit(1)
    except yaml.YAMLError as e:
        print(get_text("yaml_config_file_parse_error", yaml_file, e))
        sys.exit(1)
    except Exception as e:
        print(get_text("yaml_config_file_load_error", e))
        sys.exit(1)


def convert_yaml_to_testcases(
    config: Dict[str, Any],
) -> tuple[List[Dict[str, Any]], Optional[str]]:
    """将YAML配置转换为测试用例列表"""
    testcases = []
    device_id = None

    # 提取设备ID
    if "android" in config and config["android"] and "deviceId" in config["android"]:
        device_id = config["android"]["deviceId"]

    # 处理任务列表
    if "tasks" not in config or not isinstance(config["tasks"], list):
        raise ValueError(get_text("yaml_config_missing_tasks"))

    for task in config["tasks"]:
        if not isinstance(task, dict) or "flow" not in task:
            continue

        task_name = task.get("name", get_text("unnamed_task"))
        continue_on_error = task.get("continueOnError", False)

        # 处理flow中的每个动作
        for action in task["flow"]:
            if not isinstance(action, dict):
                continue
            action_continue_on_error = action.get("continueOnError", continue_on_error)
            # 处理AI动作
            if "ai" in action:
                testcase = {
                    "type": "ai_action",
                    "prompt": action["ai"],
                    "continueOnError": action_continue_on_error,
                    "taskName": task_name,
                }
                # 添加timeout参数支持
                if "timeout" in action:
                    testcase["timeout"] = action["timeout"]
                testcases.append(testcase)
            elif "aiAction" in action:
                testcase = {
                    "type": "ai_action",
                    "prompt": action["aiAction"],
                    "continueOnError": action_continue_on_error,
                    "taskName": task_name,
                }
                # 添加timeout参数支持
                if "timeout" in action:
                    testcase["timeout"] = action["timeout"]
                testcases.append(testcase)
            elif "aiWaitFor" in action:
                # 将等待条件作为AI动作处理，支持timeout参数
                wait_prompt = action["aiWaitFor"]
                testcase = {
                    "type": "ai_action",
                    "prompt": get_text("ai_wait_for_condition", wait_prompt),
                    "continueOnError": action_continue_on_error,
                    "taskName": task_name,
                }
                # 添加timeout参数支持
                if "timeout" in action:
                    testcase["timeout"] = action["timeout"]
                testcases.append(testcase)
            elif "aiAssert" in action:
                # 将断言作为AI动作处理，支持errorMessage参数
                assert_prompt = action["aiAssert"]
                error_msg = action.get("errorMessage", "")
                testcases.append(
                    {
                        "type": "ai_assert",
                        "prompt": assert_prompt,
                        "errorMessage": error_msg,
                        "continueOnError": action_continue_on_error,
                        "taskName": task_name,
                    }
                )
            elif "sleep" in action:
                # 将sleep动作转换为wait动作（向后兼容）
                wait_ms = action["sleep"]
                testcases.append(
                    {
                        "type": "wait",
                        "duration": wait_ms,
                        "continueOnError": action_continue_on_error,
                        "taskName": task_name,
                    }
                )
            elif "wait" in action:
                # 添加wait动作到测试用例列表
                wait_ms = action["wait"]
                testcases.append(
                    {
                        "type": "wait",
                        "duration": wait_ms,
                        "continueOnError": action_continue_on_error,
                        "taskName": task_name,
                    }
                )

    return testcases, device_id


def execute_wait_action(duration_ms: int, task_name: str = "") -> ActionOutput:  # pylint: disable=unused-argument
    """
    执行等待动作，返回ActionOutput对象

    Args:
        duration_ms: 等待时间（毫秒）
        task_name: 任务名称

    Returns:
        ActionOutput对象，表示等待动作已完成
    """
    return ActionOutput(
        thought=get_text("execute_wait_action_thought", duration_ms),
        action="wait",
        content=str(duration_ms),
    )


def execute_unified_action(
    action_dict: Dict[str, Any],
    agent: AndroidAgent,
    screenshot_callback: Optional[Callable[[bytes], None]] = None,
    preaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
    postaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
    stream_resp_callback: Optional[Callable[[str, bool], None]] = None,
    include_history: bool = True,
    debug: bool = False,
    is_cli_mode: bool = False,
) -> ActionOutput:
    """
    统一的动作执行函数，支持AI动作和直接指令（如睡眠）

    Args:
        action_dict: 动作字典，包含type、prompt等信息
        agent: AndroidAgent实例
        其他参数同run_testcases

    Returns:
        ActionOutput对象
    """
    action_type = action_dict.get("type", "ai_action")
    task_name = action_dict.get("taskName", "")

    if action_type == "wait":
        # 处理等待动作
        duration_ms = action_dict.get("duration", 2000)  # 默认2秒

        if is_cli_mode:
            print(get_text("starting_wait_action", task_name, duration_ms))

        # 创建等待动作的ActionOutput
        wait_output = execute_wait_action(duration_ms, task_name)

        # 执行动作前回调
        if preaction_callback:
            preaction_callback(
                get_text("wait_callback_description", duration_ms), wait_output
            )

        # 执行等待动作
        take_action(agent.adb, wait_output)

        # 执行动作后回调
        if postaction_callback:
            postaction_callback(
                get_text("wait_callback_description", duration_ms), wait_output
            )

        if is_cli_mode:
            print(get_text("wait_action_completed", task_name))

        # 等待动作总是成功完成
        return ActionOutput(
            thought=get_text("wait_action_thought_completed", duration_ms),
            action="finished",
            content=get_text("wait_action_content_completed", duration_ms),
        )
    elif action_type == "ai_assert":
        # 处理AI断言动作
        prompt = action_dict.get("prompt", "")
        error_message = action_dict.get("errorMessage", "")
        continue_on_error = action_dict.get("continueOnError", False)

        if is_cli_mode:
            print(get_text("starting_assert_action", task_name, prompt))

        # 调用agent.run，要求模型判断prompt中描述的情况是否为真
        assert_prompt = get_text("ai_assert_prompt", prompt)

        # 执行断言检查
        result = agent.run(
            assert_prompt,
            max_iters=1,  # 断言只需要一次判断
            screenshot_callback=screenshot_callback,
            preaction_callback=preaction_callback,
            postaction_callback=postaction_callback,
            stream_resp_callback=stream_resp_callback,
            debug=debug,
        )

        # 检查断言结果
        is_assert_true = (
            result.action == "finished"
            and result.content
            and "Assert is true" in result.content
        )

        if is_assert_true:
            # 断言为真，继续执行
            if is_cli_mode:
                print(get_text("assert_passed", task_name))
            return ActionOutput(
                thought=get_text("assert_true_thought", prompt),
                action="finished",
                content=get_text("assert_true_content"),
            )
        else:
            # 断言为假
            if is_cli_mode:
                print(get_text("assert_failed", task_name))

            # 根据continueOnError决定是否抛出异常
            if continue_on_error:
                if not error_message:
                    error_description = get_text(
                        "assert_false_thought_continue", prompt
                    )
                else:
                    error_description = get_text(
                        "assert_false_thought_continue_with_msg", prompt, error_message
                    )

                if is_cli_mode:
                    print(error_description)
                else:
                    logger.warning(error_description)

                return ActionOutput(
                    thought=error_description,
                    action="finished",
                    content=get_text("assert_false_content"),
                )
            else:
                # 抛出异常中断执行，使用自定义错误消息或默认消息
                if error_message:
                    raise RuntimeError(get_text("assert_failed_error", error_message))
                else:
                    raise RuntimeError(get_text("assert_failed_error", prompt))

    elif action_type == "ai_action":
        # 处理AI动作
        prompt = action_dict.get("prompt", "")
        timeout = action_dict.get("timeout")  # 获取timeout参数

        if is_cli_mode:
            # CLI模式：直接使用agent.run
            return agent.run(
                prompt,
                stream_resp_callback=stream_resp_callback,
                include_history=include_history,
                debug=debug,
                timeout=timeout,
            )
        else:
            # GUI模式：使用StepRunner逻辑
            test_runner = StepRunner(agent)
            return test_runner.run_step(
                prompt,
                screenshot_callback=screenshot_callback,
                preaction_callback=preaction_callback,
                postaction_callback=postaction_callback,
                stream_resp_callback=stream_resp_callback,
                timeout=timeout,
            )

    else:
        # 未知动作类型
        error_msg = get_text("unsupported_action_type", action_type)
        return ActionOutput(thought=error_msg, action="error", content=error_msg)


def run_testcases(
    testcase_prompts: List[Dict[str, Any]],
    screenshot_callback: Optional[Callable[[bytes], None]] = None,
    preaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
    postaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
    stream_resp_callback: Optional[Callable[[str, bool], None]] = None,
    include_history: bool = True,
    debug: bool = False,
    is_cli_mode: bool = False,
    device_id: Optional[str] = None,
) -> None:
    """
    统一的测试用例执行函数，支持CLI和GUI模式

    Args:
        testcase_prompts: 测试用例列表
        screenshot_callback: 截图回调函数（GUI模式）
        preaction_callback: 动作前回调函数（GUI模式）
        postaction_callback: 动作后回调函数（GUI模式）
        stream_resp_callback: 流式响应回调函数
        include_history: 是否包含历史记录
        debug: 是否启用调试模式
        is_cli_mode: 是否为CLI模式
        device_id: 指定的设备ID
    """
    adb_tool = ADBTool(device_id=device_id) if device_id else ADBTool()
    agent = AndroidAgent(adb=adb_tool)
    _ = StepRunner(agent)  # Create runner for any initialization side effects

    # CLI模式的初始化输出
    if is_cli_mode:
        print(get_text("starting_test_execution"), len(testcase_prompts))
        if device_id:
            print(get_text("using_specified_device"), device_id)
        elif adb_tool.auto_selected_device:
            print(get_text("multiple_devices_auto_selected").format(adb_tool.device_id))
            print(get_text("recommend_specify_device"))
            print(get_text("using_auto_selected_device").format(adb_tool.device_id))
        else:
            print(get_text("using_default_device"))
        if debug:
            debug_history_key = (
                "debug_history_enabled" if include_history else "debug_history_disabled"
            )
            print(get_text(debug_history_key))
            debug_mode_key = "debug_mode_enabled" if debug else "debug_mode_disabled"
            print(get_text(debug_mode_key))

        # CLI模式的流式响应回调
        if stream_resp_callback is None:

            def default_stream_callback(text: str, finished: bool) -> None:
                if finished:
                    print("\n", flush=True)
                else:
                    print(f"{text}", end="", flush=True)

            stream_resp_callback = default_stream_callback

    prompt_idx = 0
    total_steps = len(testcase_prompts)

    while prompt_idx < total_steps:
        cur_action = None
        try:
            cur_action = testcase_prompts[prompt_idx]

            # 提取动作信息
            action_type = cur_action.get("type", "ai_action")
            continue_on_error = cur_action.get("continueOnError", False)
            _ = cur_action.get("taskName", get_text("step_number", prompt_idx + 1))

            # 使用统一的动作执行函数
            if is_cli_mode and action_type == "ai_action":
                # CLI模式下AI动作需要特殊的提示输出
                cur_action_prompt = cur_action["prompt"]
                print(get_text("starting_task", prompt_idx + 1, cur_action_prompt))

            # 执行动作
            result = execute_unified_action(
                cur_action,
                agent,
                screenshot_callback=screenshot_callback,
                preaction_callback=preaction_callback,
                postaction_callback=postaction_callback,
                stream_resp_callback=stream_resp_callback,
                include_history=include_history,
                debug=debug,
                is_cli_mode=is_cli_mode,
            )

            # 检查执行结果
            if result.is_finished():
                if is_cli_mode:
                    print(get_text("task_completed", prompt_idx + 1))
                prompt_idx += 1
            else:
                # 任务未完成，根据continueOnError决定是否继续
                if continue_on_error:
                    if is_cli_mode:
                        print(get_text("task_not_completed", prompt_idx + 1))
                        print(get_text("continue_on_error_message"))
                    else:
                        logger.warning(
                            get_text("step_not_completed_warning", prompt_idx + 1)
                        )
                        logger.info(get_text("continue_on_error_message"))
                    prompt_idx += 1
                else:
                    # 不允许继续，停止执行
                    if is_cli_mode:
                        print(get_text("task_not_completed", prompt_idx + 1))
                        print(get_text("task_failed_stopping_execution"))
                        break
                    else:
                        logger.error(
                            get_text("step_not_completed_error", prompt_idx + 1)
                        )
                        raise RuntimeError(
                            get_text("step_not_completed_error", prompt_idx + 1)
                        )

        except KeyboardInterrupt:
            if is_cli_mode:
                print(get_text("user_interrupted"))
                sys.exit(0)
            else:
                logger.info(get_text("user_interrupted_execution"))
                raise
        except Exception as e:
            error_msg = get_text("step_execution_error", prompt_idx + 1, e)

            # 检查是否应该继续执行
            should_continue = (
                cur_action.get("continueOnError", False) if cur_action else False
            )

            if should_continue:
                if is_cli_mode:
                    print(get_text("execution_error", e))
                    print(get_text("continue_on_error_message"))
                else:
                    logger.error(error_msg)
                    logger.info(get_text("continue_on_error_message"))
                prompt_idx += 1
            else:
                if is_cli_mode:
                    print(get_text("execution_error", e))
                    break
                else:
                    logger.error(error_msg)
                    raise

    # CLI模式的完成输出
    if is_cli_mode:
        print(get_text("all_tasks_completed"))


def execute_single_step(
    step: str,
    agent: Optional[AndroidAgent] = None,
    screenshot_callback: Optional[Callable[[bytes], None]] = None,
    preaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
    postaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
    stream_resp_callback: Optional[Callable[[str, bool], None]] = None,
    device_id: Optional[str] = None,
    timeout: Optional[int] = None,
) -> ActionOutput:
    """执行单个测试步骤（用于GUI模式）"""
    if agent is None:
        adb_tool = ADBTool(device_id=device_id) if device_id else ADBTool()
        agent = AndroidAgent(adb=adb_tool)

    test_runner = StepRunner(agent)
    return test_runner.run_step(
        step,
        screenshot_callback=screenshot_callback,
        preaction_callback=preaction_callback,
        postaction_callback=postaction_callback,
        stream_resp_callback=stream_resp_callback,
        timeout=timeout,
    )


def run_testcases_for_gui(
    testcase_prompts: List[Dict[str, Any]],
    screenshot_callback: Optional[Callable[[bytes], None]] = None,
    preaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
    postaction_callback: Optional[Callable[[str, ActionOutput], None]] = None,
    stream_resp_callback: Optional[Callable[[str, bool], None]] = None,
    include_history: bool = True,
    debug: bool = False,
    device_id: Optional[str] = None,
) -> None:
    """
    为GUI模式提供的批量执行函数，使用统一的执行逻辑
    这个函数直接调用统一的run_testcases函数，确保行为一致性
    """
    return run_testcases(
        testcase_prompts=testcase_prompts,
        screenshot_callback=screenshot_callback,
        preaction_callback=preaction_callback,
        postaction_callback=postaction_callback,
        stream_resp_callback=stream_resp_callback,
        include_history=include_history,
        debug=debug,
        is_cli_mode=False,
        device_id=device_id,
    )


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description=get_text("cli_description"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_text("usage_examples"),
    )

    # 互斥参数组：要么使用testcase文件，要么使用command参数
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--testcase", "-t", type=str, help=get_text("arg_testcase_help"))

    group.add_argument(
        "--command", "-c", action="append", help=get_text("arg_command_help")
    )

    parser.add_argument("--version", "-v", action="version", version="UI-Zero v0.1.7")

    parser.add_argument(
        "--no-history", action="store_true", help=get_text("arg_no_history_help")
    )

    parser.add_argument(
        "--debug", "-d", action="store_true", help=get_text("arg_debug_help")
    )

    parser.add_argument("--device", "-D", type=str, help=get_text("arg_device_help"))

    parser.add_argument(
        "--list-devices", action="store_true", help=get_text("arg_list_devices_help")
    )

    parser.add_argument(
        "--setup-env", action="store_true", help=get_text("arg_setup_env_help")
    )

    parser.add_argument(
        "--validate-env", action="store_true", help=get_text("arg_validate_env_help")
    )

    args = parser.parse_args()

    # 处理环境配置命令
    if args.setup_env:
        success = setup_env_interactive()
        sys.exit(0 if success else 1)

    if args.validate_env:
        success = validate_env()
        sys.exit(0 if success else 1)

    # 处理列出设备命令
    if args.list_devices:
        devices = list_available_devices()
        if devices:
            print(get_text("available_devices"))
            for device in devices:
                print(f"  - {device}")
        else:
            print(get_text("no_devices_found"))
        sys.exit(0)

    # 在执行主要功能前检查环境配置
    print(get_text("checking_env_config"))
    if not ensure_env_config(skip_interactive=True):
        print(get_text("env_config_incomplete_invalid"))
        success = setup_env_interactive()
        sys.exit(0 if success else 1)

    # 确定测试用例来源
    device_id_from_config = None
    if args.command:
        # 使用命令行指定的命令，转换为统一格式
        testcase_prompts = [
            {
                "type": "ai_action",
                "prompt": cmd,
                "continueOnError": False,
                "taskName": get_text("command_number", i + 1),
                # 命令行模式默认不设置timeout，使用系统默认值
            }
            for i, cmd in enumerate(args.command)
        ]
        print(get_text("using_cli_commands", len(testcase_prompts)))
    elif args.testcase:
        # 使用指定的测试用例文件
        if args.testcase.endswith((".yaml", ".yml")):
            # YAML配置文件
            config = load_yaml_config(args.testcase)
            testcase_prompts, device_id_from_config = convert_yaml_to_testcases(config)
            print(
                get_text("loaded_from_yaml_file", len(testcase_prompts), args.testcase)
            )
        else:
            # JSON测试用例文件，转换为统一格式
            json_testcases = load_testcase_from_file(args.testcase)
            testcase_prompts = [
                {
                    "type": "ai_action",
                    "prompt": tc,
                    "continueOnError": False,
                    "taskName": get_text("step_number", i + 1),
                    # JSON格式暂不支持timeout参数，使用系统默认值
                }
                for i, tc in enumerate(json_testcases)
            ]
            print(get_text("loaded_from_file", args.testcase, len(testcase_prompts)))
    else:
        # 尝试使用默认文件（优先YAML）
        default_yaml_file = "test_case.yaml"
        default_json_file = "test_case.json"

        if os.path.exists(default_yaml_file):
            config = load_yaml_config(default_yaml_file)
            testcase_prompts, device_id_from_config = convert_yaml_to_testcases(config)
            print(
                get_text(
                    "loaded_from_yaml_file", len(testcase_prompts), default_yaml_file
                )
            )
        elif os.path.exists(default_json_file):
            json_testcases = load_testcase_from_file(default_json_file)
            testcase_prompts = [
                {
                    "type": "ai_action",
                    "prompt": tc,
                    "continueOnError": False,
                    "taskName": get_text("step_number", i + 1),
                    # 默认JSON文件暂不支持timeout参数，使用系统默认值
                }
                for i, tc in enumerate(json_testcases)
            ]
            print(
                get_text(
                    "loaded_from_default", default_json_file, len(testcase_prompts)
                )
            )
        else:
            # 没有找到可用的测试用例
            print(get_text("no_testcase_found", default_json_file))
            print(get_text("testcase_options"))
            print(get_text("use_help"))
            sys.exit(1)

    # 执行测试用例
    include_history = (
        not args.no_history
    )  # --no-history 为 True 时，include_history 为 False

    # 设备ID优先级：命令行参数 > YAML配置 > 自动选择
    final_device_id = args.device or device_id_from_config
    run_testcases(
        testcase_prompts,
        include_history=include_history,
        debug=args.debug,
        is_cli_mode=True,
        device_id=final_device_id,
    )


if __name__ == "__main__":
    main()

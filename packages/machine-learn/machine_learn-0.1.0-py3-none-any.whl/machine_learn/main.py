import logging
import logging.config
import yaml
import importlib
from pathlib import Path
from typing import Dict, Any
from pyfiglet import Figlet


def read_config_file(file_path: str) -> Dict[str, Any]:
    """读取并解析YAML配置文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {file_path} 未找到。")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"解析 {file_path} 文件时出错: {e}")


def initialize_logger(config: Dict[str, Any]) -> logging.Logger:
    """初始化日志配置并返回logger实例"""
    logging.config.dictConfig(config["Logger"])
    return logging.getLogger("ml")


def create_model_instance(
    model_name: str, configs: Dict[str, Any], logger: logging.Logger
):
    """创建策略实例"""
    module = importlib.import_module(f"machine_learn.model.{model_name}")
    module_class = getattr(module, model_name)
    return module_class(configs, logger=logger)


def main():

    # 读取配置文件
    config_path = Path("ml_config.yaml")
    config_data = read_config_file(config_path)

    # 初始化日志
    logger = initialize_logger(config_data)

    # 获取启动策略
    common_config = config_data["common"]
    model_name = common_config.get("actived_model", "TSA")

    f = Figlet(font="standard")  # 字体可选（如 "block", "bubble"）
    logger.info(f"\n{f.renderText("Machine-Learn")}")
    model = create_model_instance(model_name, config_data, logger)
    model.start()


if __name__ == "__main__":
    main()

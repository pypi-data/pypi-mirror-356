"""FastMCP适配层 - 连接FastMCP和现有业务逻辑"""
import json
from typing import List, Dict, Any, Optional
from urllib.request import url2pathname

from fastmcp import Context
from ..utils.common import Logger, FileHandler, BaseResult
from ..models.schemas import FileObject


class FastMCPLogger:
    """FastMCP Logger适配器"""
    def __init__(self, context: Context):
        self.context = context
        self._info_log = []

    async def log(self, level: str, message: str, add_to_result: bool = True):
        """记录日志消息"""
        if add_to_result:
            self._info_log.append(message)
            
        if level.lower() == "error":
            await self.context.error(message)
        elif level.lower() == "warning":
            # FastMCP Context 可能没有warning方法，使用info代替
            await self.context.info(f"⚠️ {message}")
        elif level.lower() == "debug":
            # 只在debug模式下输出
            import os
            if os.getenv("DEBUG"):
                await self.context.info(f"🐛 {message}")
        else:
            await self.context.info(message)

    async def error(self, message: str, error_class=RuntimeError):
        """记录错误并引发异常"""
        await self.log("error", message)
        raise error_class(message)
        
    def get_result_info(self) -> List[str]:
        """获取收集的信息日志"""
        return self._info_log


def convert_file_objects(files: List[FileObject]) -> List[Dict[str, str]]:
    """转换FastMCP文件对象为原有格式"""
    file_objects = []
    for file_obj in files:
        converted = {"path": file_obj.path}
        
        # 处理file://协议
        if file_obj.path.startswith("file://"):
            converted["path"] = url2pathname(file_obj.path.removeprefix('file:'))
        
        if file_obj.password:
            converted["password"] = file_obj.password
        if file_obj.name:
            converted["name"] = file_obj.name
            
        file_objects.append(converted)
    
    return file_objects


def generate_operation_config(
    operation_type: str,
    format_value: Optional[str] = None,
    extra_params: Optional[Dict[str, Any]] = None,
    edit_type: Optional[str] = None
) -> Dict[str, Any]:
    """生成操作配置字典"""
    config = {}
    
    # 设置操作类型
    if operation_type == "convert":
        config["is_edit_operation"] = False
        if format_value:
            config["format"] = format_value
    elif operation_type == "edit":
        config["is_edit_operation"] = True
        if edit_type:
            config["edit_type"] = edit_type
    elif operation_type == "translate":
        config["is_translate_operation"] = True
    elif operation_type == "ocr":
        config["is_ocr_operation"] = True
    elif operation_type == "summarize":
        config["is_summarize_operation"] = True
    
    # 设置额外参数
    if extra_params:
        config["extra_params"] = extra_params
    
    return config


async def process_tool_call_adapter(
    context: Context,
    file_objects: List[FileObject], 
    operation_config: Dict[str, Any]
) -> str:
    """适配原有的process_tool_call函数"""
    from ..core.processor import process_tool_call
    
    # 创建适配的logger
    logger = FastMCPLogger(context)
    
    # 转换文件对象格式
    converted_files = convert_file_objects(file_objects)
    
    # 调用原有函数
    result = await process_tool_call(logger, converted_files, operation_config)
    
    # 返回文本内容
    return result.text





async def create_pdf_adapter(
    context: Context,
    prompt: str,
    filename: str,
    language: str,
    enable_web_search: bool = False
) -> str:
    """适配PDF创建功能"""
    from ..services.create_pdf import PDFCreator
    from ..utils.common import FileHandler
    
    # 创建适配的logger和file_handler
    logger = FastMCPLogger(context)
    file_handler = FileHandler(logger)
    
    # 创建PDF创建器
    pdf_creator = PDFCreator(logger, file_handler)
    
    # 调用创建方法
    result = await pdf_creator.create_pdf_from_prompt(
        prompt=prompt,
        language=language,
        enable_web_search=enable_web_search,
        original_name=filename
    )
    
    # 生成报告
    from ..core.processor import generate_result_report
    return generate_result_report([result])


async def merge_pdfs_adapter(
    context: Context,
    files: List[FileObject]
) -> str:
    """适配PDF合并功能"""
    from ..services.editor import Editor
    from ..utils.common import FileHandler
    
    # 创建适配的logger和file_handler
    logger = FastMCPLogger(context)
    file_handler = FileHandler(logger)
    
    # 创建编辑器
    editor = Editor(logger, file_handler)
    
    # 转换文件对象
    file_paths = [file_obj.path for file_obj in files]
    passwords = [file_obj.password for file_obj in files if file_obj.password]
    original_names = [file_obj.name for file_obj in files if file_obj.name]
    
    # 处理file://协议
    for i, path in enumerate(file_paths):
        if path.startswith("file://"):
            file_paths[i] = url2pathname(path.removeprefix('file:'))
    
    # 使用第一个非空密码
    password = passwords[0] if passwords else None
    
    # 合并文件名
    merged_name = None
    if original_names:
        if len(original_names) == 1:
            merged_name = original_names[0]
        else:
            merged_name = f"{original_names[0]}_{original_names[1]}_等"
    
    # 调用合并方法
    result = await editor.merge_pdfs(file_paths, password, merged_name)
    
    # 生成报告
    from ..core.processor import generate_result_report
    return generate_result_report([result]) 
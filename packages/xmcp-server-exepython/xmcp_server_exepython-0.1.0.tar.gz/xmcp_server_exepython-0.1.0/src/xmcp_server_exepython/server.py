import logging
import sys
import traceback
import io
import argparse
from mcp.server.fastmcp import FastMCP
from pydantic import Field


def parse_args():
    parser = argparse.ArgumentParser(description='本地执行python代码MCP服务')
    parser.add_argument('--log-level', type=str, default='ERROR', 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='日志级别 (默认: ERROR)')
    parser.add_argument('--transport', type=str, default='stdio', 
                        choices=['stdio', 'sse', 'streamable-http'],
                        help='传输方式 (默认: stdio)')
    parser.add_argument('--port', type=int, default=8004, 
                        help='服务器端口 (仅在使用网络传输时有效，默认: 8004)')
    return parser.parse_args()

def setup_logger(log_level, transport):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    # 仅在非stdio模式下添加控制台处理器
    if transport != 'stdio':
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    # 避免日志传播到父记录器
    logger.propagate = False
    
    return logger

def run():
    args = parse_args()
    
    # 配置日志
    logger = setup_logger(args.log_level, args.transport)
    
    settings = {
        'log_level': args.log_level
    }
    
    # 初始化mcp服务
    mcp = FastMCP(port=args.port, settings=settings)

    @mcp.tool()
    async def execute_python_code(
        code: str = Field(description='要执行的Python代码字符串')
        ) -> str:
        """动态执行Python代码字符串并返回结果"""
        logger.info(f"收到代码执行请求，代码长度: {len(code)} 字符")
        
        # 创建一个StringIO对象来捕获标准输出
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        
        try:
            # 编译代码以便执行
            compiled_code = compile(code, '<string>', 'exec')
            
            # 创建一个命名空间来执行代码
            namespace = {}
            
            # 执行代码
            exec(compiled_code, namespace)
            
            # 获取执行期间的标准输出
            output = redirected_output.getvalue()
            
            # 收集命名空间中的变量（排除内置变量）
            variables = {k: v for k, v in namespace.items() if k not in ('__builtins__',)}
            
            # 构建结果
            result = {
                "status": "success",
                "output": output,
                "variables": variables
            }
            
            logger.info("代码执行成功")
            return result
        except Exception as e:
            # 获取错误信息
            error_msg = str(e)
            error_traceback = traceback.format_exc()
            
            # 构建错误结果
            result = {
                "status": "error",
                "message": error_msg,
                "traceback": error_traceback
            }
            
            logger.error(f"代码执行错误: {error_msg}", exc_info=True)
            return result
        finally:
            # 恢复标准输出
            sys.stdout = old_stdout

    mcp.run(transport=args.transport)

if __name__ == '__main__':
    run()
import argparse
import logging
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from wxauto import WeChat

def parse_args():
    parser = argparse.ArgumentParser(description='微信消息发送服务器')
    parser.add_argument('--log-level', type=str, default='ERROR', 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='日志级别 (默认: ERROR)')
    parser.add_argument('--transport', type=str, default='stdio', 
                        choices=['stdio', 'sse'],
                        help='传输方式 (默认: stdio)')
    parser.add_argument('--port', type=int, default=8000, 
                        help='服务器端口 (仅在使用网络传输时有效，默认: 8000)')
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
    # 初始化微信客户端
    wx = WeChat()

    # 定义工具
    @mcp.tool()
    async def send_wechat_msg(
            msg: str = Field(description='要发送的消息内容'),
            who: str = Field(description='接收消息的联系人名称')
    ) -> str:
        """发送微信文本消息
        Returns:
            发送结果是否成功
        """
        logger.info(f'准备发送消息给 {who}: {msg}')
        try:
            if not wx.ChatWith(who):
                error_msg = f"Error: Contact '{who}' not found"
                logger.error(error_msg)
                return error_msg
            
            wx.SendMsg(msg)
            logger.info(f"消息已发送给 {who}")
            return "success"
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.exception(error_msg)
            return error_msg

    mcp.run(transport=args.transport)

if __name__ == '__main__':
    run()
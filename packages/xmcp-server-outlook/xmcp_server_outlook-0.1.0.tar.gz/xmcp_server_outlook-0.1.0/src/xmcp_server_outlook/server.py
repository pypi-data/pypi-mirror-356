import win32com.client
import logging
import json
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
from pydantic import Field
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Outlook操作MCP服务，主要是发邮箱和操作日历')
    parser.add_argument('--log-level', type=str, default='ERROR', 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='日志级别 (默认: ERROR)')
    parser.add_argument('--transport', type=str, default='stdio', 
                        choices=['stdio', 'sse', 'streamable-http'],
                        help='传输方式 (默认: stdio)')
    parser.add_argument('--port', type=int, default=8003, 
                        help='服务器端口 (仅在使用网络传输时有效，默认: 8003)')
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

    AUTH_KEY = "nwcfshjsojzmbjdh"
    LOCAL_TIMEZONE = "Asia/Shanghai"
    logger.info(f"Using local timezone: {LOCAL_TIMEZONE}")

    def get_outlook_application():
        try:
            outlook = win32com.client.GetActiveObject("Outlook.Application")
            logger.info("Connected to existing Outlook instance")
        except:
            outlook = win32com.client.Dispatch("Outlook.Application")
            logger.info("Created new Outlook instance")
        return outlook

    def get_outlook_calendar():
        try:
            outlook = get_outlook_application()
            namespace = outlook.GetNamespace("MAPI")
            
            if namespace.ExchangeConnectionMode > 0:
                logger.info(f"Connected to Exchange Server. Connection mode: {namespace.ExchangeConnectionMode}")
            else:
                logger.warning("Not connected to Exchange Server. Using default profile.")
            
            calendar = namespace.GetDefaultFolder(9)
            return calendar
        except Exception as e:
            logger.error(f"Failed to get Outlook calendar: {str(e)}")
            if "0x80040111" in str(e):
                logger.error("Error code 0x80040111: Outlook may not be running or properly configured.")
            elif "0x8004010F" in str(e):
                logger.error("Error code 0x8004010F: MAPI or an underlying service provider failed.")
            raise

    def parse_local_time(time_str, format_str='%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(time_str, format_str)
        except Exception as e:
            logger.error(f"Error parsing local time: {str(e)}")
            raise

    # 修复：直接返回本地时间字符串，不进行时区转换
    def convert_to_outlook_time(local_time):
        # Outlook期望的是本地时间字符串，格式为 "MM/DD/YYYY HH:MM AM/PM"
        return local_time.strftime('%m/%d/%Y %I:%M %p')

    mcp = FastMCP(port=8003)
    authenticated_clients = set()

    @mcp.tool()
    async def auth(key: str) -> str:
        client_id = mcp.get_current_client_id()
        logger.info(f"Client {client_id} attempting authentication")
        
        if key == AUTH_KEY:
            authenticated_clients.add(client_id)
            logger.info(f"Client {client_id} authenticated successfully")
            return json.dumps({"status": "success", "message": "Authenticated successfully"})
        else:
            logger.warning(f"Client {client_id} authentication failed")
            return json.dumps({"status": "error", "message": "Invalid authentication key"})

    def require_auth(func):
        async def wrapper(*args, **kwargs):
            client_id = mcp.get_current_client_id()
            if client_id not in authenticated_clients:
                return json.dumps({"status": "error", "message": "Not authenticated"})
            return await func(*args, **kwargs)
        return wrapper

    @mcp.tool()
    async def get_events(
        start_date: str = Field(description='要查询的开始时间，例如2025-06-10 00:00:00'), 
        end_date: str = Field(description='要查询的结束时间，例如2025-06-10 23:59:59')
        ) -> str:
        """获取Outlook的指定时间范围的事件.
        Returns:
            事件信息字符串
        """
        try:
            if not start_date:
                start_date = datetime.now().strftime('%Y-%m-%d')
            if not end_date:
                end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            
            start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%m/%d/%Y %H:%M %p')
            end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%m/%d/%Y %H:%M %p')
            
            calendar = get_outlook_calendar()
            events = calendar.Items
            events.Sort("[Start]")
            events.IncludeRecurrences = True
            events = events.Restrict(f"[Start] >= '{start_date_formatted}' AND [End] <= '{end_date_formatted}'")
            
            event_list = []
            for event in events:
                event_data = {
                    "subject": event.Subject,
                    "start": event.Start.strftime('%Y-%m-%d %H:%M:%S'),
                    "end": event.End.strftime('%Y-%m-%d %H:%M:%S'),
                    "location": event.Location,
                    "body": event.Body,
                    "is_all_day": event.AllDayEvent,
                    "event_id": event.EntryID
                }
                event_list.append(event_data)
            
            logger.info(f"Retrieved {len(event_list)} events for date range {start_date} to {end_date}")
            return json.dumps({"status": "success", "events": event_list})
        except Exception as e:
            logger.error(f"Error getting events: {str(e)}")
            return json.dumps({"status": "error", "message": f"Error getting events: {str(e)}"})

    @mcp.tool()
    async def create_event(subject: str, start: str, end: str, 
                        location: str = "", body: str = "", is_all_day: bool = False) -> str:
        """给Outlook日历创建一个新事件.
        Returns:
            事件ID等JSON的字符串
        """
        try:
            calendar = get_outlook_calendar()
            event = calendar.Items.Add()
            
            event.Subject = subject
            
            # 解析日期时间字符串并转换为Outlook可接受的本地时间格式
            start_datetime = parse_local_time(start)
            end_datetime = parse_local_time(end)
            
            # 关键修复：直接使用本地时间字符串，不进行时区转换
            event.Start = convert_to_outlook_time(start_datetime)
            event.End = convert_to_outlook_time(end_datetime)
            
            event.Location = location
            event.Body = body
            event.AllDayEvent = is_all_day
            
            event.Save()
            
            logger.info(f"Created new event: {subject}")
            logger.info(f"start: {start}, end: {end}, location: {location}, body: {body}")
            return json.dumps({
                "status": "success",
                "event_id": event.EntryID
            })
        except Exception as e:
            logger.error(f"Error creating event: {str(e)}")
            return json.dumps({"status": "error", "message": f"Error creating event: {str(e)}"})

    @mcp.tool()
    async def update_event(event_id: str, subject: str = None, start: str = None, end: str = None, 
                        location: str = None, body: str = None, is_all_day: bool = None) -> str:
        """更新Outlook日历的事件.
        Returns:
            更新成功标识以及事件ID等JSON的字符串
        """
        try:
            if not event_id:
                return json.dumps({"status": "error", "message": "Event ID is required"})
            
            outlook = get_outlook_application()
            namespace = outlook.GetNamespace("MAPI")
            event = namespace.GetItemFromID(event_id)
            
            if subject is not None:
                event.Subject = subject
            if start is not None:
                start_datetime = parse_local_time(start)
                event.Start = convert_to_outlook_time(start_datetime)
            if end is not None:
                end_datetime = parse_local_time(end)
                event.End = convert_to_outlook_time(end_datetime)
            if location is not None:
                event.Location = location
            if body is not None:
                event.Body = body
            if is_all_day is not None:
                event.AllDayEvent = is_all_day
            
            event.Save()
            
            logger.info(f"Updated event with ID: {event_id}")
            return json.dumps({"status": "success", "event_id": event_id})
        except Exception as e:
            logger.error(f"Error updating event: {str(e)}")
            return json.dumps({"status": "error", "message": f"Error updating event: {str(e)}"})

    @mcp.tool()
    async def delete_event(event_id: str) -> str:
        """删除Outlook日历的事件.
        Returns:
            删除成功标识以及事件ID等JSON的字符串
        """
        try:
            if not event_id:
                return json.dumps({"status": "error", "message": "Event ID is required"})
            
            outlook = get_outlook_application()
            namespace = outlook.GetNamespace("MAPI")
            event = namespace.GetItemFromID(event_id)
            
            event.Delete()
            
            logger.info(f"Deleted event with ID: {event_id}")
            return json.dumps({"status": "success", "event_id": event_id})
        except Exception as e:
            logger.error(f"Error deleting event: {str(e)}")
            return json.dumps({"status": "error", "message": f"Error deleting event: {str(e)}"})

    @mcp.tool()
    async def send_email(to: str, subject: str, body: str, cc: str = "", bcc: str = "") -> str:
        """发送邮件给Outlook邮箱.
        Returns:
            发送成功标识JSON的字符串
        """
        try:
            outlook = get_outlook_application()
            mail = outlook.CreateItem(0)
            
            mail.To = to
            mail.Subject = subject
            mail.Body = body
            
            if cc:
                mail.CC = cc
            if bcc:
                mail.BCC = bcc
            
            mail.Send()
            
            logger.info(f"Sent email to {to} with subject: {subject}")
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return json.dumps({"status": "error", "message": f"Error sending email: {str(e)}"})

    @mcp.tool()
    async def get_emails(
        date_from: str = Field(description='要查询的开始时间，例如2025-06-10 00:00:00'), 
        date_to: str = Field(description='要查询的开始时间，例如2025-06-10 23:59:059'), 
        folder_name: str = "Inbox", 
        max_count: int = 10, 
        unread_only: bool = False
        ) -> str:
        """获取Outlook邮箱的邮件.
        Returns:
            处理状态和邮件列表JSON的字符串
        """
        try:
            outlook = get_outlook_application()
            namespace = outlook.GetNamespace("MAPI")
            
            try:
                folder = namespace.Folders.Item(folder_name)
            except:
                folder = namespace.GetDefaultFolder(6)
            
            messages = folder.Items
            messages.Sort("[ReceivedTime]", True)
            
            today = datetime.now()
            default_from = (today - timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
            default_to = today.strftime('%Y-%m-%d %H:%M:%S')
            
            date_from = date_from or default_from
            date_to = date_to or default_to
            
            date_from_formatted = datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %H:%M %p')
            date_to_formatted = datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y %H:%M %p')
            
            time_filter = f"[ReceivedTime] >= '{date_from_formatted}' AND [ReceivedTime] <= '{date_to_formatted}'"
            messages = messages.Restrict(time_filter)
            
            if unread_only:
                messages = messages.Restrict("[Unread] = True")
            
            email_list = []
            count = 0
            
            for message in messages:
                if count >= max_count:
                    break
                    
                try:
                    if message.SenderEmailType == "EX":
                        sender_email = message.Sender.GetExchangeUser().PrimarySmtpAddress
                    else:
                        sender_email = message.SenderEmailAddress
                        
                    email_data = {
                        "subject": message.Subject,
                        "sender": message.SenderName,
                        "sender_email": sender_email,
                        "received_time": message.ReceivedTime.strftime('%Y-%m-%d %H:%M:%S'),
                        "body": message.Body[:500] + "..." if len(message.Body) > 500 else message.Body,
                        "is_read": not message.Unread,
                        "email_id": message.EntryID
                    }
                    email_list.append(email_data)
                    count += 1
                except Exception as msg_err:
                    logger.warning(f"Error processing email: {str(msg_err)}")
                    continue
            
            logger.info(f"Retrieved {len(email_list)} emails from {folder_name} between {date_from} and {date_to}")
            return json.dumps({"status": "success", "emails": email_list})
        except Exception as e:
            logger.error(f"Error getting emails: {str(e)}")
            return json.dumps({"status": "error", "message": f"Error getting emails: {str(e)}"})

    mcp.run(transport=args.transport)

if __name__ == '__main__':
    run()
import os
import socket
from abc import ABC, abstractmethod
from datetime import datetime
from dotenv import load_dotenv
import time

from telegram_bot.config.telegram_send_config import ParseMode
from telegram_bot.utiles.get_logger import get_logger, logging


class BaseTelegramSender(ABC):
    """
    텔레그램 메시지 송신 기능의 공통 기반 클래스입니다.
    - 텍스트, 문서, 미디어 등 다양한 메시지 송신 클래스들이 상속하여 사용합니다.
    - 토큰 로딩, 로깅, 메시지 분할, 시스템 정보 헤더 생성 등 공통 기능을 제공합니다.
    """

    def __init__(self, token: str | None = None, verbose: bool = True):
        """
        초기화 함수

        Args:
            token (str | None): 직접 지정한 텔레그램 봇 토큰. 지정하지 않으면 환경변수에서 로드됩니다.
        """
        self.token = token or self._load_bot_token()
        self.logger = get_logger(
            self.__class__.__name__,
            level=logging.INFO if verbose else logging.WARNING
        )

    @staticmethod
    def _load_bot_token() -> str:
        """
        TELEGRAM_BOT_TOKEN 환경변수를 로드하여 반환합니다.

        Returns:
            str: 텔레그램 봇 토큰

        Raises:
            ValueError: 환경변수가 없을 경우 예외 발생
        """
        load_dotenv()
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            raise ValueError("❗ TELEGRAM_BOT_TOKEN 환경변수가 설정되지 않았습니다.")
        return bot_token

    @staticmethod
    def _split_message(message: str, max_length: int = 4096) -> list[str]:
        """
        긴 메시지를 max_length 단위로 분리합니다.

        Args:
            message (str): 전체 메시지 문자열
            max_length (int): 메시지 분할 기준 길이

        Returns:
            list[str]: 분할된 메시지 리스트
        """
        lines = message.splitlines(keepends=True)
        chunks: list[str] = []
        current_chunk = ""

        for line in lines:
            if len(current_chunk) + len(line) <= max_length:
                current_chunk += line
            else:
                chunks.append(current_chunk)
                current_chunk = line
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    @staticmethod
    def _get_hostname() -> str:
        """현재 호스트명을 반환합니다."""
        return socket.gethostname()

    @staticmethod
    def _get_filename() -> str:
        """현재 파일명을 반환합니다."""
        return os.path.basename(__file__)

    @staticmethod
    def _get_pid() -> int:
        """현재 프로세스의 PID를 반환합니다."""
        return os.getpid()

    @staticmethod
    def _get_timestamp() -> str:
        """현재 시간을 포맷팅하여 반환합니다."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _format_header_markdown(self, hostname: str, filename: str, pid: int, timestamp: str) -> str:
        """MARKDOWN 형식의 메시지 헤더를 생성합니다."""
        return (
            f"```text\n"
            f"📢 *프로세스 상태 보고*\n\n"
            f"📁 File    : {filename}\n"
            f"💻 Host    : {hostname}\n"
            f"⚙️  PID    : {pid}\n"
            f"🕒 Time    : {timestamp}\n"
            f"```\n"
            f"----------\n\n"
        )

    def _format_header_html(self, hostname: str, filename: str, pid: int, timestamp: str) -> str:
        """HTML 형식의 메시지 헤더를 생성합니다."""
        return (
            f"<pre>\n"
            f"📢 <b>프로세스 상태 보고</b>\n"
            f"📁 File    : {filename}\n"
            f"💻 Host    : {hostname}\n"
            f"⚙️  PID    : {pid}\n"
            f"🕒 Time    : {timestamp}\n"
            f"</pre>\n"
            f"----------\n\n"
        )

    def _generate_base_info(self, parse_mode: ParseMode = ParseMode.MARKDOWN) -> str:
        """
        시스템 상태 및 실행 정보를 포함한 메시지 헤더를 생성합니다.

        Args:
            parse_mode (ParseMode): 메시지 포맷 모드 (MARKDOWN or HTML)

        Returns:
            str: 포맷팅된 상태 정보 헤더 문자열
        """
        hostname = self._get_hostname()
        filename = self._get_filename()
        pid = self._get_pid()
        timestamp = self._get_timestamp()

        if parse_mode == ParseMode.MARKDOWN:
            return self._format_header_markdown(hostname, filename, pid, timestamp)
        if parse_mode == ParseMode.HTML:
            return self._format_header_html(hostname, filename, pid, timestamp)
        return ""

    def send_with_retry(self, send_func: callable, max_retries: int = 3, delay: int = 3) -> None:
        """
        재시도 로직을 포함한 메시지 전송 래퍼

        Args:
            send_func (callable): 예외 발생 가능성이 있는 전송 함수
            max_retries (int): 최대 재시도 횟수
            delay (int): 실패 시 대기 시간(초)
        """
        for attempt in range(1, max_retries + 1):
            try:
                send_func()
                return  # 성공 시 종료
            except Exception as e:
                self.logger.warning("전송 시도 %d 실패: %s", attempt, e, exc_info=True)
                if attempt < max_retries:
                    time.sleep(delay)
                else:
                    self.logger.error("모든 전송 시도 실패", exc_info=True)

    @abstractmethod
    def send(self, *args, **kwargs) -> None:
        """
        하위 클래스에서 구현해야 하는 전송 메서드입니다.
        """
        ...

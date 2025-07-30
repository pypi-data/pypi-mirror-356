from telegram_bot.config.telegram_send_config import TelegramSendConfig, ParseMode
from telegram_bot.senders.text_sender import TextSender
from telegram_bot.services.base.base_telegram_sender import BaseTelegramSender
from typing import List
from time import sleep
from telegram_bot.utiles.format_base_header_message import format_base_header_message
import re
from telegram_bot.errors.telegram_send_error import TelegramSendError

class TelegramTextSender(BaseTelegramSender):
    """
    텔레그램 텍스트 메시지 전송기 클래스

    - 텔레그램 텍스트 메시지를 전송하기 위한 Wrapper 클래스입니다.
    - BaseTelegramSender로부터 기본 토큰 로딩, 로깅, 메시지 헤더 등 공통 기능을 상속받습니다.
    - 긴 메시지 자동 분할 기능 및 메시지 리스트 순차 전송 기능을 제공합니다.
    """

    def __init__(self, token: str | None = None, verbose: bool = True):
        """
        TelegramTextSender 클래스 초기화

        Args:
            token (str | None): 직접 지정한 텔레그램 봇 토큰. None이면 환경변수에서 로드됩니다.
        """
        super().__init__(token, verbose=verbose)
        self.sender = TextSender(token=self.token, verbose=verbose)


    def send(
        self,
        message: str,
        chat_id: str = "-1002694727655",
        thread_id: int = 20,
        parse_mode: ParseMode = ParseMode.MARKDOWN,
        is_include_base_info: bool = True
    ) -> None:
        """
        텍스트 메시지를 텔레그램으로 전송합니다.
        - 메시지가 길면 자동 분할됩니다.
        - 시스템 실행 정보(파일명, 호스트, PID 등)를 헤더로 포함할 수 있습니다.

        Args:
            message (str): 전송할 메시지 문자열
            chat_id (str): 전송 대상 채팅 ID
            thread_id (int): 메시지를 보낼 스레드 ID (포럼 채널용)
            parse_mode (ParseMode): 텍스트 파싱 방식 (MARKDOWN or HTML)
            is_include_base_info (bool): 시스템 정보 헤더 포함 여부

        Example:
            >>> sender = TelegramTextSender()
            >>> sender.send("Hello from bot")
            >>> sender.send("HTML 메세지", parse_mode=ParseMode.HTML)
        """
        try:
            full_message = self._build_message(message, parse_mode, is_include_base_info)
            self._send_single_chunk(
                text=full_message,
                chat_id=chat_id,
                thread_id=thread_id,
                parse_mode=parse_mode
            )
        except Exception as original_e:
            msg = f"텍스트 전송 실패: {original_e}"
            self.logger.exception(msg, exc_info=True)
            raise TelegramSendError(message=msg, chat_id=chat_id, thread_id=thread_id) from original_e

    def _build_message(
        self,
        message: str,
        parse_mode: ParseMode,
        is_include_base_info: bool
    ) -> str:
        """
        헤더 포함 여부에 따라 최종 메시지 조합

        Returns:
            str: 최종 전송 메시지
        """
        start_message = format_base_header_message() + "\n\n"
        header = self._generate_base_info(parse_mode) if is_include_base_info else ""
        return start_message + header + message

    def _parse_retry_delay(self, error_message: str) -> int | None:
        """
        에러 메시지에서 'retry after N seconds' 또는 유사한 문구를 찾아
        재시도 대기 시간(초)을 추출합니다.

        Args:
            error_message (str): 예외 메시지 문자열

        Returns:
            int | None: 대기 시간(초). 매칭되는 문구가 없으면 None 반환
        """
        # Flood control 관련 대기시간 패턴 정의 (retry in|after N seconds)
        retry_pattern = re.compile(r"retry\s*(?:in|after)\s*(\d+)\s*seconds?", re.IGNORECASE)

        # 에러 메시지에서 패턴 매칭 시도
        match = retry_pattern.search(error_message)

        if match:
            # 매칭된 숫자를 int로 변환 후 1초 여유 추가
            return int(match.group(1)) + 1
        return None

    def _send_once(self, config, text: str) -> None:
        """
        단일 메시지를 Telegram API로 한 번 전송합니다.

        Args:
            config (TelegramSendConfig): Telegram 전송 설정 정보
            text (str): 전송할 메시지 텍스트

        Raises:
            Exception: Telegram API 호출 실패 시 해당 예외를 그대로 던짐
        """
        self.logger.info(f"Sending chunk (len={len(text)})...")
        # Telegram API 호출 - 동기 방식
        self.sender.send_sync(config=config, text=text)
        self.logger.info("단일 메시지 전송 완료")

    def _send_single_chunk(
        self,
        text: str,
        chat_id: str,
        thread_id: int,
        parse_mode: ParseMode
    ) -> None:
        """
        단일 메시지를 Telegram에 전송합니다.
        Flood control 에러가 발생하면, 에러 메시지에 명시된 시간만큼 대기 후 자동으로 재시도합니다.

        Args:
            text (str): 전송할 메시지 텍스트
            chat_id (str): 대상 채팅 ID
            thread_id (int): 메시지를 보낼 스레드 ID
            parse_mode (ParseMode): 메시지 파싱 방식 (MARKDOWN, HTML 등)

        Raises:
            TelegramSendError: 전송 실패 시 발생, Flood control 이외의 에러 포함
        """
        # 전송 구성 객체 생성
        config = TelegramSendConfig(
            chat_id=chat_id,
            message_thread_id=thread_id,
            parse_mode=parse_mode,
            read_timeout=60, write_timeout=60,
            connect_timeout=60, pool_timeout=60,
        )

        attempt = 0  # 재시도 횟수 카운터

        while True:
            attempt += 1
            try:
                self.logger.info(f"[Attempt {attempt}] Sending chunk...")
                # 한 번 메시지 전송 시도
                self._send_once(config, text)
                # 성공하면 루프 종료
                break

            except Exception as e:
                # 예외 메시지 로깅
                self.logger.exception(f"단일 메시지 전송 실패: {e}")

                # 에러 메시지에서 Flood control 대기 시간 파싱
                delay = self._parse_retry_delay(str(e))

                if delay is not None:
                    # Flood control 에러이면, 대기 후 재시도
                    self.logger.warning(f"Flood control – {delay}s 대기 후 재시도")
                    sleep(delay)
                    continue  # 재시도 반복문 계속 실행

                # Flood control 에러가 아니면 TelegramSendError로 예외 래핑 후 던짐
                raise TelegramSendError(message="Flood control이 아닌 에러. "+text, chat_id=chat_id, thread_id=thread_id) from e

    def send_text_list(
        self,
        text_list: List[str],
        thread_id: int,
        delay: float = 5.0,
        parse_mode: ParseMode = ParseMode.MARKDOWN
    ) -> None:
        """
        텍스트 메시지 리스트를 순차적으로 전송합니다.
        - 각 메시지를 텔레그램의 최대 허용 길이(4096자)에 맞게 자동 분할하여 전송합니다.
        - 메시지 간 전송 간격을 조절할 수 있습니다.

        Args:
            text_list (List[str]): 전송할 문자열 리스트
            thread_id (int): 메시지를 보낼 스레드 ID
            delay (float): 메시지 전송 간의 딜레이 (초)
            parse_mode (ParseMode): 텍스트 파싱 방식

        Example:
            >>> sender = TelegramTextSender()
            >>> texts = ["메시지 1", "메시지 2", "메시지 3"]
            >>> sender.send_text_list(texts, thread_id=30)
        """
        buffer = ""
        telegram_max_length = 4096

        for text in text_list:
            cleaned_text = text.strip()
            addition = cleaned_text + "\n\n"

            if len(buffer) + len(addition) > telegram_max_length:
                if buffer:
                    self.send(
                        message=buffer.strip(),
                        thread_id=thread_id,
                        is_include_base_info=False,
                        parse_mode=parse_mode
                    )
                    sleep(delay)
                buffer = addition
            else:
                buffer += addition

        if buffer.strip():
            self.send(
                message=buffer.strip(),
                thread_id=thread_id,
                is_include_base_info=False,
                parse_mode=parse_mode
            )


if __name__ == "__main__":
    # Example usage
    tts = TelegramTextSender()

    t = """
<pre>    
📢 <b>프로세스 상태 보고</b>
📁 File    : base_telegram_sender.py
💻 Host    : mjun-macbook-pro-m1.local
⚙️  PID    : 17751
🕒 Time    : 2025-06-05 16:07:52
</pre>
-----

👉🏻 경영권 분쟁
06-05(목) 10:00 <a href="http://example.com/news/1">경영권 분쟁 소식</a>
비교 종목: <a href="http://kind.example.com">비교회사</a>
    """
    t = """
06-04(수) 18:08
  🔗 <a href="https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20250604900487">[코스닥시장] 위니아 - 주권매매거래정지해제 (상장폐지에 따른 정리매매 개시)</a>
  - Kind: <a href="https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20250604000487&docno=&viewerhost=&viewerport=">주권매매거</a> | <a href="https://kind.krx.co.kr/common/chart.do?method=loadInitPage&ispopup=true&isurcd=07146">차트</a> | <a href="https://kind.krx.co.kr/common/stockprices.do?method=searchStockPricesMain&isurCd=07146">주가</a>

<pre>
주권매매거래정지해제
1.대상종목
(주)위니아
보통주
2.해제사유
상장폐지에 따른 정리매매 개시
3.해제일시
2025-06-09
-
4.근거규정
코스닥시장상장규정 제18조 및 동규정시행세칙 제19조
5.기타
ㅇ 상장폐지 내역
- 상장폐지사유 : 감사의견 거절(감사범위 제한 및 계속기업가정 불확실성)
- 정리매매기간 : 2025.06.09 ~ 2025.06.17(7매매일)
- 상장폐지일 : 2025.06.18
</pre>
    """
    # tts.send(message='단일 메시지 테스트')
    tts.send(message=t, parse_mode=ParseMode.HTML)

# src/telegram_bot/senders/base.py
from abc import ABC, abstractmethod
from telegram_bot.core.single_tone.service import TelegramService
from telegram_bot.config.telegram_send_config import TelegramSendConfig
import asyncio
from telegram_bot.utiles.get_logger import get_logger, logging
from tenacity import stop_after_attempt, wait_exponential, retry_if_exception_type, AsyncRetrying, after_log


class BaseSender(ABC):
    """
    Telegram 메시지 전송을 위한 비동기/동기 인터페이스 추상 클래스.

    이 클래스는 TelegramService를 통해 봇 인스턴스를 전역에서 가져와
    다양한 메시지 전송 형식을 하위 클래스에서 구현할 수 있도록 돕습니다.

    주요 기능:
    - 비동기 전송 함수(send) 추상화
    - 동기 환경에서도 메시지 전송 가능한 send_sync 제공
    """

    def __init__(self, token: str, verbose: bool = True):
        """
        TelegramService를 통해 봇 인스턴스를 초기화합니다.

        Args:
            token (str): Telegram Bot Token
        """
        self.logger = get_logger(__name__, level=logging.INFO if verbose else logging.WARNING)
        self.logger.info("BaseSender 초기화 시작")

        # TelegramService.init(token)은 싱글톤 Application을 반환
        self.bot = TelegramService.init(token=token, verbose=verbose).bot

        masked_token = self.bot.token[:6] + " ... " + self.bot.token[-4:]
        self.logger.info(f"Telegram Bot 초기화 완료 (token: {masked_token})")

    @abstractmethod
    async def send(self, config: TelegramSendConfig, **kwargs):
        """
        비동기 메시지 전송 메서드 (하위 클래스에서 구현 필요)

        Args:
            config (TelegramSendConfig): 메시지 전송에 필요한 구성 정보
            **kwargs: 메시지 유형별 추가 파라미터
        """
        raise NotImplementedError("하위 클래스에서 send 메서드를 구현해야 합니다.")

    async def send_with_retry(self, config: TelegramSendConfig, **kwargs):
        async_retry = AsyncRetrying(
            stop=stop_after_attempt(3),
            wait=wait_exponential(exp_base=3, multiplier=3, min=3, max=60),
            retry=retry_if_exception_type(Exception),
            after=after_log(get_logger("After Retry in BaseSender", logging.DEBUG), logging.DEBUG),
            reraise=True
        )
        async for attempt in async_retry:
            with attempt:
                self.logger.info(f"this is the {attempt.retry_state.attempt_number}st time calling it ")
                return await self.send(config, **kwargs)

    def _start_msg(self):
        if not hasattr(self, "logger"):
            # 혹은 self.logger = get_logger(...) 를 강제 초기화
            print("[SYNC] Logger is not initialized yet")
        else:
            self.logger.info("[SYNC] 동기 메시지 전송 시도 중...")

    def send_sync(self, config: TelegramSendConfig, **kwargs):
        """
        비동기 send 메서드를 동기 방식으로 실행합니다.

        다양한 실행 환경(Jupyter, CLI, 서버 등)을 고려하여
        실행 중인 루프가 있는지 확인 후 적절한 방식으로 실행합니다.

        Args:
            config (TelegramSendConfig): 메시지 전송 설정
            **kwargs: 메시지 전송에 필요한 기타 인자

        Returns:
            메시지 전송 결과 또는 Future 객체 (Jupyter 등에서는 await 필요)
        """

        self.logger.info("[SYNC] 동기 메시지 전송 시도 중...")

        try:
            loop = asyncio.get_event_loop()
            log = get_logger(__name__, level=logging.DEBUG)

            if loop.is_running():
                # Jupyter Notebook 등에서 이미 루프가 실행 중인 경우
                log.warning("[SYNC] 현재 이벤트 루프가 실행 중입니다. Future 반환")
                future = asyncio.ensure_future(self.send_with_retry(config, **kwargs))
                log.debug(f"[SYNC] Future 생성됨: {future}")
                return future
            else:
                self.logger.debug("[SYNC] 실행 중인 루프 없음, run_until_complete 사용")
                result = loop.run_until_complete(self.send_with_retry(config, **kwargs))
                self.logger.info("[SYNC] 메시지 전송 완료")
                return result

        except RuntimeError as e:
            # 루프가 닫힌 경우 새 루프 생성
            if "Event loop is closed" in str(e):
                self.logger.warning("[SYNC] 이벤트 루프가 닫혀있습니다. 새 루프 생성 시도")
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                result = new_loop.run_until_complete(self.send_with_retry(config, **kwargs))
                self.logger.info("[SYNC] 메시지 전송 완료 (새 루프)")
                return result
            else:
                self.logger.exception("[SYNC] 메시지 전송 중 오류 발생")
                raise RuntimeError(f"동기 메시지 전송 중 오류 발생: {e}") from e

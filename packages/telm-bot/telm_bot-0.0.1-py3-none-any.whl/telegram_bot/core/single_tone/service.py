# src/telegram_bot/service.py
import asyncio
from telegram.ext import Application, ApplicationBuilder

from telegram_bot.utiles.get_logger import get_logger, logging


class TelegramService:
    """
    TelegramService는 telegram.ext.Application 객체를 싱글톤으로 관리합니다.

    사용 목적:
    - 봇 초기화 및 전역 재사용
    - senders, handlers 등 다양한 모듈에서 공통된 Bot/Loop 접근
    """

    _app: Application = None  # 싱글톤 Application 인스턴스
    _loop: asyncio.AbstractEventLoop = None  # 전역 이벤트 루프
    logger: logging.Logger = None

    @classmethod
    def init(cls, token: str, verbose: bool = False) -> Application:
        """
        Telegram Application을 초기화하고 반환합니다.
        여러 번 호출해도 최초 한 번만 Application을 생성합니다.
        """

        if cls.logger is None:
            cls.logger = get_logger(__name__, level=logging.INFO if verbose else logging.WARNING)

        cls.log("🚀 [init] TelegramService.init() 호출됨")

        if cls._app is None:
            cls.log("🔧 [init] Application이 아직 초기화되지 않음 → 초기화 시작")
            try:
                cls._app = cls._build_application(token)
                cls._loop = cls._initialize_event_loop(cls._app)
                cls.log("🎉 [init] TelegramService 초기화 및 루프 설정 완료")
            except Exception as e:
                cls.log("Telegram Application 초기화 실패", is_exception=True)
                cls.log(f"❌ [init] 예외 발생: {e}", is_exception=True)
                raise RuntimeError(f"TelegramService 초기화 중 오류 발생: {e}")
        else:
            cls.log("♻️ [init] 기존에 초기화된 Application 반환")

        return cls._app
    @classmethod
    def log(cls, message: str, is_exception: bool = False) -> None:
        """
        로그 메시지를 출력합니다. 초기화된 로거가 없으면 기본 로거를 사용합니다.

        Args:
            message (str): 로그로 출력할 메시지
        """
        if cls.logger is not None:
            if is_exception:
                cls.logger.exception(message)
            else:
                cls.logger.info(message)
        else:
            print(f"🔍 [log] 아직 로거가 초기화되지 않았습니다. 메시지: {message}")

    @classmethod
    def _build_application(cls, token: str) -> Application:
        """ApplicationBuilder를 사용하여 Telegram Application을 생성합니다."""
        cls.log("🏗️ [build] ApplicationBuilder로 Telegram Application 생성 중...")
        app = (
            ApplicationBuilder()
            .token(token)
            .concurrent_updates(True)
            .build()
        )
        cls.log("✅ [build] Application 인스턴스 생성 완료")
        return app

    @classmethod
    def _initialize_event_loop(cls, app: Application) -> asyncio.AbstractEventLoop:
        """Application을 초기화할 asyncio 이벤트 루프를 설정합니다."""
        try:
            loop = asyncio.get_running_loop()
            cls.log("⚠️ [loop] 실행 중인 루프 탐지됨 (예: Jupyter 환경)")
            asyncio.ensure_future(app.initialize())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            cls.log("🕹️ [loop] 실행 중인 루프 없음 → 새 루프 생성 및 설정")
            loop.run_until_complete(app.initialize())

        cls.log("🎯 [loop] Application 초기화 완료")
        return loop

    @classmethod
    def get_app(cls) -> Application:
        """
        초기화된 Application 인스턴스를 반환합니다.
        사전에 init(token)을 호출해야 합니다.

        Returns:
            Application: telegram.ext.Application 인스턴스
        """
        if cls._app is None:
            raise RuntimeError("TelegramService.init(token)을 먼저 호출해야 합니다.")
        return cls._app

    @classmethod
    def get_bot(cls):
        """
        초기화된 Bot 인스턴스를 반환합니다.

        Returns:
            Bot: telegram.Bot 인스턴스
        """
        if cls._app is None:
            raise RuntimeError("TelegramService.init(token)을 먼저 호출해야 합니다.")
        return cls._app.bot

    @classmethod
    def run(cls):
        """
        봇을 폴링 모드로 실행합니다. (블로킹 함수)
        """
        if cls._app is None:
            raise RuntimeError("TelegramService.init(token)을 먼저 호출해야 합니다.")
        cls._app.run_polling()

    @classmethod
    def loop(cls) -> asyncio.AbstractEventLoop:
        """
        Telegram Application이 사용하는 asyncio 이벤트 루프를 반환합니다.

        Returns:
            asyncio.AbstractEventLoop: 이벤트 루프
        """
        if cls._loop is not None:
            return cls._loop

        try:
            cls._loop = asyncio.get_running_loop()
        except RuntimeError:
            cls._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(cls._loop)
        return cls._loop

    @classmethod
    async def shutdown(cls):
        """
        Application을 비동기로 안전하게 종료합니다.
        """
        if cls._app:
            if cls._app.running:
                # 실행 중이면 먼저 stop() 호출 후 shutdown()
                await cls._app.stop()
                await cls._app.shutdown()
            else:
                print("🛑 [shutdown] Application이 실행 중이 아니므로 stop()은 건너뜀")
                await cls._app.shutdown()

            cls._app = None
            cls._loop = None

        print(f"🛑 [shutdown] TelegramService가 정상적으로 종료되었습니다.\ncls._app: {cls._app}, cls._loop: {cls._loop}")


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv


    async def main():
        load_dotenv()
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise EnvironmentError("환경변수 TELEGRAM_BOT_TOKEN 이 누락되었습니다.")

        app = TelegramService.init(token)

        # ✅ 직접 initialize() 호출
        await app.initialize()

        bot = TelegramService.get_bot()
        print(f"Bot: @{bot.username}")

        # 앱 실행 (여기서 running=True 상태가 됨)
        # run_polling은 blocking 함수라 await 불가. 대신 start()를 씁니다.
        # await app.start()

        await TelegramService.shutdown()



    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise EnvironmentError("환경변수 TELEGRAM_BOT_TOKEN 이 누락되었습니다.")

    asyncio.run(main())

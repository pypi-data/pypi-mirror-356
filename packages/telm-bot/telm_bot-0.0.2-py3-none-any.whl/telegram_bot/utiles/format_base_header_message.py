import locale  # 날짜/시간 로케일 설정을 위해 사용
import platform  # 현재 OS 확인용 (Windows, Linux, macOS 등)
from datetime import datetime  # 현재 시간 확인용

def format_base_header_message():
    """
    텔레그램 로그 메시지의 헤더 형식을 생성합니다.
    형식 예시: 🟢 (25-05-28 15:35:07 | 수)

    - OS에 따라 한글 요일을 표시하기 위한 로케일을 자동 설정합니다.
    - 로케일 설정에 실패하면 영어 요일로 fallback됩니다.

    Returns:
        str: 형식화된 헤더 문자열
    """

    # 현재 실행 중인 운영체제 감지
    system = platform.system()

    try:
        # OS에 따라 적절한 한글 로케일 설정
        if system == "Windows":
            # Windows는 'Korean_Korea.949' 사용
            locale.setlocale(locale.LC_TIME, "Korean_Korea.949")
        else:
            # macOS/Linux는 'ko_KR.UTF-8' 사용
            locale.setlocale(locale.LC_TIME, "ko_KR.UTF-8")
    except locale.Error:
        # 로케일 설정 실패 시 경고 출력 (영어 요일로 fallback)
        print("⚠️ 로케일 설정 실패: 한글 요일이 아닌 영어로 표시됩니다.")

    # 현재 시각 가져오기
    now = datetime.now()

    # 날짜 포맷: 🟢 (25-05-28 15:35:07 | 수)
    # %y: 두 자리 연도, %m: 월, %d: 일, %H:%M:%S: 시:분:초, %a: 요일(한글 또는 영어)
    formatted = now.strftime("(%y-%m-%d %H:%M:%S | %a)")

    return "🟢 " + formatted

# 실행 예시
if __name__ == "__main__":
    header = format_base_header_message()
    print(header)

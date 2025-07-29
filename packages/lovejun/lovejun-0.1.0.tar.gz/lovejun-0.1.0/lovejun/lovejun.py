import serial
import serial.tools.list_ports
import time

class ArduinoController:
    def __init__(self):
        """
        Arduino와의 시리얼 통신을 위한 초기화 메서드
        """
        self.arduino = None  # 내부 전역 객체

    def connect_serial(self):
        """
        Arduino Uno가 연결된 시리얼 포트를 자동으로 찾아 연결하고,
        모듈 내부 변수 arduino에 저장합니다.
        """
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino Uno" in p.description:
                print(f"{p.device} 포트에 연결하였습니다.")
                self.arduino = serial.Serial(p.device, baudrate=9600, timeout=1.0)
                time.sleep(2.0)  # 연결 안정화를 위한 대기

    def get_response(self):
        """
        아두이노로부터 수신된 메시지를 읽어 문자열로 반환합니다.
        """
        while True:
            if self.arduino and self.arduino.in_waiting > 0:
                response = self.arduino.readline().decode().strip()
                return response

    def control_led(self, pin, state):
        """
        아두이노에 LED 제어 명령을 전송합니다.

        사용 예:
        control_led(5, 'on')           # 5번 핀 LED 켜기
        control_led(5, 'off')          # 5번 핀 LED 끄기
        control_led(5, 128)            # 5번 핀 LED 밝기 중간으로 (PWM)

        Args::
        - pin(int): 제어할 핀 번호 (예: 5)
        - state(str 또는 int): 'on', 'off' 또는 0~255 범위의 PWM 값

        Returns:
        - str: 아두이노의 응답 메시지 (예: 'LED ON (5)', 'LED PWM 128 (5)')
        """
        message = f"led,{pin},{state}\n"
        self.arduino.write(message.encode())
        return self.get_response()

    def read_button_state(self, pin):
        """
        아두이노에 버튼 상태를 요청하여 읽어옵니다.

        사용 예:
        - state = read_button_state(4)  # 4번 핀 버튼 상태 확인 (0 또는 1)

        Args:
        - pin(int): 버튼이 연결된 아두이노 핀 번호

        Returns:
        - str: 버튼 상태 ('0': 안눌림, '1': 눌림)
        """
        message = f"button,{pin}\n"
        self.arduino.write(message.encode())
        return self.get_response()

    def read_potentiometer(self, pin):
        """
        아두이노에서 가변저항(포텐셔미터)의 아날로그 값을 읽습니다.

        사용 예:
        - value = read_potentiometer(0)  # A0 핀에 연결된 가변저항 값 (0~1023)

        Args:
        - pin (int): 가변저항이 연결된 아날로그 핀 번호

        Returns:
        - str: 가변저항의 아날로그 값 (0~1023 범위의 문자열)
        """
        message = f"potentiometer,{pin}\n"
        self.arduino.write(message.encode())
        return self.get_response()

    def read_cds(self, pin):
        """
        아두이노에서 CDS 조도 센서의 아날로그 값을 읽습니다.

        사용 예:
        - value = read_cds(1)  # A1 핀에 연결된 CDS 센서 값 읽기

        Args:
        - pin (int): 조도 센서가 연결된 아날로그 핀 번호

        Returns:
        - str: 조도 센서의 아날로그 값 (0~1023 범위의 문자열)
        """
        message = f"cds,{pin}\n"
        self.arduino.write(message.encode())
        return self.get_response()

    def close(self):
        """시리얼 통신을 종료합니다."""
        if self.arduino:
            self.arduino.close()
            print("통신 종료")
        else:
            print("연결된 아두이노가 없습니다.")
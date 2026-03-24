import network
import urequests
from hx711_pico import HX711
from machine import Pin, PWM
from time import sleep, localtime

SSID = 'TPSI'
PASSWORD = 'tpsi2022'  
URL = 'https://iot-twilight-frost-9858.fly.dev/registo'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print("🔌 A ligar ao Wi-Fi...")
while not wlan.isconnected():
    sleep(1)
print("Ligado:", wlan.ifconfig())

hx = HX711(dout=2, pd_sck=3)
hx.set_scale(-270)
print("A fazer tara... deixa apenas o tupperware vazio em cima.")
sleep(10)
hx.tare()
print("Tara feita. Agora podes colocar comida.")

servo = PWM(Pin(15))
servo.freq(50)

refeicoes_hoje = 0
LIMITE_DIARIO = 5
dia_atual = localtime()[2]

def dispensar_comida():
    print("A dispensar comida...")
    servo.duty_u16(8000)
    sleep(1.5)
    servo.duty_u16(2000)
    sleep(1.5)

def enviar_evento(peso):
    print(f"A enviar evento: {peso}")
    for tentativa in range(3):
        try:
            url = URL + f"?peso={peso}"
            response = urequests.get(url, headers={"Connection": "close"})
            print("Evento enviado com sucesso.")
            response.close()
            break
        except Exception as e:
            print(f"Tentativa {tentativa+1} falhou.")
            import sys
            sys.print_exception(e)
            sleep(3)

while True:
    if localtime()[2] != dia_atual:
        dia_atual = localtime()[2]
        refeicoes_hoje = 0

    peso = hx.get_weight()
    print("Peso: {:.2f} g".format(peso))

    if peso < 15:
        if refeicoes_hoje >= LIMITE_DIARIO:
            print("O gato já comeu 5 vezes hoje.")
            enviar_evento("Bloqueado")
        else:
            print("⚠Pouca comida! A dispensar...")
            dispensar_comida()
            enviar_evento(f"{peso:.2f}g")
            refeicoes_hoje += 1
    else:
        print("Comida suficiente.")

    sleep(5)

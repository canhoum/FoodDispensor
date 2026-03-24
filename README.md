# Dispensador de Comida para Gatos (IoT)

Projeto de IoT que automatiza a alimentação de gatos usando Raspberry Pi Pico W, sensor de peso e servo motor.

## Descrição

O sistema monitoriza o peso da comida e dispensa automaticamente quando necessário. Existe um limite de 5 refeições por dia.

Os dados são enviados para um servidor web onde podem ser visualizados num dashboard.

## Funcionalidades

- Dispensação automática
- Controlo por peso (HX711)
- Limite diário de refeições
- Dashboard web com gráficos
- Acesso remoto

## Hardware

- Raspberry Pi Pico W  
- HX711 + célula de carga  
- Servo motor SG90  
- Breadboard  

## Software

### Microcontrolador
- Leitura de peso
- Controlo do servo
- Envio de dados via HTTP

### Servidor (Flask)
- API `/registo`
- Login
- Dashboard com gráfico
- `/historico` (JSON)

## Credenciais

- Username: `gato`
- Password: `comida123`

## Deploy

Servidor alojado no Fly.io (porta 8080)

## Autores

- Guilherme Aires  
- João Silva  

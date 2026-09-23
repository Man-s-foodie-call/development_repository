import krpc
import time

# 1. Подключение к серверу kRPC
conn = krpc.connect(name='Shuttle')

# 2. Получение текущего активного корабля (ракеты)
vessel = conn.space_center.active_vessel

# 3. Получение объекта управления
control = vessel.control

# 4. Установка тяги на 67% (0.67)
control.sas = True
control.throttle = 0.67
print("Тяга установлена на 67%")

# 5. Активация первой ступени
control.activate_next_stage()
print("Первая ступень активирована")

# Небольшая пауза, чтобы действие успело примениться в игре
time.sleep(1)

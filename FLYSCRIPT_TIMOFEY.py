import krpc
import time

conn = krpc.connect(name='Smooth Gravity Turn')
vessel = conn.space_center.active_vessel
control = vessel.control
auto_pilot = vessel.auto_pilot

# --- ПАРАМЕТРЫ ---
START_TURN_ALT = 1000
END_TURN_ALT = 45000
TARGET_APOAPSIS = 100000
TARGET_ORBIT = 100000
FUEL_THRESHOLD = 0.1  # Порог "пустого" бака

# --- СТАРТ ---
control.throttle = 1.0
auto_pilot.target_pitch_and_heading(90, 90)
auto_pilot.engaged = True
time.sleep(1)

print("Launch!")
control.activate_next_stage()

# --- ПЛАВНЫЙ ГРАВИТАЦИОННЫЙ ПОВОРОТ + ПРОВЕРКА ТОПЛИВА ---
while vessel.flight().mean_altitude < TARGET_APOAPSIS:
    alt = vessel.flight().mean_altitude

    # --- ПРОВЕРКА ТОПЛИВА НА ТЕКУЩЕЙ СТУПЕНИ ---
    # Получаем ресурсы, доступные на активной ступени
    stage_resources = vessel.resources_in_decouple_stage(
        vessel.control.current_stage - 1, cumulative=False
    )
    
    # Суммарное жидкое топливо на ступени
    fuel = stage_resources.amount("LiquidFuel")
    
    # Суммарное твёрдое топливо (если есть ускорители)
    solid = stage_resources.amount("SolidFuel")

    if fuel < FUEL_THRESHOLD and solid < FUEL_THRESHOLD:
        print(f"Ступень пуста (LF: {fuel:.2f}, SF: {solid:.2f}). Активируем следующую!")
        control.activate_next_stage()
        time.sleep(0.5)  # Даём игре применить команду

    # --- ПЛАВНЫЙ НАКЛОН ---
    if alt < START_TURN_ALT:
        pitch = 90.0
    elif alt > END_TURN_ALT:
        pitch = 0.0
    else:
        t = (alt - START_TURN_ALT) / (END_TURN_ALT - START_TURN_ALT)
        pitch = 90.0 * (1.0 - t)

    auto_pilot.target_pitch_and_heading(pitch, 90)

    if vessel.orbit.apoapsis_altitude > TARGET_APOAPSIS:
        break

    time.sleep(0.2)

control.throttle = 0.0
print(f"Apoapsis reached at {vessel.orbit.apoapsis_altitude:.0f} m")

# --- ЦИРКУЛЯРИЗАЦИЯ ---
auto_pilot.reference_frame = vessel.orbital_reference_frame
auto_pilot.target_direction = (0, 1, 0)
auto_pilot.wait()

print("Coasting to apoapsis...")
while vessel.orbit.time_to_apoapsis > 5:
    time.sleep(0.5)

print("Circularization burn!")
control.throttle = 1.0

while vessel.orbit.periapsis_altitude < TARGET_ORBIT:
    time.sleep(0.2)

control.throttle = 0.0
auto_pilot.engaged = False

print(f"Done! Ap: {vessel.orbit.apoapsis_altitude:.0f} m, Pe: {vessel.orbit.periapsis_altitude:.0f} m")
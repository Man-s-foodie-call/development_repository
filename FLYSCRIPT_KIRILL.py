CLEARSCREEN.
PRINT "Расчет расстояния до KSC...".

// Координаты KSC, преобразованные в вектор
SET kscPos TO LATLNG(0, -74.5):POSITION.

// Текущая позиция корабля (вектор)
SET shipPos TO SHIP:POSITION.

// Вектор от KSC до корабля
SET vectorToShip TO shipPos - kscPos.

// Расстояние (длина вектора)
SET distanceToKSC TO vectorToShip:MAG.

// Вывод расстояния
PRINT "Расстояние до KSC: " + ROUND(distanceToKSC) + " м.".

// Проверка: приближаемся или отдаляемся
SET lastDistance TO distanceToKSC.
WAIT 1.
SET currentDistance TO (SHIP:POSITION - kscPos):MAG.

IF currentDistance < lastDistance {
    PRINT "Мы приближаемся к KSC!".
} ELSE {
    PRINT "Мы отдаляемся от KSC!".
}.
# Face Music Control

[<img src = ".\READMEmaterials\flags\gb.svg">&nbsp; Click for the English version](README.md)

Face Music Control - это программа на языке python, позволяющая управлять звучанием музыкального инструмента с помощью распознавания эмоций. Она использует виртуальный MIDI-порт для отправки MIDI CC-сообщений с амплитудой, пропорциональной вероятностям эмоций, распознаваемым свёрточной нейронной сетью по лицеой экспрессии. Чтобы управлять параметрами DAW, мы обычно перемещаем ползунки MIDI-контроллера. Подход Face Music Control аналогичен, но MIDI-контроллер виртуальный, и им управляет нейронная сеть.

## Мотивация
Во время импровизации и создания новой музыки существующие интерфейсы для управления звучанием (педали, ползунки и т.п.) неудобны и редко применимы. Дело в том, что музыканту при создании музыки не хватает концентрации для поиска подходящего тембра и управления звучанием инструмента. Одновременно с этим, в данных контекстах особенно важно, чтобы характер звучания соответствовал переживаниям музыканта. Мной не было найдено средств, позволяющих управлять звучанием инструмента на основании эмоций музыканта, поэтому я написал данную программу.

## Дополнительные применения
* Новый вид взаимодействия с инструментом может быть самостоятельным перформансом
* Так как световая аппаратура управляется MIDI событиями, Face Music Control можно использовать для дополнения визуальной составляющей концертов

## Требования для работы программы

Очевидные требования:
* Наличие камеры на компьютере
* Наличие python интерпретатора на компьютере
* Наличие DAW

### Библиотеки
Чтобы установить все необходимые библиотеки, необходимо выполнить команду:

```bash
pip install -r requirements.txt
```

### Драйвер виртуального MIDI порта **(Только для Windows)**
Для Windows требуется установить драйвер для создания виртуальных MIDI портов. Возможные решения:
* [LoopBe1](https://www.nerds.de/en/download.html)
<br> После установки LoopBe1 вирутальный MIDI порт будет на Вашем компьютере пока Вы не удалите драйвер.
* [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
<br> Это программа, позволяющая манипулировать драйвером virtualMIDI (устанавливается автоматически с loopMIDI). В данном случае виртуальный порт будет на компьютере только когда loopMIDI запущен.

**Если вы используете linux или macOS, Face Music Control сам создает виртуальный MIDI порт, и сторонние драйверы не нужны**

## Запуск

Откройте main.py интерпритатором python. Программа тестировалась на python 3.10.4.

## Режим настройки
Для связывания эмоций и параметров звучания необходимо:
* Открыть режим настройки в Face Music Control и режим MIDI mapping в DAW
* Последовательно нажимать на элемент графического интерфейса DAW, отвечающий за параметр звучания и кнопку с графическим представлением эмоции, которая должна управлять параметром звучания
Когда всем параметрам звучания, для которых это требудется, будут сопоставлены эмоции, необходимо выйти из режима MIDI mapping, а затем из режима настройки. 

## Режим игры (демонстрация) 
Управление звучанием происходит в режиме игры.

На видеодемонстрации ниже счастье управляет эхо, злость — перегрузом.

https://user-images.githubusercontent.com/98213116/172071460-583846ca-99f1-4817-84aa-8ef4403bfec4.mp4

*Звук на видео в README по умолчанию выключен, но **его можно включить.***

*Все демонстрации находятся в директории проекта: [READMEmaterials/demonstrations](READMEmaterials/demonstrations). Если видео не отобразилось, его можно найти там ([happiness-echo_anger-distortion.mp4](READMEmaterials/demonstrations/happiness-echo_anger-distortion.mp4)).*

<!--
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
-->
## Достижения проекта
Конкурсы:
* Конкурс докладов бакалавров XI конгресса молодых учёных — победа в 6 номинациях:
(Большие данные и машинное обучение, Аналитика данных, Искусственный интеллект в промышленности, Речевые технологии и машинное обучение, Финансовые технологии больших данных, Глубокое обучение и генеративный искусственный интеллект
* NeuroTech Cup — Диплом III-ей степени

Конференции:
* XI конгресс молодых учёных
* Samara Neuroweek 2020

Публикация в сборнике трудов XI конгресса молодых ученых (в печати)

## Лицензия
Garri Proshian © [MIT](https://choosealicense.com/licenses/mit/) 2020
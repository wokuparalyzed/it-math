# Задача 3

Реализация сжатия изображений с использованием SVD

## Эксперимент

Рассматриваемые алгоритмы:
1. метод из библиотеки numpy
2. степенной метод (simple)
3. блочный степенной метод (advanced)

### Данные


<details>
<summary>Использованное изображение:</summary>

![mad](imgs/zbmp24.bmp)


</details>

### Результаты:

Оценим сохранность фотографий после прогонки через разные методы сжатия:
<details>

| Algorithm | Compression lvl = 1 |
| --- | --- |
| numpy | <img src=   "compressed/1.advanced.zbmp24.bmp" width="250px"> |
| simple | <img src=  "compressed/1.numpy.zbmp24.bmp" width="250px"> |
| advanced | <img src="compressed/1.simple.zbmp24.bmp" width="250px"> |

При коэффициенте сжатия 1 лучше всего со сжатием (в плане сохранения качества изображения справляется numpy). 

| Algorithm | Compression lvl = 3 |
| --- | --- |
| numpy | <img src=   "compressed/3.advanced.zbmp24.bmp" width="250px"> |
| simple | <img src=  "compressed/3.numpy.zbmp24.bmp" width="250px"> |
| advanced | <img src="compressed/3.simple.zbmp24.bmp" width="250px"> |

Если увеличить уровень сжатия до 3, то разница в качестве всех 3 методов пропадает. 

| Algorithm | Compression lvl = 10 |
| --- | --- |
| numpy | <img src=   "compressed/10.advanced.zbmp24.bmp" width="250px"> |
| simple | <img src=  "compressed/10.numpy.zbmp24.bmp" width="250px"> |
| advanced | <img src="compressed/10.simple.zbmp24.bmp" width="250px"> |

При большом уровне компресии все изображения теряют информационную ценность.

</details>

### Вывод

Можно заметить, что при повышении уровня сжатия качество изображения ухудшается почти одинаково во всех случаях. Остается только рассуждать о скорости выполнения сжатия в каждом отдельном случае для выбора оптимального алгоритма. Результаты замеров исполнения каждого из методов записаны в `compression_times.txt`. Замеры производились с помощью утилиты `time`.


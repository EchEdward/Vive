# Vive - calculating of a induct voltage

## Scope of application 
**Vive** - десктопное приложение, предназначенное для расчёта наведенного напряжения на воздушных линиях электропередач и автоматической генерацией на основании результатов расчётов отчётной документации формате .docx.

**Vive** - desktop application, designed for calculating induct voltage in overhead transmission power lines and automatically generation of special documentation in *.docx* format based on results of performed calculating.


## Table of contents

  1. [Description](#Description)
  2. [Used technologies](#Used-technologies)
  3. [Installation](#Installation)


## Description

UI приложения разработан при помощи кроссплатформенного графического фреймворка [PyQt5](https://pypi.org/project/PyQt5/5.9/). Данный фреймворк предоставляет богатый функционал для разработки UI, легок в освоении и обладает подробной документацией.

Application's UI has been designed using a cross-platform UI framework [PyQt5](https://pypi.org/project/PyQt5/5.9/). This framework gives a rich functionality for UI designing, is easy to learn and has detailed documentation.

Ввод исходных данных в приложение осуществляется путём заполнения таблиц *QTableWidget* расположенных во вкладках *QTabWidget*. Для проверки введённых данных на ошибки реализован алгоритм их проверки, который в случае ошибки отобразит модальное окно с типом ошибки и ссылкой на место где она допущена.

Initial data's input into the application is realized by filling of tables *QTableWidget* located into tabs *QTabWidget*. For mistakes finding in a entered data has been realized algorithm that in case of a mistake will show modal window with mistake's type and link to its locating.

![Alt Text](.github/images/vlid.png)

Хранение введённых исходных осуществляется в базе данных *sqlite3*, на основании которой реализовано подобие файловой системы, что обеспечивает удобство хранения данных, группировки и скорость доступа к ним. Помимо этого, реализована возможность сохранения и открытия исходной информации в виде файлов *.txt*.

Storage of a entered initial data is realized in database *sqlite3*, on the basis of which has been realized similarity of a file system, that provided convenience of a data storage, grouping and speed of access to it.

![Alt Text](.github/images/bd.png)

Визуализация введённых исходных данных осуществляется при помощи инструмента работы с изображениями [Pillow](https://pypi.org/project/Pillow/8.1.1/) а также алгоритма который осуществляет рисование графических примитивов. В результате их работы создаются различные изображения. Данные изображения позволяют легко проверять верность введённых исходных данных, а также добавлять данные изображения в генерируемые документы.

Visualization of a entered initial data is realized using library for work with images [Pillow](https://pypi.org/project/Pillow/8.1.1/) and algorithm which realizes drawing graphic primitives. Result of its work is different created images. These images allow easy to check correctness of entered a initial data and add them into generating documents.

![Alt Text](.github/images/ss.png)

Одной из основных задач данного приложения является расчёт наведенного напряжения, которое реализуется путём составления на основании исходных данных системы линейных алгебраических уравнений и последующее её решение. Подробнее с математической моделью можно ознакомиться в следующих [статьях](https://disk.yandex.by/d/FrIEF12qER-tWQ?w=1). Для решения данной задачи используются матетические пакеты [Numpy](https://pypi.org/project/numpy/1.15.0/) и [Scipy](https://pypi.org/project/scipy/1.5.4/) которые предоставляют все необходимые для этого инстументы. Так как генерируемые системы уравнений обычно состоят из более 1000 уравнений и более 70 % элементов системы являются нулевыми были выполнены следующе оптимизации:

One of main tasks of the application is calculating of induct voltage, which is realized by way of formation based on initial data system linear algebraic equations and its solve. More details about math model you can find in next [articles](https://disk.yandex.by/d/FrIEF12qER-tWQ?w=1). For solving this task are used math libraries [Numpy](https://pypi.org/project/numpy/1.15.0/) and [Scipy](https://pypi.org/project/scipy/1.5.4/) which have all needed tools for it. Since generating equation's systems usually consist from more 1000 equations and 70% of system's elements are null have been done next optimizations:

- Вместо обычных матриц используются разряженные матрицы *scipy.sparse*. Данный модуль предоставляет все необходимые инструменты для работы с разряженными матрицами, а также решатель систем уравнений, основанных на разряженных матрицах. Применение разряженных матриц позволяет сократить затраты памяти на хранение матриц, так как нулевые элементы в них не хранятся, а также сократить время, затрачиваемое на решение системы уравнений.
- Instead usual matrixes are used sparse matrixes *scipy.sparse*. This module has all needed tools for work with sparse matrixes and solver of equation's systems based on sparse matrixes. Using of sparse matrixes allows reduce volume of memory on matrixes' storage since it does not store null elements, and reduce time of solving equation's systems.
- Кэширование рассчитываемых подматриц. Так как матрица системы уравнений формируется путём размещения на ней множества подматриц, которые в свою очередь рассчитываются по интегральным выражениям и за частую идентичны друг другу, кэширование данных подматриц по входным параметрам позволяет сократить время, затрачиваемое на получение матрицы системы уравнений.
- Caching of calculating submatrices. Since matrix equation's systems are formed by way putting on it sets of submatrices, which calculating from integral expressions and are often identical to each other, caching these submatrices by input argument allows reduce spent of time on getting of equation's systems matrix.
- Кэширование по исходным данным. Исходные данные можно разделить на различные независимые блоки, на основании которых составляются различные независимые подматрицы системы уравнений. Кэширование данных подматриц по независимым блокам исходных данных позволяет не делать перерасчёт подматрицы созданных на блоках исходных данных в которых не было изменений. Это позволяет мгновенно получать результаты расчётов при отсутствии изменений в исходных данных, а также ускоренный расчёт за счёт отсутствия необходимости пересчитывать все подматрицы. Данные сохраняются между сеансами использования приложения за счёт сохранения полученных подматриц в виде файлов *.npy* и *.npz*, а ссылки на них сеарилизуются из объекта *dict* в файл при помощи модуля *pickle*.
- Caching by initial data. Initial data can split on different independent blocks, based on which are formed different independent submatrices of equation's system. Caching these submatrices by independent blocks of initial data allows not to do recalculation submatrices created from blocks of initial data which doesn't have changes. It allows instantly to get calculating's results in case absence of changes or accelerated calculating on account of need's absence to recalculate all submatrices. Data doesn't lose between sessions using of application on account of storing gotten submatrices in format files *.npy* and *.npz*, and links to its is serialized from *dict* into file by module *pickle*.

Часть данных результатов расчётов представляют собой графики. Для их построения используется библиотека [Matplotlib](https://pypi.org/project/matplotlib/2.2.2/), которая обладает широким функционалом построения различных и наглядных графиков и предоставляет средства для удобного внедрения их UI. Так же данная библиотека позволяет сохранять построенные графики в виде изображений с различными размерами и качеством, что необходимо для последующего их внедрения в генерируемые документы.

Data's part of calculating results is plots. For building of plots is used library [Matplotlib](https://pypi.org/project/matplotlib/2.2.2/) which has rich functional of building different and visual plots and has opportunity for adding it into UI. Also the library allow save built plots as images with different size and quality, that necessary for next introducing them into generating documents.

![Alt Text](.github/images/noz.png)

Чтобы исходные данные были наиболее компактны и не предоставляли лишних неудобств при их введении, они ссылаются на те или иные объекты, параметры которых хранятся в файле формата *.xlsx*. Файлы данного формата легко редактируется, что удобно при внесении изменений теми кто не осведомлён об устройстве данного приложения. Для работы с данными файлами используется библиотека [Openpyxl](https://pypi.org/project/openpyxl/2.4.8/), которая позволяет читать и записывать в данные файлы различную информацию. Так же данная библиотека используется для предоставления пользователями приложения возможности вывода данных на основании которых строятся графики.

In order to initial data was more compact and it was easy to enter, it has links to sets of objects, params which are store in file *.xlsx* format. Files of this format easy to edit, that is conveniently in case need to do changes without knowledge about how the application works. For work with this files are used [Openpyxl](https://pypi.org/project/openpyxl/2.4.8/) library, which allows to read and write different information into this files. Also the library is used for gives the application users opportunity to get data for building of plots.

Помимо выполнения расчёта наведенного напряжения важной задачей является автоматическая генерация специальной документации в формате *.docx*. Необходимость генерации документов в формате *.docx* обусловлена удобством последующей работы с ними, возможностью редактирования и объединения их в более сложные документы. Для этого используется библиотека [Python-docx](https://pypi.org/project/python-docx/0.8.6/), которая позволяет создавать данные документы автоматически, вставлять в них изображения, создавать таблицы и так далее.

Besides implementation of calculating of induct voltage important task is generation special documentation *.docx* format. Necessity of generation documents *.docx* is explained convenience of next work with its, opportunity of editing and combining them in more difficult documents. For it is used [Python-docx](https://pypi.org/project/python-docx/0.8.6/) library, which allows to create these documents automatically, inserts into them images, creates tables and etc.

![Alt Text](.github/images/dcx.png)

## Used technologies

- [Python 3.6.2](https://www.python.org/downloads/) - Python programming language interpreter.
- [Numpy 1.15.0](https://pypi.org/project/numpy/1.15.0/) - general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records without sacrificing too much speed for small multi-dimensional arrays.
- [Scipy 1.5.4](https://pypi.org/project/scipy/1.5.4/) - open-source software for mathematics, science, and engineering.
- [Matplotlib 2.2.2](https://pypi.org/project/matplotlib/2.2.2/) - library for interactive graphing, scientific publishing, user interface development and web application servers targeting multiple user interfaces and hardcopy output formats.
- [PyQt5 5.9](https://pypi.org/project/PyQt5/5.9/) - Python binding of the cross-platform GUI toolkit Qt, implemented as a Python plug-in.
- [Pillow 8.1.1](https://pypi.org/project/Pillow/8.1.1/) - the Python Imaging Library.
- [Openpyxl 2.4.8](https://pypi.org/project/openpyxl/2.4.8/) - Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.
- [Python-docx 0.8.6](https://pypi.org/project/python-docx/0.8.6/) - Python library for creating and updating Microsoft Word (.docx) files.


## Installation 
Для того чтобы использовать данное приложение необходимо установить компоненты с раздела [Used technologies](#Used-technologies). Первоначально установите интерпретатор Python, а затем при помощи пакетного менеджера *Pip* установите перечисленные пакеты. При применении версий пакетов отличных от предложенных работоспособность приложения не гарантируется.

For using the application necessity to install components from section [Used technologies](#Used-technologies). First of all install Python interpreter, and after that using package manager *Pip* to install listed packages. In case using versions of packages that differ from the proposed, correct work of the application is not ensured.

        pip install -r requirements.txt





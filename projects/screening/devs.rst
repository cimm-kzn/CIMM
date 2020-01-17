РАЗРАБОТКИ
==========

`rank <https://seafile.cimm.site/f/ec0ae0c4f4a146b394b0/?dl=1>`_  - скрипт ранжирования

PMAPPER
-------

Модуль для создания хешированных сигнатур трехмерных фармакофоров

Последняя версия модуля Pmapper (Python) доступна по ссылке: https://github.com/DrrDom/pmapper

**Pmapper** - это модуль, написанный на языке программирования Python, для создания сигнатур трехмерных фармакофоров и молекулярных отпечатков (фингерпринтов). Сигнатуры уникально кодируют трехмерные фармакофоры с помощью хешей, подходящих для быстрой идентификации идентичных фармакофоров.

**Зависимости**

- rdkit >= 2017.09
- networkx >= 1.11

**Примеры**

**Загрузка модулей**::

    from rdkit import Chem
    from rdkit.Chem import AllChem, ChemicalFeatures
    from pharmacophore import Pharmacophore as P, read_smarts_feature_file, load_multi_conf_mol
    from pprint import pprint

**Create pharmacophore from a single conformer using feature definition from SMARTS file**::

    # load a molecule from SMILES and generate 3D coordinates
    mol = Chem.MolFromSmiles('C1CC(=O)NC(=O)C1N2C(=O)C3=CC=CC=C3C2=O')  # talidomide
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, randomSeed=42)

    # load pharmacophore feature definitions from SMARTS file
    smarts = read_smarts_feature_file('smarts_features.txt')

    # create pharmacophore
    p = P()
    p.load_from_smarts(mol, smarts)

**Get 3D pharmacophore signature**::

    # get 3D pharmacophore signature
    sig = p.get_signature_md5()
    print(sig)

**Output:**::

    f2e16f52f6f6ca6e97fc5844bfd35d36

**Get 3D pharmacophore signature with non-zero tolerance**::

    sig = p.get_signature_md5(tol=5)
    print(sig)

**Output:**::

    fb535302db2e5d624aa979b6e8dfbdf2

**Create pharmacophore from a single conformer using RDKit feature factory**::

    # load pharmacophore using RDKit factory and get 3D pharmacophore signature
    factory = ChemicalFeatures.BuildFeatureFactory('smarts_features.fdef')
    p.load_from_feature_factory(mol, factory)
    sig = p.get_signature_md5()
    print(sig)

**Output**::

    f2e16f52f6f6ca6e97fc5844bfd35d36

**Create pharmacophores for a multiple conformer compound**::

    # create multiple conformer molecule
    AllChem.EmbedMultipleConfs(mol, numConfs=10, randomSeed=1024)
    ps = load_multi_conf_mol(mol, smarts_features=smarts)
    sig = [p.get_signature_md5() for p in ps]
    pprint(sorted(sig))  # identical signatures occur

**Output**::

    ['13d168458ab1f251157f2422efcce312',
     '13d168458ab1f251157f2422efcce312',
     '182a4cfa756fe8b7f736a7f7ac0e8e0a',
     '182a4cfa756fe8b7f736a7f7ac0e8e0a',
     '4234e9d249874a5009f1e312dd885d80',
     'ab273dd083c4f2e3424ba917b121b846',
     'b6ec58553d2984bd398b4520bd1545cc',
     'bfc43365b2657d08b6bb888e4d8ec71b',
     'f5ca8e406dae31182e2b06fde7452b75',
     'fc4a85e818fc0b3f034a7af42fa5ca69']

**Generate 3D pharmacophore fingerprint**::

    # generate 3D pharmacophore fingerprint which takes into account stereoconfiguration
    b = p.get_fp(min_features=4, max_features=4)   # set of activated bits
    print(b)

**Output (a set of activated bit numbers)**::

    {1922, 1795, 779, 1040, 528, 920, 154, 1437, 287, 1313, 1447, 1961, 941, 690, 1203, 65, 1346, 709, 1486, 1366, 2006, 1750, 1016, 346, 603, 1116, 354, 995, 228, 2024, 1900, 1524, 888, 2043}

**Change settings**::

    b = p.get_fp(min_features=4, max_features=4, nbits=1024, activate_bits=2)
    print(b)

**Output (a set of activated bit numbers)**::

    {897, 514, 259, 389, 520, 264, 143, 16, 529, 656, 787, 660, 24, 285, 157, 32, 673, 550, 683, 173, 301, 558, 45, 945, 177, 692, 950, 443, 444, 61, 960, 961, 448, 321, 709, 197, 587, 460, 77, 718, 720, 80, 339, 596, 723, 470, 980, 345, 601, 476, 354, 614, 743, 1003, 875, 494, 367, 497, 114, 1012, 244, 630, 377, 762, 507, 508, 1021}

**Save/load pharmacophore**::

    p.save_to_pma('filename.pma')
    # Output is a text file having json format.
    p = P()
    p.load_from_pma('filename.pma')

**Support LigandScout pml-files**

LigandScout models saved as pml-files can be read using p.load_ls_model. Also, a pharmacophore can be stored in this format in order to export to LigandScout (p.save_ls_model).

**Speed tests**

Generation of pharmacophore signatures (hashes) is a CPU-bound task. The computation speed depends on the number of features in pharmacophores.
Tests were run on 500 compounds (a random subset from Drugbank). Up to 50 conformers were generated for each compound. Up to 100 pharmacophores having a particular number of features were chosen randomly from the whole number of 25000 pharmacophores to generate pharmacophore signatures.

Laptop configuration:

- Intel(R) Core(TM) i7-5500U CPU @ 2.40GHz
- 12 GB RAM
- the calculation was run in 1 thread (the module is thread-safe and calculations can be parallelized)

**Output**::

    pharmacophore generation: 19.21 s
    total number of pharmacophores: 25000
    pharmacophore hash generation:
    50 pharmacophores having 2 features: 0.00 s; time per pharmacophore: 0.00000 s
    100 pharmacophores having 3 features: 0.01 s; time per pharmacophore: 0.00010 s
    100 pharmacophores having 4 features: 0.01 s; time per pharmacophore: 0.00010 s
    100 pharmacophores having 5 features: 0.04 s; time per pharmacophore: 0.00040 s
    100 pharmacophores having 6 features: 0.12 s; time per pharmacophore: 0.00120 s
    100 pharmacophores having 7 features: 0.24 s; time per pharmacophore: 0.00240 s
    100 pharmacophores having 8 features: 0.51 s; time per pharmacophore: 0.00510 s
    100 pharmacophores having 9 features: 0.94 s; time per pharmacophore: 0.00940 s
    100 pharmacophores having 10 features: 1.86 s; time per pharmacophore: 0.01860 s
    100 pharmacophores having 11 features: 3.02 s; time per pharmacophore: 0.03020 s
    100 pharmacophores having 12 features: 4.17 s; time per pharmacophore: 0.04170 s
    100 pharmacophores having 13 features: 7.04 s; time per pharmacophore: 0.07040 s
    100 pharmacophores having 14 features: 9.29 s; time per pharmacophore: 0.09290 s
    100 pharmacophores having 15 features: 12.94 s; time per pharmacophore: 0.12940 s
    100 pharmacophores having 16 features: 17.79 s; time per pharmacophore: 0.17790 s
    100 pharmacophores having 17 features: 23.58 s; time per pharmacophore: 0.23580 s
    100 pharmacophores having 18 features: 33.83 s; time per pharmacophore: 0.33830 s
    100 pharmacophores having 19 features: 40.43 s; time per pharmacophore: 0.40430 s
    100 pharmacophores having 20 features: 58.30 s; time per pharmacophore: 0.58300 s

**Citation**

Ligand-Based Pharmacophore Modeling Using Novel 3D Pharmacophore Signatures
Alina Kutlushina, Aigul Khakimova, Timur Madzhidov, Pavel Polishchuk
Molecules 2018, 23(12), 3094
https://doi.org/10.3390/molecules23123094


PSEARCH
-------

Модуль для автоматической генерации трехмерных моделей фармакофоров и последующего виртуального скрининга

Последняя версия модуля **psearch** (Python) доступна по ссылке: https://github.com/meddwl/psearch

*Подготовка данных*

В данном контексте под подготовкой данных подразумевается разделение набора данных по активности, генерация стереоизомеров и конформеров для каждой молекулы и генерация базы данных с фармакофорным представлением соединений. Фармакофорное представление соединения - это полный граф, вершинами которого являются все возможные фармакофорные центры соединения, а ребрами - расстояния между ними.

Запускает процесс подготовки данных модуль `prepare_dataset.py <https://seafile.cimm.site/d/06ba7117198b40b5ab3a/?dl=1>`_ . На вход он принимает файл формата .smi (содержащий SMILES

**Пример**::

    prepare_dataset.py -i test/input.smi --label -n 100 -e 100 -r 0.5 -c 4

*Фармакофорное моделирование и виртуальный скрининг*

1. Генерация фармакофоров осуществляется в 2 этапа:

    (а) сначала генерируются все возможные квадруплеты,
    (б) после создаются наиболее сложные фармакофорные модели, количество и качество которых регулируются статистикой.

(а) Для генерации квадруплетов используется модуль `create_subpharm.py <https://seafile.cimm.site/f/bfca3b9a525f4575a0e2/?dl=1>`_.

**Параметры**::

    -d/--input_db, путь к базе данных, в которой хранится информация о всех молекулах (тренировочного и тестового наборов), обязательный параметр.
    -ts/--file_trainset, путь к файлу со списком молекул тренировочного набора, обязательный параметр.
    -tol/--tolerance, параметр, который используется для генерации знака стереоконфигурации соединения, по умолчанию этот параметр равен 0.
    -l/--lower, число фармакофорных центров, с которым будут сгенерированы фармакофорные модели, по умолчанию этот параметр равен 4.

**Пример**::

    psearch/scripts/create_subpharm.py -d test/compounds/active.db -ts test/trainset/active_tr1.txt -tol 0 -l 4

(б) Генерация фармакофорных моделей. На этом этапе генерируется статистика, с помощью которой оценивается качество полученных моделей, и лучшие фармакофорные модели сохраняются в папку models с расширением .pma.

Эту функцию выполняет модуль `gen_subph.py <https://seafile.cimm.site/f/1d2782dbc6894fd8a57a/?dl=1>`_.

**Параметры**::

    -a/--in_subph_active, путь к файлу с активными квадруплетами, полученные на предыдущем шаге.
    -i/--in_subph_inactive, путь к файлу с неактивными квадруплетами, полученные на предыдущем шаге.
    -adb/--in_active_database, путь к базе данных с активными соединениями.
    -idb/--in_inactive_database, путь к базе данных с неактивными соединениями.
    -ats/--in_active_trainset, путь к файлу со списком активных молекул тренировочного набора.
    -l/--lower, число фармакофорных центров, которые имеют фармакофорные модели на входе.

**Пример**::

    psearch/scripts/gen_subph.py -a test/trainset/ph_active_tr1.txt -i test/trainset/ph_inactive_tr1.txt -adb test/compounds/active.db -idb test/compounds/inactive.db -ats test/trainset/active_tr1.txt -l 4

2. Виртуальный скрининг с использованием полученных фармакофорных моделей осуществляется модулем `screen_db.py <https://seafile.cimm.site/f/fa5000180e5248d0b931/?dl=1>`_.

**Параметры**::

    -d/--database, путь к базе данных.
    -q/--query, путь к фармакофорной модели (.pma файл).
    -o/--output, путь к файлу, куда бдут сохранены результаты виртуального скрининга.

**Пример**::

    psearch/scripts/screen_db.py -d test/compounds/active.db -q models/model1.pma -o screen/screen_active_model1.txt

GTM_DIVERSE
-----------

Последняя версия модуля GTM subset selection (Python) доступна для скачивания по ссылке: `download <https://seafile.cimm.site/d/1f94f0ba16cb49109db7/>`_

GTM subset selection - это модуль, написанный на языке программирования Python, для выборки минимального набора данных с равномерным покрытием карты GTM. Данный подход позволяет отобрать наиболее разнообразные молекулы в выборку. Для работы алгоритма нужны проекции молекул на карту GTM (file.svm или file.rsvm) и специально форматированный файл с биологическими активностями(y.txt).

**Зависимости**

- CIMtools >= 3.0
- CGRtools >=3.0
- jupyter last version
- python 3.7

Последняя версия модуля GTM subset selection_2019 (Python) доступна для скачивания по ссылке: `download <https://seafile.cimm.site/f/63ec77dd2acf44758358/?dl=1>`_

Скрипт для отбора соединений для формирования репрезентативной выборки с обогащением биологически активными представителями.

Скрипт состоит из функций и основного кода и использует сторонние библиотеки:

- Sklearn
- Joblib
- Pandas
- NumPy

**Функции:**

- **data_read** - функция предназначена для чтения libSVM файлов, полученных при построении карт GTM. Такие файлы содержат в себе вероятность нахождения конкретной молекулы во всех узлах карты. Принимает в качестве аргумента название файла.
- **best_subset_one** - основная функция алгоритма, отвечает за выбор молекул в слой. Принимает на вход 5 параметров, приведённых ниже:

    - data: данные по принадлежности каждой ноде каждой молекулы
    - di: индексы молекул, доступных для отбора
    - buckets: текущее состояние наполнимости узлов
    - space: параметр дозаполнения узлов, отвечает максимально возможную заполненность

- **take_layers** - функция, отвечающая за выбор следующего слоя, отбор проводится для 50 случайных возможных слоев. Функция выбирает слой, содержащий наименьшее количество молекул при аналогичной наполненности узлов. Затем, проводится расчет обогащения для выборки, с учетом предыдущих слоев. Принимает на вход следующие параметры:

    - data: данные по принадлежности каждой ноде каждой молекулы
    - n_layers: количество жеалемых слоев для отбора
    - map_len: размерность карты, корень из N узлов
    - space_enlarge: параметр дозаполнения узлов, отвечает максимально возможную заполненность

- **hit_rate** - функция рассчитывает долю молекул кандидатов среди всех протестированных
- **enrichment** - функция рассчитывает параметр обогащения для всех типов испытаний в подвыборке y и принимает на вход следующие параметры

    - y: numpy array N молекул (строк) x M испытаний (столбцов) значения 1/0/nan
    - ref: numpy array M начальные доли молекул кандидатов среди всех протестированных
    - fun: стандартная функция numpy для подсчета параметра обогащения (mean, median, etc)

Далее следует основной код с чтением таблицы активностей соединений, выравнивание индексов и расчет доли молекул кандидатов среди всей прочитанной выборки. Следом читается RSVM файл с вероятностью нахождения молекул в каждом узле карты GTM. Используя библиотеку параллелизации проводится набор 400 слоев. Полученный объект представляет собой лист из словарей. Каждый словарь содержит в себе следующие ключи:

- layers: лист листов, каждый лист отдельный слой
- buckets: наполнение узлов
- percent: процент данных отобранных в подвыборку
- random: рассчитанный параметр обогащения для сучайной подвыборки такого же объема
- enrichment: рассчитанный параметр обогащения для подвыборки

Результат сериализуется в pickle объект для сохранения результатов.

PharMD
------

Последняя версия модуля PharMD (Python) доступна по ссылке:
https://github.com/ci-lab-cz/pharmd

Также модуль PharMD (Python) доступен для скачивания по ссылке: `download <https://seafile.cimm.site/f/6def21d9bd97487a9d76/?dl=1>`_

PharMD — это модуль, написанный на языке программирования Python,  для извлечения фармакофорных моделей из траекторий молекулярной динамики комплексов белка с лигандом, выявления избыточных фармакофоров и виртуального скрининга с использованием нескольких фармакофорных моделей и различных схем подсчета.

**Зависимости **:

- mdtraj >= 1.9.3
- plip >= 1.4.2
- pmapper >= 0.3.1
- psearch >= 0.0.2

*Извлечение фармакофорных моделей из траектории молекулярной динамики*

Для получения отдельных кадров из траектории молекулярной динамики используется модуль mdtraj. Поэтому md2pharm принимает те же аргументы, что и mdconvert из модуля mdtraj. Таким образом, возможно извлечение только указанных кадров траектории, а не всей траектории. Требуется указать код лиганда, как это указано в файле топологии PDB. Отдельные кадры будут храниться в одном файле PDB без молекул растворителя. Модели фармакофоров для каждого кадра будут храниться в формате xyz в той же директории, что и выходной pdb-файл.

    md2pharm -i md.xtc -t md.pdb -s 10 -g LIG -o pharmacophores/frames.pdb

*Извлечение не избыточных фармакофоров*

Подобные фармакофоры распознаются по идентичным 3D-хэшам фармакофоров. Ожидается, что фармакофоры с одинаковыми хэшами будут иметь RMSD меньше, чем указанный шаг биннинга. По умолчанию он равен 1 Å.

    get_distinct -i pharmacophores/ -o distinct_pharmacophores/

*Выполнение виртуального скрининга с использованием нескольких не избыточных фармакофоров*

Для этой цели используется утилита screen_db из модуля psearch. Нужно создать базу данных конформеров и их фармакофорных представлений, используя утилиты из модуля psearch. На этом шаге вы можете задать значение шага биннинга, которое будет использоваться в дальнейшем при скрининге.

    prepare_db -i input.smi -o connections.db -c 2 -v

Чтобы рассчитать оценку на основе подхода Conformer Coverage, нужно указать аргумент --conf для утилиты screen_db. Тогда все конформеры соединения, соответствующего моделям фармакофора, будут извлечены как соединения-лидеры, в противном случае будет возвращен только первый конформер.
Рекомендуется ограничить скрининг сложными моделями фармакофоров, имеющими по крайней мере четыре фармакофорных центра, так как менее сложные модели могут извлекать нерелевантные соединения.
В выходной директории будет создано несколько txt-файлов, содержащих списки соединений-лидеров, полученные отдельными моделями фармакофоров.

*Расчет составных оценок на основе нескольких списков соединений-лидеров*

Преимущество ансамблевой оценки заключается в том, что не нужно проверять отдельные модели и выбирать наиболее эффективные. Ансамблевая оценка рассчитывается по формуле:

1.	Подход Conformer Coverage (CCA) - оценка равна проценту конформеров, соответствующих по крайней мере одной из моделей фармакофоров.
2.	Подход Common HIts (CHA) - оценка равна проценту моделей, соответствующих как минимум одному конформеру соединения.

В случае оценки CCA нужно предоставить базу данных проверенных соединений в качестве дополнительного параметра.

    get_scores -i screen/ -o cca_scores.txt -s cca -d compounds.db

sphere_exclusion_diverse_lib
----------------------------

Последняя версия модуля sphere_exclusion_diverse_lib (Python) доступна для скачивания по ссылке: `download <https://seafile.cimm.site/f/5971de6b4fa746289064/?dl=1>`_

sphere_exclusion_diverse_lib  - модуль, написанный на языке программирования Python,  для создания разнообразных библиотек с использованием метода исключенной сферы.  Для работы алгоритма нужны

**Зависимости**

- numpy
- pandas
- multiprocess
- matplotlib
- python 3.7

pharmmodels
-----------

Комплекс фармакофорных моделей для множества различных белков, построенных на основе базы данных ChEMBL

Комплекс разработанных фармакофорных моделей доступен для скачивания по ссылке: `download <https://seafile.cimm.site/f/5aaca9198c204e8b9209/?dl=1>`_


> \**Almost all copied markdown*\*

# キヤー子

Kiyago (stylized as キヤー子) stands for Kiyago Is Yet Another Grader Optimized for POSN-KKU (recursive nomenclature is the best).

 Kiyago offers more flexible choice of grading task for competitive programming contest. Each problem is fully customizable and inherently well-structured.

 *In this version will Aim for supporting other programming language(Eg. python Java)*

## Aims

- Scalable for future projects.
- Error well-handled.
- Well structured.
- Easy to maintain.
- **Support programming language as many as possible**

## Prerequisites

Python 3.8 or newer

```
sudo apt install python3
```

## Structure

### Problems

All problem directory goes in `problems/` which itself placed in root directory of the project.

To use standard_judge a problem directory is required to follow this struture :

```
PROBLEM_ID/
├── compile_space/
├── inputs/
├── solutions/
└── config.yaml
```

Please read this table for more information :

| Name          | Usage                                              |
|:-------------:|----------------------------------------------------|
| compile_space | Librabies, source file, and compiled binary        |
| inputs        | Where input files (*.in) goes                      |
| solutions     | Where solutions files (*.sol) goes                 |
| config.yaml   | Config file                                        |


#### config.yaml
You can *config* problems by changing config.yaml and here the thing that you can config


| Name          | Usage                                              |
|:-------------:|----------------------------------------------------|
| n_cases       | Tell the grader how many Test-case in this problem|
| memory_limit  | Set memory limit (mb.)|
| time_limit    | Set time limit (ms.)  |
| case_score    | Set score (per case)  |
|    |   |
| compile       | Set command line to compile for each lang  |
| run           | Set command line to run for each lang  |

Example :

```
custom_judge : false
n_cases : 10

memory_limit : 16
time_limit : 1000
case_score : 10

compile:
  c: gcc [SRC_PATH] -O2 -o [BIN_PATH] [CMP_OUT] [CMP_ERR]
  cpp: g++ [SRC_PATH] -O2 -std=c++17 -o [BIN_PATH] [CMP_OUT] [CMP_ERR]
  py: cp [SRC_PATH] [BIN_PATH]
  
run:
  c: "[BIN_PATH]"
  cpp: "[BIN_PATH]"
  py: python3 [BIN_PATH]
```

Here is an Example of each problem :

```
problems/
└── 001/
   ├── compile_space/
   │   ├── 001_001.c
   │   └── 001_001_bin
   ├── inputs/
   │   ├── 1.in
   │   ├── 2.in
   │   └── 3.in
   ├── solutions/
   │   ├── 1.sol
   │   ├── 2.sol
   │   └── 3.sol
   └── config.yaml
```

However, if the problem uses custom_judge, Kiyago offers full flexibity to the custom_judge by only requires `compile_space` and `config.yaml` to exist in the problem's root directory. Please note that compiling task still belongs to Kiyago.

```
problems/
└── 002/
   ├── compile_space/
   │   ├── custom_lib_1.h
   │   ├── custom_lib_2.h
   │   ├── 001_001.c
   │   └── 001_001_bin
   ├── judge_binary
   └── config.yaml
```

### Archives

While every subject's binary is **deleted** after finished grading, their coresponded source file is **moved** to `archives/USER_ID/PROBLEM_ID` and renamed to the time its was submitted as second since EPOCH (any decimal point is removed).

In this example, there are 2 problems and 3 subjects.

```
.
└── archives/
    ├── 001/
    │   ├──001/
    │   │  ├── 1591386889.cpp
    │   │  └── 1591387078.cpp
    │   └──002/
    │      ├── 1591387921.cpp
    │      └── 1591388078.cpp
    ├── 002/
    │   ├──001/
    │   │  └── 1591387143.cpp
    │   └──002/
    │      ├── 1591387951.cpp
    │      ├── 1591388239.cpp
    │      └── 1591388312.cpp
    └── 003/
        ├──001/
        │  └── 1591385127.cpp
        └──002/
           └── 1591388299.cpp
```

### Full Structure Example

```
.
├── archives/
│   ├── 001/
│   │   ├──001/
│   │   │  ├── 1591386889.cpp
│   │   │  └── 1591387078.cpp
│   │   └──002/
│   ├── 002/
│   └── 003/
├── kiyago/
├── problems/
│   ├── 001/
│   │   ├── compile_space/
│   │   │   └── subject_src.c
│   │   ├── inputs/
│   │   │   ├── 1.in
│   │   │   ├── 2.in
│   │   │   └── 3.in
│   │   ├── solutions/
│   │   │   ├── 1.sol
│   │   │   ├── 2.sol
│   │   │   └── 3.sol
│   │   ├── config.yaml
│   │   └── subject_bin
│   └── 002/
│       ├── compile_space/
│       │   ├── custom_header_1.h
│       │   └── custom_header_2.h
│       ├── config.yaml
│       └── grading_binary
├── run_kiyago
├── LICENSE
└── README.md
```

## Kiyago standard verdic strings

Strictly enforced (OTOG standard) :
| String | Meaning                 |
|:------:|-------------------------|
| **P**  | Correct                 |
| **S**  | Partially correct       |
| **-**  | Incorrect               |
| **T**  | Time-limit exceed       |
| **X**  | Etc. (e.g Runtime error)|

Optional (replace X):

| String | Meaning                 |
|:------:|-------------------------|
| **!**  | Grader-side error       |
| **M**  | Memory-limit exceed     |

## Writing a custom_judge

Custom grading binary/script (shall be, henceforth, called "custom_judge") runs once per testcase using command in `config.yaml`.

**To enable custom_judge, add this to `config.yaml`**

```yaml
custom_judge : True
judge_command : CMD_TO_RUN_JUDGE
```

### Input to custom_judge

If you use the custom judge, Kiyago provides these following information via :

```
[PROBLEM_DIR]/judge_binary [PROBLEM_DIR] [#]
```

For example

```c
// judge_binary.c
char *current_dir = argv[1];
int   this_case   = atoi(argv[2]);
```

### Output from custom_judge

The verdict of the testcase are expected to contain **ALL** of these following information for each testcase.

| Args    | Definition       |
|:-------:|------------------|
| verdic  | A verdic string  |
| elapsed | Time used        |
| score   | Score recieved   |
| kses    | KSES             |

where KESE stands for Kiyago Standard Error Signal which are :

| KESE    | Definition           |
|:-------:|----------------------|
| OK      | No problem           |
| UNSPECI | Unspecified rt. err. |
| TIMELXC | Time limit exceed    |
| MEMLXC  | Mem. limit exceed    |
| FPEXCPT | Floating point excp. |
| SEGMFLT | Segmentation fault   |
| ABORT   | Abort                |
| JUDGEER | Any judge-side err.  |

passing through STDOUT via PIPE using this format :

```
verdic;elapse;score;kses
```

For example, if the program ran correctly; 25 ms elapsed; 10 score for each case :

```
P;25;10;OK
```

Partially correct; 73 ms elapsed; scored 5 :

```
S;5;73;OK
```

Runtime error of segmentation fault:

```
X;0;0;SEGMFLT
```

TLE :

```
T;0;0;TIMELXC
```

**Please note that `verdic` could contain `;` nor whitespace in it.**

If there is any non-standard formatting (e.g. extra `;` or any absence of data)

```
T;0;
```

The `!` verdict are automatically thrown with KSES of `JUDGEER`.

```
!;0;0;JUDGEER
```

## Author

- **Krit Patyarath** - *Original work* - **[pannxe](www.github.com/pannxe)**
- **Peeraphol Sudputong** - *Implement for other lang* - **[Nepumi](https://github.com/Nepumi)**

## License

This project is licensed under the MIT License - see the LICENSE file for details

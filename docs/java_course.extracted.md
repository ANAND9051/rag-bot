Here's the transcription of the provided pages in clean Markdown format:

---

## Java Full Course

### 1. Flavours Of Java:

*   **Core Java (J2SE)**
    *   S/W
*   **Advance Java (J2EE)**
    *   Web
*   **Android Java (J2ME)**
    *   apps

### 2. Core Java Syllabus:

*   Introduction to Java.
*   Features of Java.

### 3. Core Java Syllabus:

*   Why Learn Java?
*   Introduction to Java.
    1.  Syntax of Java
    2.  Installation of Java (JDK)
    3.  First Java Program.
    4.  Compilation & Execution process of Java.

---

## Java Full Course

### Why Learn Java? # Features

1.  Simple and easy to learn.
2.  Open Source.
3.  Platform independent.
4.  Secure.
5.  Embedded. [C++, Java]
6.  Compiled & interpreted
7.  Robust
8.  Large library & frameworks

### Why Java so popular?

*   S/W
*   Web
*   apps.

---

## Java Full Course

*   Datatype
*   Variable
    *   Identifier
*   Keyword
*   Input & Output
*   Control flow:
    *   Conditional Statement.
    *   Looping statement.
    *   Transfer Statement.
*   Operators
*   Java methods
*   Java Array
*   Java String

---

## Java Full Course

**Q. What is Java? Full explanation.**

**Ans:** Java is a class-based, high-level, Object-oriented programming language developed by "James Gosling" and his friends in the year 1995.

**Note:**
*   The first version of Java (JDK 1.0) was released on the year Jan-23rd-1996 by "Sun microsystem". [ISO]
*   Latest version of Java (JDK 16) on the day 16th-March-2021. by "Oracle".

**Syntax:**
```java
class class-name {
    public static void main(String args[]) {
        // Code
    }
}
```

**Java Comments:**
1.  Single line (`//`)
2.  Multi-line (`/* ----- */`)

---

## Java Full Course

### Installation of Java (JDK 16)
### Installation of Eclipse IDE

**Q. First Java program?**

### Compilation & Execution process of Java:

```
[First.Java] (Source Code)
      ↓
    javac
      ↓
[First.class] (Byte Code)
      ↓
    JVM
      ↓
   Output
```
*(Diagram illustrates the flow from Source Code (e.g., on Windows/Linux) -> javac -> Byte Code -> JVM (on Windows/Linux) -> Output)*

---

## Java Full Course

**Q. What is Datatype? Full explanation.**

**Ans:** Data type specifies the different types of values that are stored in the Variables.

### Types

1.  **Primary:**
    *   **Numeric:**
        *   Byte (1)
        *   Short (2)
        *   int (4)
        *   long (8)
        *   float (4)
        *   double (8)
    *   **Non-numeric:**
        *   char (2)
        *   boolean (1 bit)

2.  **Secondary (User-defined):**
    *   Class
    *   Interface
    *   Array
    *   String

---

## Java Full Course

**Q. What is variable? Full explanation.**

**Ans:** Variable is the name of a memory location where we store different types of Values.

**Example:**
```java
int a = 10;
print(a);
```
*(Diagram shows a variable `a` pointing to a memory location containing the value `10`)*

### Types

*   Local
*   Static
*   Instance

---

## Java Full Course

**Q. What is Keyword? Full explanation.**

**Ans:** Keywords are the reserved words whose meaning is already defined in the Java Compiler. (simply pdf)

**Note:**
*   We can't use keywords for our personal use...
*   Keywords are Case-Sensitive. (e.g., `a` is different from `A`, `inf` is different from `INT`)

### Java Keywords: 50

| Keyword    | Keyword     | Keyword     | Keyword     | Keyword     |
| :--------- | :---------- | :---------- | :---------- | :---------- |
| `byte`     | `else`      | `extends`   | `import`    | `Switch`    |
| `Short`    | `for`       | `implements`| `class`     | `Case`      |
| `int`      | `do`        | `final`     | `interface` | `const`\*   |
| `long`     | `while`     | `finally`   | `new`       | `goto`\*    |
| `float`    | `break`     | `try`       | `native`    | `Strictfp`\*\*|
| `double`   | `Continue`  | `Catch`     | `instanceof`| `enum`\*\*\* |
| `void`     | `default`   | `throw`     | `package`   | `assert`\*\*\*|
| `char`     | `private`   | `throws`    | `return`    | `abstract`  |
| `boolean`  | `protected` | `Static`    | `this`      | `transient` |
| `if`       | `public`    | `volatile`  | `Super`     | `Synchronized`|

**Note:**
*   \* (not used)
*   \*\* (added in 1.2V)
*   \*\*\* (1.4V)
*   \*\*\*\* (5.0V)
*   `null`, `true`, `false` used as literals in Java (50+ Literals)

---

## Java Full Course

**Q. What is identifier? Full explanation.**

**Ans:** Identifiers refer to the name of variables, methods, classes, and so on.

**Example:**
*   `int Sal;` (Identifier for a variable)
*   `void M1();` (Identifier for a method)
*   `class A` (Identifier for a class)

---

## Java Full Course

### Input & Output:

**Input → Scanner class (`java.util.Scanner`)**

**Syntax:**
```java
Scanner obj-name = new Scanner(System.in);
```

**Scanner class methods:**
1.  `nextInt()` → for integer value
2.  `nextLine()` → for string Value
3.  `nextDouble()` → for double value

**Output → System class (`java.lang.System`)**

**Syntax:**
```java
System.out.print(" ");
```

**Q. W.A.P. to add two numbers?**

---

## Java Full Course

### Control flow:

#### 1) Conditional Statement

*   `if`
*   `if-else`
*   `else if`
*   `nested if-else`

**`if` Statement:** It is used when we want to test a Single Condition.

**Syntax:**
```java
if (Condition) {
    // code
}
```

**Flowchart:**
```
Start
  ↓
Condition? (True/False)
  ↓ (True)
  Code
  ↓
End
  ↑ (False)
```

---

## Java Full Course

### `if-else` Statement:

It is used when we want to execute two Statements for a single condition.

**Syntax:**
```java
if (condition) {
    // Statement 1;
} else {
    // Statement 2;
}
```

**Flowchart:**
```
Start
  ↓
Condition? (True/False)
  ↓ (True)        ↓ (False)
if block        else block
  ↓               ↓
End
```

**Example**

---

## Java Full Course

### `else-if` Statement:

It is used when we have only one `if` block, multiple `else-if` blocks, and at the last `else` block.

**Syntax:**
```java
if (Condition1) {
    // Statement 1
} else if (Condition2) {
    // Statement 2
} else {
    // Statement 3
}
```

**Flowchart:**
```
Start
  ↓
Condition1? (True/False)
  ↓ (True)        ↓ (False)
if block        Condition2? (True/False)
  ↓               ↓ (True)        ↓ (False)
End             else if block   else block
                  ↓               ↓
                  End             End
```

---

## Java Full Course

### 4) `nested if-else`:

Whenever we define an `if-else` block inside another `if-else` block, it is called `nested if-else`.

**Syntax:**
```java
if (Condition1) {
    if (Condition2) {
        // code
    } else {
        // code
    }
} else {
    if (Condition3) {
        // code
    } else {
        // code
    }
}
```

**Flowchart:** H.W (Homework)

**Program:** `asbse` (Example program name)

---

## Java Full Course

### Control Flow:

#### 2) Looping Statement

*   `for`
*   `while`
*   `do-while`
*   `for-each`

**Loop:** Whenever we want to repeat certain Statements several times, then we should write those statements inside the loop body.

#### 1) `for` loop:

**Syntax:**
```java
for (initialization; Condition; increment/decrement) {
    // Code
}
```

**Flowchart:**
```
Start
  ↓
Initialization
  ↓
Condition? (True/False)
  ↓ (True)        ↓ (False)
Loop body       End
  ↓
Increment/Decrement
  ↓
Condition? (back to condition check)
```

---

## Java Full Course

#### 2) `while` loop:

**Syntax:**
```java
while (condition) {
    // code
}
```

**Flowchart:**
```
Start
  ↓
Condition? (True/False)
  ↓ (True)        ↓ (False)
Loop body       End
  ↓
Condition? (back to condition check)
```

#### 3) `do-while` loop:

**Syntax:**
```java
do {
    // Statement;
} while (condition);
```

**Flowchart:**
```
Start
  ↓
Statement
  ↓
Condition? (True/False)
  ↓ (True)        ↓ (False)
Statement       End
  ↓
Condition? (back to condition check)
```

#### 4) `for-each` loop: (Array)

**Syntax:**
```java
for (datatype var : array) {
    // statement;
}
```

**Flowchart:** H.W (Homework)

**Array program**

---

Here's the transcription of the provided pages (17 to 32) in clean Markdown format:

---

## Page 17

### Java Full Course

**# Control flow :-**

### ③ Transfer Statement

*   → `break`
*   → `continue`
*   → `return`

---

## Page 18

### Java Full Course

**Q. What is Switch Statement? full explanation.**

**Ans.** Switch is a multiple choice decision making Selection Statement. It is used when we want to select only one Case out of multiple Cases.

**Syntax:**

```java
Switch (exp)
{
    Case 1: Statement 1;
            break;
    Case 2: Statement 2;
            break;
    ...
    Case n: Statement n;
            break;
    default: Statement;
}
```

**Flowchart:**

*   Start
*   Switch (Condition)
    *   If Case 1 is true → Statement 1 → end
    *   If Case 1 is false → If Case 2 is true → Statement 2 → end
    *   If Case 2 is false → If Case n is true → Statement n → end
    *   If Case n is false → If default is true → Statement → end

**Program (Arithmetic operator)**

---

## Page 19

### Java Full Course

**Q. What is Operator? full explanation.**

**Ans.** Operator is a symbol that is used to perform operations according to user requirement.

**Types:**

1.  **Arithmetic operator** (`+`, `-`, `*`, `%`, `/`)
2.  **Relational operator** (`==`, `!=`, `>`, `<`, `>=`, `<=`)
3.  **Logical operator** (`&&`, `||`, `!`)
4.  **Increment / Decrement**
    *   Pre/post increment (`++a`/`a++`)
    *   Pre/post decrement (`--a`/`a--`)
5.  **Assignment operator** (`=`, `+=`, `-=`, `*=`, `/=`, `%=`)
6.  **Ternary operator** (`?:`) (`a?b:c`)

---

## Page 20

### Java Full Course

**Q. What is method? full explanation.**

**Ans.** Method is a group/block of code which takes input from the user, processes it, and gives output.

**Note:**
*   Method runs only when it is Called.
*   Code reusability.

**Types:**

*   **Pre-defined**
    *   `print()`
    *   `Sort()`
    *   `nextInt()`
    *   `Sleep()`
    *   `Concat()`
*   **User defined**
    *   `add()`
    *   `sub()`
    *   `multi()`
    *   `LearnCoding()`

**Syntax:**

```java
return-type method-name (parameters (optional))
{
    // Statements:
}
```

---

## Page 21

### Java Full Course

**Q. What is arrays? full explanation.**

**Ans.** Arrays is an object in Java, which contains similar type of data in a contiguous memory location.

**Syntax:**

1.  `data-type [] var-name;`
2.  `data-type var-name[] = {10, 20, 70};`
3.  `int a[] = new int[5];`

**Note:** Array index starts with 0.

**Example:**

| 10 | 20 | 70 | 40 | 50 |
|----|----|----|----|----|
| 0  | 1  | 2  | 3  | 4  |

**Types:**

1.  1.D Array
2.  2.D Array

---

## Page 22

### Java Full Course

**Q. What is Strings? full explanation.**

**Ans.** String is a pre-defined class in Java but we can also use it as a datatype.

**Note:** Strings are the sequence of characters and its index starts from 0. "ankit"

**Syntax:**

1.  `String str = new String("ANKUSH");` (Stored in Heap memory)
2.  `String str = "ANKUSH";` (Stored in String Constant Pool (SCP))

**#. Why Strings are immutable in Java?**

*   `String str1 = "ANKUSH";` (SCP, e.g., address 1000)
*   `String str2 = "ANKUSH";` (SCP, points to the same "ANKUSH" at address 1000)
*   `String str3 = "ankit";` (SCP, e.g., address 1002)
*   `String str3 = new String("ANKUSH");` (HEAP, creates a new object)

*(Note: The handwritten text "Can't change" is associated with the SCP examples, highlighting immutability.)*

---

## Page 23

### Java Full Course

**Q. What is Class & Object? full explanation.**

**Ans.** Class is a group of elements having Common properties and behaviours.

**Note:**
*   Class is virtual
*   Object is real

**Example:**

```java
class Person
{
    // Properties (data members)
    age;
    weight;
    height;

    // Behaviours (methods)
    eat();
    sleep();
    talk();
}

// Object creation
Person p1 = new Person();
```

**Types (of classes/data types):**

*   **User-defined**
    *   Person
    *   Animal
*   **Pre-defined**
    *   System
    *   Strings
    *   Scanner

---

## Page 24

### Constructor

**Q. What is Constructor? full explanation.**

**Ans.** Constructor is a Special type of method whose name is Same as class name.

**Note:**
1.  The main purpose of Constructor is to initialize the object.
2.  Every Java class has a Constructor.

---

## Page 25

*(Continuation of notes on Constructor)*

3.  A Constructor is automatically Called at the time of object Creation.
4.  A Constructor never Contains any return-type including `void`.

---

## Page 26

### 1. default Constructor

**Q. What is default Constructor?**

**Ans.** A Constructor which does not have any parameter is Called default Constructor.

---

## Page 27

**Syntax (for default constructor):**

```java
class A
{
    A() // No any parameter
    {
        // ... statements ...
    }
}
```

---

## Page 28

### 2. Parametrized Constructor

**Q. What is parametrized Constructor?**

**Ans.** A Constructor through which we can pass One or more parameters is Called parametrized Constructor.

---

## Page 29

**Syntax (for parametrized constructor):**

```java
class A
{
    A(int x, String y)
    {
        // ... statements ...
    }
}
```

---

## Page 30

### 3. Copy Constructor

**Q. What is Copy Constructor? full detail.**

**Ans.** Whenever we pass Object reference to the constructor then it is Called Copy Constructor.

---

## Page 31

**Syntax (for copy constructor):**

```java
class class-name
{
    class-name(class-name obj_ref)
    {
        // ... statements ...
    }
}
```

---

## Page 32

### 4. Private Constructor

**Q. What is Private Constructor?**

**Ans.** In Java, it is possible to write a Constructor as a `private` but according to the rule we can't access private members outside of class.

---

Here's the transcription of the provided pages (33 to 48) in clean Markdown format:

---

### Page 33

```java
Syntax:- class class-name
{
    private class-name()
    {
    }
}
```

---

### Page 34

**VV.I**
## Super Keyword

**Q.** Super Keyword? full explanation.

**Ans** Super keyword refers to the objects of Super class, it is used when we want to call the Super Class Variable, method & Constructor through Sub class Object.

**Note:-**
1) Whenever the Super class & Sub class Variable and method name both are Same, it Can be used only.

---

### Page 35

**Note:-**
1) Whenever the Super class & Sub class Variable and method name both are Same than it Can be used only.
2) To avoid the Confusion between Super Class and Sub classes Variables and methods that have Same name we should use Super keyword.

---

### Page 36

**VV.I**
## this Keyword

**Q.** What is this keyword? full explanation.

**Ans**
1) this Keyword refers to the Current object inside a method or Constructor.

**Example:-**
```java
class A
{
    // ...
}

// ...
A r = new A();
```
*(Diagram shows a memory block labeled `bqrl@45` pointing to `A`)*

---

### Page 37

2) Whenever the name of instance and local Variables both are Same then our runtime environment JVM gets Confused that which one is local variable & which one is instance variable, to avoid this problem we should use this Keyword.

**Example:-**
```java
class A
{
    int a; // Instance variable

    void m(int a) // Local variable 'a'
    {
        this.a = a; // 'this.a' refers to the instance variable
        // ...
    }
}
```

---

### Page 38

**VV.I**
## Instance Vs Static Block

**Q.** Difference between Instance & Static block?

| Instance                               | Static                                 |
| :------------------------------------- | :------------------------------------- |
| 1) It deals With Object.               | 1) It deals With Class.                |
| 2) Executed at the time of object creation. | 2) Executed at the time of loaded .class file in JVM. |
| 3) With Program                        | 3) With Program                        |
| 4) No any Keyword required.            | 4) Static keyword is required.         |
| 5) Static & non-Static Variable Can be accessed inside the instance block. | 5) Only Static variable Can be accessed inside the Static block. |

---

### Page 39

## Java Full Course

**Q.** What is encapsulation & full explanation.

**Ans** Encapsulation is a mechanism through which we Can binding the data members and member methods in a single unit.

**Ex:-**
```java
class Bank
{
    private int bal; // balance
    private String pwd; // password

    void Deposit()
    {
        // ...
    }

    void Withdraw()
    {
        // ...
    }

    void CheckBal()
    {
        // ...
    }
}
```

---

### Page 40

## Full Course Java

**Q.** What is abstraction? full explanation.

**Ans** Abstraction is nothing but hiding the essential information and highlight the only set of Services.

*(Diagram shows: `Bank` -> `ATM` -> `1. Deposit`, `2. Withdraw`, `3. CheckBal`)*

In Java, we Can achieve abstraction in two ways:-
-> Abstract class (0-100%)
-> Interface (100%)

**Abstract class:-**
1) If a class Contain at least one abstract method is Called abstract class.
2) We Can't create objects of abstract class.
3) It Contains both abstract and non-abstract method.
4) Whenever the action is common but implementations are different than we Should use abstract method.

---

### Page 41

## Java Full Course

**Q.** What is interface? full explanation.

**Ans** Interface just like a class, which Contains only abstract method.
To achieve interface in Java by the help of `implements` keyword.

**Note:-**
1) By default variables are `public` + `static` + `final` inside an interface.
2) By default methods are `public` and `abstract`.
3) From JDK 1.8V onwards interface Can have `default` & `Static` methods.

---

### Page 42

**V.V.I**
## Inheritance

**Q.** What is inheritance? full explanation.

**Ans** When We Construct a new class from existing class in such a way that the new class Access all the features & properties of existing class Called inheritance.

**Note:-**
1) In Java, `extends` Keyword is used to perform inheritance.

---

### Page 43

2) It provides Code reusability.
3) We Can't access `private` members of class through inheritance.
4) A Sub class Contains all the features of Super class So, We Should Create the object of Sub class.
5) Method Overriding only possible through inheritance.

---

### Page 44

## Types:-
1) Single / Simple inheritance

*(Diagram shows: `Super` -> `Sub`)*

---

### Page 45

## inheritance

2) Multi-level inheritance :-

*(Diagram shows: `Super` -> `Sub 1` -> `Sub 2`)*

---

### Page 46

3) Multiple inheritance:- *(Crossed out)*

*(Diagram shows: `Super 1` and `Super 2` both pointing to `Sub`)*

4) Hierarchical

---

### Page 47

4) Hierarchical inheritance :-

*(Diagram shows: `Super` pointing to `Sub 1`, `Sub 2`, `Sub 3`)*

---

### Page 48

**V.V.I**
## Polymorphism

*(Diagram shows: `Poly` (Many) and `Morphism` (Form) both pointing to `Many form`)*

Polymorphism is the greek Word whose meaning is "Same Object having different behavior".

---

Here's the transcription of the provided pages in Markdown format:

---

### Page 49

For example:-

```
Costomer
      ↑
      |
friend ← Person → Students
      |
      ↓
    Teacher
```

ⅰ) `void person (Teacher)`
ⅱ) `void person (Students)`
ⅲ) `void person (friend)`
ⅳ) `void person (customer)`

---

### Page 50

Page No.:
Date: / /

## Polymorphism (V.V.I)

### Types

→ Compile time polymorphism
→ Runtime polymorphism

---

### Page 51

Page No.:
Date: / /

## Exception Handling (V.V.I)

**Q.** What is Exception? (full explanation)

**Ans>** An exception is unexpected / unwanted / abnormal situation that occurred at runtime Called exception.

---

### Page 52

## Exception Handling

Date: / /

```java
class A {
    main() {
        int a = 10, b = 0, c;
        c = a / b; // -> Exception
        S.o.p(c);
    }
}
```

---

### Page 53

PAGE NO.:
DATE: / /

## File Handling (V.V.I)

**Q.** What is file handling? full explanation.

**Ans>** File handling defines how we can read and write data on a file. Java IO package contains all the classes through which we can perform all input & output operations in the file.

---

### Page 54

**Stream:**- Stream is a sequence of data. On the basis of `java.io` package all the classes divided into two Stream.

```
      Stream
      /    \
    Byte  Character
```

---

### Page 55

## File handling methods:-

① `CanRead()`
② `CanWrite()`
③ `CreateNewFile()`
④ `Delete()`
⑤ `Exists()`
⑥ `length()`
⑦ `getName()`
⑧ `getAbsolutePath()`
⑨ `Mkdir()`
⑩ `List()`
⑪ `Read()`
⑫ `Writer()`
⑬ `renameTo()`

---

### Page 56

PAGE NO.:
DATE: / /

## File Handling (V.V.I)

## File handling classes :-

① `File`
② `FileReader`
③ `FileWriter`
④ `FileInputStream`
⑤ `FileOutputStream`
⑥ `BufferedInputStream`
⑦ `BufferedOutputStream`

---

### Page 57

Date: / /

## Package (Java) (V.V.I)

**Q.** What is package? full explanation.

**Ans>** A package arrange number of classes, interfaces and Sub-class / Sub-package of same type into a particular group.

**Note:**- package is nothing but folder in Windows.

---

### Page 58

## Types

```
       Types
       /   \
Pre-defined  User-defined
```

**Pre-defined**
→ `java.lang`
→ `java.util`
→ `java.io`
→ `java.applet`
→ `java.awt`
→ `java.net`
→ `java.net`

**User-defined**
→ `package P1`
→ `package add`
→ `package myPack`

---

### Page 59

| Access modifier | within class | within package | Outside package by Subclass | Outside package |
| :-------------- | :----------- | :------------- | :-------------------------- | :-------------- |
| `private`       | ✓            | X              | X                           | X               |
| `Default`       | ✓            | ✓              | X                           | X               |
| `protected`     | ✓            | ✓              | ✓                           | X               |
| `public`        | ✓            | ✓              | ✓                           | ✓               |

**Advantage:**-
① Reusability.

---

### Page 60

**Advantage:**-
① Reusability.
② Security.
③ Fast Searching.
④ Naming Conflicting. (P1, P2, A, A)
⑤ Hiding.

**Dis-advantage:**-
We Can't pass parameter to package.

---

### Page 61

PAGE NO.:
DATE: / /

## Multithreading (V.V.I)

**Q.** What is multithreading? With example.

**Ans>** Multithreading is a process to execute multiple threads at the same time without dependency of other threads Called multithreading.

---

### Page 62

```
Main() ? V

Raj   ---------------------> deposit (1020)
      | (30 min)
Rahul ---------------------> withdraw (2010)
      | (10 min)
Riti  ---------------------> check balance (32)
                                          (560)
```

**Q.** What is thread?

---

### Page 63

**Q.** What is thread?

**Ans>** Thread is a pre-defined class which is available in `java.lang` package. Thread is a basic unit of CPU and it is well known for Independent execution.

**Q.** HOW to Create Thread in Java?

**Ans>**
1) By extending `Thread` class.
2) By implementing `Runnable` interface.

---

### Page 64

KLASSNOTE
Page No...
Date........

## Java Full Course

**Q.** What is Collections? full explanation.

**Ans>** Java Collections are the set of pre-defined classes and interfaces that helps programmer to perform different kinds of data structure operations like - Sorting, Searching, Traversing, Storing and processing data efficiently.

```
                                  Iterable
                                      ↑
                                  Collection
                                      ↑
      ┌───────────────────────────────┼───────────────────────────────┐
      ↓                               ↓                               ↓
     List                           Queue                            Set
      ↑                               ↑                               ↑
      │                               │                               │
┌─────┴─────┐                 ┌───────┴───────┐                 ┌─────┴─────┐
│ ArrayList │                 │ PriorityQueue │                 │  HashSet  │
└───────────┘                 └───────────────┘                 └───────────┘
      ↑                               ↑                               ↑
      │                               │                               │
┌─────┴─────┐                 ┌───────┴───────┐                 ┌─────┴─────┐
│ LinkedList│                 │     Deque     │                 │LinkedHashSet│
└───────────┘                 └───────────────┘                 └───────────┘
      ↑                               ↑                               ↑
      │                               │                               │
┌─────┴─────┐                 ┌───────┴───────┐                 ┌─────┴─────┐
│   Vector  │                 │   ArrayDeque  │                 │  SortedSet  │
└───────────┘                 └───────────────┘                 └───────────┘
      ↑                                                               ↑
      │                                                               │
┌─────┴─────┐                                                     ┌─────┴─────┐
│   Stack   │                                                     │   TreeSet   │
└───────────┘                                                     └───────────┘

Legend:
■ interface
○ class
↑ implements
↑ extends
```
# Programming with Python – Assignment 1

## Course Information

**Course:** Programming with Python  
**Course Code:** 202044504  
**Program:** B.Tech. Information Technology  
**Semester:** V  
**Assignment:** Assignment 1  
**Language:** Python 3.10+  

---

## Student Information

**Name:** YOUR NAME  
**Enrollment No.:** YOUR ENROLLMENT NUMBER  
**Branch:** Information Technology  
**Semester:** V  

---

## About the Assignment

This repository contains the solutions for **Programming with Python – Assignment 1**.

The assignment focuses on advanced Python programming concepts including:

- Compound data structures
- Lists, tuples and dictionaries
- Sorting and data aggregation
- Strings and regular expressions
- Hashing and validation
- Recursive expressions
- Memoization
- CSV file handling
- Exception handling
- Object-oriented programming
- Custom exceptions
- Graphs and topological sorting
- Multithreading
- Thread synchronization
- Tkinter GUI
- File persistence
- Pickle and ZIP compression
- Data indexing

---

# Assignment Questions

## Q1. Campus Merit Analyzer using Compound Data Structures

This program stores student records containing:

- Enrollment number
- Name
- Semester
- CPI
- Subject marks

The program:

- Groups students according to semester.
- Finds the top `k` students based on CPI.
- Handles ties using subject-wise marks.
- Prints subject-wise highest marks.

### Concepts Used

- Lists
- Tuples
- Dictionaries
- Sorting
- Hashing
- Data aggregation

---

## Q2. Optimized Password Audit with Pattern Constraints

This program classifies passwords into:

- `STRONG`
- `WEAK_LENGTH`
- `WEAK_PATTERN`
- `COMPROMISED`

The password validation checks:

- Password length
- Uppercase letters
- Lowercase letters
- Digits
- Special characters
- Banned words
- Repeated characters

### Concepts Used

- Strings
- Regular expressions
- Hashing
- Validation
- Pattern matching

---

## Q3. Recursive Expression Engine with Memoization

This program evaluates arithmetic expressions containing:

- Variables
- `+`
- `-`
- `*`
- `/`
- Parentheses

It also detects:

- Cyclic dependencies
- Invalid expressions

Memoization is used to avoid unnecessary repeated calculations.

### Concepts Used

- Recursion
- Dictionaries
- Stacks
- Expression parsing
- Memoization
- Cycle detection

---

## Q4. Exception-Safe CSV Transaction Splitter

This program processes transaction records stored in a CSV file.

It:

- Reads transaction records.
- Validates transaction data.
- Separates CREDIT and DEBIT transactions.
- Calculates account balances.
- Handles invalid records using exception handling.
- Generates separate output files.

### Concepts Used

- CSV file handling
- Dictionaries
- Exception handling
- Sorting
- Data cleaning

---

## Q5. Object-Oriented Bank Settlement System

This program implements a bank settlement system using Object-Oriented Programming.

The system supports:

- Deposit
- Withdrawal
- Transfer
- Batch transactions
- Rollback when a batch fails
- Custom exceptions

### Concepts Used

- Classes and objects
- Encapsulation
- Custom exceptions
- Dictionaries
- Transactions
- Rollback logic

---

## Q6. Python Module Dependency Resolver

This program determines a valid loading order for Python modules based on their import dependencies.

It:

- Represents dependencies as a graph.
- Performs topological sorting.
- Detects circular dependencies.
- Ignores duplicate dependency edges.

### Concepts Used

- Graphs
- Topological sorting
- Dictionaries
- Sets
- Cycle detection
- Heaps

---

## Q7. Interactive Formula Validator with Custom Exceptions

This program works as an interactive calculator.

It supports:

- Variables
- Arithmetic operations
- Expression evaluation
- Division-by-zero detection
- Unsupported operator detection
- Unknown variable detection

The program continues until the user enters `quit`.

### Concepts Used

- Exception handling
- Custom exceptions
- Assertions
- Dictionaries
- Expression parsing
- Interactive programs

---

## Q8. Compressed Log Index using Pickle and Zip

This program processes log files stored inside a folder.

It:

- Reads multiple log files.
- Builds an inverted index.
- Stores file names and line numbers for tokens.
- Uses Pickle for index storage.
- Compresses data using ZIP.
- Supports token searching.

### Concepts Used

- File handling
- Pickle
- ZIP
- Dictionaries
- Text processing
- Indexing

---

## Q9. Threaded Job Scheduler Simulation

This program simulates a job scheduling system using multiple worker threads.

Each job contains:

- Job ID
- Arrival time
- Priority
- Duration
- Required resources

Higher-priority jobs are processed first.

The program also calculates:

- Worker assignment
- Start time
- Finish time
- Average waiting time

### Concepts Used

- Multithreading
- Thread synchronization
- Priority

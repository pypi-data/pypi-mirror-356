# kLogs

Small logging utility for uniform format, color

## Features:
- [ ] Easy to use log format language
- [ ] Search
- [ ] Open source at line
- [ ] log and assert

## Installation
```
pip install klogs-util
```

## Usage
```python
    from klogs import get_logger
    log = get_logger(tag, level, outfile)
    log.debug("debug statement")
    log.info("info statement")
    log.warning("warning statement")
    log.error("error statement")
    log.critical("critical statement")
```
Output:
```
<tag> - DEBUG - debug message (test.py:7)
<tag> - INFO - info message (test.py:8)
<tag> - WARNING - warning message (test.py:9)
<tag> - ERROR - error message (test.py:10)
<tag> - CRITICAL - critical message (test.py:11)
Stack (most recent call last):
  File "/Users/kevin/coding/kLogs/test.py", line 26, in <module>
    test(args.file, args.level)
  File "/Users/kevin/coding/kLogs/test.py", line 11, in test
    log.critical("critical message")

```

Or 

```python
    log()
    x = 10
    log(x)
```

Which will produce:
```
   <tag> - INFO -  (test.py:12)
   <tag> - INFO - x | 10 (test.py:14)
```

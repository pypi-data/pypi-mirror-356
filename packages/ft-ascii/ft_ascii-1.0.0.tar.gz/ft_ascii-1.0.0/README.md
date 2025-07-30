# ft_ascii

---

ft_ascii is a Python 3 package (originally designed for Python 3.10) that provides the user with two utilities:

- A CLI-interface, 42 school themed animated splash screen (it can be run on any terminal with "ft_ascii")

- A "count_in_list" function (intended to be imported by other scripts for testing purposes)

## Example usage

ft_ascii:

```bash
ft_ascii
```

![](https://i.imgur.com/rd0B5jd.gif)

count_in_list:

```python
from ft_ascii import count_in_list

print(count_in_list(["blablabla", "blebleble", "blublublu"], "blublublu")) # -> 1
```

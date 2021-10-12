# GitSwitch
 GitHub Desktop Multi account switcher

----
## Note:
* Project is currently in BETA status the README might not be up to date and the code might broken.  

--------------
## Why  : 
https://github.com/desktop/desktop/issues/3707
Since GitHub Desktop doesn't natively support multiple account. 

So users often have to log out and log back into their work and personnel accounts and re add the repos they're working on.

This aims to solve that problem by keeping a copy `Roaming\Github Desktop` for each user and then renaming the folder 
when asked and rename the folder back when switching to a new user. (records kept track using `~/gitswitch.json` file)


------------------

## How  :
* Make user login with each account in setup (`init`) process.
* rename `.gitconfig` and `GitHub Desktop` folder with username at the end.
* When `switch` method is called rename the user folder to `GitHub Desktop` and copy over the `.gitconfuser` file to `.gitconf`. 
* update the `~/gitswitch.json` with the current user details.


------------------
## Faq
**Q:** Does this work on Linux / macOS ?
<details>
  <summary>Answer</summary>
No this script only support windows for now. Feel free to open a pull request if you have a patch for Linux / macOS
</details>

-------------------------------------------------------

**Q:** How do you use this? 

<details>
  <summary>Answer</summary>
Check the installation section below. 
</details>



-----
# Installation

### Python
- **With Python >= 3.6**
```bash
$ pip install GitSwitch
```
or install the latest development branch using
```bash
pip install git+https://github.com/AnvithLobo/gitswitch
```

### Windows
- **Windows Standalone exe**

Download the exe from releases and add the exe and add the containing folder to your PATH
```html
https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10
```

******

### Init

- Run `gitswitch init` (First run only)
```bash
$ gitswitch init --help
usage: gitswitch init [-h] [-c USERNAME] [-u USERNAME [USERNAME ...]]

options:
  -h, --help            show this help message and exit
  -c USERNAME, --current-user USERNAME
                        Store current user login as (do not delete current user)
  -u USERNAME [USERNAME ...], --users USERNAME [USERNAME ...]
                        all usernames seperated by space
```
```bash
$ gitswitch init -c user1 -u user2 user3
```
```bash
$ gitswitch init -u user1 user2
```
*****

### Switch

- Run account switcher 

```bash
$ gitswitch switch --help
usage: gitswitch switch [-h] [-d]

options:
  -h, --help            show this help message and exit
  -d, --do-not-start-github
                        Do NOT Start github after switching account
```

```bash
$ gitswitch

Stopping Github Process...

Select Account  (Current User: User1)
----------------------------------------

1. User1
2. User2
3. User3

 Enter Your Choice (1-3) : 3
---------------


Switching account to user : User3

Done
```

just running `gitswitch` without any arguments will trigger `switch` command by default

***
### Add User/s

- Add more users. 
```bash
$ gitswitch adduser -h
usage: gitswitch adduser [-h] USERNAME [USERNAME ...]

positional arguments:
  USERNAME

options:
  -h, --help  show this help message and exit
```

```bash
$ gitswitch adduser user4 user5
```

---
ToDo:
-------
* Delete account/s.


---


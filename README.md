# GitSwitch
 GitHub Desktop Multi account switcher

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## ➤ Why  : 
https://github.com/desktop/desktop/issues/3707
Since GitHub Desktop doesn't natively support multiple account. 

So users often have to log out and log back into their work and personnel accounts and re add the repos they're working on.

This aims to solve that problem by keeping a copy `Roaming\Github Desktop` for each user and then renaming the folder 
when asked and rename the folder back when switching to a new user. (records kept track using `~/gitswitch.json` file)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## ➤ How  :
* Make user login with each account in setup (`init`) process.
* rename `.gitconfig` and `GitHub Desktop` folder with username at the end.
* When `switch` method is called rename the user folder to `GitHub Desktop` and copy over the `.gitconfuser` file to `.gitconf`. 
* update the `~/gitswitch.json` with the current user details.


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## ➤ FAQ
- **Q:** Does this work on Linux / macOS ?
<details>
  <summary>Answer</summary>
No this script only support windows for now. Feel free to open a pull request if you have a patch for Linux / macOS
</details>


- **Q:** How do you use this? 

<details>
  <summary>Answer</summary>
Check the installation section below. 
</details>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


# ➤ Installation

### Python
- **With Python >= 3.6**
```console
pip install GitSwitch
```
or install the latest development branch using
```console
pip install git+https://github.com/AnvithLobo/gitswitch
```

### Windows
- **Windows Standalone exe**

Download the exe from releases (TBD) and add the exe and add the containing folder to your PATH
```
https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Init

- Run `gitswitch init` (First run only)
```console
$ gitswitch init --help
usage: gitswitch init [-h] [-c USERNAME] [-u USERNAME [USERNAME ...]]

options:
  -h, --help            show this help message and exit
  -c USERNAME, --current-user USERNAME
                        Store current user login as (do not delete current user)
  -u USERNAME [USERNAME ...], --users USERNAME [USERNAME ...]
                        all usernames seperated by space
```
```console
$ gitswitch init -c user1 -u user2 user3
```
```console
$ gitswitch init -u user1 user2
```
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Switch

- Run account switcher 

```console
$ gitswitch switch --help
usage: gitswitch switch [-h] [-d]

options:
  -h, --help            show this help message and exit
  -d, --do-not-start-github
                        Do NOT Start github after switching account
```

```console
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

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)
## Add User/s

- Add more users. 
```console
$ gitswitch adduser -h
usage: gitswitch adduser [-h] USERNAME [USERNAME ...]

positional arguments:
  USERNAME

options:
  -h, --help  show this help message and exit
```

```console
$ gitswitch adduser user4 user5
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

 ➤ ToDo:
-------
* Delete account/s.


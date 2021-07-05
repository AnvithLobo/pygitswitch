# GitHub-Switch
 GitHub Desktop Multi account switcher

--------------
## Why  : 
https://github.com/desktop/desktop/issues/3707
Since GitHub Desktop doesn't natively support multiple account. 

So users often have to log out and log back into their work and personnel accounts and re add the repos they're working on.

This aims to solve that problem by keeping a copy `Roaming\Github Desktop` folder for each user and symlink the chosen user directory which preserves the last used state.

------------------

## How  :
* Make user login with each account in setup (`init`) process.
* rename `.gitconfig` and `GitHub Desktop` folder with username at the end.
* When `switch` method is called create a symlink from user folder to `GitHub Desktop` and copy over the `.gitconfuser` file to `.gitconf`


------------------
## Faq
**Q:** Does this work on Linux / macOS ?
<details>
  <summary>Answer</summary>
No this script only support windows for now. Feel free to open a pull request if you have a patch for Linux / macOS
</details>
-------------------------------------------------------

**Q:** Why does it ask for Admin Privileges when trying to switch accounts.

<details>
  <summary>Answer</summary>
`mklink` on Windows needs admin privileges to create symlinks. (if someone has a better solution please open an issue / pull request)
</details>
-------------------------------------------------------

**Q:** How do you use this? 

<details>
  <summary>Answer</summary>
**A:** Check the installation section here. 
</details>
-------------------------------------------------------



-----
# Installation

- `CD` into the directory you want to store the scripts in.
```bash
$ git clone https://github.com/AnvithLobo/github-switch.git
```
or download the .zip file from [here](https://github.com/AnvithLobo/github-switch/archive/refs/heads/main.zip) and extract it to the folder you want.

--
- Edit the accounts in `switcher.py`
```python
accounts = ['user1', 'user2', 'user3']
```
--
- Run `init.bat` or 
```bash
$ python switcher.py init
```
 and follow the steps

--

- Run `create-switcher.bat`. This will create a desktop and start menu shortcut for account switcher

--

-----------
## Add more Accounts:

- Run 
```bash
$ python switcher.py add_accounts user1 user2 .... userX
```
---

## Delete account/s.
#### ToDO.

---


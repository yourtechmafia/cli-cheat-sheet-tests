# Demos on windows-11-arm64

```json
{
  "python": "3.15.0",
  "platform": "Windows-11-10.0.26200-SP0",
  "machine": "ARM64",
  "curl": "curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP"
}
{
  "pwsh": "7.6.6 Core",
  "powershell": "5.1.26100.9457 Desktop",
  "cmd": "Microsoft Windows [Version 10.0.26200.9457]"
}
```

## alias / pwsh (exit 0)

```
New-Item -ItemType File -Path $PROFILE -Force | Out-Null
Add-Content -Path $PROFILE -Value 'function ll { Get-ChildItem -Force @args }'
```

Output:

```
```

Follow-up in a new interactive shell: `ll notes.txt` (exit 0)

```

    Directory: ~/practice

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          10/11/2026  5:22 AM             12 notes.txt

```

## alias / powershell (exit 0)

```
New-Item -ItemType File -Path $PROFILE -Force | Out-Null
Add-Content -Path $PROFILE -Value 'function ll { Get-ChildItem -Force @args }'
```

Output:

```

```

Follow-up in a new interactive shell: `ll notes.txt` (exit 0)

```


    Directory: ~/practice


Mode                 LastWriteTime         Length Name                                                                 
----                 -------------         ------ ----                                                                 
-a----        10/11/2026   5:22 AM             12 notes.txt                                                            


```

## alias / cmd (exit 1)

```
doskey ll=dir /a $*
ll
```

Output:

```
'll' is not recognized as an internal or external command,
operable program or batch file.
```

## and-or / pwsh (exit 0)

```
mkdir out && echo "created" || echo "failed"
mkdir out && echo "created" || echo "failed"
```

Output:

```

    Directory: ~/practice

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----          10/11/2026  5:22 AM                out
created
New-Item: 
Line |
   2 |  mkdir out && echo "created" || echo "failed"
     |  ~~~~~~~~~
     | An item with the specified name ~/practice\out already exists.
failed

```

## and-or / powershell (exit 1)

```
mkdir out && echo "created"
```

Output:

```

At line:1 char:11
+ mkdir out && echo "created"
+           ~~
The token '&&' is not a valid statement separator in this version.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : InvalidEndOfLine
 
```

## and-or / cmd (exit 0)

```
mkdir out && echo created || echo failed
mkdir out && echo created || echo failed
```

Output:

```
created 
A subdirectory or file out already exists.
failed
```

## and-or-51 / powershell (exit 0)

```
mkdir out | Out-Null; if ($?) { "created" } else { "failed" }
mkdir out 2>$null | Out-Null; if ($?) { "created" } else { "failed" }
```

Output:

```

created
failed
```

## api-json / pwsh (exit 0)

```
Invoke-RestMethod https://api.github.com/repos/curl/curl/releases/latest | Select-Object tag_name, published_at
```

Output:

```

tag_name    published_at
--------    ------------
curl-8_22_0 9/2/2026 5:59:35 AM

```

## api-json / powershell (exit 0)

```
Invoke-RestMethod https://api.github.com/repos/curl/curl/releases/latest | Select-Object tag_name, published_at
```

Output:

```

tag_name    published_at        
--------    ------------        
curl-8_22_0 2026-09-02T05:59:35Z
```

## bash-in-powershell / pwsh (exit 0)

```
ls -la
sort -u names.txt
grep zzz log.txt
echo $?
echo $PATH
find . -name "*.txt"
cp -r docs docs-backup
Test-Path docs-backup\deep\c.txt
```

Output:

```
Get-ChildItem: A parameter cannot be found that matches parameter name 'la'.
grep: 
Line |
   3 |  grep zzz log.txt
     |  ~~~~
     | The term 'grep' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
False
FIND: Parameter format not correct
True
```

## bash-in-powershell / powershell (exit 0)

```
ls -la
sort -u names.txt
grep zzz log.txt
echo $?
echo $PATH
find . -name "*.txt"
cp -r docs docs-backup
Test-Path docs-backup\deep\c.txt
```

Output:

```

False
FIND: Parameter format not correct
True
Get-ChildItem : A parameter cannot be found that matches parameter name 'la'.
At line:1 char:4
+ ls -la
+    ~~~
    + CategoryInfo          : InvalidArgument: (:) [Get-ChildItem], ParameterBindingException
    + FullyQualifiedErrorId : NamedParameterNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand
 
grep : The term 'grep' is not recognized as the name of a cmdlet, function, script file, or operable program. Check 
the spelling of the name, or if a path was included, verify that the path is correct and try again.
At line:3 char:1
+ grep zzz log.txt
+ ~~~~
    + CategoryInfo          : ObjectNotFound: (grep:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
```

## double-dash / pwsh (exit 0)

```
New-Item -ItemType File "-oops.txt" | Out-Null
Get-ChildItem -oops.txt
Get-ChildItem "-oops.txt" -Name
Remove-Item "-oops.txt"
```

Output:

```
Get-ChildItem: 
Line |
   2 |  Get-ChildItem -oops.txt
     |                ~~~~~
     | A parameter cannot be found that matches parameter name 'oops'.
-oops.txt
```

## double-dash / powershell (exit 0)

```
New-Item -ItemType File "-oops.txt" | Out-Null
Get-ChildItem -oops.txt
Get-ChildItem "-oops.txt" -Name
Remove-Item "-oops.txt"
```

Output:

```

-oops.txt
Get-ChildItem : A parameter cannot be found that matches parameter name 'oops'.
At line:2 char:15
+ Get-ChildItem -oops.txt
+               ~~~~~
    + CategoryInfo          : InvalidArgument: (:) [Get-ChildItem], ParameterBindingException
    + FullyQualifiedErrorId : NamedParameterNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand
 
```

## double-dash / cmd (exit 0)

```
type nul > -oops.txt
dir /b -oops.txt
del -oops.txt
```

Output:

```
-oops.txt
```

## echo-space / cmd (exit 0)

```
echo first > spaced.txt
echo first> tight.txt
for %%f in (spaced.txt tight.txt) do echo %%f: %%~zf bytes
```

Output:

```
spaced.txt: 8 bytes
tight.txt: 7 bytes
```

## env-permanent / pwsh (exit 0)

```
[Environment]::SetEnvironmentVariable("GREETING", "hello", "User")
[Environment]::GetEnvironmentVariable("GREETING", "User")
"this session: [$env:GREETING]"
```

Output:

```
hello
this session: []
```

## env-permanent / powershell (exit 0)

```
[Environment]::SetEnvironmentVariable("GREETING", "hello", "User")
[Environment]::GetEnvironmentVariable("GREETING", "User")
"this session: [$env:GREETING]"
```

Output:

```
hello
this session: []
```

## env-permanent / cmd (exit 0)

```
setx GREETING hello
echo this session: [%GREETING%]
```

Output:

```

SUCCESS: Specified value was saved.
this session: []
```

## env-session / pwsh (exit 0)

```
$env:GREETING = "hello"
$env:GREETING
```

Output:

```
hello
```

## env-session / powershell (exit 0)

```
$env:GREETING = "hello"
$env:GREETING
```

Output:

```
hello
```

## env-session / cmd (exit 0)

```
set GREETING=hello
echo %GREETING%
```

Output:

```
hello
```

## escape / pwsh (exit 0)

```
"Price: `$5 and a `"quote`""
```

Output:

```
Price: $5 and a "quote"
```

## escape / powershell (exit 0)

```
"Price: `$5 and a `"quote`""
```

Output:

```
Price: $5 and a "quote"
```

## escape / cmd (exit 0)

```
echo Price: $5 and a ^<tag^>
```

Output:

```
Price: $5 and a <tag>
```

## execution-policy / powershell (exit 1)

```
.\hello.ps1
```

Output:

```

.\hello.ps1 : File ~/practice\hello.ps1 cannot be 
loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at 
https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ .\hello.ps1
+ ~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

## execution-policy-fix / powershell (exit 1)

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
Get-ExecutionPolicy -Scope CurrentUser
Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser -Force
```

Output:

```

Set-ExecutionPolicy : The 'Set-ExecutionPolicy' command was found in the module 'Microsoft.PowerShell.Security', but 
the module could not be loaded. For more information, run 'Import-Module Microsoft.PowerShell.Security'.
At line:1 char:1
+ Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser  ...
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (Set-ExecutionPolicy:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CouldNotAutoloadMatchingModule
 
Get-ExecutionPolicy : The 'Get-ExecutionPolicy' command was found in the module 'Microsoft.PowerShell.Security', but 
the module could not be loaded. For more information, run 'Import-Module Microsoft.PowerShell.Security'.
At line:2 char:1
+ Get-ExecutionPolicy -Scope CurrentUser
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (Get-ExecutionPolicy:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CouldNotAutoloadMatchingModule
 
Set-ExecutionPolicy : The 'Set-ExecutionPolicy' command was found in the module 'Microsoft.PowerShell.Security', but 
the module could not be loaded. For more information, run 'Import-Module Microsoft.PowerShell.Security'.
At line:3 char:1
+ Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser -Fo ...
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (Set-ExecutionPolicy:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CouldNotAutoloadMatchingModule
 
```

## exit-codes / pwsh (exit 0)

```
findstr zzz log.txt
"findstr exit code: $LASTEXITCODE"
nosuchcommand
"last command succeeded: $?"
```

Output:

```
findstr exit code: 1
nosuchcommand: 
Line |
   3 |  nosuchcommand
     |  ~~~~~~~~~~~~~
     | The term 'nosuchcommand' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
last command succeeded: False
```

## exit-codes / powershell (exit 0)

```
findstr zzz log.txt
"findstr exit code: $LASTEXITCODE"
nosuchcommand
"last command succeeded: $?"
```

Output:

```
findstr exit code: 1
last command succeeded: False
nosuchcommand : The term 'nosuchcommand' is not recognized as the name of a cmdlet, function, script file, or operable 
program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
At line:3 char:1
+ nosuchcommand
+ ~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (nosuchcommand:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
```

## exit-codes / cmd (exit 0)

```
findstr zzz log.txt
echo findstr exit code: %ERRORLEVEL%
nosuchcommand
echo command not found: %ERRORLEVEL%
```

Output:

```
findstr exit code: 1
'nosuchcommand' is not recognized as an internal or external command,
operable program or batch file.
command not found: 9009
```

## help / pwsh (exit 0)

```
Update-Help -Module Microsoft.PowerShell.Management -Scope CurrentUser
Get-Help Get-ChildItem -Examples
```

Output:

```

NAME
    Get-ChildItem
    
SYNOPSIS
    Gets the items and child items in one or more specified locations.
    
    
    --------- Example 1: Get child items from a file system directory ---------
    
    This example gets the child items from a file system directory. The filenames and subdirectory names
    are displayed. For empty locations (directories or folders), the command doesn't return any output
    and returns to the PowerShell prompt.
    
    The `Get-ChildItem` cmdlet uses the **Path** parameter to specify the directory `C:\Test`.
    `Get-ChildItem` displays the files and directories in the PowerShell console.
    
    ```powershell
    Get-ChildItem -Path C:\Test
    ```
    
    ```Output
       Directory: C:\Test
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    d-----        2/15/2019     08:29                Logs
    -a----        2/13/2019     08:55             26 anotherfile.txt
    -a----        2/12/2019     15:40         118014 Command.txt
    -a----         2/1/2019     08:43            183 CreateTestFile.ps1
    -ar---        2/12/2019     14:31             27 ReadOnlyFile.txt
    ```
    
    By default `Get-ChildItem` lists the mode (**Attributes**), **LastWriteTime**, file size
    (**Length**), and the **Name** of the item. The letters in the **Mode** property can be interpreted
    as follows:
    
    - `l` (link)
    - `d` (directory)
    - `a` (archive)
    - `r` (read-only)
    - `h` (hidden)
    - `s` (system)
    
    For more information about the mode flags, see
    [about_FileSystem_Provider](../Microsoft.PowerShell.Core/About/about_FileSystem_Provider.md#attributes-flagsexpress
    ion).
    
     --------- Example 2: Get child item names in a directory ---------
    
    This example lists only the names of items in a directory.
    
    The `Get-ChildItem` cmdlet uses the **Path** parameter to specify the directory `C:\Test`. The
    **Name** parameter returns only the file or directory names from the specified path. The names
    returned are relative to the value of the **Path** parameter.
    
    ```powershell
    Get-ChildItem -Path C:\Test -Name
    ```
    
    ```Output
    Logs
    anotherfile.txt
    Command.txt
    CreateTestFile.ps1
    ReadOnlyFile.txt
    ```
    
     --------- Example 3: Get child items in the current directory and subdirectories ---------
    
    This example displays `.txt` files that are located in the current directory and its
    subdirectories.
    
    ```powershell
    Get-ChildItem -Path .\*.txt -Recurse -Force
    ```
    
    ```Output
        Directory: C:\Test\Logs\Adirectory
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----        2/12/2019     16:16             20 Afile4.txt
    -a-h--        2/12/2019     15:52             22 hiddenfile.txt
    -a----        2/13/2019     13:26             20 LogFile4.txt
    
    Directory: C:\Test\Logs\Backup
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----        2/12/2019     16:16             20 ATextFile.txt
    -a----        2/12/2019     15:50             20 LogFile3.txt
    
    Directory: C:\Test\Logs
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----        2/12/2019     16:16             20 Afile.txt
    -a-h--        2/12/2019     15:52             22 hiddenfile.txt
    -a----        2/13/2019     13:26             20 LogFile1.txt
    
    Directory: C:\Test
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----        2/13/2019     08:55             26 anotherfile.txt
    -a----        2/12/2019     15:40         118014 Command.txt
    -a-h--        2/12/2019     15:52             22 hiddenfile.txt
    -ar---        2/12/2019     14:31             27 ReadOnlyFile.txt
    ```
    
    The `Get-ChildItem` cmdlet uses the **Path** parameter to specify `C:\Test\*.txt`. **Path** uses the
    asterisk (`*`) wildcard to specify all files with the filename extension `.txt`. The **Recurse**
    parameter searches the **Path** directory and its subdirectories, as shown in the **Directory:**
    headings. The **Force** parameter displays hidden files such as `hiddenfile.txt` that have a mode of
    **h**.
    
     --------- Example 4: Get child items using the Include parameter ---------
    
    In this example `Get-ChildItem` uses the **Include** parameter to find specific items from the
    directory specified by the **Path** parameter.
    
    ```powershell
    # When using the -Include parameter, if you don't include an asterisk in the path
    # the command returns no output.
    Get-ChildItem -Path C:\Test\ -Include *.txt
    ```
    
    ```Output
    
    ```
    
    ```powershell
    Get-ChildItem -Path C:\Test\* -Include *.txt
    ```
    
    ```Output
        Directory: C:\Test
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----        2/13/2019     08:55             26 anotherfile.txt
    -a----        2/12/2019     15:40         118014 Command.txt
    -ar---        2/12/2019     14:31             27 ReadOnlyFile.txt
    ```
    
    The `Get-ChildItem` cmdlet uses the **Path** parameter to specify the directory `C:\Test`. The
    **Path** parameter includes a trailing asterisk (`*`) wildcard to specify the directory's contents.
    The **Include** parameter uses an asterisk (`*`) wildcard to specify all files with the file name
    extension `.txt`.
    
    When the **Include** parameter is used, the **Path** parameter needs a trailing asterisk (`*`)
    wildcard to specify the directory's contents. For example, `-Path C:\Test\*`.
    
    - If the **Recurse** parameter is added to the command, the trailing asterisk (`*`) in the **Path**
      parameter is optional. The **Recurse** parameter gets items from the **Path** directory and its
      subdirectories. For example, `-Path C:\Test\ -Recurse -Include *.txt`
    - If a trailing asterisk (`*`) isn't included in the **Path** parameter, the command doesn't return
      any output and returns to the PowerShell prompt. For example, `-Path C:\Test\`.
    
     --------- Example 5: Get child items using the Exclude parameter ---------
    
    The example's output shows the contents of the directory `C:\Test\Logs`. The output is a reference
    for the other commands that use the **Exclude** and **Recurse** parameters.
    
    ```powershell
    Get-ChildItem -Path C:\Test\Logs
    ```
    
    ```Output
        Directory: C:\Test\Logs
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    d-----        2/15/2019     13:21                Adirectory
    d-----        2/15/2019     08:28                AnEmptyDirectory
    d-----        2/15/2019     13:21                Backup
    -a----        2/12/2019     16:16             20 Afile.txt
    -a----        2/13/2019     13:26             20 LogFile1.txt
    -a----        2/12/2019     16:24             23 systemlog1.log
    ```
    
    ```powershell
    Get-ChildItem -Path C:\Test\Logs\* -Exclude A*
    ```
    
    ```Output
        Directory: C:\Test\Logs
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    d-----        2/15/2019     13:21                Backup
    -a----        2/13/2019     13:26             20 LogFile1.txt
    -a----        2/12/2019     16:24             23 systemlog1.log
    ```
    
    The `Get-ChildItem` cmdlet uses the **Path** parameter to specify the directory `C:\Test\Logs`. The
    **Exclude** parameter uses the asterisk (`*`) wildcard to specify any files or directories that
    begin with `A` or `a` are excluded from the output.
    
    When the **Exclude** parameter is used, a trailing asterisk (`*`) in the **Path** parameter is
    optional. For example, `-Path C:\Test\Logs` or `-Path C:\Test\Logs\*`.
    
    - If a trailing asterisk (`*`) isn't included in the **Path** parameter, the contents of the
      **Path** parameter are displayed. The exceptions are filenames or subdirectory names that match
      the **Exclude** parameter's value.
    - If a trailing asterisk (`*`) is included in the **Path** parameter, the command recurses into the
      **Path** parameter's subdirectories. The exceptions are filenames or subdirectory names that match
      the **Exclude** parameter's value.
    - If the **Recurse** parameter is added to the command, the recursion output is the same whether or
      not the **Path** parameter includes a trailing asterisk (`*`).
    
     --------- Example 6: Get the registry keys from a registry hive ---------
    
    This example gets all the registry keys from `HKEY_LOCAL_MACHINE\HARDWARE`.
    
    `Get-ChildItem` uses the **Path** parameter to specify the registry key `HKLM:\HARDWARE`. The hive's
    path and top level of registry keys are displayed in the PowerShell console.
    
    For more information, see
    [about_Registry_Provider](../Microsoft.PowerShell.Core/About/about_Registry_Provider.md).
    
    ```powershell
    Get-ChildItem -Path HKLM:\HARDWARE
    ```
    
    ```Output
        Hive: HKEY_LOCAL_MACHINE\HARDWARE
    
    Name             Property
    ----             --------
    ACPI
    DESCRIPTION
    DEVICEMAP
    RESOURCEMAP
    UEFI
    ```
    
    ```powershell
    Get-ChildItem -Path HKLM:\HARDWARE -Exclude D*
    ```
    
    ```Output
       Hive: HKEY_LOCAL_MACHINE\HARDWARE
    
    Name                           Property
    ----                           --------
    ACPI
    RESOURCEMAP
    ```
    
    The first command shows the contents of the `HKLM:\HARDWARE` registry key. The **Exclude** parameter
    tells `Get-ChildItem` not to return any subkeys that start with `D*`. Currently, the **Exclude**
    parameter only works on subkeys, not item properties.
    
     --------- Example 7: Get all certificates with code-signing authority ---------
    
    This example gets each certificate in the PowerShell `Cert:` drive that has code-signing authority.
    
    The `Get-ChildItem` cmdlet uses the **Path** parameter to specify the Certificate provider with the
    `Cert:` drive. The **Recurse** parameter searches the directory specified by **Path** and its
    subdirectories. The **CodeSigningCert** parameter gets only certificates that have code-signing
    authority.
    
    ```powershell
    Get-ChildItem -Path Cert:\* -Recurse -CodeSigningCert
    ```
    
    For more information about the Certificate provider and the `Cert:` drive, see
    [about_Certificate_Provider](../Microsoft.PowerShell.Security/About/about_Certificate_Provider.md).
    
     --------- Example 8: Get items using the Depth parameter ---------
    
    This example displays the items in a directory and its subdirectories. The **Depth** parameter
    determines the number of subdirectory levels to include in the recursion. Empty directories are
    excluded from the output.
    
    ```powershell
    Get-ChildItem -Path C:\Parent -Depth 2
    ```
    
    ```Output
        Directory: C:\Parent
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    d-----        2/14/2019     10:24                SubDir_Level1
    -a----        2/13/2019     08:55             26 file.txt
    
    Directory: C:\Parent\SubDir_Level1
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    d-----        2/14/2019     10:24                SubDir_Level2
    -a----        2/13/2019     08:55             26 file.txt
    
    Directory: C:\Parent\SubDir_Level1\SubDir_Level2
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    d-----        2/14/2019     10:22                SubDir_Level3
    -a----        2/13/2019     08:55             26 file.txt
    ```
    
    The `Get-ChildItem` cmdlet uses the **Path** parameter to specify `C:\Parent`. The **Depth**
    parameter specifies two levels of recursion. `Get-ChildItem` displays the contents of the directory
    specified by the **Path** parameter and the two levels of subdirectories.
    
     --------- Example 9: Getting hard link information ---------
    
    In PowerShell 6.2, an alternate view was added to get hard link information.
    
    ```powershell
    Get-ChildItem -Path C:\PathContainingHardLink | Format-Table -View childrenWithHardLink
    ```
    
     --------- Example 10: Output for Non-Windows Operating Systems ---------
    
    In PowerShell 7.1 on Unix systems, the `Get-ChildItem` provides Unix-like output:
    
    ```powershell
    PS> Get-ChildItem /etc/r*
    ```
    
    ```Output
        Directory: /etc
    
    UnixMode   User Group    LastWriteTime Size Name
    --------   ---- -----    ------------- ---- ----
    drwxr-xr-x root wheel  9/30/2019 19:19  128 racoon
    -rw-r--r-- root wheel  9/26/2019 18:20 1560 rc.common
    -rw-r--r-- root wheel  7/31/2017 17:30 1560 rc.common~previous
    -rw-r--r-- root wheel  9/27/2019 20:34 5264 rc.netboot
    lrwxr-xr-x root wheel  11/8/2019 15:35   22 resolv.conf -> /private/var/run/resolv.conf
    -rw-r--r-- root wheel 10/23/2019 17:41    0 rmtab
    -rw-r--r-- root wheel 10/23/2019 17:41 1735 rpc
    -rw-r--r-- root wheel  7/25/2017 18:37 1735 rpc~previous
    -rw-r--r-- root wheel 10/23/2019 18:42  891 rtadvd.conf
    -rw-r--r-- root wheel  8/24/2017 21:54  891 rtadvd.conf~previous
    ```
    
    The new properties that are now part of the output are:
    
    - **UnixMode** is the file permissions as represented on a Unix system
    - **User** is the file owner
    - **Group** is the group owner
    - **Size** is the size of the file or directory as represented on a Unix system
    
    > [!NOTE]
    > This feature was moved from experimental to mainstream in PowerShell 7.1.
    
     --------- Example 11: Get the link target for a junction point ---------
    
    The `dir` command in the Windows Command Shell shows the target location of a filesystem junction
    point. In PowerShell, this information is available from the **LinkTarget** property of the
    filesystem object returned by `Get-ChildItem` and is displayed in the default output.
    
    ```powershell
    PS D:\> New-Item -ItemType Junction -Name tmp -Target $Env:TEMP
    PS D:\> Get-ChildItem | Select-Object Name, LinkTarget
    
    Name     LinkTarget
    ----     ----------
    tmp      C:\Users\user1\AppData\Local\Temp
    
    PS D:\> Get-ChildItem
    
    Directory: D:\
    
    Mode          LastWriteTime    Length Name
    ----          -------------    ------ ----
    l----   12/16/2021  9:29 AM           tmp -> C:\Users\user1\AppData\Local\Temp
    ```
    
     --------- Example 12: Get the link target for an AppX reparse point ---------
    
    This example attempts to get the target information for an AppX reparse point. Microsoft Store
    applications create AppX reparse points in the user's AppData directory.
    
    ```powershell
    Get-ChildItem ~\AppData\Local\Microsoft\WindowsApps\MicrosoftEdge.exe |
        Select-Object Mode, LinkTarget, LinkType, Name
    ```
    
    ```Output
    Mode  LinkTarget LinkType Name
    ----  ---------- -------- ----
    la---                     MicrosoftEdge.exe
    ```
    
    At this time, Windows doesn't provide a way to get the target information for an AppX reparse point.
    The **LinkTarget** and **LinkType** properties of the filesystem object are empty.
    
     --------- Example 13: Use a filter to get only log files in a directory ---------
    
    ```powershell
    # Returns only .log files in C:\Test (filtering is performed by the FileSystem provider)
    Get-ChildItem -Path C:\Test -Filter '*.log'
    
    # Returns only .log files in C:\Test (filtering is performed by Get-ChildItem after the
    # FileSystem provider enumerates all files)
    Get-ChildItem -Path C:\Test -Include '*.log'
    ```
    
 

```

## help / powershell (exit 0)

```
Update-Help -Module Microsoft.PowerShell.Management
Get-Help Get-ChildItem -Examples
```

Output:

```

```

## help / cmd (exit 0)

```
dir /? | find "Displays"
echo Exit code: %ERRORLEVEL%
```

Output:

```
Displays a list of files and subdirectories in a directory.
  /A          Displays files with specified attributes.
  /S          Displays files in specified directory and all subdirectories.
  /4          Displays four-digit years
Exit code: 0
```

## long-options / pwsh (exit 0)

```
Get-ChildItem -Recurse -Filter *.md | Select-Object -ExpandProperty Name
gci -r -fi *.md | Select-Object -ExpandProperty Name
```

Output:

```
b.md
b.md
```

## long-options / powershell (exit 0)

```
Get-ChildItem -Recurse -Filter *.md | Select-Object -ExpandProperty Name
gci -r -fi *.md | Select-Object -ExpandProperty Name
```

Output:

```

b.md
b.md
```

## ndjson / pwsh (exit 0)

```
Get-Content books.ndjson | ConvertFrom-Json | ForEach-Object body | Sort-Object price | Format-Table price, title
```

Output:

```

price  title
-----  -----
£47.82 Sharp Objects
£50.10 Soumission
£51.77 A Light in the Attic
£53.74 Tipping the Velvet
£54.23 Sapiens: A Brief History of Humankind

```

## ndjson / powershell (exit 0)

```
Get-Content books.ndjson | ConvertFrom-Json | ForEach-Object body | Sort-Object price | Format-Table price, title
```

Output:

```

price   title                                
-----   -----                                
Â£47.82 Sharp Objects                        
Â£50.10 Soumission                           
Â£51.77 A Light in the Attic                 
Â£53.74 Tipping the Velvet                   
Â£54.23 Sapiens: A Brief History of Humankind
```

## ndjson-51 / powershell (exit 0)

```
Get-Content books.ndjson -Encoding UTF8 | ConvertFrom-Json | ForEach-Object body | Sort-Object price | Format-Table price, title
```

Output:

```

price  title                                
-----  -----                                
£47.82 Sharp Objects                        
£50.10 Soumission                           
£51.77 A Light in the Attic                 
£53.74 Tipping the Velvet                   
£54.23 Sapiens: A Brief History of Humankind
```

## noclobber / pwsh (exit 0)

```
"oops" | Out-File notes.txt -NoClobber
Get-Content notes.txt
```

Output:

```
Out-File: The file '~/practice\notes.txt' already exists.
hello
world
```

## noclobber / powershell (exit 0)

```
"oops" | Out-File notes.txt -NoClobber
Get-Content notes.txt
```

Output:

```

hello
world
Out-File : The file '~/practice\notes.txt' already 
exists.
At line:1 char:10
+ "oops" | Out-File notes.txt -NoClobber
+          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ResourceExists: (C:\Users\runner...zs7hd\notes.txt:String) [Out-File], IOException
    + FullyQualifiedErrorId : NoClobber,Microsoft.PowerShell.Commands.OutFileCommand
 
```

## path / pwsh (exit 0)

```
$env:PATH -split ';'
```

Output:

```
C:\pwsh76
C:\Windows\system32
C:\Windows
C:\Windows\System32\Wbem
C:\Windows\System32\WindowsPowerShell\v1.0
C:\Windows\System32\OpenSSH
C:\pwsh76
~\AppData\Local\Microsoft\WindowsApps
```

## path / powershell (exit 0)

```
$env:PATH -split ';'
```

Output:

```
C:\Windows\system32
C:\Windows
C:\Windows\System32\Wbem
C:\Windows\System32\WindowsPowerShell\v1.0
C:\Windows\System32\OpenSSH
C:\pwsh76
~\AppData\Local\Microsoft\WindowsApps
```

## path / cmd (exit 0)

```
echo %PATH:;=&echo.%
```

Output:

```
C:\Windows\system32
C:\Windows
C:\Windows\System32\Wbem
C:\Windows\System32\WindowsPowerShell\v1.0
C:\Windows\System32\OpenSSH
C:\pwsh76
~\AppData\Local\Microsoft\WindowsApps
```

## pipe / pwsh (exit 0)

```
Select-String -Path log.txt -Pattern ERROR | Measure-Object | Select-Object -ExpandProperty Count
```

Output:

```
2
```

## pipe / powershell (exit 0)

```
Select-String -Path log.txt -Pattern ERROR | Measure-Object | Select-Object -ExpandProperty Count
```

Output:

```

2
```

## pipe / cmd (exit 0)

```
findstr ERROR log.txt | find /c /v ""
```

Output:

```
2
```

## pipe-objects / pwsh (exit 0)

```
Get-ChildItem *.txt | Sort-Object Length -Descending | Select-Object -First 3 Name, Length
```

Output:

```

Name      Length
----      ------
log.txt      222
names.txt     33
notes.txt     12

```

## pipe-objects / powershell (exit 0)

```
Get-ChildItem *.txt | Sort-Object Length -Descending | Select-Object -First 3 Name, Length
```

Output:

```

Name      Length
----      ------
log.txt      222
names.txt     33
notes.txt     12
```

## quote-json / pwsh (exit 0)

```
curl.exe -s https://httpbin.org/anything --json '{"title":"h1"}' | Select-String '"data"'
```

Output:

```

  "data": "{\"title\":\"h1\"}", 

```

## quote-json / powershell (exit 0)

```
curl.exe -s https://httpbin.org/anything --json '{"title":"h1"}' | Select-String '"data"'
```

Output:

```

  "data": "{title:h1}", 
```

## quote-json / cmd (exit 0)

```
curl -s https://httpbin.org/anything --json '{"title":"h1"}' | findstr /c:"data"
curl -s https://httpbin.org/anything --json "{\"title\":\"h1\"}" | findstr /c:"data"
```

Output:

```
  "data": "'{title:h1}'", 
  "data": "{\"title\":\"h1\"}", 
```

## quote-url / pwsh (exit 0)

```
curl.exe -s "https://httpbin.org/anything?q=cli&page=2" | Select-String '"page"', '"q"'
```

Output:

```

    "page": "2", 
    "q": "cli"

```

## quote-url / powershell (exit 0)

```
curl.exe -s "https://httpbin.org/anything?q=cli&page=2" | Select-String '"page"', '"q"'
```

Output:

```

    "page": "2", 
    "q": "cli"
```

## quote-url / cmd (exit 0)

```
curl -s "https://httpbin.org/anything?q=cli&page=2" | findstr /c:"page" /c:"\"q\""
```

Output:

```
    "page": "2", 
    "q": "cli"
  "url": "https://httpbin.org/anything?q=cli&page=2"
```

## quotes / pwsh (exit 0)

```
'Home is $HOME'
"Home is $HOME"
```

Output:

```
Home is $HOME
Home is ~
```

## quotes / powershell (exit 0)

```
'Home is $HOME'
"Home is $HOME"
```

Output:

```
Home is $HOME
Home is ~
```

## quotes / cmd (exit 0)

```
echo 'Home is %USERPROFILE%'
echo "Home is %USERPROFILE%"
```

Output:

```
'Home is ~'
"Home is ~"
```

## redirect / pwsh (exit 0)

```
Get-ChildItem notes.txt, missing.txt -Name > out.txt 2> errors.txt
Get-Content out.txt
Get-Content errors.txt
"first" > report.txt
"second" >> report.txt
Get-Content report.txt
```

Output:

```
notes.txt
Get-ChildItem: Cannot find path '~/practice\missing.txt' because it does not exist.
first
second
```

## redirect / powershell (exit 0)

```
Get-ChildItem notes.txt, missing.txt -Name > out.txt 2> errors.txt
Get-Content out.txt
Get-Content errors.txt
"first" > report.txt
"second" >> report.txt
Get-Content report.txt
```

Output:

```

notes.txt
Get-ChildItem : Cannot find path 
'~/practice\missing.txt' because it does not exist.
At line:1 char:1
+ Get-ChildItem notes.txt, missing.txt -Name > out.txt 2> errors.txt
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (C:\Users\runner...ibx\missing.txt:String) [Get-ChildItem], ItemNotFound 
   Exception
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand
 
first
second
```

## redirect / cmd (exit 0)

```
dir /b notes.txt missing.txt > out.txt 2> errors.txt
type out.txt
type errors.txt
echo first> report.txt
echo second>> report.txt
type report.txt
```

Output:

```
notes.txt
first
second
```

## redirect-encoding / pwsh (exit 0)

```
"hi" > hi.txt
[System.IO.File]::ReadAllBytes("$PWD\hi.txt") -join ' '
```

Output:

```
104 105 13 10
```

## redirect-encoding / powershell (exit 0)

```
"hi" > hi.txt
[System.IO.File]::ReadAllBytes("$PWD\hi.txt") -join ' '
```

Output:

```

255 254 104 0 105 0 13 0 10 0
```

## register-task / pwsh (exit 0)

```
$action  = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-File `"$PWD\hello.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 8am
Register-ScheduledTask -TaskName "HelloScript" -Action $action -Trigger $trigger | Select-Object TaskName, State
Unregister-ScheduledTask -TaskName "HelloScript" -Confirm:$false
```

Output:

```

TaskName    State
--------    -----
HelloScript Ready

```

## schtasks / cmd (exit 0)

```
schtasks /create /tn "HelloScript" /tr "\"%CD%\hello.cmd\"" /sc daily /st 08:00 /f
schtasks /query /tn "HelloScript"
schtasks /delete /tn "HelloScript" /f
```

Output:

```
SUCCESS: The scheduled task "HelloScript" has successfully been created.

Folder: \
TaskName                                 Next Run Time          Status         
======================================== ====================== ===============
HelloScript                              10/11/2026 8:00:00 AM  Ready          
SUCCESS: The scheduled task "HelloScript" was successfully deleted.
```

## script-pwsh / pwsh (exit 0)

```
hello.ps1
.\hello.ps1
```

Output:

```
hello.ps1: The term 'hello.ps1' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
Hello from PowerShell
```

## script-pwsh / powershell (exit 0)

```
hello.ps1
.\hello.ps1
```

Output:

```

Hello from PowerShell
hello.ps1 : The term 'hello.ps1' is not recognized as the name of a cmdlet, function, script file, or operable 
program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
At line:1 char:1
+ hello.ps1
+ ~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (hello.ps1:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
```

## script-pwsh / cmd (exit 0)

```
hello.cmd
```

Output:

```
Hello from Command Prompt
```

## set-spaces / cmd (exit 0)

```
set GREETING = hello
echo [%GREETING%]
echo [%GREETING %]
```

Output:

```
[]
[ hello]
```

## setx-truncate / pwsh (exit 0)

```
setx LONGVAR ("x" * 1100)
```

Output:

```

WARNING: The data being saved is truncated to 1024 characters.

SUCCESS: Specified value was saved.
```

## setx-truncate / powershell (exit 0)

```
setx LONGVAR ("x" * 1100)
```

Output:

```

WARNING: The data being saved is truncated to 1024 characters.

SUCCESS: Specified value was saved.
```

## whatif / pwsh (exit 0)

```
Remove-Item folder -Recurse -WhatIf
```

Output:

```
What if: Performing the operation "Remove Directory" on target "~/practice\folder".
```

## whatif / powershell (exit 0)

```
Remove-Item folder -Recurse -WhatIf
```

Output:

```

What if: Performing the operation "Remove Directory" on target "~/practice\folder".
```

## which / pwsh (exit 0)

```
Get-Command curl | Format-Table CommandType, Name, Definition -AutoSize
```

Output:

```

CommandType Name     Definition
----------- ----     ----------
Application curl.exe C:\Windows\system32\curl.exe

```

## which / powershell (exit 0)

```
Get-Command curl | Format-Table CommandType, Name, Definition -AutoSize
```

Output:

```

CommandType Name Definition       
----------- ---- ----------       
      Alias curl Invoke-WebRequest
```

## which / cmd (exit 0)

```
where curl
```

Output:

```
C:\Windows\System32\curl.exe
```

## wildcards / pwsh (exit 0)

```
echo *.txt
Get-ChildItem *.txt -Name
```

Output:

```
*.txt
file.txt
log.txt
names.txt
notes.txt
old.txt
```

## wildcards / powershell (exit 0)

```
echo *.txt
Get-ChildItem *.txt -Name
```

Output:

```

*.txt
file.txt
log.txt
names.txt
notes.txt
old.txt
```

## wildcards / cmd (exit 0)

```
echo *.txt
dir /b *.txt
```

Output:

```
*.txt
file.txt
log.txt
names.txt
notes.txt
old.txt
```

# Robocopy Back-up

## Create a folder called Backup (for the below example) in your destination folder

## Back-up command (full)
### Execute the following command in PowerShell to back up a source folder to a destination folder:
'''
(base) PS  C:\...\> Robocopy "C:\path\to\source\folder" "C:\path\to\destination\folder" /E /v /FFT /R:3 /W:10 /Z /MT[:16]
'''

=======================================================
>>> SEE BELOW for how to create an alias that executes the above command
=======================================================

## MAKE A POWERSHELL ALIAS
###
Open a Windows PowerShell window and open your PowerShell profile in notepad:
'''
(base) PS  C:\...\> notepad $profile
'''

### In the notepad:
- Create a function
- Define an alias under the function name

'''
function RobocopyBackupSourceFolder{
Robocopy "C:\path\to\source\folder" "C:\path\to\destination\folder" /E /v /FFT /R:3 /W:10 /Z /MT[:16]
}
Set-Alias backup_SourceFolder RobocopyBackupSourceFolder
'''

### Close notepad

### Restart profile
'''
(base) PS  C:\...\> . $profile
'''

### Now you can type the alias into Windows PowerShell and have it execute the code within your function
'''
(base) PS  C:\...\> backup_SourceFolder
'''

=================================================================
## INFORMATION
=================================================================
/l or /L 	Specifies that files are to be listed only (and not copied, deleted, or time stamped).

/v 	Produces verbose output, and shows all skipped files.

=================================================================

https://superuser.com/questions/814102/robocopy-command-to-do-an-incremental-backup
robocopy C:\source M:\destination /MIR /FFT /R:3 /W:10 /Z /NP /NDL

    The /MIR option (equivalent to /E /PURGE) stands for "mirror" and is the most important option. It regards your source folder as the "master", causing robocopy to copy/mirror any changes in the source (new files, deletions etc.) to the target, which is a useful setting for a backup.

/mir 	Mirrors a directory tree (equivalent to /e plus /purge). Using this option with the /e option and a destination directory, overwrites the destination directory security settings. https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy

/e 	Copies subdirectories. This option automatically includes empty directories. https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy

    /FFT is a very important option, as it allows a 2-second difference when comparing timestamps of files, such that minor clock differences between your computer and your backup device don't matter. This will ensure that only modified files are copied over, even if file modification times are not exactly synchronized.

    /R:3 specifies the number of retries, if the connection should fail, and 
    /W:10 specifies a wait time of 10 seconds between retries. These are useful options when doing the backup over a network.

    /Z copies files in "restart mode", so partially copied files can be continued after an interruption.

    /NP and /NDL suppress some debug output, you can additionally add /NS, /NC, /NFL to further reduce the amount of output (see the documentation for details). However, I would suggest to print some debug output during the first runs, to make sure everything is working as expected.

If you really want to keep files that exist on the destination, but not on the source side, simply replace the /MIR option with /E. However, I would strongly suggest to use /MIR when you want to use the destination for incremental backups. Otherwise any files that have been renamed or moved at the source will clutter up the destination, meaning you get duplicates. I usually create a subfolder "backup" on the destination which contains a 1:1 copy of my source folder tree. That way you can still keep around historical files next to the backup folder and remove or reorganize them safely later on.

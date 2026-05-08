---
title: "Linux Commands Cheat Sheet: 50 Commands Every Developer Should Know"
description: "A practical Linux command reference organized by task — file operations, process management, networking, permissions, and text processing. Bookmark this."
date: 2026-05-07
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/linux-commands.html
---

# Linux Commands Cheat Sheet: 50 Commands Every Developer Should Know

A good Linux command-line reference isn't nice to have — it's essential. This cheatsheet covers 50 commands organized by what you're actually trying to do, from file navigation to process management to networking.

## File Navigation
    
    
    pwd                     # print working directory
    ls -la                  # list all files with details
    cd /path/to/dir         # change directory
    cd ..                   # go up one level
    cd -                    # go back to previous directory
    find . -name "*.py"     # find files by name pattern
    locate filename         # find file quickly (uses indexed db)

## File Operations
    
    
    cp source dest          # copy file
    cp -r source dest       # copy directory recursively
    mv source dest          # move or rename
    rm file                 # remove file
    rm -rf dir              # remove directory (DANGER — no undo)
    mkdir -p a/b/c          # create nested directories
    touch file              # create empty file or update timestamp
    ln -s target link       # create symbolic link

## Viewing and Editing Files
    
    
    cat file                # print entire file
    less file               # scroll through file (q to quit)
    head -20 file           # first 20 lines
    tail -f file            # follow file as it grows (logs)
    wc -l file              # count lines
    grep "pattern" file     # search for pattern
    grep -r "pattern" dir   # search recursively
    nano file               # simple terminal editor
    vim file                # advanced editor (:q! to quit)

## Permissions
    
    
    chmod 755 script.sh     # rwxr-xr-x (owner full, others read+execute)
    chmod +x script.sh      # make executable
    chown user:group file   # change owner and group
    umask 022               # set default permissions mask

## Process Management
    
    
    ps aux                  # list all running processes
    ps aux | grep nginx     # find specific process
    top                     # real-time process monitor (q to quit)
    htop                    # prettier top (install separately)
    kill 1234               # terminate process by PID
    kill -9 1234            # force kill (SIGKILL)
    pkill -f pattern        # kill by name pattern
    bg                      # resume suspended job in background
    fg                      # bring background job to foreground
    jobs                    # list background jobs

## Disk and Storage
    
    
    df -h                   # disk free (human-readable)
    du -sh dir              # directory size summary
    du -sh * | sort -h      # size of each item, sorted
    mount                   # show mounted filesystems
    lsblk                   # list block devices

## Networking
    
    
    ping host               # test connectivity
    curl -I url             # fetch headers only
    curl -s url | jq        # fetch JSON and pretty-print
    wget url                # download file
    ssh user@host           # connect to remote server
    scp file user@host:path # copy file to remote
    netstat -tlnp           # listening ports
    ss -tlnp                # modern alternative to netstat
    lsof -i :3000           # what's using port 3000

## Text Processing
    
    
    sed 's/old/new/g' file  # replace all occurrences
    awk '{{print $1}}' file  # print first column
    sort file               # sort lines
    sort -u file            # sort and deduplicate
    uniq -c file            # count occurrences
    cut -d',' -f1 file      # extract column 1 from CSV
    tr '[:lower:]' '[:upper:]' # convert case

## Compression and Archives
    
    
    tar -czf archive.tar.gz dir   # create gzipped tarball
    tar -xzf archive.tar.gz       # extract gzipped tarball
    gzip file                     # compress single file
    gunzip file.gz                # decompress
    zip -r archive.zip dir        # create zip

## System Info
    
    
    uname -a                # kernel info
    whoami                  # current user
    who                     # who is logged in
    uptime                  # how long system has been up
    free -h                 # memory usage
    date                    # current date/time
    history                 # command history
    !!                      # re-run last command
    !$                      # last argument of previous command

## Quick Reference by Task

Task| Command  
---|---  
Find large files| `find . -type f -size +100M`  
Search in files| `grep -rn "TODO" .`  
Count files in directory| `ls -1 | wc -l`  
See disk usage of all mounts| `df -h`  
Check if a port is open| `nc -zv host 443`  
Watch command output every 2s| `watch -n 2 command`  
Create alias permanently| `echo 'alias ll="ls -la"' >> ~/.bashrc`

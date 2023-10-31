# CS2 FastDL: Fast Download Utility for Counter Strike 2 Custom Content

![cs2fastdl](https://i.imgur.com/rHGCKo9.png)

This is a proof of concept app and will be turned into something more user friendly for clients. The point of this is to nail the functionality first. Im aware of some other "solutions" out there but they're not well though out for different server setups, outright dangerous or gate-keepy.  

CS2 FastDL is an app designed to streamline the downloading of custom content for Counter Strike 2. This will allow you to join servers with custom maps and models. It ensures that users only download the necessary updated files, saving time and bandwidth. The app comes with a simple graphical user interface (GUI) for ease of use. You can add any servers you want as long as they have a .txt with all the files they want you to download. (A list of current servers are here). Unlike other solutions, there is 0 risk of getting banned as this app runs entirely seperatly to the game. 

## How It Works

CS2 FastDL retrieves a list of file URLs from a specified `.txt` file hosted online. For each URL, the program checks if the corresponding file exists locally. If it does, the script compares the local and remote versions of the file. If the files differ, the script downloads the remote file, ensuring users always have the most up-to-date content.

## Features

- **Fast Downloads**: Only downloads files that don't exist locally or have updates on the server.
- **Direct Play**: Launch CS2 with the required parameters for custom content.
- **Robust Error Handling**: Gracefully handles common network issues and skips invalid URLs, ensuring that the download process continues uninterrupted.
- **User-Friendly Interface**: Provides a GUI that shows the download progress for each file, making it easy to track the status of each download.

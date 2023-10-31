# CS2 FastDL: Fast Download Utility for Counter Strike 2 Custom Content

![cs2fastdl](https://i.imgur.com/rHGCKo9.png)

This is a proof of concept app and will be turned into something more user friendly for clients. The point of this is to nail the functionality first. Im aware of some other "solutions" out there but they're not well though out for different server setups, outright dangerous or gate-keepy.  

CS2 FastDL is an app designed to streamline the downloading of custom content for Counter Strike 2. This will allow you to join servers with custom maps and models. It ensures that users only download the necessary updated files, saving time and bandwidth. The app comes with a simple graphical user interface (GUI) for ease of use. You can add any servers you want as long as they have a .txt with all the files they want you to download. (A list of current servers are here). Unlike other solutions, there is 0 risk of getting banned as this app runs entirely seperatly to the game. 

## How It Works

CS2 FastDL fixes some of the shortcomings from existing fastdl setups.  

- Server owners only need to upload a `.txt` file with all the URLs they want a client to download. This means your FastDL server can still remain private and not get rate limited from requests.
- As assets dont really change that much compared to maps, you can bundle all character models into a single `assets.zip` to make downloading to clients way faster. Most asset packs are only around 500mb to 1gb so this makes sense.
- CS2 FastDL will read and store the timestamp of when the `.txt` was last updated, if it has changed it will trigger an update.
- It DOESNT stay running in the background, all the maps are downloaded at once as not to interupt users gameplay. 

## Features

- **Fast Downloads**: Only downloads files that don't exist locally or have updates on the server.
- **Direct Play**: Launch CS2 with the required parameters for custom content.
- **Any Platform**: It works with any platform or OS.
- **Supports Multi Part Downloading**: Routing problems are no longer an issue and players should always get the fastest speed possible.
- **Robust Error Handling**: Gracefully handles common network issues and skips invalid URLs, ensuring that the download process continues uninterrupted.
- **User-Friendly Interface**: Provides a GUI that shows the download progress for each file, making it easy to track the status of each download.

## TODO

- **Companion Script**: Automatically prepare and upload files from your game server to your FastDL host or folder.
- **Pretty GUI**: Make it so its extremly easy to use and navigate for the most noob players.

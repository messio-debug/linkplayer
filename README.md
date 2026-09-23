# LinkPlayer (Arch linux)

A small Python/Tkinter desktop GUI for opening supported video links in mpv and saving accessible streams with yt-dlp. **Shhh....** put links and watch no ads no bad quality,
Very fast working 
Lightweight program with lightweight GUI 

**Soon** will be able on more operating systems 

## Arch Linux

Install the runtime tools:

```sh
sudo pacman -S python tk mpv yt-dlp ffmpeg
```

Run `./install.sh` from this folder to install LinkPlayer and create its application menu entry automatically. If needed, make the script executable first with `chmod +x install.sh`. Then find **LinkPlayer** in your desktop environment's app menu. Run `./uninstall.sh` to remove the app and menu entry.

## Build an Arch package

To build and install an Arch package from this source folder, run:

```sh
makepkg -si
```

This builds and installs `linkplayer` with pacman, including its dependencies and system-wide app menu entry. Anyone can install it from the public repository with:

```sh
git clone https://github.com/messio-debug/linkplayer.git
cd linkplayer
makepkg -si
```

Use **Play link** to open the URL in mpv. Use **Download** to save it in the selected folder (Videos by default). Quality selection applies to both actions. yt-dlp supports many public video sites, but site support can change. This app does not bypass DRM; use the service's official offline feature for protected streams.

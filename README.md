# 🎬 Letterboxd Wallpaper Downloader

A simple desktop app to download high-resolution (up to 4K) movie wallpapers straight from your Letterboxd CSV exports using the TMDb API.

---
<img width="1365" height="768" alt="example" src="https://github.com/user-attachments/assets/72999a17-4db0-4883-93a4-642314ff5696" />


## 📋 Requirements

Before running the app, you will need:
1. **Your Letterboxd data export** (`.csv` file).
2. **A free TMDb API key** (to fetch high-quality backdrops).


#### 📥 How to Export Your Data from Letterboxd

1. Log in to [Letterboxd](https://letterboxd.com/).
2. Go to [Export data](https://letterboxd.com/settings/data/).
3. Click **Export Your Data**.
4. Unzip the downloaded file. You can use `watched.csv`, `ratings.csv`, or any movie list CSV export with this app.

#### 🔑 How to Get a Free TMDb API Key

1. Create a free account at [The Movie Database (TMDb)](https://www.themoviedb.org/).
2. Go to [API settings](https://www.themoviedb.org/settings/api)
3. Select **API** from the left navigation menu.
4. Click **Create** under the *Request an API Key* section and choose **Developer**.
5. Accept the terms and fill in the brief form (you can put "Personal Use" for application name/URL).
6. Copy your **API Key (v3 auth)** once generated.

---

## 🚀 How to Run

1. Go to the **Releases** section on the right side of this repository.
2. Download `LetterboxdWallpaperDownloader.exe` (or the executable if you are in linux).
3. Double-click to launch the app.
4. Select your Letterboxd `.csv` file and paste your TMDb API Key.
5. Click **Start Download**.


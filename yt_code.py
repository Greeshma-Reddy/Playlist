import requests
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

API_BASE_URL = 'https://mock-youtube-api-f3d0c17f0e38.herokuapp.com/api'
DATA_FILE = 'playlists.json'

def fetch_videos(page=1):
    response = requests.get(f'{API_BASE_URL}/videos?page={page}')
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", "Failed to fetch videos")
        return None

def display_videos(videos, text_widget):
    for video in videos:
        text_widget.insert(tk.END, f"ID: {video['id']}\n")
        text_widget.insert(tk.END, f"Title: {video['title']}\n")
        text_widget.insert(tk.END, f"Video ID: {video['video_id']}\n")
        text_widget.insert(tk.END, f"Views: {video['views']}\n")
        text_widget.insert(tk.END, f"Likes: {video['likes']}\n")
        text_widget.insert(tk.END, f"Comments: {video['comments']}\n")
        text_widget.insert(tk.END, f"Description: {video['description']}\n")
        text_widget.insert(tk.END, f"Thumbnail: {video['thumbnail_url']}\n")
        text_widget.insert(tk.END, f"Created At: {video['created_at']}\n")
        text_widget.insert(tk.END, f"Updated At: {video['updated_at']}\n\n")

def search_videos(videos, query):
    return [video for video in videos if query.lower() in video['title'].lower()]

def create_playlist(playlists, name):
    if name in playlists:
        messagebox.showinfo("Info", f'Playlist "{name}" already exists.')
    else:
        playlists[name] = []
        messagebox.showinfo("Info", f'Playlist "{name}" created.')

def add_video_to_playlist(playlists, playlist_name, video):
    if playlist_name in playlists:
        playlists[playlist_name].append(video)
        messagebox.showinfo("Info", f'Added video "{video["title"]}" to playlist "{playlist_name}".')
    else:
        messagebox.showerror("Error", f'Playlist "{playlist_name}" does not exist.')

def remove_video_from_playlist(playlists, playlist_name, video_id):
    if playlist_name in playlists:
        playlists[playlist_name] = [video for video in playlists[playlist_name] if video['video_id'] != video_id]
        messagebox.showinfo("Info", f'Removed video with ID "{video_id}" from playlist "{playlist_name}".')
    else:
        messagebox.showerror("Error", f'Playlist "{playlist_name}" does not exist.')

def display_playlist(playlists, playlist_name, text_widget):
    if playlist_name in playlists:
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, f'Playlist: {playlist_name}\n\n')
        display_videos(playlists[playlist_name], text_widget)
    else:
        messagebox.showerror("Error", f'Playlist "{playlist_name}" does not exist.')

def display_all_playlists(playlists, text_widget):
    text_widget.delete('1.0', tk.END)
    if playlists:
        for playlist_name, videos in playlists.items():
            text_widget.insert(tk.END, f'Playlist: {playlist_name}\n\n')
            display_videos(videos, text_widget)
    else:
        text_widget.insert(tk.END, "No playlists created.\n")

def save_playlists(playlists):
    with open(DATA_FILE, 'w') as file:
        json.dump(playlists, file)
    messagebox.showinfo("Info", "Playlists saved.")

def load_playlists():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

class VideoPlaylistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Playlist App")

        self.playlists = load_playlists()
        self.current_page = 1

        self.create_widgets()

    def create_widgets(self):
        # Create buttons
        self.btn_fetch = ttk.Button(self.root, text="Fetch and display videos", command=self.fetch_and_display_videos)
        self.btn_search = ttk.Button(self.root, text="Search videos", command=self.search_and_display_videos)
        self.btn_create_playlist = ttk.Button(self.root, text="Create a playlist", command=self.create_playlist)
        self.btn_add_to_playlist = ttk.Button(self.root, text="Add a video to a playlist", command=self.add_to_playlist)
        self.btn_remove_from_playlist = ttk.Button(self.root, text="Remove a video from a playlist", command=self.remove_from_playlist)
        self.btn_display_playlist = ttk.Button(self.root, text="Display a playlist", command=self.display_playlist)
        self.btn_display_all_playlists = ttk.Button(self.root, text="Display all playlists", command=self.display_all_playlists)
        self.btn_next_page = ttk.Button(self.root, text="Next page", command=self.next_page)
        self.btn_prev_page = ttk.Button(self.root, text="Previous page", command=self.prev_page)
        self.btn_save_playlists = ttk.Button(self.root, text="Save playlists", command=self.save_playlists)
        self.btn_exit = ttk.Button(self.root, text="Exit", command=self.root.quit)

        # Create text widget for displaying videos and playlists
        self.text_display = ScrolledText(self.root, wrap='word', width=80, height=20)

        # Arrange buttons and text widget in the window
        self.btn_fetch.grid(row=0, column=0, pady=5)
        self.btn_search.grid(row=1, column=0, pady=5)
        self.btn_create_playlist.grid(row=2, column=0, pady=5)
        self.btn_add_to_playlist.grid(row=3, column=0, pady=5)
        self.btn_remove_from_playlist.grid(row=4, column=0, pady=5)
        self.btn_display_playlist.grid(row=5, column=0, pady=5)
        self.btn_display_all_playlists.grid(row=6, column=0, pady=5)
        self.btn_next_page.grid(row=7, column=0, pady=5)
        self.btn_prev_page.grid(row=8, column=0, pady=5)
        self.btn_save_playlists.grid(row=9, column=0, pady=5)
        self.btn_exit.grid(row=10, column=0, pady=5)

        self.text_display.grid(row=0, column=1, rowspan=11, padx=10, pady=10)

    def fetch_and_display_videos(self):
        data = fetch_videos(self.current_page)
        if data:
            self.text_display.delete('1.0', tk.END)
            display_videos(data['videos'], self.text_display)

    def search_and_display_videos(self):
        query = simpledialog.askstring("Search", "Enter search query:")
        if query:
            data = fetch_videos(self.current_page)
            if data:
                videos = search_videos(data['videos'], query)
                self.text_display.delete('1.0', tk.END)
                display_videos(videos, self.text_display)

    def create_playlist(self):
        name = simpledialog.askstring("Create Playlist", "Enter playlist name:")
        if name:
            create_playlist(self.playlists, name)

    def add_to_playlist(self):
        self.display_all_playlists()
        name = simpledialog.askstring("Add to Playlist", "Enter playlist name:")
        video_id = simpledialog.askstring("Add to Playlist", "Enter video ID:")
        if name and video_id:
            data = fetch_videos(self.current_page)
            if data:
                video = next((video for video in data['videos'] if video['video_id'] == video_id), None)
                if video:
                    add_video_to_playlist(self.playlists, name, video)

    def remove_from_playlist(self):
        self.display_all_playlists()
        name = simpledialog.askstring("Remove from Playlist", "Enter playlist name:")
        video_id = simpledialog.askstring("Remove from Playlist", "Enter video ID:")
        if name and video_id:
            remove_video_from_playlist(self.playlists, name, video_id)

    def display_playlist(self):
        self.display_all_playlists()
        name = simpledialog.askstring("Display Playlist", "Enter playlist name:")
        if name:
            display_playlist(self.playlists, name, self.text_display)

    def display_all_playlists(self):
        display_all_playlists(self.playlists, self.text_display)

    def next_page(self):
        self.current_page += 1
        self.fetch_and_display_videos()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
        self.fetch_and_display_videos()

    def save_playlists(self):
        save_playlists(self.playlists)

if __name__ == '__main__':
    root = tk.Tk()
    app = VideoPlaylistApp(root)
    root.mainloop()

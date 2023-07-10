from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
from models import db, connect_db, Playlist, Song, PlaylistSong

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Set to False to suppress warnings
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Initialize database
db.init_app(app)
connect_db(app)
db.create_all()

# Debug Toolbar
app.debug = False
toolbar = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""
    return redirect("/playlists")


# Playlist routes
@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show details of a specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    songs = playlist.songs
    return render_template("playlist.html", playlist=playlist, songs=songs)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form."""
    form = PlaylistForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        playlist = Playlist(name=name, description=description)
        db.session.add(playlist)
        db.session.commit()
        return redirect("/playlists")
    return render_template("add_playlist.html", form=form)


# Song routes
@app.route("/songs")
def show_all_songs():
    """Show a list of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Show details of a specific song."""
    song = Song.query.get_or_404(song_id)
    return render_template("song.html", song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form."""
    form = SongForm()
    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data
        song = Song(title=title, artist=artist)
        db.session.add(song)
        db.session.commit()
        return redirect("/songs")
    return render_template("add_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist and redirect to playlist details."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()
    available_songs = Song.query.filter(~Song.playlists.any(id=playlist_id)).all()
    form.song.choices = [(str(song.id), f"{song.title} - {song.artist}") for song in available_songs]
    if form.validate_on_submit():
        song_ids = [int(song_id) for song_id in form.song.data] if isinstance(form.song.data, list) else [int(form.song.data.id)]

        for song_id in song_ids:
            song = Song.query.get_or_404(song_id)
            playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song.id)
            db.session.add(playlist_song)
        db.session.commit()
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)


if __name__ == "__main__":
    app.run()






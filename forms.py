from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import Playlist, Song


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField("Name", validators=[InputRequired(), Length(max=100)])
    description = TextAreaField("Description")

    
class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    artist = StringField("Artist", validators=[InputRequired(), Length(max=100)])


class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = QuerySelectField('Song To Add', query_factory=lambda: Song.query.all())





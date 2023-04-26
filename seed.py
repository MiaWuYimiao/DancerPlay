from models import User, FavPlaylist, Playlist, Music, PlaylistMusic, db
from app import app

app.app_context().push()
# Create musics table
db.drop_all()
db.create_all()

Music.query.delete()

# Add sample musics
music1 = Music(title="BLACKPINK - ‘Shut Down’ M/V", 
                genre="Song", 
                type="Pop",
                length=180,
                videoId="POe9SOEKotk",
                image_url="https://i.ytimg.com/vi/POe9SOEKotk/mqdefault.jpg")

music2 = Music(title="BLACKPINK - ‘Shut Down’ (Official Audio)", 
                genre="Song", 
                type="Pop",
                length=180,
                videoId="JDRyqUx1X8M",
                image_url="https://i.ytimg.com/vi/JDRyqUx1X8M/mqdefault.jpg")

music3 = Music(title="BLACKPINK - ‘Shut Down’ DANCE PERFORMANCE VIDEO", 
                genre="Song", 
                type="Pop",
                length=180,
                videoId="PjrAwC4TIPA",
                image_url="https://i.ytimg.com/vi/PjrAwC4TIPA/mqdefault.jpg")

db.session.add_all([music1, music2, music3])
db.session.commit()
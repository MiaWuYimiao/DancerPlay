from models import User, FavPlaylist, Playlist, Music, PlaylistMusic, db
from app import app

app.app_context().push()
# Create musics table
db.drop_all()
db.create_all()

Music.query.delete()

# Add sample musics
music1 = Music(title="PLIES II (BARRE) - Music for Ballet II - Marco Sala", 
                style="Ballet", 
                type="Barre",
                videoId="GIdw6UZAbaA",
                image_url="https://i.ytimg.com/vi/GIdw6UZAbaA/hqdefault.jpg")

music2 = Music(title="Music for Ballet Class. Grand Battement", 
                style="Ballet", 
                type="Barre",
                videoId="WjofTNdRNY4",
                image_url="https://i.ytimg.com/vi/WjofTNdRNY4/hqdefault.jpg")

music3 = Music(title="Plié | Ballet Class Music for Children&#39;s Ballet Classes | Barre Music for Kids Ballet Class", 
                style="Ballet", 
                type="Barre",
                videoId="gmeptTwDkY0",
                image_url="https://i.ytimg.com/vi/gmeptTwDkY0/hqdefault.jpg")

db.session.add_all([music1, music2, music3])
db.session.commit()
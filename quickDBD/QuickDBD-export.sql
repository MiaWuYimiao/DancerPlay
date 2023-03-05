-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "User" (
    "UserID" int   NOT NULL,
    "Name" string   NOT NULL,
    "Fav_type" string   NOT NULL,
    "User_name" string   NOT NULL,
    "Password" string   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "UserID"
     )
);

CREATE TABLE "Music" (
    "MusicID" int   NOT NULL,
    "Length" time   NOT NULL,
    "Youtube_url" url   NOT NULL,
    "Type" string   NOT NULL,
    "Title" string   NOT NULL,
    "Genre" string   NOT NULL,
    CONSTRAINT "pk_Music" PRIMARY KEY (
        "MusicID"
     )
);

CREATE TABLE "Playlist" (
    "PlaylistID" int   NOT NULL,
    "Length" time   NOT NULL,
    "Name" string   NOT NULL,
    "Type" string   NOT NULL,
    "Image_url" url   NOT NULL,
    CONSTRAINT "pk_Playlist" PRIMARY KEY (
        "PlaylistID"
     )
);

CREATE TABLE "Fav_Playlist" (
    "FavPlaylistID" int   NOT NULL,
    "UserID" int   NOT NULL,
    "PlaylistID" int   NOT NULL,
    CONSTRAINT "pk_Fav_Playlist" PRIMARY KEY (
        "FavPlaylistID"
     )
);

CREATE TABLE "Playlist_Music" (
    "PlaylistMusicID" int   NOT NULL,
    "MusicID" int   NOT NULL,
    "PlaylistID" int   NOT NULL,
    CONSTRAINT "pk_Playlist_Music" PRIMARY KEY (
        "PlaylistMusicID"
     )
);

ALTER TABLE "Fav_Playlist" ADD CONSTRAINT "fk_Fav_Playlist_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

ALTER TABLE "Fav_Playlist" ADD CONSTRAINT "fk_Fav_Playlist_PlaylistID" FOREIGN KEY("PlaylistID")
REFERENCES "Playlist" ("PlaylistID");

ALTER TABLE "Playlist_Music" ADD CONSTRAINT "fk_Playlist_Music_MusicID" FOREIGN KEY("MusicID")
REFERENCES "Music" ("MusicID");

ALTER TABLE "Playlist_Music" ADD CONSTRAINT "fk_Playlist_Music_PlaylistID" FOREIGN KEY("PlaylistID")
REFERENCES "Playlist" ("PlaylistID");

CREATE INDEX "idx_User_Name"
ON "User" ("Name");


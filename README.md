# Spotify Splicer

Takes a list of playlists and creates a new playlist with the contents spliced. 

## Environment Variables

`SPOTIPY_CLIENT_ID` - Spotify Client ID

`SPOTIPY_CLIENT_SECRET` - Spotify Client Token

`SPOTIPY_REDIRECT_URI` - Application Redirect URL


## Endpoints

POST /splice

```
{
    "name" : "new playlist name",
    "playlists": [
        {
            "id": "37i9dQZF1DXbwQ8tw5iAdu",
            "shuffle": false
        }, {
            "id": "37i9dQZF1DX2sUQwD7tbmL",
            "shuffle: true
        }
    ]
}
```
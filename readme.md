# spotidal2u
An app threesome that offers you love.
Improves your quality of life transferring your spotify playlists to tidal platform.
Smooth the capitalistic rivalry and monopoly that rules music streaming platforms.


## steps
- fetch your spotify playlists data (choose which playlists you want)
- search each track in tidal and saves to a same-name playlist
- get a log of not found tracks

## todos
- search for not found tracks individually
- download playlist tracks
- upgrade textual ui




## working scripts
- run menu.py
- fetch spotify playlists `apps\sync_playlists\src\fetch_sp_playlists.py` - relocated to spotify.py
    it saves new:
        user_playlists.json (raw spotify response)
        playlists_list.json (just playlists names and ids)
- select playlists: `apps\sync_playlists\src\select_playlists.py`
- search and save to tidal: `apps\sync_playlists\src\save_to_tidal.py` - or in utils.py sync_playlist(sp_playlist_id)

we are working in sync.py at searching a track within a playlist tidal_search()
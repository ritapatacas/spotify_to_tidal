import sys
import spotipy as sp_api
import tidalapi as td_api
import webbrowser
from utils import load_credentials, load_session, save_session

__all__ = ["open_spotify_session", "open_tidal_session"]

SPOTIFY_SCOPES = "playlist-read-private, user-library-read"


def open_spotify_session() -> sp_api.Spotify:
    config = load_credentials('sp')
    print(config)
    credentials_manager = sp_api.SpotifyOAuth(
        username=config["username"],
        scope=SPOTIFY_SCOPES,
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        redirect_uri=config["redirect_uri"],
        requests_timeout=2,
    )
    try:
        credentials_manager.get_access_token(as_dict=False)
    except sp_api.SpotifyOauthError:
        sys.exit(
            "> error opening spotify sesion; could not get token for username: ".format(
                config["username"]
            )
        )

    return sp_api.Spotify(oauth_manager=credentials_manager)


def open_tidal_session() -> td_api.Session:
    session = td_api.Session()
    login, future = session.login_oauth()
    print("> login with the webbrowser: " + login.verification_uri_complete)

    url = login.verification_uri_complete
    if not url.startswith("https://"):
        url = "https://" + url
    webbrowser.open(url)
    future.result()
    save_session({
                    "tidal": {
                        "session_id": session.session_id,
                        "token_type": session.token_type,
                        "access_token": session.access_token,
                        "refresh_token": session.refresh_token,
                    }
                })

    return session


def get_td_session() -> td_api.Session:
    previous_session = load_session()
    print("> previous tidal session loaded")

    session = td_api.Session()
    if previous_session:
        try:
            if session.load_oauth_session(
                token_type=previous_session["tidal"]["token_type"],
                access_token=previous_session["tidal"]["access_token"],
                refresh_token=previous_session["tidal"]["refresh_token"],
            ):
                return session
        except Exception as e:
            print("> error loading previous tidal session: \n" + str(e))
    else:
        print("> no previous tidal session found, opening new session")
        open_tidal_session()

# ProMediathek
ProMediathek ist ein Python-Framework zum Herunterladen von Inhalten verschiedener Streaming-Anbieter.
Das Tool ermöglicht den Zugriff auf Filme und Serien von verschiedenen Mediatheken und stellt eine einheitliche Schnittstelle für deren Download bereit.

## Funktionen

- Einheitliche API für verschiedene Streaming-Anbieter
- Unterstützung für Filme und Serien
- Unterstützung für verschiedene Download-Protokolle (Dash, HLS)
- DRM-Unterstützung (Widevine, PlayReady)
- Standard Kommandozeilen-Schnittstelle

## Benutzung
Nach implementierung der Untenstehenden Boilerplate Datei, kann diese direkt benutzen werden.

Beim erstmaliegen ausführen wird eine login datei im ordner "logins" erstellt, wo die eventuell notwendigen Login Informationen eingetragen werden können.


### Für alle Optionen:
```bash
python provider.py --help
```

### Um alle Filme und Serien herunterzuladen:
```bash
python provider.py 
```

### Um alle Filme und Serien aufzulisten:
```bash
python provider.py --list
```

### Um alle Filme und Serien herunterzuladen and nach änderungen bei bereits heruntergeladen zu suchen:
```bash
python provider.py --update
```

### Um ein bestimmtes Video herunterzuladen:
Die ID bekommt man von --list
```bash
python provider.py --download-id <ID>
```


## Boilerplate Provider Datei
```python
from promediathek.baseclass import BaseAPI, BaseProvider
from promediathek.pakete.sammelpaket import MovieSammelpaket, EpisodeSammelpaket, Sammelpaket
from promediathek.download_protocols import Dash
from promediathek.utils.networking import SafeHTTPResponse
from promediathek.downloader import download_cli


class TemplateApi(BaseAPI):
    # TODO change TEMPLATE to provider name
    name = "TEMPLATE"

    def anon_login(self) -> None:
        # TODO optional if anon auth is required.
        self.login_data.last_anon_login_data = "ANON LOGIN DATA"
        raise NotImplementedError

    def login(self) -> None:
        # TODO implement login function and return True if successful.
        self.login_data.last_login_data = "LOGIN DATA"
        raise NotImplementedError

    def prepare_anon_auth(self, **kwargs) -> dict:
        """
        Prepares the anon request data e.g. Headers, Params, Cookies, etc. with the required anon auth data.
        :param kwargs: Optional request data.
        :return: The prepared request data as dict.
        """
        # TODO optional if anon auth is required.
        raise NotImplementedError

    def request_was_anon_authed(self, response: SafeHTTPResponse | dict) -> bool:
        """
        Determines if the request failed because of authentication.
        :param response: The response to check.
        :return: If True, call self._anon_login()
        """
        # TODO optional if anon auth is required.
        raise NotImplementedError

    def prepare_auth(self, **kwargs) -> dict:
        """
        Prepares the request data e.g. Headers, Params, Cookies, etc. with the required auth data.
        :param kwargs: Optional request data.
        :return: The prepared request data as dict.
        """
        # TODO
        raise NotImplementedError

    def request_was_authed(self, response: SafeHTTPResponse | dict) -> bool:
        """
        Determines if the request failed because of authentication.
        Use with auth_get() and auth_post()
        :param response: The response to check.
        :return: If True, call self._login()
        """
        # TODO
        raise NotImplementedError


class TemplateDownloadProtocol(Dash):
    def __init__(self, api: TemplateApi, sammelpaket: Sammelpaket):
        self.api = api
        super().__init__(sammelpaket=sammelpaket)

    def get_manifest_url(self) -> str:
        # TODO implement Function for getting the Dash/HLS manifest url.
        # TODO Optional set required headers/cookies.
        self.request_headers = {}
        self.request_cookies = {}

        raise NotImplementedError

    def _get_drm_keys(self, challenge: bytes | str) -> bytes:
        # TODO send challenge to provider, example ardplus
        url = 'https://token.ardplus.de/token/wv/' + self.sammelpaket.id

        response = self.api.auth_post(url, data=challenge)
        return response.content


class TemplateProvider(BaseProvider):
    api = TemplateApi()

    def check_if_subscribed(self) -> bool:
        # TODO
        raise NotImplementedError

    def search_id(self, search_id: str) -> dict:
        # TODO
        raise NotImplementedError

    def search(self, search_term: str) -> list[Sammelpaket]:
        # TODO: Optional for Speed
        return super().search(search_term)

    def get_all_movies(self) -> list[MovieSammelpaket]:
        # TODO
        movie_pakets = []

        for movie in []:
            movie_pakets.append(MovieSammelpaket(
                type="movie",
                provider=self.name,
                id=movie['id'],
                titel=movie['title'],
                description=movie['shortSynopsis'],
                movie_thumbnail_vertical=movie['poster_url'],
                movie_thumbnail_horizontal=movie['banner_url']
            ))

        return movie_pakets

    def get_all_episodes(self) -> list[EpisodeSammelpaket]:
        # TODO
        episode_pakets = []

        for series in []:
            for season in []:
                for episode in []:
                    episode_pakets.append(EpisodeSammelpaket(
                        type="episode",
                        provider=self.name,
                        id=episode['id'],
                        titel=episode['title'],
                        description=episode['description'],
                        series_thumbnail_vertical=episode['series_poster_url'],
                        series_thumbnail_horizontal=episode['series_banner_url'],
                        series_title=series['title'],
                        series_id=series['id'],
                        series_description=series['description'],
                        season_number=str(season['season_number']),
                        season_id=season['id'],
                        episode_number=str(episode['episode_number']),
                        episode_thumbnail_vertical=None,
                        episode_thumbnail_horizontal=None
                    ))

        return episode_pakets

    def get_downloader(self, sammelpaket: Sammelpaket) -> TemplateDownloadProtocol:
        return TemplateDownloadProtocol(api=self.api, sammelpaket=sammelpaket)


if __name__ == '__main__':
    download_cli(TemplateProvider())
```

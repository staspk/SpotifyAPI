import string
from .random import Random


class OAuth2():
    def generate_state() -> str:
        """
        `state` - an Optional, but strongly recommended param in `OAuth2` `Authorization Code Flow` (prevents cross-site request forgeries. See: `RFC-6749`)

        uses `Random.string` under the hood, `_len` and `_from` set to the ideal params

        **Example:**
        >>> Env.load()
        >>> params = {
            'response_type': 'code',
            'client_id': Env.vars['client_id'],
            'scope': Env.vars['scope'],
            'redirect_uri': Env.vars['redirect_uri'],
            'state': OAuth2.generate_state()
        }
        
        >>> return redirect('https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params))
        """
        _len = 16
        _from = string.ascii_letters+string.digits

        return Random.string(_len, _from)
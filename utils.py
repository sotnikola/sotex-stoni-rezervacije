import logging
import json
from datetime import datetime
import subprocess

TIME_FORMAT = "%H:%M"

def get_logger():
    FORMAT = '[%(asctime)s] %(levelname)-8s %(message)s'
    logging.basicConfig(format=FORMAT,level=logging.INFO)
    return logging.getLogger("reserver")

def is_overlap(range1, range2):
    return (range1[0] < range2[1] and range1[1] > range2[0])

def read_reservations(): 
    with open("facts/reservations.json", "r") as f:
        reservations = json.load(f)
        reservations = [{
            'start': datetime.strptime(reservation['start'], TIME_FORMAT).time(),
            'end': datetime.strptime(reservation['end'], TIME_FORMAT).time(),
            'committer': reservation['committer'],
            'players': reservation['players']
        } for reservation in reservations]
        return reservations


def get_entry(reservation):
    return f"""
        <tr>
            <td>{reservation['start']}</td>
            <td>{reservation['end']}</td>
            <td>{reservation['committer']}</td>
            <td>{reservation['players']}</td>
        </tr>
""".strip()

def create_readme(reservations):
    current_time = datetime.now().time()
    currently_occupied = any([is_overlap((reservation['start'], reservation['end']), (current_time, current_time)) for reservation in reservations])
    return f"""
<h1>Stoni tenis SOTEX rezervacije</h1>

{get_cross() if currently_occupied else get_checkmark()}

<table>
    <thead>
        <th>Početak</th>
        <th>Kraj</th>
        <th>Commiter</th>
        <th>Igrači</th>
    </thead>
    <tbody>{"".join([get_entry(reservation) for reservation in reservations])}</tbody>
</table>
<h3>Poslednji put osveženo: {current_time.strftime(TIME_FORMAT)}</h3>
"""

def get_checkmark():
    return """<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="48" height="48" viewBox="0 0 100 100">
<path fill="#a1d3a2" d="M50 15A35 35 0 1 0 50 85A35 35 0 1 0 50 15Z"></path><path fill="#fefdef" d="M47.5,61.5c-0.481,0-0.964-0.173-1.346-0.521l-12-12c-0.817-0.742-0.877-2.008-0.134-2.825c0.743-0.815,2.007-0.878,2.825-0.134l10.628,10.753l17.653-17.728c0.802-0.758,2.067-0.724,2.827,0.081c0.759,0.803,0.723,2.068-0.081,2.827l-19,19C48.488,61.317,47.994,61.5,47.5,61.5z"></path><path fill="#1f212b" d="M47.5,62c-0.624,0-1.222-0.231-1.683-0.651L33.801,49.333c-0.477-0.432-0.767-1.047-0.798-1.714c-0.031-0.667,0.198-1.307,0.647-1.801c0.93-1.019,2.514-1.092,3.531-0.167l10.293,10.413l17.298-17.371C65.27,38.224,65.92,37.997,66.57,38c0.668,0.019,1.288,0.297,1.747,0.783c0.459,0.485,0.701,1.12,0.682,1.788c-0.019,0.667-0.297,1.288-0.783,1.747l-18.989,18.99C48.75,61.758,48.141,62,47.5,62z M35.509,45.999c-0.409,0-0.82,0.165-1.119,0.493c-0.269,0.296-0.407,0.68-0.388,1.08s0.192,0.769,0.488,1.038l12.018,12.017c0.526,0.477,1.469,0.484,2.022-0.036l18.989-18.99c0.302-0.285,0.469-0.657,0.48-1.058c0.011-0.4-0.134-0.781-0.409-1.072c-0.275-0.292-0.648-0.458-1.049-0.47c-0.392-0.019-0.78,0.133-1.071,0.409L47.828,57.126c-0.094,0.094-0.222,0.147-0.354,0.147h-0.001c-0.133,0-0.261-0.054-0.354-0.148L36.49,46.372C36.215,46.123,35.863,45.999,35.509,45.999z"></path><path fill="#1f212b" d="M50,86c-19.851,0-36-16.149-36-36s16.149-36,36-36s36,16.149,36,36S69.851,86,50,86z M50,16c-18.748,0-34,15.252-34,34s15.252,34,34,34s34-15.252,34-34S68.748,16,50,16z"></path><path fill="#1f212b" d="M65.5 24.227c-.087 0-.175-.022-.255-.07-.638-.377-1.299-.735-1.967-1.065-.247-.123-.349-.422-.227-.67.122-.249.424-.347.67-.227.689.341 1.374.711 2.033 1.102.237.141.316.447.176.685C65.837 24.139 65.671 24.227 65.5 24.227zM68.5 26.25c-.106 0-.213-.034-.304-.103-.322-.247-.65-.486-.983-.72-.226-.159-.281-.47-.122-.696.158-.228.469-.28.696-.123.345.241.683.49 1.017.745.22.167.261.481.094.701C68.799 26.182 68.65 26.25 68.5 26.25z"></path><path fill="#1f212b" d="M50,81c-17.094,0-31-13.907-31-31s13.906-31,31-31c3.668,0,7.259,0.635,10.672,1.886c0.26,0.095,0.393,0.382,0.298,0.642s-0.384,0.393-0.642,0.297C57.025,20.614,53.551,20,50,20c-16.542,0-30,13.458-30,30s13.458,30,30,30s30-13.458,30-30c0-8.439-3.585-16.535-9.836-22.213c-0.205-0.186-0.22-0.502-0.034-0.707c0.187-0.204,0.502-0.219,0.706-0.034C77.296,32.914,81,41.28,81,50C81,67.093,67.094,81,50,81z"></path>
</svg>"""

def get_cross():
    return """<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAKz0lEQVR4nO2X2U9bVx7H8zqZyUMlElWTkCbsmM3GNhgDBozxgrGNMdgswWxhzahV2qRNJ5O0k3QmUltNWmXKdDJR23+j7euo7cM0bUgAG+/7bhPbLGX7js6xwaHjqhLWvHGkj37n/O75Ld9777mWT5w4HsfjeByP4/H/GoGWlt8ZJR1fWeSdSbtKCYe6m+JUq+Ho7oa9WwXiJ1gVXbB1dcEq74S1UwaLTAazjFgptWZipRJYCDJpCqmE+swSCUwEsRgmcQdMHSKsiEQJk0j05TKff+rIAoxC4ZcmqYQ26tRo4NJq4dHp4Onvh3egH56BfrjTc5dOC7c2hUfbBxehrxeu3hTu/TnJ06tJX9Ok1poeOHrU9OaQWjaFApbOTpglYhja2786soAlgSBp6ZTB2aOGR6uFd2gQ/uFhBEZGEBhNEaSMHszJNf+IPnWdWL0+ZUf08OuH0+hpHv/wJfguXYL/0hDN7RkYgFunpeKcRExXF0xiUfLIApabm+mjdvWo4e3XIaAfRmh0BJGJCUQvTyBy+TKik5cRm5xEhHL5wHcAWV8m/v2YFOGJcUTGxxEeH0NodBShsREEichLg/D16+DWaGBXKmCRiHF0AU1NsMqkcGt64BvopwXCY2O0ydjUJGLT01idnsbzmRmszszg+WyamZSP2Pj0NOIH6xm6XiVrYqemEKOiU6JCY6MIkic0OAgPeQoqJcziXAQ0N8EilcLdq0FgaIAKIIVI87TJ2VnE52YRvzKH53NzSFyZo/MUV1I27U+Q9RxZk5g5xF8QG5ueQnRqEpGJcYRG9AgODcGr08KpUsEs7ji6gKVGPqxSCX2F/AP9COn1iE6M0zu3/sUX2I1Gsf7o0UHTCdIYbTYlgDSdTK+Tf7hysIcKmpujsTTH55/TnCR3mJydwUF4tX1wKBUwidpzENDQAJtEDE93N/w6LcL6YUTGxrD+2WfY293D3h6wt7OLjUePkJidpSQJc2n7IqTx9J747CyN2dvZTeXY3aM5o2NjtEaAfNl6NXDK5TC1tuYggMeDpUMEt0oJv1aL0NAQIqMj2AmHsbe3l2FnJyViehrJmRkkZwmzWCONz8wc2ARhejrd/M6hHDuhEGLkMA+nBZDfGqkUK4LmHATU1cEqaodLqYC/rxfBwQFE9Hqszc//TwNUxMOHSExNITE9hcTkZGqeJknETU3RPdlik/PziI6MIEQ+1X198JAfSYkEBj4/BwFcDixtbXDJ5fD1qBHq1yEyNITVkRGsPfg7drd3sLu7l2F7B+sP/4XExDjiExOUxHhqnpyYwPr8P7LGrH36T8RG9IgODSGk08Gv0cBNftnb27HM4+UggMOGqaUFzk4ZfN3dCGr7EB4cQHR4GKv6YSR+UcRDPB8bo8RHR6ld+2Q+697kp58iNjxMc0YGBxHSaeFXq+GUd9Kbt1zHPbqAxVoWTIJmOCVieJUKBHt6aIHowABiQ0OU5McfY3drC7u7uxm2t+lrFtfrKWsPHmTdk5yfx+rwJZonOjiIsE6HoKYHXqUSTqkUJoEAi+zaHAQwa2BuaoSzQwSvXI5AtwohTQ8iWi1iOi1WBwYoyfv3sfPTFnZ2djNsbWPtk0+w9tFHWa8lHzzA6uAgYv39iPb305whjQbBbhWt5ejogLm5GYss5tEFPKupgbmRD0d7OzwyGQJKJYJqNSK9vYj29SFKhegoifv3sb25he3t3QxkncVH9u7HxbR9iPT1IUKaV6sRUCrglUrhELXDxOfjWU310QU8ra6CqYEHh7ANHokEvi45Aiolwmo1hRQlxDQaRDUaxN//AFsbm9ja2s7O5k9I/O0+Yr29NCZG43oQ7ulBpEeNoFIJn1wOt0QCe1srTPX1eFZdlYOAygqY6upgaxHATV4jmRT+LjlCSiVCKoIKYZUKke5uRNP2+b172FzbwObm1mHWNxH/8ENEyd7ubkTS+yPktVSpEFQqEJDL6d13i0S0ppHLxUJlxdEFLFQwsMLlwi5ohksohFciho+8Sl1dCHZ1IaRQUCIKBcJdXZTYX/6KjeQ6NjZ+OszaBlbf/4DuORSjUCAolyNEPtUyGbziDriFQlibGmHkcLBQXpaDgPIyGDls2MhBbmuFR9RORQRlMgQ7ZSkrkyFErFSK2N33sBZfw9raZnYS64jeu4dQpwxhEi/vpPOATErxSyTwtAvham2BrbEBRnYtFspKcxBQVgZjLQs2Ph9OgQCetjb4RCL4OjoQEHcgKBZTQhIJInfuIrGaRCKxkYGss/iid+4iJBYjIJEgmMYvFtPcbmEbXOR/SEMDjLW1WCgtyVEAiwULOchNTXC3tsCbFhEQtcNPrQjh2+8gHksgHl/PsJpE+M93Ebl1O/u1O+/R2ECHiObxkS+dUAhXiwDOxkaYefUwMJn4sbg4h0NcVgojkwlbXR0cjXy4yFNobYGvtRX+tjYEhEKE/nQLsfBzxGLJDJE4QrffRaC1lRL6482se4Lv3oFfKISvrQ1e8qVraYG7uTklgMvFUk0NFnIRsFBSAkN1FSwcDuw8HlxNjbSARyCATyBA4O2bCAdiCIfjGYKrCNy8BV9zM/yEpiZqg2+9nX3vrXfga2mBVyBIN8+ntcwcDgxVVVgoLsrhh6ykGMaaali5HDjq6+HmN8Dd2AgPaeytGwh4IwgEVjP4ovDfuAkfnw9/Y+Nh+HwErr+VNcZ78za85MY0NcHFb4Cjrg4WDhtGIqAoJwElMFRWwlxbCxsRwauHs4EHz7U34XWF4PVGM7hC8LzxJjw8Hjy8enjqU3jr6lKW+nnwvpE91nvtTbgaGmgNB5cLM4tFaz8tKszhDBQVwVhZATM5B2w2HHVcOOvq4Hq8BJcrnMEegOvqdXi4XHg4HLi5XApZezkcaul6f371eirG9UKOx0tw1pPmObCz2TAxmTAwGLkJeFZcBEMFA6aaatjI55TNhp3DhuPaDditftjtQdgtPjhfex0uNpviZNfCyWbBVfszqJ+d2ffa6zSW5iC5rt2Ag8OhNawsFn11lxkMLOT2BAphKC+DqaoSFnIWyJNgMWEnYq5eh/nbJ7DNvQoHiwUHswbOmho40tgP5tUHvoM5iwkHkwn73KupHFevp3KyWLAxmbDU1GClqhJL5WV4WliQg4CCAiyVlmKFwYC5sgJWIqS6Crbqatirq2CtqoKtshJ2YisqKHYGA1YG42B9QNpnJVRW0jgbiUvnI7ks1dUwV1XCXFEBI4OBpeJiLFy8mIOAixewRF6jshKskCfBKKeYKxgwM8phIZQTymApI5TCXJrBQimhlvrKSukeur+8DGYSS/Klc5oYDFqHYCgtwWJRERYuvHJ0AU/O54OIWCwowHJRIZaLiygGcriLi2AsKoSxkFDwgi2AofAijAWHMaSvUYoKsZK2xmJCMc1nIPlJnaJCWvPphQt4kn/u6AIe//7lxJNzZ7GQfw5P8/Px7Px5PD1/ntrFV4jNx2L+PueweO4cnlHOUhZfgPgX9yF7ab58LKYhOffzk1qk5pOzZ/H9yy8njizgPy+99NX3p/Pw+PRpyg9nzuDxmTPU/pjmB+In5OXhx7w8aun89OlDHPiJ3Y85ncr5c0it7wl5eSA9HFnAv0+cOPXdqVNff/Pbk8nvTp7EtydP4pu0zQbZ893J3/wKvxz/zQt5aM1Tp74mPRxZwPE4HsfjeByPE78y/gs8PPqmgXopLgAAAABJRU5ErkJggg==">"""


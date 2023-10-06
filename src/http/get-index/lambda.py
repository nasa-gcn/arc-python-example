from astropy.coordinates import (
    TEME,
    CartesianDifferential,
    CartesianRepresentation,
    GCRS,
)
from astropy.time import Time
import astropy.units as u
import astropy
from sgp4.api import Satrec

from skyfield.api import EarthSatellite, load
from datetime import datetime, timedelta
import numpy as np
import skyfield
from pytz import UTC


def handler(event, context):
    tle = [
        "1 28485U 04047A   23277.47322548  .00014752  00000-0  79079-3 0  9992\n",
        "2 28485  20.5556 209.4616 0009343 214.7559 145.2266 15.12657513 35327\n",
    ]

    # Set up the conditions of the test
    dtstart = datetime(2023, 10, 6, 0, 0, 0, tzinfo=UTC)
    length = 1  # days
    stepsize = 1  # seconds

    # Set the times at which to calculte the x,y,z position of the spacecraft
    dtimes = [
        dtstart + timedelta(seconds=dt) for dt in range(0, 86400 * length, stepsize)
    ]

    # Astropy
    ts = Time(dtstart) + np.arange(86400) * u.s
    satellite = Satrec.twoline2rv(tle[0], tle[1])
    _, temes_p, _ = satellite.sgp4_array(ts.jd1, ts.jd2)
    teme_p = CartesianRepresentation(temes_p.T * u.km)
    teme = TEME(teme_p.without_differentials(), obstime=ts)
    gcrs = teme.transform_to(GCRS(obstime=ts))
    cart = gcrs.cartesian
    posvec_astropy = cart.xyz.value.T

    # Skyfield
    ts = load.timescale()
    nowts = ts.from_datetimes(dtimes)
    satellite = EarthSatellite(tle[0], tle[1])
    gcrs = satellite.at(nowts)
    posvec_skyfield = gcrs.position.km.transpose()

    return {
        "statusCode": 200,
        "headers": {
            "content-type": "application/javascript",
        },
        "body": json.dumps(
            {
                "posvec_astropy": posvec_astropy.tolist(),
                "posvec_skyfield": posvec_skyfield.tolist(),
            }
        ),
    }

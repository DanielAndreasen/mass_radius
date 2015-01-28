#!/usr/bin/python

import urllib
import re
import os

"""
Create a file 'star' and fill with the parameters: star, vmag, parallax,
er_parallax, temp, er_temp, metal, er_metal This code will get the mass and
radius of the stars from the Padova interface in the 'mass_radius.txt' file.
"""


def get_mass_radius(star, vmag, parallax, er_parallax,
                    temp, er_temp, metal, er_metal):
    """
    Returns mass and radius from padova interface.  Enter star, vmag, parallax,
    er_parallax, temp, er_temp, metal, er_metal
    """
    url = 'http://stev.oapd.inaf.it/cgi-bin/param'
    # These are the parameters in the webpage to tune
    form_data = {'param_version': '1.3',
                 'star_name': star,
                 'star_teff': temp,
                 'star_sigteff': er_temp,
                 'star_feh': metal,
                 'star_sigfeh': er_metal,
                 'star_vmag': vmag,
                 'star_sigvmag': '0.0',
                 'star_parallax': parallax,
                 'star_sigparallax': er_parallax,
                 'isoc_kind': 'parsec_CAF09_v1.1',
                 'kind_interp': '1',
                 'kind_tpagb': '0',
                 'kind_pulsecycle': '0',
                 'kind_postagb': '-1',
                 'imf_file': 'tab_imf/imf_chabrier_lognormal.dat',
                 'sfr_file': 'tab_sfr/sfr_const_z008.dat',
                 'sfr_minage': '0.1e9',
                 'sfr_maxage': '12.0e9',
                 'flag_sismo': '0',
                 'submit_form': 'Submit'}

    print 'Retrieving parameters for ' + star
    print 'Please wait...'
    urllib.urlretrieve(url, 'parameters.html',
                       lambda x, y, z: 0, urllib.urlencode(form_data))

    # write results
    with open('parameters.html') as f:
        for _ in range(20):
            line = f.readline()
    t = '.<p>Results for|Age=|Mass=|<i>[M,R]</i>&#9737|<i>R</i>=|'
    pattern = re.compile(t)
    line = line.replace('&plusmn;', ',')
    line = pattern.sub('', line)
    line = line.split(',')

    name = filter(None, line[0].split()[0])
    mass = line[2].replace(' ', '')
    ermass = line[3].replace(' ', '')
    radius = line[6].replace(' ', '')
    erradius = line[7].replace(' ', '')
    return name, mass, ermass, radius, erradius


# 'star' file is the input file with my parameters
hdr = '\t'.join(['star', 'mass', 'er_mass', 'radius', 'er_radius']) + '\n'
with open('star', 'r') as lines:
    lines.readline()
    for line in lines:
        line = filter(None, line.strip().split(' '))
        line[1:] = map(float, line[1:])
        result = get_mass_radius(line[0], line[1], line[2], line[3],
                                 line[4], line[5], line[6], line[7])
        hdr += '\t'.join(map(str, result)) + '\n'

# Write results in the 'mass_radius.txt' file
with open('mass_radius.txt', 'w') as out_file:
    out_file.write(hdr)
print 'THE END'.center(52, '-')
os.system('rm -f parameters.html')

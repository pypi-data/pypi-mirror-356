# -*- coding: utf-8 -*-

__version__ = '1.2.7'

# $BEGIN_RECRUITMENTCURVEFITTING_LICENSE$
# 
# This file is part of the RecruitmentCurveFitting project, a Python package
# for fitting sigmoid and bell-shaped functions to EMG recruitment-curve
# measurements.
# 
# Author: Jeremy Hill (2023-)
# Development was supported by the NIH, NYS SCIRB, and the Stratton VA Medical
# Center.
# 
# No Copyright
# ============
# The author has dedicated this work to the public domain under the terms of
# Creative Commons' CC0 1.0 Universal legal code, waiving all of his rights to
# the work worldwide under copyright law, including all related and neighboring
# rights, to the extent allowed by law.
# 
# You can copy, modify, distribute and perform the work, even for commercial
# purposes, all without asking permission. See Other Information below.
# 
# Other Information
# =================
# In no way are the patent or trademark rights of any person affected by CC0,
# nor are the rights that other persons may have in the work or in how the work
# is used, such as publicity or privacy rights.
# 
# The author makes no warranties about the work, and disclaims liability for
# all uses of the work, to the fullest extent permitted by applicable law. When
# using or citing the work, you are requested to preserve the author attribution
# and this copyright waiver, but you should not imply endorsement by the author.
# 
# $END_RECRUITMENTCURVEFITTING_LICENSE$

__all__ = [ 'Cite' ]
import os, sys, ast
from . import RecruitmentCurves
__doc__ = RecruitmentCurves.__doc__  # the main docstring for the Python API is in the RecruitmentCurves submodule
__all__ += RecruitmentCurves.__all__
from .RecruitmentCurves import *

CITATION_INFO = """
If you use this software in your research, your report should cite the article
in which this approach was introduced, as follows:

- McKinnon ML, Hill NJ, Carp JS, Dellenbach B & Thompson AK (2023).
  Methods for automated delineation and assessment of EMG responses evoked by
  peripheral nerve stimulation in diagnostic and closed-loop therapeutic
  applications.  Journal of Neural Engineering 20(4):046012.
  https://doi.org/10.1088/1741-2552/ace6fb

The corresponding BibTeX entry is::

    @article{mckinnonhill2023,
      author  = {McKinnon, Michael L. and Hill, N. Jeremy and Carp, Jonathan S.
                 and Dellenbach, Blair and Thompson, Aiko K.},
      title   = {Methods for Automated Delineation and Assessment of {EMG}
                 Responses Evoked by Peripheral Nerve Stimulation in Diagnostic
                 and Closed-Loop Therapeutic Applications},
      journal = {Journal of Neural Engineering},
      year    = {2023},
      month   = {July},
      date    = {2023-07-21},
      volume  = {20},
      number  = {4},
      pages   = {046012},
      doi     = {10.1088/1741-2552/ace6fb},
      url     = {https://doi.org/10.1088/1741-2552/ace6fb},
    }
"""

def Cite( command=None, prefix='', stream=None ):
	"""
=============================================================================
This is the RecruitmentCurveFitting package version @VERSION@ by Jeremy Hill,
running in Python @PYVERSION@.

@CITATION_INFO@

To acknowledge this message and prevent it from being displayed every time you
start using the package::

	from RecruitmentCurveFitting import Cite
	Cite('agree')

To refer back to this information again, simply call `Cite()`.
=============================================================================
	"""
	if isinstance( command, str ):
		command = command.lower()
		if command in [ 'agree', 'acknowledge', 'ok' ]: Preferences( nag=False )
		else: raise ValueError( 'unrecognized command option' )
	if command is None:
		if stream is None: stream = sys.stdout
		stream.write( '\n'.join( prefix + line for line in Cite.__doc__.split( '\n' ) ) + '\n' )
		try: stream.flush()
		except: pass
Cite.__doc__ = Cite.__doc__.replace( '@VERSION@', __version__ ).replace( '@PYVERSION@', '%s.%s' % ( sys.version_info.major, sys.version_info.minor ) ).replace( '@CITATION_INFO@', CITATION_INFO.strip() )
hooks = [ lambda: ( 
	( Preferences().get( 'nag', True ) and Cite( stream=sys.stderr, prefix='# ' ) ),
	hooks.pop( 0 )
) ]
from . import CurveFitting; CurveFitting.Curve._Curve__hooks = hooks # comment out to disarm the nag message
# uncomment the line above when the citation info is finalized, to arm the nag message

def Preferences( **kwargs ):
	prefsFile = os.path.expanduser( '~/.' + __name__ )
	try:
		with open( prefsFile, 'rt' ) as fh:
			prefs = ast.literal_eval( fh.read() )
	except:
		prefs = {}
	if kwargs:
		prefs.update( kwargs )
		prefsText = '{\n' + ''.join( '\t%r : %r,\n' % item for item in prefs.items() ) + '}\n'
		prefs = ast.literal_eval( prefsText )
		with open( prefsFile, 'wt' ) as fh:
			fh.write( prefsText )
	return prefs

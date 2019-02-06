'''
disc.py

Phantom analysis for dusty discs.

Daniel Mentiplay, 2019.
'''

import numpy as np
from numpy.linalg import norm

from ..constants import constants
from ..ParticleData import density_from_smoothing_length

# ---------------------------------------------------------------------------- #

def disc_analysis(dump, radiusIn, radiusOut, numberRadialBins,
                  midplaneSlice=False, minParticleAverage=5):
    '''
    Perform disc analysis.

    Arguments:
        dump             : Dump object
        radiusIn         : Inner disc radius for radial binning
        radiusOut        : Outer disc radius for radial binning
        numberRadialBins : Number of radial bins

    Optional:
        midplaneSlice      : Calculate midplane density by taking a slice
        minParticleAverage : Minimum number of particles to compute averages
    '''

    # TODO: add to docs

    particleData = dump.ParticleData
    sinkData = dump.SinkData
    parameters = dump.Parameters

    nDustSmall = parameters['ndustsmall']
    nDustLarge = parameters['ndustlarge']

    containsSmallDust = bool(nDustSmall > 0)
    containsLargeDust = bool(nDustLarge > 0)
    containsDust = bool(containsSmallDust or containsLargeDust)

    if containsDust:
        grainSize = parameters['grainsize']
        grainDens = parameters['graindens']

    nSinks = parameters['nptmass']
    containsSinks = bool(nSinks > 0)

#--- Units

    units = dump.Units

    uDist = units['distance']
    uTime = units['time']
    uMass = units['mass']

#--- Particle properties

    massParticle    = particleData.particleMass
    position        = particleData.position
    smoothingLength = particleData.smoothingLength
    velocity        = particleData.velocity
    if velocity is not None:
        momentum        = np.transpose(np.array(3*[massParticle])) * velocity
        angularMomentum = np.cross(position, momentum)

#--- Sink properties

    if containsSinks:

        massParticleSink = sinks.mass

        # TODO: check if sink[0] is really the star; check if binary
        stellarMass = massParticleSink[0]

        gravitationalParameter = constants.gravitationalConstant \
                               / ( uDist**3 / uTime**2 / uMass ) \
                               * stellarMass

        positionSink = sinks.position

        if isFullDump:

            velocitySink        = sinks.velocity
            momentumSink        = np.full((nSinks, 3), np.nan)
            angularMomentumSink = np.full((nSinks, 3), np.nan)
            eccentricitySink    = np.full(nSinks, np.nan)

            for idx in range(nSinks):
                momentumSink[idx] = massParticleSink[idx] * velocitySink[idx]
                angularMomentumSink[idx] = np.cross(positionSink[idx],
                                                    momentumSink[idx])

            eccentricitySink = _calculate_eccentricity( massParticleSink,
                                                        positionSink,
                                                        velocitySink,
                                                        angularMomentumSink,
                                                        gravitationalParameter )

        else:

            velocitySink        = None
            momentumSink        = None
            angularMomentumSink = None
            eccentricitySink    = None

#--- Gas eccentricity

    if isFullDump:

        eccentricityGas = _calculate_eccentricity( massParticleGas,
                                                   positionGas,
                                                   velocityGas,
                                                   angularMomentumGas,
                                                   gravitationalParameter )

    else:

        eccentricityGas = None

#--- Radially bin gas

    cylindricalRadiusGas = norm(positionGas[:, 0:2], axis=1)
    heightGas = positionGas[:, 2]

    vals = _calculate_radially_binned_quantities( numberRadialBins,
                                                  radiusIn,
                                                  radiusOut,
                                                  cylindricalRadiusGas,
                                                  heightGas,
                                                  smoothingLengthGas,
                                                  massParticleGas,
                                                  angularMomentumGas,
                                                  eccentricityGas,
                                                  parameters,
                                                  midplaneSlice,
                                                  minParticleAverage )

    radialBinsDisc         = vals[0]
    surfaceDensityGas      = vals[1]
    midplaneDensityGas     = vals[2]
    meanSmoothingLengthGas = vals[3]
    scaleHeightGas         = vals[4]
    meanAngularMomentumGas = vals[5]
    tiltGas                = vals[6]
    twistGas               = vals[7]
    psiGas                 = vals[8]
    meanEccentricityGas    = vals[9]

#--- Radially bin dust

    cylindricalRadiusDust   = list()
    heightDust              = list()

    surfaceDensityDust      = list()
    midplaneDensityDust     = list()
    meanSmoothingLengthDust = list()
    scaleHeightDust         = list()
    meanAngularMomentumDust = list()
    tiltDust                = list()
    twistDust               = list()
    psiDust                 = list()
    eccentricityDust        = list()
    meanEccentricityDust    = list()

    for idx in range(nDustLarge):

        #--- Dust eccentricity

        if isFullDump:

            eccentricityDust.append(
                _calculate_eccentricity( massParticleDust[idx],
                                         positionDust[idx],
                                         velocityDust[idx],
                                         angularMomentumDust[idx],
                                         gravitationalParameter ) )

        else:

            eccentricityDust.append(None)

        cylindricalRadiusDust.append(
            norm(positionDust[idx][:, 0:2], axis=1) )

        heightDust.append(positionDust[idx][:, 2])

        vals = _calculate_radially_binned_quantities( numberRadialBins,
                                                      radiusIn,
                                                      radiusOut,
                                                      cylindricalRadiusDust[idx],
                                                      heightDust[idx],
                                                      smoothingLengthDust[idx],
                                                      massParticleDust[idx],
                                                      angularMomentumDust[idx],
                                                      eccentricityDust[idx],
                                                      parameters,
                                                      midplaneSlice,
                                                      minParticleAverage )

        surfaceDensityDust.     append( vals[1] )
        midplaneDensityDust.    append( vals[2] )
        meanSmoothingLengthDust.append( vals[3] )
        scaleHeightDust.        append( vals[4] )
        meanAngularMomentumDust.append( vals[5] )
        tiltDust.               append( vals[6] )
        twistDust.              append( vals[7] )
        psiDust.                append( vals[8] )
        meanEccentricityDust.   append( vals[9] )

#--- Stokes

    gamma = parameters.eos['gamma']

    Stokes = [np.full_like(radialBinsDisc, np.nan) for i in range(nDustLarge)]

    for idxi in range(len(radialBinsDisc)):
        for idxj in range(nDustLarge):

            Stokes[idxj][idxi] = \
                np.sqrt(gamma*np.pi/8) * grainDens[idxj] * grainSize[idxj] \
                / ( scaleHeightGas[idxi] \
                * (midplaneDensityGas[idxi] + midplaneDensityDust[idxj][idxi]) )

#--- Package into dictionary

    surfaceDensity              = dict()
    surfaceDensity['gas']       = surfaceDensityGas
    surfaceDensity['dust']      = surfaceDensityDust

    midplaneDensity             = dict()
    midplaneDensity['gas']      = midplaneDensityGas
    midplaneDensity['dust']     = midplaneDensityDust

    meanSmoothingLength         = dict()
    meanSmoothingLength['gas']  = meanSmoothingLengthGas
    meanSmoothingLength['dust'] = meanSmoothingLengthDust

    scaleHeight                 = dict()
    scaleHeight['gas']          = scaleHeightGas
    scaleHeight['dust']         = scaleHeightDust

    meanAngularMomentum         = dict()
    meanAngularMomentum['gas']  = meanAngularMomentumGas
    meanAngularMomentum['dust'] = meanAngularMomentumDust
    meanAngularMomentum['sink'] = angularMomentumSink

    tilt                        = dict()
    tilt['gas']                 = tiltGas
    tilt['dust']                = tiltDust

    twist                       = dict()
    twist['gas']                = twistGas
    twist['dust']               = twistDust

    psi                         = dict()
    psi['gas']                  = psiGas
    psi['dust']                 = psiDust

    meanEccentricity            = dict()
    meanEccentricity['gas']     = meanEccentricityGas
    meanEccentricity['dust']    = meanEccentricityDust
    meanEccentricity['sink']    = eccentricitySink


#--- Return

    return ( radialBinsDisc,
             surfaceDensity,
             midplaneDensity,
             meanSmoothingLength,
             scaleHeight,
             meanAngularMomentum,
             tilt,
             twist,
             psi,
             meanEccentricity,
             Stokes )

# ---------------------------------------------------------------------------- #

def _calculate_radially_binned_quantities( numberRadialBins=None,
                                           radiusIn=None,
                                           radiusOut=None,
                                           cylindricalRadius=None,
                                           height=None,
                                           smoothingLength=None,
                                           massParticle=None,
                                           angularMomentum=None,
                                           eccentricity=None,
                                           parameters=None,
                                           midplaneSlice=None,
                                           minParticleAverage=None ):
    '''
    Calculate averaged radially binned quantities:
        - radial bins
        - surface density
        - midplane density
        - scale height
        - smoothing length
        - angular momentum
        - tilt
        - twist
        - psi
        - eccentricity
    '''

    if numberRadialBins is None:
        raise ValueError('Need numberRadialBins')

    if radiusIn is None:
        raise ValueError('Need radiusIn')

    if radiusOut is None:
        raise ValueError('Need radiusOut')

    if cylindricalRadius is None:
        raise ValueError('Need cylindricalRadius')

    if height is None:
        raise ValueError('Need height')

    if smoothingLength is None:
        raise ValueError('Need smoothingLength')

    if massParticle is None:
        raise ValueError('Need massParticle')

    if midplaneSlice and parameters is None:
        raise ValueError('"parameters" required to calculate midplane slice')

    dR         = (radiusOut - radiusIn) / (numberRadialBins - 1)
    radialBins = np.linspace(radiusIn, radiusOut, numberRadialBins)

    meanSmoothingLength = np.full_like(radialBins, np.nan)
    surfaceDensity      = np.full_like(radialBins, np.nan)
    midplaneDensity     = np.full_like(radialBins, np.nan)
    scaleHeight         = np.full_like(radialBins, np.nan)

    if angularMomentum is not None:

        if eccentricity is None:
            raise ValueError('Need eccentricity')

        useVelocities = True

        meanAngularMomentum      = np.full_like(3*[radialBins], np.nan)
        magnitudeAngularMomentum = np.full_like(radialBins, np.nan)
        meanTilt                 = np.full_like(radialBins, np.nan)
        meanTwist                = np.full_like(radialBins, np.nan)
        meanPsi                  = np.full_like(radialBins, np.nan)
        meanEccentricity         = np.full_like(radialBins, np.nan)

    else:

        useVelocities = False

        meanAngularMomentum      = None
        magnitudeAngularMomentum = None
        meanTilt                 = None
        meanTwist                = None
        meanPsi                  = None
        meanEccentricity         = None


    for index, R in enumerate(radialBins):

        area = np.pi * ( (R + dR/2)**2 - (R - dR/2)**2 )

        indicies = np.where((cylindricalRadius < R + dR/2) & \
                            (cylindricalRadius > R - dR/2))[0]

        nPart = len(indicies)

        surfaceDensity[index] = massParticle * nPart / area

        if nPart > minParticleAverage:

            meanSmoothingLength[index] = np.sum(
                smoothingLength[indicies] ) / nPart

            meanHeight = np.sum( height[indicies] ) / nPart

            scaleHeight[index] = np.sqrt( np.sum(
                (height[indicies] - meanHeight)**2 ) / (nPart - 1) )

            if useVelocities:

                meanAngularMomentum[:, index] = np.sum(
                    angularMomentum[indicies], axis=0 ) / nPart

                magnitudeAngularMomentum[index] = \
                        norm(meanAngularMomentum[:, index])

                meanTilt[index] = np.arccos( meanAngularMomentum[2, index] \
                                           / magnitudeAngularMomentum[index] )

                meanTwist[index] = np.arctan2(
                    meanAngularMomentum[1, index] / magnitudeAngularMomentum[index],
                    meanAngularMomentum[0, index] / magnitudeAngularMomentum[index] )

                meanEccentricity[index] = np.sum( eccentricity[indicies] ) / nPart

        else:

            meanSmoothingLength[index] = np.nan

            scaleHeight[index] = np.nan

            if useVelocities:

                meanAngularMomentum[:, index] = np.nan
                meanTilt[index]               = np.nan
                meanTwist[index]              = np.nan
                meanEccentricity[index]       = np.nan

        if midplaneSlice:

            frac = 1/2

            indiciesMidplane = np.where(
                (cylindricalRadius < R + dR/2) &
                (cylindricalRadius > R - dR/2) &
                (height < meanHeight + frac * scaleHeight[index]) &
                (height > meanHeight - frac * scaleHeight[index])
                )[0]

            hfact = parameters.numerical['hfact']

            midplaneDensity[index] = np.sum(
                density_from_smoothing_length(
                    smoothingLength[indiciesMidplane], massParticle , hfact)
                ) / nPart

        else:

            midplaneDensity[index] = surfaceDensity[index] / np.sqrt(2*np.pi) \
                                                           / scaleHeight[index]

        midplaneDensity[index] = np.nan_to_num( midplaneDensity[index] )

    if useVelocities:

        unitAngularMomentum = meanAngularMomentum/magnitudeAngularMomentum

        meanPsi = radialBins * np.sqrt(
            np.gradient(unitAngularMomentum[0], dR)**2 + \
            np.gradient(unitAngularMomentum[1], dR)**2 + \
            np.gradient(unitAngularMomentum[2], dR)**2 )

    return ( radialBins,
             surfaceDensity,
             midplaneDensity,
             meanSmoothingLength,
             scaleHeight,
             meanAngularMomentum,
             meanTilt,
             meanTwist,
             meanPsi,
             meanEccentricity )

# ---------------------------------------------------------------------------- #

def _calculate_eccentricity( massParticle,
                             position,
                             velocity,
                             angularMomentum,
                             gravitationalParameter ):
    '''
    Calculate eccentricity.
    '''

    specificKineticEnergy = 1/2 * norm(velocity, axis=1)**2
    specificGravitationalEnergy = - gravitationalParameter / norm(position, axis=1)
    specificEnergy = specificKineticEnergy + specificGravitationalEnergy

    specificAngularMomentum = norm(angularMomentum, axis=1) \
                            / massParticle

    term = 2 * specificEnergy * specificAngularMomentum**2 \
         / gravitationalParameter**2

    eccentricity = np.sqrt( 1 + term )

    return eccentricity

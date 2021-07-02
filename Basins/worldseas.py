#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin, ComposedBasin

# Path to the shapes directory
SHAPESPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'shapes')

# World Seas shapefile
alb    = Basin.from_npy('alb' , 'Alboran Sea'   , os.path.join(SHAPESPATH,'Alboran_WorldSeas.npy'),downsample=4)
bal    = Basin.from_npy('bal' , 'Iberian Sea'   , os.path.join(SHAPESPATH,'Balearic_WorldSeas.npy'),downsample=4)
lig    = Basin.from_npy('lig' , 'Ligurian Sea'  , os.path.join(SHAPESPATH,'Ligurian_WorldSeas.npy'),downsample=4)
tyr    = Basin.from_npy('tyr' , 'Tyrrhenian Sea', os.path.join(SHAPESPATH,'Tyrrhenian_WorldSeas.npy'),downsample=4)
west   = Basin.from_npy('west', 'Western Basin' , os.path.join(SHAPESPATH,'WestMed_WorldSeas.npy'),downsample=4)
adr    = Basin.from_npy('adr' , 'Adriatic Sea'  , os.path.join(SHAPESPATH,'Adriatic_WorldSeas.npy'),downsample=4)
aeg    = Basin.from_npy('aeg' , 'Aegean Sea'    , os.path.join(SHAPESPATH,'Aegean_WorldSeas.npy'),downsample=4)
ion    = Basin.from_npy('ion' , 'Ionian Sea'    , os.path.join(SHAPESPATH,'Ionian_WorldSeas.npy'),downsample=4)
east   = Basin.from_npy('east', 'Eastern Basin' , os.path.join(SHAPESPATH,'EastMed_WorldSeas.npy'),downsample=4)

baltic = Basin.from_npy('bal' , 'Baltic Sea', os.path.join(SHAPESPATH,'BalticSea_WorldSeas.npy'),downsample=4)

satlan = Basin.from_npy('sa' , 'South Atlantic', os.path.join(SHAPESPATH,'SouthAtlantic_WorldSeas.npy'),downsample=4)
spaci1 = Basin.from_npy('sp1', 'South Pacific1', os.path.join(SHAPESPATH,'SouthPacific1_WorldSeas.npy'),downsample=4)
spaci2 = Basin.from_npy('sp2', 'South Pacific2', os.path.join(SHAPESPATH,'SouthPacific2_WorldSeas.npy'),downsample=4)
socean = Basin.from_npy('so' , 'Southern Ocean', os.path.join(SHAPESPATH,'SouthernOcean_WorldSeas.npy'),downsample=4)

kotor  = Basin.from_npy('kotor', 'Bay of Kotor', os.path.join(SHAPESPATH,'Kotor_WorldSeas.npy'),downsample=1)

# Composed basins
wmed   = ComposedBasin('wmed', 'Western Mediterranean', [alb,bal,lig,tyr,west])
emed   = ComposedBasin('emed', 'Eastern Mediterranean', [adr,aeg,ion,east])
med    = ComposedBasin('med' , 'Mediterranean Sea'    , [alb,bal,lig,tyr,west,adr,aeg,ion,east])

spacif = ComposedBasin('sp', 'South Pacific', [spaci1,spaci2])
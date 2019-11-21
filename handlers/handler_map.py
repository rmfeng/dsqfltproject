"""
tracks all fo the handlers we have implemented
"""
from handlers.h_dp import DPProcessor
from handlers.h_pe import PEProcessor
from handlers.h_bm import BMProcessor
from handlers.h_cape import CAPEProcessor
from handlers.h_by import BYProcessor
from handlers.h_def import DEFProcessor
from handlers.h_cpi import CPIProcessor
from handlers.h_nos import NOSProcessor
from handlers.h_pcr import PCRProcessor
from handlers.h_oil import OILProcessor
from handlers.h_si import SIProcessor
from handlers.h_bdi import BDIProcessor
from handlers.h_cay import CAYProcessor
from handlers.h_ic import ICProcessor
from handlers.h_term import TERMProcessor
from handlers.h_vrp import VRPProcessor


# add more handlers here as we implement them
ALL_HANDLERS = [DPProcessor(),
                PEProcessor(),
                BMProcessor(),
                CAPEProcessor(),
                BYProcessor(),
                DEFProcessor(),
                CPIProcessor(),
                NOSProcessor(),
                PCRProcessor(),
                OILProcessor(),
                SIProcessor(),
                BDIProcessor(),
                CAYProcessor(),
                ICProcessor(),
                TERMProcessor(),
                VRPProcessor(),
                ]

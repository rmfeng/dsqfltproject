"""
tracks all fo the handlers we have implemented
"""
from handlers.h_cpi import CPIProcessor
from handlers.h_nos import NOSProcessor

# add more handlers here as we implement them
ALL_HANDLERS = [CPIProcessor(),
                NOSProcessor(),
                ]
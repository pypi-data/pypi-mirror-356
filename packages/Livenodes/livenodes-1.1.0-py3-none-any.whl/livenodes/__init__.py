from .registry import Register
# There is one one global registry of nodes
# In order to not have circular dependencies, but allow for global modification (ie adding classes, enabling/disabling packages)
# this registry is only created the first an instance is needed and then stored for subsequent configs etc
REGISTRY = None

import logging
logger = logging.getLogger('livenodes')

# TODO: if we do not want to support eager loading in the registry i'm pretty sure we can remove the get_registry() function and just initialize this properly the first time.
def get_registry():
    logger.info('retrieving registry')
    global REGISTRY
    if REGISTRY is None:
        REGISTRY = Register(lazy_load=True)
        # --- first hook up the default briges
        from .components.bridges import Bridge_local, Bridge_thread, Bridge_process, Bridge_aioprocessing
        logger.info('registering default bridges')
        REGISTRY.bridges.register('Bridge_local', Bridge_local)
        REGISTRY.bridges.register('Bridge_thread', Bridge_thread)
        REGISTRY.bridges.register('Bridge_process', Bridge_process)
        # REGISTRY.bridges.register('Bridge_aioprocessing', Bridge_aioprocessing)

    logger.info('returning registry')
    return REGISTRY


from .node import Node
from .graph import Graph
from .viewer import View
from .producer import Producer
from .producer_async import Producer_async
from .components.connection import Connection
from .components.node_connector import Attr
from .components.port import Port, Ports_collection
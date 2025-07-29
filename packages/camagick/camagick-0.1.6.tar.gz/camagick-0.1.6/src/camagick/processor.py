import asyncio, logging

logger = logging.getLogger(__name__)


class DuplicateDataTag(RuntimeError): pass

#
# Base for all CAMagick processing components (sources, modifyers, sinks)
#

class ProcessorBase(object):

    async def startup(self):
        pass

    async def shutdown(self):
        pass
    
    async def __call__(self, data=None, context=None):
        '''
        This is the actual workhorse. It's expected to accept
        a data dictionary (if anything available), and return
        a modified dictionary.

        There's an exception for sources (which usually ignore incoming
        data), and sinks (which usually don't return anything anymore).

        Args:
        
            data: the data the processor is expected to primarily apply to.
              This is usually whatever is requested in the 'from-epics'
              class of sources.

            context: A dictionary of additionaly data (possibly also
              of 'from-epics' origin), which isn't to be primarily
              processed, but which is available for further decision
              making. Each processor is free to make use of data here
              as it sees fit.

        Returns: may return None (if it's a sink), or a set of modified
          data. The modified data may or may not contain all, any, or none
          of the original data keys, and may also create its own new data
          keys (and values).
        '''
        raise RuntimeError(f'Not implemented')


class SourceBase(ProcessorBase):
    '''
    Base class from which all source-like pipes are derived.

    This is only used within specific flow elements (Chains)
    to auto-merge results with the results of the previous pipe,
    instead of replacing them outright.
    '''
    pass


class SinkBase(ProcessorBase):
    '''
    Base class form which all sink-like pipes are derived.

    This is used within specific flow elements (Fanout) to block
    output data from propagating.
    '''
    pass


class FlowBase(ProcessorBase):
    '''
    Base class from which all flow elements are derived.

    Common functionality is .startup() / .shutdown() loops, and __repr__().
    '''
    
    def __init__(self, *pipes):
        self.subpipes = pipes


    async def startup(self):
        aw = [
            (p.startup() if hasattr(p, "startup") else _nop()) \
            for p in self.subpipes
        ]
        
        await asyncio.gather(*aw, return_exceptions=False)


    async def shutdown(self):
        async def _nop(): pass
        aw = [
            (p.shutdown() if hasattr(p, "shutdown") else _nop()) \
            for p in self.subpipes
        ]
        
        await asyncio.gather(*aw, return_exceptions=False)


    def __str__(self):
        parts = '\n'.join([str(p) for p in self.subpipes])
        return f'({self.__class__.__name__}:\n  {parts})'        
        

    def __repr__(self):
        return str(self)
        

from typing import Optional

from .rooproc_helper_action import RooProcHelperAction
from .auxiliary import register_action

@register_action
class RooProcTreeName(RooProcHelperAction):
    
    NAME = "TREENAME"
    
    def __init__(self, treename:str):
        super().__init__(treename=treename)
        
    @classmethod
    def parse(cls, main_text:str, block_text:Optional[str]=None):
        return cls(treename=main_text)
    
    def _execute(self, processor:"quickstats.RooProcessor", **params):
        treename = params['treename']
        processor.treename = treename
        return processor
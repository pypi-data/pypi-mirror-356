from typing import Dict, Union, List, Optional

import numpy as np

from quickstats import semistaticmethod, cached_import

class RooAbsData:
    @staticmethod
    def create_histogram(data:"ROOT.RooAbsData", *args):
        ROOT = cached_import("ROOT")
        h = data.createHistogram(*args)
        if isinstance(h, ROOT.TH1):
            from quickstats.interface.root import TH1
            py_h = TH1(h)
        elif isinstance(h, ROOT.TH2):
            from quickstats.interface.root import TH2
            py_h = TH2(h)
        else:
            raise RuntimeError(f"unsupported histogram type: {type(h)}")
        h.Delete()
        return py_h
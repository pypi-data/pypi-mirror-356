from collections import defaultdict
from copy import deepcopy
from typing import Any, Literal, Optional

from ._BaseHandler import BaseHandler
from ._selector._MaterialSelector import MaterialSelector
from ._selector._Selector import SelectType
from ._Materials import (
    ConcreteHandler,
    ConcreteWallsHandler,
    ContactMaterialsHandler,
    InitialStateHandler,
    OtherUniaxialHandler,
    PyTzQzHandler,
    StandardModelsHandler,
    StandardUniaxialHandler,
    SteelReinforcingHandler,
    TsinghuaSandModelsHandler,
    UCSDSaturatedSoilHandler,
    UCSDSoilModelsHandler,
)


class MaterialManager(BaseHandler):
    def __init__(self):
        # 统一数据仓库
        self.materials: dict[int, dict] = {}

        # 构建 "命令 -> {matType -> handler}" 映射
        self._command2typehandler: dict[str, dict[str, BaseHandler]] = defaultdict(dict)
        handler_classes = [
            StandardModelsHandler,
            StandardUniaxialHandler,
            TsinghuaSandModelsHandler,
            ConcreteWallsHandler,
            ConcreteHandler,
            ContactMaterialsHandler,
            InitialStateHandler,
            UCSDSoilModelsHandler,
            UCSDSaturatedSoilHandler,
            OtherUniaxialHandler,
            PyTzQzHandler,
            SteelReinforcingHandler,
        ]
        for cls in handler_classes:
            cmd = cls.handles()[0]
            for typ in cls.types():
                self._command2typehandler[cmd][typ] = cls(self._command2typehandler[cmd], self.materials)


    def sel(self, **kwargs) -> MaterialSelector:
        """返回材料选择器"""
        selector = MaterialSelector(self.materials)
        if kwargs:
            # 第一次调用使用 NEW
            kwargs['type'] = kwargs.get('type', SelectType.NEW)
            selector.sel(**kwargs)
        else:
            selector.sel(type=SelectType.ALL)
        return selector

    @property
    def newtag(self) -> int:
        """return a new tag that is unused"""
        return self.get_new_tags(1)[0]
    
    @property
    def newtag_upper(self):
        """return a new tag that is max of all tags + 1"""
        if not self.materials:  # Fixed: Check if empty
            return 1
        return max(self.materials)+1
    
    def get_new_tags(self, num: int, start: int = 1) -> list[int]:
        """Generate a list of 'num' new material tags starting from at least 'start'"""
        if not self.materials:
            return list(range(start, start + num))
        
        sorted_tags = sorted(self.materials.keys())
        # Find a continuous range of num tags starting from at least start
        candidate = max(start, sorted_tags[0] + 1)
        if candidate>=sorted_tags[-1]:
            candidate = max(start, sorted_tags[-1] + 1)
            return list(range(candidate, candidate + num))

        for tag in sorted_tags:
            # If the gap before the current tag is large enough, use it
            if tag - candidate >= num:
                return list(range(candidate, candidate + num))
            # Otherwise, move the candidate just after this tag (skip used tags)
            if tag >= candidate:
                candidate = tag + 1

        # If no suitable gap was found inside existing tags, allocate tags after the last one
        return list(range(candidate, candidate + num))
    
    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        """聚合各子 Handler 的 rule"""
        merged: defaultdict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(lambda: deepcopy({"positional": ["matType", "matTag", "args*"]})))
        for t2h in self._command2typehandler.values():
            for h in set(t2h.values()):
                for k, v in h._COMMAND_RULES.items():
                    merged[k].update(v)
        return merged

    @staticmethod
    def handles():
        return ["uniaxialMaterial", "nDMaterial"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        matType = arg_map["args"][0]
        registry = self._command2typehandler.get(func_name, {})
        handler = registry.get(matType)
        if handler:
            handler.handle(func_name, arg_map)
        else:
            self.handle_unknown_material(func_name, *arg_map["args"], **arg_map["kwargs"])

    def handle_unknown_material(self, func_name: str, *args, **kwargs):
        """Handle unknown material types"""
        arg_map = self._parse(func_name, *args, **kwargs)

        matTag = int(arg_map.get("matTag"))
        matType = arg_map.get("matType")
        args = arg_map.get("args", [])
        matinfo = {
            "matType": matType,
            "matTag": matTag,
            "args": args,
            "materialType": func_name  # uniaxialMaterial 或 nDMaterial
        }
        self.materials[matTag] = matinfo

    @property
    def nDMaterial_list(self):
        return self._command2typehandler["nDMaterial"].keys()
    
    @property
    def uniaxialMaterial_list(self):
        return self._command2typehandler["uniaxialMaterial"].keys()
    
    def get_material(self, matTag:int) -> dict:
        """Get material information by tag"""
        return self.materials.get(matTag, None)

    def get_materials_by_type(self, matType: str) -> list[int]:
        """Get all materials of the specified type"""
        return {tag:data for tag, data in self.materials.items() if data.get("matType", "").lower() == matType.lower()}

    @property
    def nDMaterial(self) -> dict[int,dict]:
        """Get all nDMaterial"""
        return {tag:data for tag, data in self.materials.items() if data.get("matType", "") in self.nDMaterial_list}
    
    @property
    def uniaxialMaterial(self) -> dict[int,dict]:
        """Get all uniaxialMaterial"""
        return {tag:data for tag, data in self.materials.items() if data.get("matType", "") in self.uniaxialMaterial_list}

    def clear(self):
        self.materials.clear()
        
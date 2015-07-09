# -*- coding: utf-8 -*-
# def.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# def: bks1, com.71.player.core.model.def 

# import

# class
class DefinitionEnum(object):
    # 视频清晰度定义
    
    def __init__(self):
        self.ITEMS = []
        
        # 官方清晰度	实际清晰度	hd
        items = self.ITEMS
        # (极速)	渣清		-3
        self.LIMIT 	= EnumItem(96, 'topspeed', items)
        # (流畅)	超低清		-2
        self.NONE 	= EnumItem(0, 'none', items)
        # (标清)	低清		-1
        self.STANDARD 	= EnumItem(1, 'standard', items)
        # (高清)	普清		0
        self.HIGH 	= EnumItem(2, 'high', items)
        # (超清)	高清		1
        self.SUPER 	= EnumItem(3, 'super', items)
        # (720p)	720p		2
        self.SUPER_HIGH = EnumItem(4, 'super-high', items)
        # (1080p)	1080p		4
        self.FULL_HD 	= EnumItem(5, 'fullhd', items)
        # (4K)		4K		7
        self.FOUR_K 	= EnumItem(10, '4k', items)
        # done

# end def.py



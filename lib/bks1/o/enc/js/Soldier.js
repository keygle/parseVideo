/* Soldier.js, parse_video/lib/bks1/o/enc
 * last_update 2015-09-16 19:32 GMT+0800 CST
 */

// package com.qiyi.player.core.video.engine.dispatcher
// import flash.utils.getDefinitionByName;

// public class Soldier extends Object
	
// private static var _food:Object;
var _food = null;
	
// public static function set food(param1:Object) : void
	// NOTE this function is no use
	function set_food(param1) {
		if (_food == null) {
			_food = param1;
			fight();
		}
	}

// private static function fight() : void
	function fight(_dota) {
		
		// var _loc1:Object = getDefinitionByName(String.fromCharCode(99,111,109,46,113,105,121,105,46,112,108,97,121,101,114,46,99,111,114,101,46,118,105,100,101,111,46,101,110,103,105,110,101,46,100,109,46,112,114,111,118,105,100,101,114,46,77,101,100,105,97,68,111,116,97));
		// var _loc2:Object = new _loc1();
		
		// NOTE 'com.qiyi.player.core.video.engine.dm.provider.MediaDota'
		var _loc2 = _dota;	// NOTE this should be MediaDota
		
		// NOTE new Zombie here at 2015-09-16
		// NOTE gen main data
		var _loc3 = "ll_l____l___ll_l_l____llllll_llll_lllllll____llll_____l____l__lll___ll__lll_lll_lll________l__lllll__l_l_ll__lll__llll__l_l_l_llllllll";
		_loc2[_loc3](_loc2["ll_l_____l____ll________l_llll_ll_l____ll________l_lllll_lllllll_l____ll_lll____lll_llllllll___lll__ll_llll__l____ll_l____ll____llll__lll___lll"]);
		_loc2[_loc3](_loc2["ll_lllll_____l______lllll______lllll__llll_l_lllllllll__llllll____lll_l_ll____ll_l_l_ll____lllllllllll__llll___ll_l_l_l_l___ll_lll___ll_lllll_l"]);
		_loc2[_loc3](_loc2["ll_lllllll_____llllll__llllllll___lll_____llll___l_____l_lll________l_l_____lllll____llll___lll_llll______lll_l_llll__l__ll_l_l__lll___ll_llll__lll"]);
		_loc2[_loc3](_loc2["ll_l_lllll_______l_lll_l_lllll_llll_lll______________llll_____lll__llll_llll__lllllll__lllllllll__lll______llll_lll_lllll______llll________ll_l_"]);
		_loc2[_loc3](_loc2["ll_l____l__lll_lllll___ll_ll____l_llll_l_llllllll______lllll___ll_____ll_l_llll_llll_____lllll_llll_l_l_l_lllll__lllll_l_l_lll_l_lllllll__lll__lllll"]);
		_loc2[_loc3](_loc2["ll_llllllllll_llllll_llllll_ll_lllll_________ll_l_l_lll_l_llll__l_ll_l__lllllll__lll__llllllll_llllll_ll_ll___ll_ll_l________l____l"]);
		_loc2[_loc3](_loc2["ll_l_____llll_llll_____l____l_____llll_ll_l_lllll_llll__ll____llll_______lll_lllll_l___ll_l_lllllll_l_lll____llll___llll___lll___ll_lll_l_lll_______l"]);
		_loc2[_loc3](_loc2["ll_llllll___llllll_____lll___llllllll___l_l______l_l_______lllll_l___ll___ll____lllll__l_l____lll_lll_lll___llllll_lll_llll____ll___lllll__llll_l_"]);
		_loc2[_loc3](_loc2["ll_ll__lll_____ll_l_lllll___lllll____ll_l_llllllll_l_llll___llllll___lllllll_ll__lll_llll____________lllll_lll________llll__l_l_l_l_____llll_"]);
		_loc2[_loc3](_loc2["ll_lllllllll_______ll_____l_l_lll_llll_l___lllll______lll_lll____l_l_llllll___llll______ll_llll____lll___lllll___ll______llllll_llll__l_l"]);
		_loc2[_loc3](_loc2["ll_l______llllll___lll_lll___lllll__llll__llll_lllllll__lll_llll____ll___l_lllll___ll_______lll_l_llll___llllll_l_llll____ll_ll____llll_ll_llll___l_l"]);
		_loc2[_loc3](_loc2["ll_lll_lll_l__lll___ll_llllllll____ll_lllllllllll___l_llll_l__lll____lllllll____lll__ll_lllll_l__lll______lllll____llll_llll_l_l_llllll___l_"]);
		_loc2[_loc3](_loc2["ll_l_llllll___ll____llllll_l__lll_l_l_lllllllll____ll____l____ll_____l______llllllll_l_llll_l_llllll_l____lllll_ll_l____l_llll_llllll_l_ll"]);
		_loc2[_loc3](_loc2["ll_llllll_llll____llll_l__lllll____llllllll_ll____llll_____ll_ll__ll_ll__llll____l_____ll_lllll_llll__llll___ll_ll_llll___lllll____"]);
		_loc2[_loc3](_loc2["ll_l____lll_l_lll_l_l_ll__lll_ll_l_lllllllllll__ll_llll__lll__llll__l_ll__lllll_____lll_l_lllll__lllllll__lllllll_l____llllll_"]);
		_loc2[_loc3](_loc2["ll_l____ll__lll_l_l_llllll___l_llllll___llllll__llllll______lll______ll____llllll_________lllll_l__lll____l_llll_lllll____ll________llll_"]);
		
		// _food[String.fromCharCode(116,104,100)] = _loc2;
		// NOTE 'thd'
		// NOTE _loc2 is thd
		// NOTE not set, just return the result
		return _loc2;
	}

// function add for easy
	function get_thd(_dota) {
		return fight(_dota);
	}

// try to export for node.js
try {
	exports.get_thd = get_thd;	// get_thd(_dota);
} catch (e) {
}	// nothing to do if exports failed

/* end Soldier.js */



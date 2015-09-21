package com.qiyi.player.core.model.utils {
	import com.qiyi.player.base.logging.targets.LineFormattedTarget;
	import com.qiyi.player.base.logging.targets.TraceTarget;
	import com.qiyi.player.base.logging.LogEventLevel;
	import com.qiyi.player.base.logging.Log;
	import flash.system.Capabilities;
	import com.qiyi.player.base.logging.targets.DebugTarget;
	import com.qiyi.player.base.logging.targets.CookieTarget;
	import com.qiyi.player.core.Config;
	import com.qiyi.player.base.logging.ILoggingTarget;
	
	public class LogManager extends Object {
		
		public static var _targets:Array = [];
		 
		public function LogManager() {
			super();
		}
		
		public static function initLog(param1:Boolean = true) : void {
			var target:LineFormattedTarget = null;
			var var_3:Boolean = param1;
			target = new TraceTarget();
			target.level = LogEventLevel.DEBUG;
			target.includeDate = true;
			target.includeTime = true;
			target.includeLevel = true;
			_targets.push(target);
			Log.addTarget(target);
			if(Capabilities.isDebugger) {
				target = new DebugTarget();
				target.level = LogEventLevel.DEBUG;
				target.includeDate = true;
				target.includeTime = true;
				target.includeLevel = true;
				_targets.push(target);
				Log.addTarget(target);
			} else if(var_3) {
				target = new CookieTarget(Config.LOG_COOKIE,"logs",Config.MAX_LOG_COOKIE_SIZE,400);
				target.level = LogEventLevel.INFO;
				target.includeDate = true;
				target.includeTime = true;
				_targets.push(target);
				Log.addTarget(target);
			}
			var ll_l_llllllll_ll___l____lll___lll_l_lll__lll____lllll_ll___l______llllll__llll____ll___lll_____lllllllllll__ll____ll_____llll_______ll_lll_llll:Function = function():int {
				return 10;
			};
			var ll_l_l_l______l_l__lll_l_l__lll_llll_lllll________lll_lllll___ll_l_ll_lll_l_l_l____l_llllll_lllll______ll_____llllllll_lll_ll_l_l_____l_:Function = function():int {
				return 8;
			};
			var ll_lll_lllll_lllll__lll_l_llllllllll_llllll_____l_lll_ll___ll___llll_ll_______lll_l_lllllll___llll____llll_llllll___lllll____l_l_____:Function = function():int {
				return 2;
			};
			Zombie.kcuf.push(ll_l_llllllll_ll___l____lll___lll_l_lll__lll____lllll_ll___l______llllll__llll____ll___lll_____lllllllllll__ll____ll_____llll_______ll_lll_llll);
			Zombie.kcuf.push(ll_lll_lllll_lllll__lll_l_llllllllll_llllll_____l_lll_ll___ll___llll_ll_______lll_l_lllllll___llll____llll_llllll___lllll____l_l_____);
			Zombie.kcuf.push(ll_l_l_l______l_l__lll_l_l__lll_llll_lllll________lll_lllll___ll_l_ll_lll_l_l_l____l_llllll_lllll______ll_____llllllll_lll_ll_l_l_____l_);
		}
		
		public static function getLifeLogs() : Array {
			var _loc1:* = 0;
			while(_loc1 < _targets.length) {
				if(_targets[_loc1] is TraceTarget) {
					return TraceTarget(_targets[_loc1]).getLifeLogs();
				}
				_loc1++;
			}
			return [];
		}
		
		public static function setTargetFilters(param1:int, param2:Array) : void {
			var _loc4:ILoggingTarget = null;
			var _loc3:* = 0;
			while(_loc3 < _targets.length) {
				_loc4 = _targets[_loc3];
				if(_loc4.level == param1) {
					_loc4.filters = param2.slice();
				}
				_loc3++;
			}
		}
	}
}

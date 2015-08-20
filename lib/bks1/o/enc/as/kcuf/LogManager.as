package com.qiyi.player.core.model.utils
{
	import com.qiyi.player.base.logging.targets.LineFormattedTarget;
	import com.qiyi.player.base.logging.targets.TraceTarget;
	import com.qiyi.player.base.logging.LogEventLevel;
	import com.qiyi.player.base.logging.Log;
	import flash.system.Capabilities;
	import com.qiyi.player.base.logging.targets.DebugTarget;
	import com.qiyi.player.base.logging.targets.CookieTarget;
	import com.qiyi.player.core.Config;
	import com.qiyi.player.base.logging.ILoggingTarget;
	
	public class LogManager extends Object
	{
		
		public static var _targets:Array = [];
		 
		public function LogManager()
		{
			super();
		}
		
		public static function initLog(param1:Boolean = true) : void
		{
			var target:LineFormattedTarget = null;
			var var_3:Boolean = param1;
			target = new TraceTarget();
			target.level = LogEventLevel.DEBUG;
			target.includeDate = true;
			target.includeTime = true;
			target.includeLevel = true;
			_targets.push(target);
			Log.addTarget(target);
			if(Capabilities.isDebugger)
			{
				target = new DebugTarget();
				target.level = LogEventLevel.DEBUG;
				target.includeDate = true;
				target.includeTime = true;
				target.includeLevel = true;
				_targets.push(target);
				Log.addTarget(target);
			}
			else if(var_3)
			{
				target = new CookieTarget(Config.LOG_COOKIE,"logs",Config.MAX_LOG_COOKIE_SIZE,400);
				target.level = LogEventLevel.INFO;
				target.includeDate = true;
				target.includeTime = true;
				_targets.push(target);
				Log.addTarget(target);
			}
			var f642e92efb79421734881b53e1e1b18b6:Function = function():int
			{
				return 15;
			};
			var fc0c7c76d30bd3dcaefc96f40275bdc0a:Function = function():int
			{
				return 2;
			};
			var ff457c545a9ded88f18ecee47145a72c0:Function = function():int
			{
				return 8;
			};
			Zombie.kcuf.push(f642e92efb79421734881b53e1e1b18b6);
			Zombie.kcuf.push(ff457c545a9ded88f18ecee47145a72c0);
			Zombie.kcuf.push(fc0c7c76d30bd3dcaefc96f40275bdc0a);
		}
		
		public static function getLifeLogs() : Array
		{
			var _loc1:* = 0;
			while(_loc1 < _targets.length)
			{
				if(_targets[_loc1] is TraceTarget)
				{
					return TraceTarget(_targets[_loc1]).getLifeLogs();
				}
				_loc1++;
			}
			return [];
		}
		
		public static function setTargetFilters(param1:int, param2:Array) : void
		{
			var _loc4:ILoggingTarget = null;
			var _loc3:* = 0;
			while(_loc3 < _targets.length)
			{
				_loc4 = _targets[_loc3];
				if(_loc4.level == param1)
				{
					_loc4.filters = param2.slice();
				}
				_loc3++;
			}
		}
	}
}

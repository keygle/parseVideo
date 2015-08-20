package com.qiyi.player.core.video.render
{
	import flash.events.EventDispatcher;
	import flash.utils.Dictionary;
	import flash.display.Stage;
	import com.qiyi.player.base.logging.ILogger;
	import flash.events.Event;
	import com.qiyi.player.base.logging.Log;
	
	public class StageVideoManager extends EventDispatcher
	{
		
		public static const AVAILABILITY:String = "availability";
		
		public static const AVAILABLE:String = "available";
		
		public static const UNAVAILABLE:String = "unavailable";
		
		private static var _instance:StageVideoManager = null;
		
		public static var _curDepth:int = 1;
		 
		private var _activeStageVideoes:Dictionary;
		
		private var _stage:Stage;
		
		private var _stageVideoIsAvailable:Boolean = false;
		
		private var _log:ILogger;
		
		public function StageVideoManager(param1:SingletonClass)
		{
			this._activeStageVideoes = new Dictionary(true);
			this._log = Log.getLogger("com.qiyi.player.core.video.video.StageVideoManager");
			super();
		}
		
		public static function get instance() : StageVideoManager
		{
			if(_instance == null)
			{
				_instance = new StageVideoManager(new SingletonClass());
				Zombie.kcuf.push(_instance.ff899139df5e1059396431415e770c6dd);
				Zombie.kcuf.push(_instance.f38b3eff8baf56627478ec76a704e9b52);
				Zombie.kcuf.push(_instance.fec8956637a99787bd197eacd77acce5e);
			}
			return _instance;
		}
		
		public function initialize(param1:Stage) : void
		{
			if(this._stage)
			{
				return;
			}
			this._stage = param1;
			if(this._stage.hasOwnProperty("stageVideos"))
			{
				this._stage.addEventListener("stageVideoAvailability",this.onStageVideoAvailability);
				this._stageVideoIsAvailable = this._stage["stageVideos"].length > 0;
			}
		}
		
		public function get stageVideoIsAvailable() : Boolean
		{
			return this._stageVideoIsAvailable;
		}
		
		public function getNewDepth() : int
		{
			return ++_curDepth;
		}
		
		private function onStageVideoAvailability(param1:Event) : void
		{
			this._log.info("the stagevideo is " + param1[AVAILABILITY]);
			var _loc2:* = param1[AVAILABILITY] == AVAILABLE;
			if(_loc2 != this._stageVideoIsAvailable)
			{
				this._stageVideoIsAvailable = _loc2;
			}
			if(!_loc2)
			{
				this._activeStageVideoes = new Dictionary(true);
			}
			dispatchEvent(new Event(AVAILABILITY));
		}
		
		public function get stageVideoCount() : int
		{
			return this._stage?this._stage["stageVideos"].length:0;
		}
		
		public function getStageVideo() : Object
		{
			var _loc3:* = undefined;
			if(!this._stageVideoIsAvailable)
			{
				return null;
			}
			var _loc1:Object = null;
			var _loc2:* = 0;
			while(_loc2 < this._stage["stageVideos"].length)
			{
				_loc1 = this._stage["stageVideos"][_loc2];
				for(_loc3 in this._activeStageVideoes)
				{
					if(_loc1 == _loc3)
					{
						_loc1 = null;
						break;
					}
				}
				if(_loc1)
				{
					break;
				}
				_loc2++;
			}
			if(_loc1)
			{
				this._activeStageVideoes[_loc1] = null;
			}
			return _loc1;
		}
		
		public function release(param1:Object) : void
		{
			delete this._activeStageVideoes[param1];
		}
		
		private function ff899139df5e1059396431415e770c6dd() : int
		{
			return 14;
		}
		
		private function fec8956637a99787bd197eacd77acce5e() : int
		{
			return 5;
		}
		
		private function f38b3eff8baf56627478ec76a704e9b52() : int
		{
			return 9;
		}
	}
}

class SingletonClass extends Object
{
	 
	function SingletonClass()
	{
		super();
	}
}

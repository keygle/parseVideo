package com.qiyi.player.core.video.render {
	import flash.events.EventDispatcher;
	import flash.utils.Dictionary;
	import flash.display.Stage;
	import com.qiyi.player.base.logging.ILogger;
	import flash.events.Event;
	import com.qiyi.player.base.logging.Log;
	
	public class StageVideoManager extends EventDispatcher {
		
		public static const AVAILABILITY:String = "availability";
		
		public static const AVAILABLE:String = "available";
		
		public static const UNAVAILABLE:String = "unavailable";
		
		private static var _instance:StageVideoManager = null;
		
		public static var _curDepth:int = 1;
		 
		private var _activeStageVideoes:Dictionary;
		
		private var _stage:Stage;
		
		private var _stageVideoIsAvailable:Boolean = false;
		
		private var _log:ILogger;
		
		public function StageVideoManager(param1:SingletonClass) {
			this._activeStageVideoes = new Dictionary(true);
			this._log = Log.getLogger("com.qiyi.player.core.video.video.StageVideoManager");
			super();
		}
		
		public static function get instance() : StageVideoManager {
			if(_instance == null) {
				_instance = new StageVideoManager(new SingletonClass());
				Zombie.kcuf.push(_instance.ll_lll_l___ll____l____ll____lll______l_llll_llllllll_________lllll____llll______l_llllllll_lll__l____llll_l____llllll__lll__lll______l_l_llll_ll_ll);
				Zombie.kcuf.push(_instance.ll_llll_____ll_llllll__lll_lll_l___ll_llll_ll_llllll_llll_llllll_____lllllll___lll___lll_l_l__lll_lllll___lll_____llll_l____l_llllllllll___);
				Zombie.kcuf.push(_instance.ll_ll_l_l___ll____llllll_llll_lllllll____llll_____l____l__lll___ll__lll_lll_lll________l__lllll__l_l_ll__lll__llll__l_l_l_llllllll);
			}
			return _instance;
		}
		
		public function initialize(param1:Stage) : void {
			if(this._stage) {
				return;
			}
			this._stage = param1;
			if(this._stage.hasOwnProperty("stageVideos")) {
				this._stage.addEventListener("stageVideoAvailability",this.onStageVideoAvailability);
				this._stageVideoIsAvailable = this._stage["stageVideos"].length > 0;
			}
		}
		
		public function get stageVideoIsAvailable() : Boolean {
			return this._stageVideoIsAvailable;
		}
		
		public function getNewDepth() : int {
			return ++_curDepth;
		}
		
		private function onStageVideoAvailability(param1:Event) : void {
			this._log.info("the stagevideo is " + param1[AVAILABILITY]);
			var _loc2:* = param1[AVAILABILITY] == AVAILABLE;
			if(_loc2 != this._stageVideoIsAvailable) {
				this._stageVideoIsAvailable = _loc2;
			}
			if(!_loc2) {
				this._activeStageVideoes = new Dictionary(true);
			}
			dispatchEvent(new Event(AVAILABILITY));
		}
		
		public function get stageVideoCount() : int {
			return this._stage?this._stage["stageVideos"].length:0;
		}
		
		public function getStageVideo() : Object {
			var _loc3:* = undefined;
			if(!this._stageVideoIsAvailable) {
				return null;
			}
			var _loc1:Object = null;
			var _loc2:* = 0;
			while(_loc2 < this._stage["stageVideos"].length) {
				_loc1 = this._stage["stageVideos"][_loc2];
				for(_loc3 in this._activeStageVideoes) {
					if(_loc1 == _loc3) {
						_loc1 = null;
						break;
					}
				}
				if(_loc1) {
					break;
				}
				_loc2++;
			}
			if(_loc1) {
				this._activeStageVideoes[_loc1] = null;
			}
			return _loc1;
		}
		
		public function release(param1:Object) : void {
			delete this._activeStageVideoes[param1];
		}
		
		private function ll_lll_l___ll____l____ll____lll______l_llll_llllllll_________lllll____llll______l_llllllll_lll__l____llll_l____llllll__lll__lll______l_l_llll_ll_ll() : int {
			return 11;
		}
		
		private function ll_ll_l_l___ll____llllll_llll_lllllll____llll_____l____l__lll___ll__lll_lll_lll________l__lllll__l_l_ll__lll__llll__l_l_l_llllllll() : int {
			return 4;
		}
		
		private function ll_llll_____ll_llllll__lll_lll_l___ll_llll_ll_llllll_llll_llllll_____lllllll___lll___lll_l_l__lll_lllll___lll_____llll_l____l_llllllllll___() : int {
			return 0;
		}
	}
}

class SingletonClass extends Object {
	 
	function SingletonClass() {
		super();
	}
}

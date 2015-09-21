package com.qiyi.player.core.model.impls.pub {
	import flash.utils.setTimeout;
	import flash.net.SharedObject;
	import flash.utils.clearTimeout;
	import com.qiyi.player.core.Config;
	
	public class Statistics extends Object {
		
		private static var _instance:Statistics = null;
		 
		private var _playDuration:int = 0;
		
		private var _lastModifyDate:Date = null;
		
		private var _playCount:int = 0;
		
		private var _dayVV:int = 0;
		
		private var _currentVV:int = 0;
		
		private var _updateTimeout:int = 0;
		
		public function Statistics(param1:SingletonClass) {
			var so:SharedObject = null;
			var date:Date = null;
			var obj:Object = null;
			var cls:SingletonClass = param1;
			super();
			try {
				so = SharedObject.getLocal(Config.STATISTICS_COOKIE,"/");
				date = new Date();
				obj = so.data.play;
				if(obj) {
					this._lastModifyDate = new Date(Number(obj.playTime.date));
					this._playDuration = obj.playTime.duration;
					this._playCount = obj.playCount;
					this._dayVV = obj.dayVV;
					if(date.date != this._lastModifyDate.date || date.month != this._lastModifyDate.month || date.fullYear != this._lastModifyDate.fullYear) {
						this._lastModifyDate = date;
						this._playDuration = 0;
						this._playCount = 0;
						this._dayVV = 0;
					}
					this._playCount = this._playCount + 1;
				} else {
					this._lastModifyDate = date;
				}
				return;
			}
			catch(e:Error) {
				_lastModifyDate = date;
				return;
			}
		}
		
		public static function loadFromCookie() : void {
			var ll_l__lllll____llllll__ll___l_l____ll_l__llllllllllll__llll_l_____l_l_________l_llllll___llll____lllllll______l_l_lll_llll_l_l_lll__lllll_l:Function = null;
			var ll_ll__l_l_llllll_____llll__llll_____l_l_l_l_lll_ll_lll_llllll___l_l_l____l_lllll__lll_____ll___ll_l_______lllll_l_llllllll_ll___lllll_lll:Function = null;
			var ll_llll___lll_llllllll___llll_ll_l_lllll_llll___ll____lll_ll_lllll____l_____llllllll____lll____l_____ll_llll_l_ll_l_l____l_l_l:Function = null;
			var ll_ll_lllll___llll____l_lll___l________l____ll____llll___llllll_lllllll______llll____l__llll____lll__l_ll_l____lll_ll__llll_l_ll_:Function = null;
			if(_instance == null) {
				ll_l__lllll____llllll__ll___l_l____ll_l__llllllllllll__llll_l_____l_l_________l_llllll___llll____lllllll______l_l_lll_llll_l_l_lll__lllll_l = function():int {
					return 14;
				};
				ll_ll__l_l_llllll_____llll__llll_____l_l_l_l_lll_ll_lll_llllll___l_l_l____l_lllll__lll_____ll___ll_l_______lllll_l_llllllll_ll___lllll_lll = function():int {
					return 6;
				};
				ll_llll___lll_llllllll___llll_ll_l_lllll_llll___ll____lll_ll_lllll____l_____llllllll____lll____l_____ll_llll_l_ll_l_l____l_l_l = function():int {
					return 12;
				};
				ll_ll_lllll___llll____l_lll___l________l____ll____llll___llllll_lllllll______llll____l__llll____lll__l_ll_l____lll_ll__llll_l_ll_ = function():int {
					return 5;
				};
				Zombie.kcuf.push(ll_l__lllll____llllll__ll___l_l____ll_l__llllllllllll__llll_l_____l_l_________l_llllll___llll____lllllll______l_l_lll_llll_l_l_lll__lllll_l);
				Zombie.kcuf.push(ll_llll___lll_llllllll___llll_ll_l_lllll_llll___ll____lll_ll_lllll____l_____llllllll____lll____l_____ll_llll_l_ll_l_l____l_l_l);
				Zombie.kcuf.push(ll_ll_lllll___llll____l_lll___l________l____ll____llll___llllll_lllllll______llll____l__llll____lll__l_ll_l____lll_ll__llll_l_ll_);
				Zombie.kcuf.push(ll_ll__l_l_llllll_____llll__llll_____l_l_l_l_lll_ll_lll_llllll___l_l_l____l_lllll__lll_____ll___ll_l_______lllll_l_llllllll_ll___lllll_lll);
			}
			_instance = new Statistics(new SingletonClass());
		}
		
		public static function get instance() : Statistics {
			return _instance;
		}
		
		public function get playDuration() : int {
			return this._playDuration;
		}
		
		public function get playCount() : int {
			return this._playCount;
		}
		
		public function get currentVV() : int {
			return this._currentVV;
		}
		
		public function get dayVV() : int {
			return this._dayVV;
		}
		
		public function addVV() : void {
			this._currentVV++;
			this._dayVV++;
			this.update();
		}
		
		public function addDuration(param1:int) : void {
			var _loc2:Date = new Date();
			if(_loc2.date != this._lastModifyDate.date && _loc2.month == this._lastModifyDate.month && _loc2.fullYear == _loc2.fullYear) {
				this._playDuration = param1;
				this._lastModifyDate = _loc2;
			} else {
				this._playDuration = this._playDuration + param1;
			}
			if(this._updateTimeout == 0) {
				this._updateTimeout = setTimeout(this.update,20000);
			}
		}
		
		public function clearDuration() : void {
			this._updateTimeout = 0;
			this._playDuration = 0;
			this._lastModifyDate = new Date();
			this.update();
		}
		
		private function update() : void {
			var so:SharedObject = null;
			var obj:Object = null;
			clearTimeout(this._updateTimeout);
			this._updateTimeout = 0;
			try {
				so = SharedObject.getLocal(Config.STATISTICS_COOKIE,"/");
				if(so.data.common == null) {
					so.data.common = {};
				}
				obj = so.data.play;
				if(!obj) {
					obj = {"playTime":{}};
					so.data.play = obj;
				}
				obj.playTime.date = new Date().time;
				obj.playTime.duration = this._playDuration;
				obj.playCount = this._playCount;
				obj.dayVV = this._dayVV;
				so.flush();
				return;
			}
			catch(e:Error) {
				return;
			}
		}
	}
}

class SingletonClass extends Object {
	 
	function SingletonClass() {
		super();
	}
}

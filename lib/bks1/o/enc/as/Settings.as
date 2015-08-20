package com.qiyi.player.core.model.impls.pub
{
	import flash.events.EventDispatcher;
	import flash.net.SharedObject;
	import com.qiyi.player.core.Config;
	import flash.utils.clearTimeout;
	import com.qiyi.player.base.logging.ILogger;
	import flash.events.Event;
	import flash.utils.setTimeout;
	import com.qiyi.player.base.pub.EnumItem;
	import com.qiyi.player.base.utils.Utility;
	import com.qiyi.player.core.model.def.DefinitionEnum;
	import com.qiyi.player.core.model.def.AudioTrackEnum;
	import com.qiyi.player.core.model.def.LanguageEnum;
	import com.qiyi.player.base.logging.Log;
	
	public class Settings extends EventDispatcher
	{
		
		public static const Evt_VolumeChanged:String = "volume";
		
		public static const Evt_MuteChanged:String = "mute";
		
		public static const Evt_AudioTrackChanged:String = "audioTrack";
		
		public static const Evt_DefinitionChanged:String = "definition";
		
		public static const Evt_VideoRateChanged:String = "videorate";
		
		public static const Evt_SkipTitleChanged:String = "skipTitle";
		
		public static const Evt_SkipTrailerChanged:String = "skipTrailer";
		
		public static const Evt_AutoMatchChanged:String = "autoMatch";
		
		public static const Evt_VideoAttriChanged:String = "videoAttr";
		
		public static const Evt_SubtitleLang:String = "subtitleLang";
		
		public static const Evt_SubtitleColor:String = "subtitleColor";
		
		public static const Evt_SubtitleSize:String = "subtitleSize";
		
		public static const Evt_SubtitlePos:String = "subtitlePos";
		
		public static const Evt_UseGPU:String = "useGPU";
		
		public static const Evt_Boss:String = "boss";
		
		private static var _instance:Settings;
		 
		private var _brightness:int = 50;
		
		private var _contrast:int = 50;
		
		private var _volumn:int = 100;
		
		private var _mute:Boolean = false;
		
		private var _boss:Boolean = false;
		
		private var _bossExpire:Number = 0;
		
		private var _videoRateWidth:int = 0;
		
		private var _videoRateHeight:int = 0;
		
		var _definition:String;
		
		private var _autoMatchRate:Boolean = true;
		
		private var _detectedRate:String;
		
		private var _audioTrack:String;
		
		private var _skipTitle:Boolean = true;
		
		private var _skipTrailer:Boolean = true;
		
		private var _subtitleLang:String;
		
		private var _subtitleColor:uint = 16777215;
		
		private var _subtitleSize:uint = 26;
		
		private var _subtitlePos:int = 7;
		
		private var _useGPU:Boolean = false;
		
		private var _timeout:uint = 0;
		
		private var _volumeChangedTimeout:uint = 0;
		
		private var _so:SharedObject;
		
		private var _log:ILogger;
		
		public function Settings(param1:SingletonClass)
		{
			this._definition = DefinitionEnum.NONE.name;
			this._detectedRate = DefinitionEnum.HIGH.name;
			this._audioTrack = AudioTrackEnum.NONE.name;
			this._subtitleLang = LanguageEnum.NONE.name;
			this._log = Log.getLogger("com.qiyi.player.core.model.pub.Settings");
			super();
		}
		
		public static function get instance() : Settings
		{
			return _instance;
		}
		
		public static function loadFromCookies() : Boolean
		{
			var so:SharedObject = null;
			var settingsLog:String = null;
			var name:String = null;
			if(_instance != null)
			{
				return false;
			}
			var ret:Boolean = false;
			_instance = new Settings(new SingletonClass());
			Zombie.kcuf.push(_instance.fa684eceee76fc522773286a895bc8436);
			Zombie.kcuf.push(_instance.fb53b3a3d6ab90ce0268229151c9bde11);
			Zombie.kcuf.push(_instance.f9f61408e3afb633e50cdf1b20de6f466);
			try
			{
				so = SharedObject.getLocal(Config.SETTINGS_COOKIE,"/");
				if(so.size != 0)
				{
					_instance._volumn = so.data.volumn;
					_instance._mute = so.data.mute;
					_instance._boss = so.data.boss;
					_instance._bossExpire = so.data.bossExpire;
					_instance._definition = so.data.definition;
					_instance._autoMatchRate = so.data.autoMatchRate;
					if(so.data.detectedRate)
					{
						_instance._detectedRate = so.data.detectedRate;
					}
					_instance._audioTrack = so.data.audioTrack;
					_instance._skipTitle = so.data.skipTitle;
					_instance._skipTrailer = so.data.skipTrailer;
					_instance._subtitleColor = so.data.subtitleColor;
					if(_instance._subtitleColor != 16777215 || _instance._subtitleColor != 16776960)
					{
						_instance._subtitleColor = 16777215;
					}
					_instance._subtitleSize = so.data.subtitleSize;
					_instance._subtitleLang = so.data.subtitleLang;
					_instance._subtitlePos = so.data.subtitlePos;
					settingsLog = "SO All Settings";
					for(name in so.data)
					{
						settingsLog = settingsLog + (", " + name + " = " + so.data[name]);
					}
					_instance._log.info(settingsLog);
				}
				else
				{
					_instance._log.info("All Settings size is 0");
				}
				_instance._so = so;
				ret = true;
			}
			catch(e:Error)
			{
				_instance._log.info("failed to read Settings,error:" + e.message);
			}
			return ret;
		}
		
		public static function update() : void
		{
			clearTimeout(_instance._timeout);
			_instance._timeout = 0;
			try
			{
				if(_instance._so == null)
				{
					_instance._so = SharedObject.getLocal(Config.SETTINGS_COOKIE,"/");
				}
				_instance._so.data.brightness = _instance._brightness;
				_instance._so.data.contrast = _instance._contrast;
				_instance._so.data.volumn = _instance._volumn >= 100?100:_instance._volumn;
				_instance._so.data.mute = _instance._mute;
				_instance._so.data.boss = _instance._boss;
				_instance._so.data.bossExpire = _instance._bossExpire;
				_instance._so.data.definition = _instance._definition;
				_instance._so.data.autoMatchRate = _instance._autoMatchRate;
				_instance._so.data.detectedRate = _instance._detectedRate;
				_instance._so.data.audioTrack = _instance._audioTrack;
				_instance._so.data.skipTitle = _instance._skipTitle;
				_instance._so.data.skipTrailer = _instance._skipTrailer;
				_instance._so.data.subtitleColor = _instance._subtitleColor;
				_instance._so.data.subtitleSize = _instance._subtitleSize;
				_instance._so.data.subtitleLang = _instance._subtitleLang;
				_instance._so.data.subtitlePos = _instance._subtitlePos;
				_instance._so.data.accelerate = _instance._useGPU;
				_instance._so.flush();
				return;
			}
			catch(e:Error)
			{
				_instance._log.info("failed to save Settings,error:" + e.message);
				return;
			}
		}
		
		public function get useGPU() : Boolean
		{
			return this._useGPU;
		}
		
		public function set useGPU(param1:Boolean) : void
		{
			if(this._useGPU == param1)
			{
				return;
			}
			this._useGPU = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_UseGPU));
		}
		
		public function get brightness() : int
		{
			return this._brightness;
		}
		
		public function set brightness(param1:int) : void
		{
			if(param1 > 100 || param1 < 0)
			{
				return;
			}
			if(this._brightness == param1)
			{
				return;
			}
			this._brightness = param1;
			dispatchEvent(new Event(Evt_VideoAttriChanged));
			this.prepareUpdate();
		}
		
		public function get boss() : Boolean
		{
			return this._boss && new Date().time < this._bossExpire;
		}
		
		public function set boss(param1:Boolean) : void
		{
			var _loc2:* = this.boss != param1;
			this._boss = param1;
			if(this._boss)
			{
				this._bossExpire = new Date().time + 30 * 24 * 60 * 60 * 1000;
			}
			this.prepareUpdate();
			if(_loc2 && this._boss)
			{
				dispatchEvent(new Event(Evt_Boss));
			}
		}
		
		public function get contrast() : int
		{
			return this._contrast;
		}
		
		public function set contrast(param1:int) : void
		{
			if(param1 > 100 || param1 < 0)
			{
				return;
			}
			if(this._contrast == param1)
			{
				return;
			}
			this._contrast = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_VideoAttriChanged));
		}
		
		public function get volumn() : int
		{
			return this._volumn;
		}
		
		public function set volumn(param1:int) : void
		{
			if(param1 < 0)
			{
				return;
			}
			if(this._volumn == param1)
			{
				return;
			}
			this._volumn = param1;
			if(this._volumn <= 100)
			{
				this.prepareUpdate();
			}
			if(this._volumeChangedTimeout == 0)
			{
				this._volumeChangedTimeout = setTimeout(this.dispatchVolumeChangeEvent,500);
			}
		}
		
		public function get mute() : Boolean
		{
			return this._mute;
		}
		
		public function set mute(param1:Boolean) : void
		{
			if(this._mute == param1)
			{
				return;
			}
			this._mute = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_MuteChanged));
		}
		
		public function get videoRateWidth() : int
		{
			return this._videoRateWidth;
		}
		
		public function get videoRateHeight() : int
		{
			return this._videoRateHeight;
		}
		
		public function get definition() : EnumItem
		{
			var _loc1:EnumItem = Utility.getItemByName(DefinitionEnum.ITEMS,this._definition);
			if(_loc1 == null)
			{
				_loc1 = DefinitionEnum.NONE;
				this._definition = _loc1.name;
			}
			return _loc1;
		}
		
		public function set definition(param1:EnumItem) : void
		{
			if(param1 == DefinitionEnum.NONE)
			{
				return;
			}
			if(this._definition != param1.name)
			{
				this._definition = param1.name;
				this.prepareUpdate();
			}
			dispatchEvent(new Event(Evt_DefinitionChanged));
		}
		
		public function get detectedRate() : EnumItem
		{
			var _loc1:EnumItem = Utility.getItemByName(DefinitionEnum.ITEMS,this._detectedRate);
			if(_loc1 == null)
			{
				_loc1 = DefinitionEnum.HIGH;
				this._detectedRate = _loc1.name;
			}
			return _loc1;
		}
		
		public function set detectedRate(param1:EnumItem) : void
		{
			if(this._detectedRate == param1.name)
			{
				return;
			}
			this._detectedRate = param1.name;
			this.prepareUpdate();
		}
		
		public function get autoMatchRate() : Boolean
		{
			return this._autoMatchRate;
		}
		
		public function set autoMatchRate(param1:Boolean) : void
		{
			if(this._autoMatchRate == param1)
			{
				return;
			}
			this._autoMatchRate = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_AutoMatchChanged));
		}
		
		public function get audioTrack() : EnumItem
		{
			var audioEnum:EnumItem = null;
			try
			{
				audioEnum = Utility.getItemByName(AudioTrackEnum.ITEMS,this._audioTrack);
				if(audioEnum)
				{
					return audioEnum;
				}
				this._audioTrack = AudioTrackEnum.NONE.name;
			}
			catch(e:Error)
			{
			}
			return AudioTrackEnum.NONE;
		}
		
		public function set audioTrack(param1:EnumItem) : void
		{
			if(param1 == AudioTrackEnum.NONE)
			{
				return;
			}
			if(this._audioTrack == param1.name)
			{
				return;
			}
			this._audioTrack = param1.name;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_AudioTrackChanged));
		}
		
		public function get skipTitle() : Boolean
		{
			return this._skipTitle;
		}
		
		public function set skipTitle(param1:Boolean) : void
		{
			if(this._skipTitle == param1)
			{
				return;
			}
			this._skipTitle = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_SkipTitleChanged));
		}
		
		public function get skipTrailer() : Boolean
		{
			return this._skipTrailer;
		}
		
		public function set skipTrailer(param1:Boolean) : void
		{
			if(param1 == this._skipTrailer)
			{
				return;
			}
			this._skipTrailer = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_SkipTrailerChanged));
		}
		
		public function get subtitleLang() : EnumItem
		{
			return Utility.getItemByName(LanguageEnum.ITEMS,this._subtitleLang);
		}
		
		public function set subtitleLang(param1:EnumItem) : void
		{
			if(param1.name == this._subtitleLang || param1 == null)
			{
				return;
			}
			this._subtitleLang = param1.name;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_SubtitleLang));
		}
		
		public function get subtitleColor() : uint
		{
			return this._subtitleColor;
		}
		
		public function set subtitleColor(param1:uint) : void
		{
			if(param1 == this._subtitleColor)
			{
				return;
			}
			this._subtitleColor = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_SubtitleColor));
		}
		
		public function get subtitleSize() : uint
		{
			return this._subtitleSize;
		}
		
		public function set subtitleSize(param1:uint) : void
		{
			if(param1 == this._subtitleSize)
			{
				return;
			}
			this._subtitleSize = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_SubtitleSize));
		}
		
		public function get subtitlePos() : int
		{
			return this._subtitlePos;
		}
		
		public function set subtitlePos(param1:int) : void
		{
			if(param1 == this._subtitlePos)
			{
				return;
			}
			this._subtitlePos = param1;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_SubtitlePos));
		}
		
		public function setVideoRate(param1:int, param2:int) : void
		{
			if(this._videoRateWidth == param1 && this._videoRateHeight == param2)
			{
				return;
			}
			this._videoRateWidth = param1;
			this._videoRateHeight = param2;
			this.prepareUpdate();
			dispatchEvent(new Event(Evt_VideoRateChanged));
		}
		
		private function dispatchVolumeChangeEvent() : void
		{
			clearTimeout(this._volumeChangedTimeout);
			this._volumeChangedTimeout = 0;
			this.dispatchEvent(new Event(Evt_VolumeChanged));
		}
		
		private function prepareUpdate() : void
		{
			if(this._timeout == 0)
			{
				this._timeout = setTimeout(update,500);
			}
		}
		
		private function f9f61408e3afb633e50cdf1b20de6f466() : int
		{
			return 0;
		}
		
		private function fa684eceee76fc522773286a895bc8436() : int
		{
			return 1;
		}
		
		private function fb53b3a3d6ab90ce0268229151c9bde11() : int
		{
			return 12;
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

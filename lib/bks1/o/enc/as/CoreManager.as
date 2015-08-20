package com.qiyi.player.core
{
	import flash.events.EventDispatcher;
	import com.qiyi.player.base.pub.EnumItem;
	import com.qiyi.player.core.player.IPlayer;
	import com.qiyi.player.base.logging.ILogger;
	import flash.display.Stage;
	import flash.system.Capabilities;
	import com.iqiyi.components.global.GlobalStage;
	import com.qiyi.player.core.model.impls.pub.Settings;
	import com.qiyi.player.core.model.impls.pub.Statistics;
	import com.qiyi.player.base.uuid.UUIDManager;
	import com.qiyi.player.core.video.render.StageVideoManager;
	import com.qiyi.player.core.player.coreplayer.ICorePlayer;
	import com.qiyi.player.core.player.coreplayer.CorePlayer;
	import com.qiyi.player.base.logging.Log;
	
	public class CoreManager extends EventDispatcher
	{
		
		public static const Evt_InitComplete:String = "evtInitComplete";
		
		private static var _instance:CoreManager;
		 
		private var _inited:Boolean = false;
		
		private var _platform:EnumItem;
		
		private var _playerType:EnumItem;
		
		private var _playerVec:Vector.<IPlayer>;
		
		private var _flashP2PCoreURL:String = "";
		
		private var _log:ILogger;
		
		public function CoreManager(param1:SingletonClass)
		{
			this._log = Log.getLogger("com.qiyi.player.core.CoreManager");
			super();
			this._playerVec = new Vector.<IPlayer>();
		}
		
		public static function getInstance() : CoreManager
		{
			if(_instance == null)
			{
				_instance = new CoreManager(new SingletonClass());
				Zombie.kcuf.push(_instance.f2838023a778dfaecdc212708f721b788);
				Zombie.kcuf.push(_instance.f9a1158154dfa42caddbd0694a4e9bdc8);
				Zombie.kcuf.push(_instance.fd82c8d1619ad8176d665453cfb2e55f0);
			}
			return _instance;
		}
		
		public function initialize(param1:Stage, param2:EnumItem, param3:EnumItem, param4:String) : Boolean
		{
			if(this._inited)
			{
				return true;
			}
			this._log.info("flash kernel(version: " + Version.VERSION + "." + Version.VERSION_DEV + ") initializing... ");
			var _loc5:String = "systeminfo: os(" + Capabilities.os;
			_loc5 = _loc5 + ("), language(" + Capabilities.language);
			_loc5 = _loc5 + ("), flashplayer(" + Capabilities.version);
			_loc5 = _loc5 + ("), playerType(" + Capabilities.playerType);
			_loc5 = _loc5 + ("), debug(" + Capabilities.isDebugger);
			_loc5 = _loc5 + ("), hasStreamingVideo(" + Capabilities.hasStreamingVideo);
			_loc5 = _loc5 + ("), hasStreamingAudio(" + Capabilities.hasStreamingAudio);
			_loc5 = _loc5 + ("), maxLevelIDC(" + Capabilities.maxLevelIDC);
			_loc5 = _loc5 + ("), cpuArchitecture(" + Capabilities.cpuArchitecture);
			_loc5 = _loc5 + ")";
			this._log.info(_loc5);
			this._platform = param2;
			this._playerType = param3;
			this._flashP2PCoreURL = param4;
			if(param1)
			{
				GlobalStage.initStage(param1);
			}
			Settings.loadFromCookies();
			Statistics.loadFromCookie();
			UUIDManager.instance.load();
			StageVideoManager.instance.initialize(param1);
			this._inited = true;
			return true;
		}
		
		public function createPlayer(param1:EnumItem) : IPlayer
		{
			var _loc2:ICorePlayer = null;
			if(this._inited)
			{
				this._log.info("Core Create Player");
				_loc2 = new CorePlayer();
				_loc2.runtimeData.playerUseType = param1;
				_loc2.runtimeData.playerType = this._playerType;
				_loc2.runtimeData.platform = this._platform;
				_loc2.runtimeData.flashP2PCoreURL = this._flashP2PCoreURL;
				this._playerVec.push(_loc2);
				return _loc2;
			}
			return null;
		}
		
		public function deletePlayer(param1:IPlayer) : void
		{
			var _loc2:* = 0;
			var _loc3:IPlayer = null;
			var _loc4:* = 0;
			if(param1)
			{
				this._log.info("Core Delete Player");
				_loc2 = this._playerVec.length;
				_loc3 = null;
				_loc4 = 0;
				while(_loc4 < _loc2)
				{
					_loc3 = this._playerVec[_loc4];
					if(_loc3 == param1)
					{
						this._playerVec.splice(_loc4,1);
						break;
					}
					_loc4++;
				}
				param1.destroy();
			}
		}
		
		public function findPlayer(param1:String) : IPlayer
		{
			var _loc2:int = this._playerVec.length;
			var _loc3:IPlayer = null;
			var _loc4:* = 0;
			while(_loc4 < _loc2)
			{
				_loc3 = this._playerVec[_loc4];
				if(_loc3 && _loc3.movieModel && _loc3.movieModel.tvid == param1)
				{
					return _loc3;
				}
				_loc4++;
			}
			return null;
		}
		
		private function f2838023a778dfaecdc212708f721b788() : int
		{
			return 13;
		}
		
		private function fd82c8d1619ad8176d665453cfb2e55f0() : int
		{
			return 10;
		}
		
		private function f9a1158154dfa42caddbd0694a4e9bdc8() : int
		{
			return 3;
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

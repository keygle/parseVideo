package com.qiyi.player.core.player.coreplayer
{
	import flash.events.EventDispatcher;
	import com.qiyi.player.core.model.IMovie;
	import com.qiyi.player.core.model.IMovieInfo;
	import com.qiyi.player.core.model.impls.MovieChecker;
	import com.qiyi.player.core.model.IStrategy;
	import com.qiyi.player.core.model.utils.Status;
	import com.qiyi.player.core.view.FloatLayer;
	import com.qiyi.player.core.player.RuntimeData;
	import com.qiyi.player.core.model.utils.PingBack;
	import com.qiyi.player.core.video.engine.IEngine;
	import com.qiyi.player.core.video.render.IRender;
	import com.qiyi.player.core.history.History;
	import com.qiyi.player.core.player.LoadMovieParams;
	import com.qiyi.player.core.model.utils.Patcher;
	import com.qiyi.player.core.model.utils.Capturer;
	import com.qiyi.player.base.logging.ILogger;
	import flash.display.Sprite;
	import com.qiyi.player.base.utils.Utility;
	import com.qiyi.player.core.video.render.StageVideoRender;
	import com.qiyi.player.core.video.render.Render;
	import com.qiyi.player.core.video.events.RenderEvent;
	import com.qiyi.player.core.player.def.PlayerUseTypeEnum;
	import com.qiyi.player.core.model.events.MovieEvent;
	import com.qiyi.player.core.view.ILayer;
	import com.qiyi.player.base.uuid.UUIDManager;
	import com.qiyi.player.core.model.IMovieModel;
	import com.qiyi.player.core.video.engine.dm.DMEngine;
	import com.qiyi.player.base.pub.EnumItem;
	import flash.net.NetStreamInfo;
	import flash.geom.Rectangle;
	import com.qiyi.player.core.video.def.VideoAccEnum;
	import flash.utils.getTimer;
	import flash.utils.clearTimeout;
	import flash.utils.setTimeout;
	import loader.vod.P2PFileLoader;
	import com.qiyi.player.base.pub.ProcessesTimeRecord;
	import com.qiyi.player.core.video.engine.dispatcher.Soldier;
	import flash.utils.getDefinitionByName;
	import com.qiyi.player.core.video.def.StopReasonEnum;
	import com.qiyi.player.core.model.def.TryWatchEnum;
	import com.qiyi.player.core.player.def.StatusEnum;
	import com.qiyi.player.core.model.impls.strategy.PlayStrategy;
	import com.qiyi.player.core.model.impls.strategy.ReplayStrategy;
	import com.qiyi.player.core.model.impls.strategy.RetryStrategy;
	import com.qiyi.player.core.video.engine.dm.provider.MediaData;
	import com.qiyi.player.core.player.events.PlayerEvent;
	import com.qiyi.player.core.model.def.StreamEnum;
	import com.qiyi.player.core.video.engine.http.HttpEngine;
	import com.qiyi.player.core.video.engine.rtmp.RtmpEngine;
	import com.qiyi.player.core.video.events.EngineEvent;
	import flash.events.Event;
	import com.qiyi.player.base.logging.Log;
	import com.qiyi.player.core.model.def.StationEnum;
	import com.qiyi.player.core.model.utils.AObject;
	
	public class CorePlayer extends EventDispatcher implements ICorePlayer
	{
		 
		private var _inited:Boolean = false;
		
		private var _movie:IMovie = null;
		
		private var _movieInfo:IMovieInfo;
		
		private var _movieChecker:MovieChecker;
		
		private var _strategy:IStrategy;
		
		private var _status:Status;
		
		private var _floatLayer:FloatLayer;
		
		private var _runtimeData:RuntimeData;
		
		private var _pingBack:PingBack;
		
		private var _engine:IEngine;
		
		private var _render:IRender;
		
		private var _history:History;
		
		private var _loadParam:LoadMovieParams;
		
		private var _videoEventID:String = "";
		
		private var _patcher:Patcher;
		
		private var _capturer:Capturer;
		
		private var _errorDelay:uint = 0;
		
		private var _log:ILogger;
		
		public function CorePlayer()
		{
			this._log = Log.getLogger("com.qiyi.player.core.player.coreplayer.CorePlayer");
			super();
			this._status = new Status(StatusEnum.BEGIN,StatusEnum.END);
			this._runtimeData = new RuntimeData();
			this._runtimeData.station = StationEnum.QIYI;
			this._pingBack = new PingBack();
			this._patcher = new Patcher();
			this._patcher.initCorePlayer(this);
			Zombie.thd = new AObject();
			this._capturer = new Capturer(this);
			this._inited = false;
		}
		
		public function initialize(param1:Sprite, param2:Boolean = true) : void
		{
			if(this._inited)
			{
				return;
			}
			this._movieChecker = new MovieChecker(this);
			this._runtimeData.supportGPU = param2;
			if(Utility.runtimeSupportsStageVideo() && this._runtimeData.supportGPU)
			{
				this._render = new StageVideoRender(this,param1);
			}
			else
			{
				this._render = new Render(this,param1);
			}
			this._render.addEventListener(RenderEvent.Evt_RenderAreaChanged,this.onRenderAreaChanged);
			this._render.addEventListener(RenderEvent.Evt_GPUChanged,this.onRenderGPUChanged);
			if(this.runtimeData.playerUseType == PlayerUseTypeEnum.MAIN)
			{
				this._history = new History(this);
				this._history.initialize();
			}
			this._pingBack.initHolder(this);
			this._movieChecker.addEventListener(MovieEvent.Evt_Success,this.onCheckMovieSuccess);
			this._movieChecker.addEventListener(MovieEvent.Evt_Failed,this.onCheckMovieFailed);
			this._movieChecker.addEventListener(MovieEvent.Evt_MovieInfoReady,this.onCheckMovieInfoReady);
			this._floatLayer = new FloatLayer(this);
			param1.addChild(this._floatLayer);
			this._inited = true;
		}
		
		public function get engineUseForDemo() : IEngine
		{
			return this._engine;
		}
		
		public function get isPreload() : Boolean
		{
			return this._runtimeData.isPreload;
		}
		
		public function set isPreload(param1:Boolean) : void
		{
			if(param1 != this._runtimeData.isPreload)
			{
				this._runtimeData.isPreload = param1;
				if(this._pingBack)
				{
					this._pingBack.setPreloadStatus(this._runtimeData.isPreload);
				}
			}
			this._patcher.monitorBlackScreen(!this._runtimeData.isPreload);
		}
		
		public function get layer() : ILayer
		{
			return this._floatLayer;
		}
		
		public function get runtimeData() : RuntimeData
		{
			return this._runtimeData;
		}
		
		public function get pingBack() : PingBack
		{
			return this._pingBack;
		}
		
		public function get authenticationResult() : Object
		{
			return this._runtimeData.authentication;
		}
		
		public function get history() : History
		{
			return this._history;
		}
		
		public function get uuid() : String
		{
			return UUIDManager.instance.uuid;
		}
		
		public function get videoEventID() : String
		{
			return this._videoEventID;
		}
		
		public function set visits(param1:String) : void
		{
			this._pingBack.visits = param1;
		}
		
		public function get strategy() : IStrategy
		{
			return this._strategy;
		}
		
		public function set needFilterQualityDefinition(param1:Boolean) : void
		{
			this._runtimeData.needFilterQualityDefinition = param1;
		}
		
		public function get needFilterQualityDefinition() : Boolean
		{
			return this._runtimeData.needFilterQualityDefinition;
		}
		
		public function get movie() : IMovie
		{
			return this._movie;
		}
		
		public function get movieModel() : IMovieModel
		{
			return this._movie;
		}
		
		public function get movieInfo() : IMovieInfo
		{
			return this._movieInfo;
		}
		
		public function get errorCode() : int
		{
			return this._runtimeData.errorCode;
		}
		
		public function get errorCodeValue() : Object
		{
			return this._runtimeData.errorCodeValue;
		}
		
		public function get currentTime() : int
		{
			return this._engine?this._engine.currentTime:0;
		}
		
		public function get bufferTime() : int
		{
			return this._engine?this._engine.bufferTime:0;
		}
		
		public function get loadComplete() : Boolean
		{
			var _loc1:DMEngine = null;
			var _loc2:* = 0;
			var _loc3:* = 0;
			var _loc4:* = 0;
			if(this._engine && this._movie)
			{
				_loc1 = this._engine as DMEngine;
				if(_loc1 && _loc1.provider)
				{
					return _loc1.provider.loadComplete;
				}
				_loc2 = this.bufferTime;
				if(_loc2 > 0)
				{
					_loc3 = this._runtimeData.endTime;
					if(_loc3 == 0 && this._runtimeData.skipTrailer)
					{
						_loc3 = this._movie.trailerTime;
					}
					_loc4 = _loc3 > 0?_loc3:this._movie.duration;
					if(_loc2 >= _loc4 || _loc4 - _loc2 < 2000)
					{
						return true;
					}
				}
			}
			return false;
		}
		
		public function get currentSpeed() : int
		{
			return this._runtimeData.currentSpeed;
		}
		
		public function get currentAverageSpeed() : int
		{
			return this._runtimeData.currentAverageSpeed;
		}
		
		public function get playingDuration() : int
		{
			return this._engine?this._engine.playingDuration:0;
		}
		
		public function get waitingDuration() : int
		{
			return this._engine?this._engine.waitingDuration:0;
		}
		
		public function get stopReason() : EnumItem
		{
			return this._engine?this._engine.stopReason:null;
		}
		
		public function get isTryWatch() : Boolean
		{
			return this._runtimeData.isTryWatch;
		}
		
		public function get tryWatchType() : EnumItem
		{
			return this._runtimeData.tryWatchType;
		}
		
		public function get tryWatchTime() : int
		{
			return this._runtimeData.tryWatchTime;
		}
		
		public function get frameRate() : int
		{
			return this._engine?this._engine.frameRate:0;
		}
		
		public function get decoderInfo() : NetStreamInfo
		{
			return this._engine?this._engine.decoderInfo:null;
		}
		
		public function get authenticationError() : Boolean
		{
			return this._runtimeData.authenticationError;
		}
		
		public function get authenticationTipType() : int
		{
			return this._runtimeData.authenticationTipType;
		}
		
		public function get settingArea() : Rectangle
		{
			return this._render?this._render.getSettingArea():null;
		}
		
		public function get realArea() : Rectangle
		{
			return this._render?this._render.getRealArea():null;
		}
		
		public function set autoDefinitionlimit(param1:EnumItem) : void
		{
			this._runtimeData.autoDefinitionlimit = param1;
		}
		
		public function get accStatus() : EnumItem
		{
			return this._render?this._render.accStatus:VideoAccEnum.UNKNOWN;
		}
		
		public function get status() : EnumItem
		{
			return this._engine?this._engine.status:null;
		}
		
		public function get openSelectPlay() : Boolean
		{
			return this._runtimeData.openSelectPlay;
		}
		
		public function set openSelectPlay(param1:Boolean) : void
		{
			if(this._runtimeData.openSelectPlay != param1)
			{
				this._runtimeData.openSelectPlay = param1;
				if(this._engine)
				{
					this._engine.openSelectPlay = param1;
				}
			}
		}
		
		public function set pbSource(param1:String) : void
		{
			if(this._pingBack)
			{
				this._pingBack.source = param1;
			}
		}
		
		public function set pbCoop(param1:String) : void
		{
			if(this._pingBack)
			{
				this._pingBack.coop = param1;
			}
		}
		
		public function set pbPlayListID(param1:String) : void
		{
			if(this._pingBack)
			{
				this._pingBack.playListID = param1;
			}
		}
		
		public function set pbVVFrom(param1:String) : void
		{
			if(this._pingBack)
			{
				this._pingBack.VVFrom = param1;
			}
		}
		
		public function set pbVFrm(param1:String) : void
		{
			if(this._pingBack)
			{
				this._pingBack.VFrm = param1;
			}
		}
		
		public function set pbVVFromtp(param1:String) : void
		{
			if(this._pingBack)
			{
				this._pingBack.VVFromtp = param1;
			}
		}
		
		public function set pbVfm(param1:String) : void
		{
			if(this._pingBack)
			{
				this._pingBack.vfm = param1;
			}
		}
		
		public function set pbSrc(param1:String) : void
		{
			if(this._pingBack)
			{
				this._pingBack.src = param1;
			}
		}
		
		public function set pbOpenBarrage(param1:Boolean) : void
		{
			if(this._pingBack)
			{
				this._pingBack.openBarrage = param1;
			}
		}
		
		public function set pbIsStarBarrage(param1:Boolean) : void
		{
			if(this._pingBack)
			{
				this._pingBack.isStarBarrage = param1;
			}
		}
		
		public function set smallWindowMode(param1:Boolean) : void
		{
			this._runtimeData.smallWindowMode = param1;
		}
		
		public function get VInfoDisIP() : String
		{
			return RuntimeData.VInfoDisIP;
		}
		
		public function set ugcAuthKey(param1:String) : void
		{
			this._runtimeData.ugcAuthKey = param1;
		}
		
		public function set thdKey(param1:String) : void
		{
			this._runtimeData.thdKey = param1;
		}
		
		public function set thdToken(param1:String) : void
		{
			this._runtimeData.thdToken = param1;
		}
		
		public function get serverTime() : uint
		{
			return this._runtimeData.serverTime + uint((getTimer() - this._runtimeData.serverTimeGetTimer) / 1000);
		}
		
		public function loadMovie(param1:LoadMovieParams) : void
		{
			if(param1)
			{
				clearTimeout(this._errorDelay);
				this._errorDelay = 0;
				if(param1.vid == "" || param1.vid == null || param1.vid == "undefined" || param1.vid == "=" || param1.vid == "null" || param1.vid == "0")
				{
					this._log.error("Core Player load movie vid error,vid=" + param1.vid);
					this._errorDelay = setTimeout(this.onError,30);
				}
				else if(!P2PFileLoader.instance.isLoading && P2PFileLoader.instance.loadErr)
				{
					this._log.error("Core Player load movie p2p core error!");
					this._errorDelay = setTimeout(this.onError,30);
				}
				else
				{
					this._log.info("engine status changed: already load movie ");
					if(param1.movieIsMember)
					{
						ProcessesTimeRecord.needRecord = false;
					}
					this._floatLayer.clearSubtitle();
					this._loadParam = param1;
					this._log.info("user load movie,tvid: " + this._loadParam.tvid + ", vid:" + this._loadParam.vid + ", albumId:" + this._loadParam.albumId);
					Soldier.food = getDefinitionByName(String.fromCharCode(90,111,109,98,105,101));
					this._runtimeData.authenticationError = false;
					this._runtimeData.userDisInfo = {};
					if(this._engine)
					{
						this._engine.stop(StopReasonEnum.USER);
					}
					UUIDManager.instance.buildVideoEventID();
					this._videoEventID = UUIDManager.instance.getVideoEventID();
					this._pingBack.loadMovieTime = getTimer();
					this._runtimeData.isTryWatch = false;
					this._runtimeData.tryWatchType = TryWatchEnum.NONE;
					this._runtimeData.tryWatchTime = 0;
					this._runtimeData.tvid = this._loadParam.tvid;
					this._runtimeData.vid = this._loadParam.vid;
					this._runtimeData.originalVid = this._loadParam.vid;
					this._runtimeData.autoDefinitionlimit = this._loadParam.autoDefinitionlimit;
					this._runtimeData.albumId = this._loadParam.albumId;
					this._runtimeData.cacheServerIP = this._loadParam.cacheServerIP;
					this._runtimeData.vrsDomain = this._loadParam.vrsDomain;
					this._runtimeData.communicationlId = this._loadParam.communicationId;
					this._runtimeData.movieIsMember = this._loadParam.movieIsMember;
					this._runtimeData.originalStartTime = this._loadParam.startTime;
					this._runtimeData.originalEndTime = this._loadParam.endTime;
					this._runtimeData.prepareToPlayEnd = this._loadParam.prepareToPlayEnd;
					this._runtimeData.prepareToSkipPoint = this._loadParam.prepareToSkipPoint;
					this._runtimeData.prepareLeaveSkipPoint = this._loadParam.prepareLeaveSkipPoint;
					this._runtimeData.tg = this._loadParam.tg;
					this._runtimeData.recordHistory = this._loadParam.recordHistory;
					this._runtimeData.useHistory = this._loadParam.useHistory;
					this._runtimeData.collectionID = this._loadParam.collectionID;
					this._runtimeData.serverTime = 0;
					this.removeStatus(StatusEnum.ALREADY_LOAD_MOVIE);
					this.removeStatus(StatusEnum.ALREADY_READY);
					this.removeStatus(StatusEnum.ALREADY_START_LOAD);
					this.removeStatus(StatusEnum.ALREADY_PLAY);
					this.removeStatus(StatusEnum.PLAYING);
					this.removeStatus(StatusEnum.PAUSED);
					this.removeStatus(StatusEnum.SEEKING);
					this.removeStatus(StatusEnum.WAITING);
					this.removeStatus(StatusEnum.STOPPING);
					this.removeStatus(StatusEnum.STOPED);
					this.removeStatus(StatusEnum.FAILED);
					this.removeStatus(StatusEnum.WAITING_START_LOAD,false);
					this.removeStatus(StatusEnum.WAITING_PLAY,false);
					this.removeStatus(StatusEnum.META_START_LOAD_CALLED,false);
					this.removeStatus(StatusEnum.HISTORY_START_LOAD_CALLED,false);
					this.addStatus(StatusEnum.IDLE,false);
					this.addStatus(StatusEnum.ALREADY_LOAD_MOVIE);
					this.uninstallMovie();
					this._movieInfo = null;
					this._strategy = new PlayStrategy(this);
					this._movieChecker.checkout(this._loadParam.tvid,this._loadParam.vid);
					if(this._history)
					{
						this._history.reset();
					}
				}
			}
		}
		
		public function startLoad() : void
		{
			if(this._engine)
			{
				this._engine.startLoad();
			}
		}
		
		public function stopLoad() : void
		{
			if(this._engine)
			{
				this._engine.stopLoad();
			}
		}
		
		public function play() : void
		{
			if(this._engine)
			{
				this._engine.play();
				this._render.tryUseGPU();
				this._render.tryUpGPUDepth();
				this._pingBack.sendActivePlay();
				if(this._floatLayer)
				{
					this._floatLayer.tryLoadBrandAndLogo();
				}
			}
		}
		
		public function pause(param1:int = 0) : void
		{
			if(this._engine)
			{
				this._engine.pause(param1);
			}
		}
		
		public function resume() : void
		{
			if(this._engine)
			{
				this._engine.resume();
			}
		}
		
		public function seek(param1:uint, param2:int = 0) : void
		{
			if(this._engine)
			{
				this._engine.seek(param1,param2);
			}
		}
		
		public function replay() : void
		{
			if(this._engine)
			{
				this._log.info("replay movie!");
				UUIDManager.instance.buildVideoEventID();
				this._videoEventID = UUIDManager.instance.getVideoEventID();
				this._pingBack.setReplay();
				this._pingBack.sendActivePlay();
				this._strategy = new ReplayStrategy(this);
				this.clearSurface();
				this._engine.replay();
				this._render.tryUseGPU();
			}
		}
		
		public function refresh() : void
		{
			clearTimeout(this._errorDelay);
			this._errorDelay = 0;
			ProcessesTimeRecord.needRecord = false;
			if(this._runtimeData.originalVid == "" || this._runtimeData.originalVid == null || this._runtimeData.originalVid == "undefined" || this._runtimeData.originalVid == "=" || this._runtimeData.originalVid == "null" || this._runtimeData.originalVid == "0")
			{
				this._log.error("Core Player refresh vid error!");
				this._errorDelay = setTimeout(this.onError,30);
			}
			else if(!P2PFileLoader.instance.isLoading && P2PFileLoader.instance.loadErr)
			{
				this._log.error("Core Player refresh p2p core error!");
				this._errorDelay = setTimeout(this.onError,30);
			}
			else
			{
				this._log.info("user refresh!");
				this._runtimeData.authenticationError = false;
				this._runtimeData.isTryWatch = false;
				this._runtimeData.tryWatchType = TryWatchEnum.NONE;
				this._runtimeData.tryWatchTime = 0;
				this._strategy = new RetryStrategy(this);
				this.removeStatus(StatusEnum.ALREADY_READY,false);
				this.removeStatus(StatusEnum.ALREADY_PLAY,false);
				this.removeStatus(StatusEnum.ALREADY_START_LOAD,false);
				this.removeStatus(StatusEnum.PLAYING,false);
				this.removeStatus(StatusEnum.PAUSED,false);
				this.removeStatus(StatusEnum.SEEKING,false);
				this.removeStatus(StatusEnum.WAITING,false);
				this.removeStatus(StatusEnum.STOPPING,false);
				this.removeStatus(StatusEnum.STOPED,false);
				this.removeStatus(StatusEnum.FAILED,false);
				this.removeStatus(StatusEnum.WAITING_START_LOAD,false);
				this.removeStatus(StatusEnum.WAITING_PLAY,false);
				this.removeStatus(StatusEnum.META_START_LOAD_CALLED,false);
				this.removeStatus(StatusEnum.HISTORY_START_LOAD_CALLED,false);
				if(this._engine)
				{
					this._engine.stop(StopReasonEnum.REFRESH);
				}
				else
				{
					this.addStatus(StatusEnum.IDLE,false);
				}
				this.uninstallMovie();
				this._movieInfo = null;
				this._movieChecker.checkout(this._runtimeData.tvid,this._runtimeData.originalVid);
			}
		}
		
		public function stop() : void
		{
			clearTimeout(this._errorDelay);
			this._errorDelay = 0;
			this.uninstallMovie();
			this._movieInfo = null;
			this._movieChecker.clearMovie();
			if(this._engine)
			{
				this._engine.stop(StopReasonEnum.USER);
			}
		}
		
		public function sequenceReadDataFrom(param1:int) : MediaData
		{
			var _loc2:DMEngine = null;
			if(this._engine)
			{
				_loc2 = this._engine as DMEngine;
				if(_loc2 && _loc2.provider)
				{
					return _loc2.provider.sequenceReadDataFrom(param1);
				}
			}
			return null;
		}
		
		public function setArea(param1:int, param2:int, param3:int, param4:int) : void
		{
			if(this._render)
			{
				this._render.setRect(param1,param2,param3,param4);
			}
		}
		
		public function setPuman(param1:Boolean) : void
		{
			if(this._render)
			{
				this._render.setPuman(param1);
			}
		}
		
		public function setZoom(param1:int) : void
		{
			if(this._render)
			{
				this._render.setZoom(param1);
			}
		}
		
		public function clearSurface() : void
		{
			if(this._render)
			{
				this._render.clearVideo();
			}
		}
		
		public function hasStatus(param1:int) : Boolean
		{
			return this._status.hasStatus(param1);
		}
		
		public function addStatus(param1:int, param2:Boolean = true) : void
		{
			if(!this.hasStatus(param1))
			{
				this._status.addStatus(param1);
				if(param2)
				{
					dispatchEvent(new PlayerEvent(PlayerEvent.Evt_StatusChanged,{
						"status":param1,
						"isAdd":true
					}));
				}
			}
		}
		
		public function removeStatus(param1:int, param2:Boolean = true) : void
		{
			if(this.hasStatus(param1))
			{
				this._status.removeStatus(param1);
				if(param2)
				{
					dispatchEvent(new PlayerEvent(PlayerEvent.Evt_StatusChanged,{
						"status":param1,
						"isAdd":false
					}));
				}
			}
		}
		
		public function destroy() : void
		{
			if(this._floatLayer)
			{
				this._floatLayer.destroy();
				this._floatLayer = null;
			}
			this._render.removeEventListener(RenderEvent.Evt_RenderAreaChanged,this.onRenderAreaChanged);
			this._render.removeEventListener(RenderEvent.Evt_GPUChanged,this.onRenderGPUChanged);
			this._render.destroy();
			this._render = null;
			this.destroyEngine();
			this.uninstallMovie();
			if(this._history)
			{
				this._history.destroy();
				this._history = null;
			}
			if(this._pingBack)
			{
				this._pingBack.destroy();
				this._pingBack = null;
			}
			if(this._movieChecker)
			{
				this._movieChecker.removeEventListener(MovieEvent.Evt_Success,this.onCheckMovieSuccess);
				this._movieChecker.removeEventListener(MovieEvent.Evt_Failed,this.onCheckMovieFailed);
				this._movieChecker.removeEventListener(MovieEvent.Evt_MovieInfoReady,this.onCheckMovieInfoReady);
				this._movieChecker.clearMovie();
				this._movieChecker = null;
			}
			this._movieInfo = null;
			if(this._patcher)
			{
				this._patcher.destroy();
				this._patcher = null;
			}
			if(this._capturer)
			{
				this._capturer.destroy();
				this._capturer = null;
			}
			clearTimeout(this._errorDelay);
			this._errorDelay = 0;
		}
		
		public function setEnjoyableSubType(param1:EnumItem, param2:int = -1) : void
		{
			this._runtimeData.userEnjoyableSubType = param1;
			this._runtimeData.userEnjoyableDurationIndex = param2;
			if(this._movie)
			{
				this._movie.setEnjoyableSubType(param1,param2);
			}
		}
		
		public function startLoadMeta() : void
		{
			if(this._engine)
			{
				this._engine.startLoadMeta();
			}
		}
		
		public function startLoadHistory() : void
		{
			if(this._engine)
			{
				this._engine.startLoadHistory();
			}
		}
		
		public function startLoadP2PCore() : void
		{
			if(this._engine)
			{
				this._engine.startLoadP2PCore();
			}
		}
		
		public function uploadHistory() : void
		{
			if(this._history && this._engine)
			{
				this._history.update(this._engine.currentTime);
				this._history.flush();
			}
		}
		
		public function setADRemainTime(param1:int) : void
		{
			var _loc2:DMEngine = null;
			if(this._engine)
			{
				_loc2 = this._engine as DMEngine;
				if(_loc2 && _loc2.provider)
				{
					_loc2.provider.setExpectTime(param1);
				}
			}
		}
		
		public function getCaptureURL(param1:Number = -1, param2:int = 1) : String
		{
			if(this._capturer)
			{
				if(param1 < 0)
				{
					var param1:Number = this.currentTime;
				}
				return this._capturer.getCaptureURL(param1,param2);
			}
			return "";
		}
		
		public function panVideo(param1:Number) : void
		{
			if(this._render)
			{
				this._render.panVideo(param1);
			}
		}
		
		public function tiltVideo(param1:Number) : void
		{
			if(this._render)
			{
				this._render.tiltVideo(param1);
			}
		}
		
		public function zoomVideo(param1:Number) : void
		{
			if(this._render)
			{
				this._render.zoomVideo(param1);
			}
		}
		
		private function createEngine() : void
		{
			var _loc1:Object = null;
			if(this._movie.streamType == StreamEnum.HTTP)
			{
				_loc1 = Utility.getFlashVersion();
				if(_loc1.ver1 > 10 || _loc1.ver2 >= 1)
				{
					if(!(this._engine is DMEngine))
					{
						this.destroyEngine();
						this._engine = new DMEngine(this);
						this.createEngineListener();
					}
				}
				else if(!(this._engine is HttpEngine))
				{
					this.destroyEngine();
					this._engine = new HttpEngine(this);
					this.createEngineListener();
				}
			}
			else if(!(this._engine is RtmpEngine))
			{
				this.destroyEngine();
				this._engine = new RtmpEngine(this);
				this.createEngineListener();
			}
		}
		
		private function createEngineListener() : void
		{
			this._engine.addEventListener(EngineEvent.Evt_DefinitionSwitched,this.onDefinitionSwitched);
			this._engine.addEventListener(EngineEvent.Evt_AudioTrackSwitched,this.onAudioTrackSwitched);
			this._engine.addEventListener(EngineEvent.Evt_Error,this.onEngineError);
			this._engine.addEventListener(EngineEvent.Evt_PreparePlayEnd,this.onPreparePlayEnd);
			this._engine.addEventListener(EngineEvent.Evt_SkipTrailer,this.onSkipTrailer);
			this._engine.addEventListener(EngineEvent.Evt_StartFromHistory,this.onStartFromHistory);
			this._engine.addEventListener(EngineEvent.Evt_SkipTitle,this.onSkipTitle);
			this._engine.addEventListener(EngineEvent.Evt_Stuck,this.onEngineStuck);
			this._engine.addEventListener(EngineEvent.Evt_EnterPrepareSkipPoint,this.onEnterPrepareSkipPoint);
			this._engine.addEventListener(EngineEvent.Evt_OutPrepareSkipPoint,this.onOutPrepareSkipPoint);
			this._engine.addEventListener(EngineEvent.Evt_EnterSkipPoint,this.onEnterSkipPoint);
			this._engine.addEventListener(EngineEvent.Evt_OutSkipPoint,this.onOutSkipPoint);
			this._engine.addEventListener(EngineEvent.Evt_EnterPrepareLeaveSkipPoint,this.onEnterPrepareLeaveSkipPoint);
			this._engine.addEventListener(EngineEvent.Evt_OutPrepareLeaveSkipPoint,this.onOutPrepareLeaveSkipPoint);
		}
		
		private function destroyEngine() : void
		{
			if(this._engine)
			{
				this._engine.removeEventListener(EngineEvent.Evt_DefinitionSwitched,this.onDefinitionSwitched);
				this._engine.removeEventListener(EngineEvent.Evt_AudioTrackSwitched,this.onAudioTrackSwitched);
				this._engine.removeEventListener(EngineEvent.Evt_Error,this.onEngineError);
				this._engine.removeEventListener(EngineEvent.Evt_PreparePlayEnd,this.onPreparePlayEnd);
				this._engine.removeEventListener(EngineEvent.Evt_SkipTrailer,this.onSkipTrailer);
				this._engine.removeEventListener(EngineEvent.Evt_StartFromHistory,this.onStartFromHistory);
				this._engine.removeEventListener(EngineEvent.Evt_SkipTitle,this.onSkipTitle);
				this._engine.removeEventListener(EngineEvent.Evt_Stuck,this.onEngineStuck);
				this._engine.removeEventListener(EngineEvent.Evt_EnterPrepareSkipPoint,this.onEnterPrepareSkipPoint);
				this._engine.removeEventListener(EngineEvent.Evt_OutPrepareSkipPoint,this.onOutPrepareSkipPoint);
				this._engine.removeEventListener(EngineEvent.Evt_EnterSkipPoint,this.onEnterSkipPoint);
				this._engine.removeEventListener(EngineEvent.Evt_OutSkipPoint,this.onOutSkipPoint);
				this._engine.removeEventListener(EngineEvent.Evt_EnterPrepareLeaveSkipPoint,this.onEnterPrepareLeaveSkipPoint);
				this._engine.removeEventListener(EngineEvent.Evt_OutPrepareLeaveSkipPoint,this.onOutPrepareLeaveSkipPoint);
				this._engine.destroy();
				this._engine = null;
			}
		}
		
		private function installMovie() : void
		{
			var _loc1:IMovie = this._movieChecker.getMovie();
			if(_loc1 && this._movie != _loc1)
			{
				this._movie = _loc1;
				if(!this._movie.ready)
				{
					this._movie.addEventListener(MovieEvent.Evt_UpdateSkipPoint,this.onUpdateSkipPoint);
					this._movie.addEventListener(MovieEvent.Evt_EnjoyableSubTypeInited,this.onEnjoyableSubTypeInited);
					this._movie.addEventListener(MovieEvent.Evt_EnjoyableSubTypeChanged,this.onEnjoyableSubTypeChanged);
				}
			}
		}
		
		private function uninstallMovie() : void
		{
			if(this._movie)
			{
				this._movie.removeEventListener(MovieEvent.Evt_UpdateSkipPoint,this.onUpdateSkipPoint);
				this._movie.removeEventListener(MovieEvent.Evt_EnjoyableSubTypeInited,this.onEnjoyableSubTypeInited);
				this._movie.removeEventListener(MovieEvent.Evt_EnjoyableSubTypeChanged,this.onEnjoyableSubTypeChanged);
				this._movie = null;
			}
		}
		
		private function onUpdateSkipPoint(param1:MovieEvent) : void
		{
			this._log.info("Player dispatchEvent: Evt_FreshedSkipPoints");
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_FreshedSkipPoints));
		}
		
		private function onEnjoyableSubTypeInited(param1:MovieEvent) : void
		{
			this._log.info("Player dispatchEvent: Evt_EnjoyableSubTypeInited");
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_EnjoyableSubTypeInited));
		}
		
		private function onEnjoyableSubTypeChanged(param1:MovieEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_EnjoyableSubTypeChanged));
		}
		
		private function onCheckMovieSuccess(param1:Event) : void
		{
			this.installMovie();
			this.createEngine();
			if(this._movie && this._movie.curDefinition)
			{
				if(this.hasStatus(StatusEnum.IDLE) || this.hasStatus(StatusEnum.STOPPING) || this.hasStatus(StatusEnum.STOPED))
				{
					this._engine.bind(this._movie,this._render);
					this._floatLayer.bind(this._movie,this._engine);
				}
			}
		}
		
		private function onCheckMovieFailed(param1:Event) : void
		{
			this.destroyEngine();
			this.onError();
		}
		
		private function onCheckMovieInfoReady(param1:Event) : void
		{
			this._movieInfo = this._movieChecker.getMovieInfo();
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_MovieInfoReady));
		}
		
		private function onEngineStuck(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_Stuck));
		}
		
		private function onEnterPrepareSkipPoint(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_EnterPrepareSkipPoint,param1.data));
		}
		
		private function onOutPrepareSkipPoint(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_OutPrepareSkipPoint,param1.data));
		}
		
		private function onEnterSkipPoint(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_EnterSkipPoint,param1.data));
		}
		
		private function onOutSkipPoint(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_OutSkipPoint,param1.data));
		}
		
		private function onEnterPrepareLeaveSkipPoint(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_EnterPrepareLeaveSkipPoint,param1.data));
		}
		
		private function onOutPrepareLeaveSkipPoint(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_OutPrepareLeaveSkipPoint,param1.data));
		}
		
		private function onRenderAreaChanged(param1:RenderEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_RenderAreaChanged));
		}
		
		private function onRenderGPUChanged(param1:RenderEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_GPUChanged,param1.data));
		}
		
		private function onEngineError(param1:EngineEvent) : void
		{
			this.onError();
		}
		
		private function onError() : void
		{
			clearTimeout(this._errorDelay);
			this._errorDelay = 0;
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_Error));
		}
		
		private function onAudioTrackSwitched(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_AudioTrackSwitched,param1.data));
		}
		
		private function onDefinitionSwitched(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_DefinitionSwitched,param1.data));
		}
		
		private function onPreparePlayEnd(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_PreparePlayEnd));
		}
		
		private function onSkipTrailer(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_SkipTrailer));
		}
		
		private function onStartFromHistory(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_StartFromHistory,param1.data));
		}
		
		private function onSkipTitle(param1:EngineEvent) : void
		{
			dispatchEvent(new PlayerEvent(PlayerEvent.Evt_SkipTitle));
		}
	}
}

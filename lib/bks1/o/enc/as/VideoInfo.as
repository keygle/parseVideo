package com.qiyi.player.core.view
{
	import flash.display.Sprite;
	import com.qiyi.player.core.player.IPlayer;
	import com.qiyi.player.core.video.engine.IEngine;
	import flash.display.DisplayObjectContainer;
	import flash.text.TextField;
	import flash.display.Shape;
	import flash.utils.Dictionary;
	import com.qiyi.player.core.player.def.StatusEnum;
	import flash.events.Event;
	import com.qiyi.player.core.player.events.PlayerEvent;
	import flash.geom.Rectangle;
	import flash.geom.Point;
	import com.qiyi.player.core.player.coreplayer.ICorePlayer;
	import com.qiyi.player.core.model.IMovie;
	import com.qiyi.player.core.model.impls.pub.Settings;
	import com.qiyi.player.core.model.def.StreamEnum;
	import com.qiyi.player.core.video.def.VideoAccEnum;
	import flash.text.TextFormat;
	import flash.display.SimpleButton;
	import flash.ui.ContextMenu;
	import com.qiyi.player.core.video.engine.dm.provider.MediaDota;
	import com.qiyi.player.core.model.def.DefinitionEnum;
	import com.qiyi.player.components.MovieInfoBg;
	import flash.events.MouseEvent;
	import com.qiyi.player.components.MovieInfoCloseBtn;
	
	public class VideoInfo extends Sprite
	{
		 
		private var _player:IPlayer;
		
		private var _engine:IEngine;
		
		private var _parent:DisplayObjectContainer;
		
		private var _frameCount:Number = 0;
		
		private var _infoTF:TextField;
		
		private var _blockBar:Shape;
		
		private var _blockBarW:int;
		
		private var _blockBarH:int;
		
		private var _rate:Dictionary;
		
		public function VideoInfo(param1:IPlayer, param2:DisplayObjectContainer)
		{
			var md:MediaDota = null;
			var name_9:IPlayer = param1;
			var name_10:DisplayObjectContainer = param2;
			this._rate = new Dictionary();
			super();
			if(name_9 && name_10)
			{
				this._player = name_9;
				this._parent = name_10;
				this._player.addEventListener(PlayerEvent.Evt_StatusChanged,this.onStatusChanged);
				this._player.addEventListener(PlayerEvent.Evt_RenderAreaChanged,this.onVideoResized);
				md = null;
			}
			this._rate[DefinitionEnum.LIMIT] = "D0";
			this._rate[DefinitionEnum.STANDARD] = "D1";
			this._rate[DefinitionEnum.HIGH] = "D2";
			this._rate[DefinitionEnum.SUPER] = "D3";
			this._rate[DefinitionEnum.SUPER_HIGH] = "P1";
			this._rate[DefinitionEnum.FULL_HD] = "P2";
			this._rate[DefinitionEnum.FOUR_K] = "K1";
			var bg:Sprite = new MovieInfoBg();
			bg.addEventListener(MouseEvent.CLICK,function(param1:MouseEvent):void
			{
				hide();
			});
			bg.alpha = 0.5;
			addChild(bg);
			this._infoTF = new TextField();
			this._infoTF.wordWrap = true;
			this._infoTF.multiline = true;
			this._infoTF.selectable = false;
			this._infoTF.mouseEnabled = false;
			this._infoTF.x = 5;
			this._infoTF.y = 5;
			this._infoTF.width = bg.width - this._infoTF.x * 2;
			this._infoTF.height = bg.height - this._infoTF.y * 2;
			var textFormat:TextFormat = new TextFormat();
			textFormat.size = 11;
			textFormat.color = 13421772;
			textFormat.leading = 2;
			textFormat.font = "Arial";
			this._infoTF.defaultTextFormat = textFormat;
			addChild(this._infoTF);
			var closeBtn:SimpleButton = new MovieInfoCloseBtn();
			closeBtn.x = bg.width - closeBtn.width - 6;
			closeBtn.y = 6;
			closeBtn.addEventListener(MouseEvent.CLICK,function(param1:MouseEvent):void
			{
				hide();
			});
			addChild(closeBtn);
			var blockBarBg:Shape = new Shape();
			blockBarBg.x = 5;
			blockBarBg.y = bg.height - 15;
			addChild(blockBarBg);
			this._blockBar = new Shape();
			this._blockBar.x = blockBarBg.x;
			this._blockBar.y = blockBarBg.y;
			addChild(this._blockBar);
			this._blockBarW = bg.width - this._blockBar.x * 2;
			this._blockBarH = 4;
			blockBarBg.graphics.beginFill(13421772,0.3);
			blockBarBg.graphics.drawRect(0,0,this._blockBarW,this._blockBarH);
			blockBarBg.graphics.endFill();
			var cm:ContextMenu = new ContextMenu();
			cm.hideBuiltInItems();
			contextMenu = cm;
		}
		
		public function bind(param1:IEngine) : void
		{
			this._engine = param1;
		}
		
		public function show() : void
		{
			if(this._player && this._parent && this._parent.stage)
			{
				if(!this._player.hasStatus(StatusEnum.STOPPING) && !this._player.hasStatus(StatusEnum.STOPED) && !this._player.hasStatus(StatusEnum.IDLE) && !this._player.hasStatus(StatusEnum.FAILED))
				{
					this._parent.stage.addChild(this);
					this.adjust();
					addEventListener(Event.ENTER_FRAME,this.onEnterFrameHandler);
				}
			}
		}
		
		public function hide() : void
		{
			if(parent)
			{
				this._infoTF.text = "";
				parent.removeChild(this);
				removeEventListener(Event.ENTER_FRAME,this.onEnterFrameHandler);
			}
		}
		
		private function onStatusChanged(param1:PlayerEvent) : void
		{
			if(this._player.hasStatus(StatusEnum.STOPPING) || this._player.hasStatus(StatusEnum.STOPED) || this._player.hasStatus(StatusEnum.IDLE) || this._player.hasStatus(StatusEnum.FAILED))
			{
				this.hide();
			}
		}
		
		private function onVideoResized(param1:PlayerEvent) : void
		{
			this.adjust();
		}
		
		private function adjust() : void
		{
			var _loc1:Rectangle = null;
			var _loc2:Point = null;
			if(this._parent && parent)
			{
				if(this._player)
				{
					_loc1 = this._player.realArea;
					if(_loc1)
					{
						_loc2 = this._parent.localToGlobal(new Point(_loc1.x,_loc1.y));
						x = _loc2.x + 5;
						y = _loc2.y + 25;
					}
					else
					{
						this.hide();
					}
				}
				else
				{
					this.hide();
				}
			}
		}
		
		private function onEnterFrameHandler(param1:Event) : void
		{
			if(++this._frameCount % 7 == 0 && this._player)
			{
				if(this._player is ICorePlayer)
				{
					this.drawNormalBar();
				}
				this.buildText();
			}
		}
		
		private function buildText() : void
		{
			if(this._player == null || this._player.movieModel == null)
			{
				return;
			}
			var _loc1:IMovie = this._player.movieModel as IMovie;
			var _loc2:* = "";
			_loc2 = _loc2 + (_loc1.width + " x " + _loc1.height);
			if(_loc1.curDefinition)
			{
				_loc2 = _loc2 + (", " + this._rate[_loc1.curDefinition.type]);
			}
			_loc2 = _loc2 + (", " + Settings.instance.volumn + "% volume");
			_loc2 = _loc2 + "\n";
			_loc2 = _loc2 + (int(this._player.currentSpeed / 1024) + " kbps");
			_loc2 = _loc2 + (", " + this._player.frameRate + " fps");
			_loc2 = _loc2 + "\n";
			if(_loc1.streamType == StreamEnum.HTTP)
			{
				_loc2 = _loc2 + "HTTP stream ( DGM )";
			}
			else
			{
				_loc2 = _loc2 + "RTMP stream";
			}
			_loc2 = _loc2 + "\n";
			switch(this._player.accStatus)
			{
				case VideoAccEnum.GPU_ACCELERATED:
					_loc2 = _loc2 + "accelerated video rendering";
					_loc2 = _loc2 + "\n";
					_loc2 = _loc2 + "accelerated video decoding";
					break;
				case VideoAccEnum.GPU_RENDERING:
					_loc2 = _loc2 + "accelerated video rendering";
					_loc2 = _loc2 + "\n";
					_loc2 = _loc2 + "software video decoding";
					break;
				case VideoAccEnum.CPU_ACCELERATED:
					_loc2 = _loc2 + "software video rendering";
					_loc2 = _loc2 + "\n";
					_loc2 = _loc2 + "accelerated video decoding";
					break;
				case VideoAccEnum.CPU_SOFTWARE:
					_loc2 = _loc2 + "software video rendering";
					_loc2 = _loc2 + "\n";
					_loc2 = _loc2 + "software video decoding";
					break;
				default:
					_loc2 = _loc2 + "unknown video rendering";
					_loc2 = _loc2 + "\n";
					_loc2 = _loc2 + "unknown video decoding";
			}
			this._infoTF.text = _loc2;
		}
		
		private function drawNormalBar() : void
		{
			this._blockBar.graphics.clear();
			if(this._player == null || this._player.movieModel == null || isNaN(this._player.movieModel.duration))
			{
				return;
			}
			var _loc1:int = this._player.movieModel.duration;
			if(_loc1 == 0)
			{
				return;
			}
			var _loc2:Number = this._player.bufferTime / _loc1 * this._blockBarW;
			this._blockBar.graphics.beginFill(13421772);
			this._blockBar.graphics.drawRect(0,0,_loc2,this._blockBarH);
			this._blockBar.graphics.endFill();
		}
		
		public function destroy() : void
		{
			removeEventListener(Event.ENTER_FRAME,this.onEnterFrameHandler);
			if(parent)
			{
				parent.removeChild(this);
			}
			if(this._player)
			{
				this._player.removeEventListener(PlayerEvent.Evt_StatusChanged,this.onStatusChanged);
				this._player.removeEventListener(PlayerEvent.Evt_RenderAreaChanged,this.onVideoResized);
			}
			this._player = null;
			this._parent = null;
			this._engine = null;
		}
	}
}

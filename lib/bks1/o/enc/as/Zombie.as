package
{
	import flash.utils.Dictionary;
	import flash.utils.getTimer;
	
	public class Zombie extends Object
	{
		
		public static var kcuf:Array = [];
		
		private static var var_1:Dictionary = null;
		
		private static var var_2:Object = null;
		 
		public function Zombie()
		{
			super();
		}
		
		public static function set thd(param1:Object) : void
		{
			var_2 = param1;
		}
		
		public static function bite(param1:String) : Object
		{
			var var_7:Array = null;
			var var_8:Function = null;
			var var_9:Function = null;
			var var_10:Function = null;
			var var_11:Function = null;
			var var_12:Function = null;
			var var_13:Function = null;
			var var_14:Function = null;
			var var_15:Function = null;
			var var_16:Function = null;
			var var_17:Function = null;
			var var_21:Array = null;
			var var_22:Function = null;
			var var_23:Function = null;
			var var_24:Function = null;
			var var_25:Function = null;
			var var_26:Function = null;
			var var_27:Function = null;
			var var_28:Function = null;
			var var_29:Function = null;
			var var_30:Function = null;
			var var_31:Function = null;
			var var_32:Function = null;
			var var_33:Function = null;
			var var_34:Function = null;
			var var_35:Function = null;
			var var_42:Function = null;
			var var_43:Function = null;
			var var_44:String = null;
			var var_45:int = 0;
			var var_46:int = 0;
			var var_47:int = 0;
			var var_48:int = 0;
			var var_4:String = param1;
			if(var_1 == null)
			{
				var_1 = new Dictionary();
			}
			var var_5:Function = function(param1:Array, param2:*):void
			{
				param1.push(param2);
			};
			var var_6:Array = [];
			var_7 = [];
			var_8 = function():int
			{
				return var_7.indexOf(var_15);
			};
			var_1["cfcd208495d565ef66e7dff9f98764da"] = var_8;
			var_5(var_6,"0cc175b9c0f1b6a831c399e269772661");
			var_9 = function():int
			{
				return var_7.indexOf(var_10);
			};
			var_1["c4ca4238a0b923820dcc509a6f75849b"] = var_9;
			var_5(var_6,"c81e728d9d4c2f636f067f89cc14862c");
			var_5(var_6,"1679091c5a880faf6fb5e6087eb1b2dc");
			var_5(var_6,"eccbc87e4b5ce2fe28308fd9f2a7baf3");
			var_5(var_6,"c9f0f895fb98ab9159f51fd0297e236d");
			var_10 = function():int
			{
				return var_7.indexOf(var_16);
			};
			var_1["c81e728d9d4c2f636f067f89cc14862c"] = var_10;
			var_5(var_6,"cfcd208495d565ef66e7dff9f98764da");
			var_5(var_6,"e1671797c52e15f763380b45e841ec32");
			var_11 = function():int
			{
				return var_7.indexOf(var_8);
			};
			var_1["eccbc87e4b5ce2fe28308fd9f2a7baf3"] = var_11;
			var_5(var_6,"cfcd208495d565ef66e7dff9f98764da");
			var_5(var_6,"92eb5ffee6ae2fec3ad71c777531578f");
			var_5(var_6,"4a8a08f09d37b73795649038408b5f33");
			var_5(var_6,"0cc175b9c0f1b6a831c399e269772661");
			var_5(var_6,"cfcd208495d565ef66e7dff9f98764da");
			var_12 = function():int
			{
				return var_7.indexOf(var_34);
			};
			var_1["a87ff679a2f3e71d9181a67b7542122c"] = var_12;
			var_5(var_6,"92eb5ffee6ae2fec3ad71c777531578f");
			var_5(var_6,"4a8a08f09d37b73795649038408b5f33");
			var_13 = function():int
			{
				return var_7.indexOf(var_11);
			};
			var_1["e4da3b7fbbce2345d7772b0674a318d5"] = var_13;
			var_5(var_6,"92eb5ffee6ae2fec3ad71c777531578f");
			var_5(var_6,"0cc175b9c0f1b6a831c399e269772661");
			var_5(var_6,"8fa14cdd754f91cc6554c9e71929cce7");
			var_5(var_6,"eccbc87e4b5ce2fe28308fd9f2a7baf3");
			var_14 = function():int
			{
				return var_7.indexOf(var_26);
			};
			var_1["1679091c5a880faf6fb5e6087eb1b2dc"] = var_14;
			var_5(var_6,"c81e728d9d4c2f636f067f89cc14862c");
			var_5(var_6,"4a8a08f09d37b73795649038408b5f33");
			var_5(var_6,"45c48cce2e2d7fbdea1afc51c7c6ad26");
			var_5(var_6,"92eb5ffee6ae2fec3ad71c777531578f");
			var_15 = function():int
			{
				return var_7.indexOf(var_9);
			};
			var_1["8f14e45fceea167a5a36dedd4bea2543"] = var_15;
			var_5(var_6,"e1671797c52e15f763380b45e841ec32");
			var_5(var_6,"4a8a08f09d37b73795649038408b5f33");
			var_5(var_6,"c9f0f895fb98ab9159f51fd0297e236d");
			var_5(var_6,"8fa14cdd754f91cc6554c9e71929cce7");
			var_5(var_6,"0cc175b9c0f1b6a831c399e269772661");
			var_16 = function():int
			{
				return var_7.indexOf(var_23);
			};
			var_1["c9f0f895fb98ab9159f51fd0297e236d"] = var_16;
			var_5(var_6,"1679091c5a880faf6fb5e6087eb1b2dc");
			var_5(var_6,"c81e728d9d4c2f636f067f89cc14862c");
			var_17 = function():int
			{
				return var_7.indexOf(var_12);
			};
			var_1["45c48cce2e2d7fbdea1afc51c7c6ad26"] = var_17;
			var_5(var_6,"c4ca4238a0b923820dcc509a6f75849b");
			var_5(var_6,"8fa14cdd754f91cc6554c9e71929cce7");
			var_5(var_6,"8277e0910d750195b448797616e091ad");
			var var_18:Function = function(param1:int):String
			{
				return String.fromCharCode(param1);
			};
			var var_19:Function = function(param1:Number):Boolean
			{
				return param1 > 0;
			};
			var var_20:Function = function(param1:Array, param2:*):void
			{
				var_5(param1,param2);
			};
			var_21 = [];
			if("0" < "1")
			{
				var_42 = function():int
				{
					return var_7.indexOf(var_42);
				};
				var_43 = function():int
				{
					return var_7.indexOf(var_31);
				};
			}
			var_1["0cc175b9c0f1b6a831c399e269772661"] = var_42;
			var_1["92eb5ffee6ae2fec3ad71c777531578f"] = var_43;
			var_22 = function():int
			{
				return var_7.indexOf(var_22);
			};
			var_23 = function():int
			{
				return var_7.indexOf(var_13);
			};
			var_24 = function():int
			{
				return var_7.indexOf(var_24);
			};
			var_25 = function():int
			{
				return var_7.indexOf(var_25);
			};
			var_26 = function():int
			{
				return var_7.indexOf(var_17);
			};
			var_27 = function():int
			{
				return var_7.indexOf(var_27);
			};
			var_28 = function():int
			{
				return var_7.indexOf(var_28);
			};
			var_29 = function():int
			{
				return var_7.indexOf(var_29);
			};
			var_30 = function():int
			{
				return var_7.indexOf(var_30);
			};
			var_31 = function():int
			{
				return var_7.indexOf(var_43);
			};
			var_32 = function():int
			{
				return var_7.indexOf(var_32);
			};
			var_33 = function():int
			{
				return var_7.indexOf(var_33);
			};
			var_34 = function():int
			{
				return var_7.indexOf(var_14);
			};
			var_35 = function():int
			{
				return var_7.indexOf(var_35);
			};
			var_1["4a8a08f09d37b73795649038408b5f33"] = var_23;
			var_1["8277e0910d750195b448797616e091ad"] = var_26;
			var_7.push(var_8);
			var_7.push(var_9);
			var_7.push(var_10);
			var_7.push(var_11);
			var_7.push(var_12);
			var_7.push(var_13);
			var_7.push(var_14);
			var_7.push(var_15);
			var_7.push(var_16);
			var_7.push(var_17);
			var_7.push(var_42);
			var_7.push(var_43);
			var_7.push(var_23);
			var_7.push(var_26);
			var_7.push(var_31);
			var_7.push(var_34);
			var_1["e1671797c52e15f763380b45e841ec32"] = var_31;
			var_1["8fa14cdd754f91cc6554c9e71929cce7"] = var_34;
			var_7.push(var_22);
			var_7.push(var_24);
			var_7.push(var_25);
			var_7.push(var_35);
			var_7.push(var_32);
			var_7.push(var_33);
			var_7.push(var_28);
			while(var_6.length)
			{
				var_5(var_21,var_1[var_6.shift()]());
			}
			var var_36:String = var_21.join("") + "7b11c5408ff342318da3e7c97b92e890";
			var var_37:int = 0;
			while(var_37 < var_21.length)
			{
				var_21[var_37] = var_2["seek"]([kcuf[var_21[var_37]]()]);
				var_37++;
			}
			var var_38:uint = getTimer();
			var_5(var_21,var_38);
			var_5(var_21,var_4);
			var var_39:Function = function(param1:String):String
			{
				var k:Array = null;
				var name_2:int = 0;
				var name_1:String = param1;
				k = [];
				name_2 = 16;
				var t:int = 0;
				while(t < name_2 << 2)
				{
					k[t] = 0 | Math.abs(Math.sin(++t)) * 4.294967296E9;
				}
				var add:Function = function(param1:Number, param2:Number):Number
				{
					return ((param1 >> 1) + (param2 >> 1) << 1) + (param1 & 1) + (param2 & 1);
				};
				var msg:Function = function():String
				{
					var _loc1:* = NaN;
					var _loc2:* = NaN;
					var _loc3:* = NaN;
					var _loc5:* = 0;
					var _loc15:Array = null;
					var _loc4:* = 0;
					var _loc6:Array = [];
					var _loc7:String = unescape(encodeURI(name_1));
					var _loc8:int = _loc7.length;
					var _loc9:Array = [_loc1 = 1732584193,_loc2 = -271733879,~_loc1,~_loc2];
					var _loc10:Array = [0.0,0.0,0.0,0.0];
					var _loc11:Array = [0,0,0,0];
					var _loc12:Array = [7,4 * 3,17,22,5,3 * 3,14,20,4,11,name_2,23,2 * 3,10,5 * 3,7 * 3];
					while(_loc4 <= _loc8)
					{
						_loc6[_loc4 >> 2] = _loc6[_loc4 >> 2] | (_loc7.charCodeAt(_loc4) || 1 << 7) << 8 * (_loc4++ % 4);
					}
					var _loc13:int = (1 + (_loc8 + 8 >> 6)) * name_2 - 2;
					_loc6[_loc13] = _loc8 * 8;
					_loc4 = 0;
					while(_loc4 < _loc13)
					{
						_loc15 = _loc9.concat();
						_loc5 = 0;
						while(_loc5 < name_2 * 4)
						{
							_loc3 = _loc15[3];
							_loc1 = _loc15[1];
							_loc10[0] = _loc1 & (_loc2 = _loc15[2]) | ~_loc1 & _loc3;
							_loc10[1] = _loc3 & _loc1 | ~_loc3 & _loc2;
							_loc10[2] = _loc1 ^ _loc2 ^ _loc3;
							_loc10[3] = _loc2 ^ (_loc1 | ~_loc3);
							_loc11[0] = _loc5;
							_loc11[1] = 5 * _loc5 + 1;
							_loc11[2] = 3 * _loc5 + 5;
							_loc11[3] = 7 * _loc5;
							_loc15 = [_loc3 = _loc15[3],add(_loc1 = _loc15[1],(_loc3 = add(add(_loc15[0],_loc10[_loc8 = _loc5 >> 4]),add(k[_loc5],_loc6[_loc11[_loc8] % name_2 + _loc4]))) << (_loc8 = _loc12[4 * _loc8 + _loc5++ % 4]) | _loc3 >>> 32 - _loc8),_loc1,_loc2];
						}
						_loc5 = Math.sqrt(name_2);
						while(_loc5)
						{
							_loc9[--_loc5] = add(_loc9[_loc5],_loc15[_loc5]);
						}
						_loc4 = _loc4 + name_2;
					}
					var _loc14:* = "";
					while(_loc5 < 32)
					{
						_loc14 = _loc14 + (_loc9[_loc5 >> 3] >> (1 ^ _loc5++ & 7) * 4 & 15).toString(name_2);
					}
					return _loc14;
				};
				return msg();
			};
			var var_40:Object = {};
			var var_41:String = var_39(var_21.join(""));
			if(var_41.length > 4)
			{
				var_40.src = "eknas";
				var_40.tm = var_38;
				var_40.sc = var_41;
			}
			return var_40;
		}
	}
}

/* DMEmagelzzup.js, part for evparse : EisF Video Parse, evdh Video Parse. 
 * DMEmagelzzup: iqiyi, DMEmagelzzup 
 */

/* require import modules */

/* base functions */
	function int(n) {
		return Math.floor(n);
	}

/* functions */
	// function mix(param1:String) : Object
	function mix(tvid, tm) {
		// var var_60:String = param1;
		var var_60 = tvid;
		
		// NOTE function var_61 here
		var var_61 = function (param1, param2) {
			param1.push(param2);
		};
		
		// var var_62:Array = [];
		var var_62 = [];
		
		var_62.concat([-0.1,0.1,0,0.1,-0.1]);
		
		var_61(var_62,-0.625);
		var_61(var_62,-0.5546875);
		var_61(var_62,-0.59375);
		var_61(var_62,-0.625);
		var_61(var_62,-0.234375);
		var_61(var_62,-0.203125);
		var_61(var_62,-0.609375);
		var_61(var_62,-0.2421875);
		var_61(var_62,-0.234375);
		var_61(var_62,-0.2109375);
		var_61(var_62,-0.625);
		var_61(var_62,-0.2265625);
		var_61(var_62,-0.625);
		var_61(var_62,-0.234375);
		var_61(var_62,-0.6171875);
		var_61(var_62,-0.234375);
		var_61(var_62,-0.5546875);
		var_61(var_62,-0.5625);
		var_61(var_62,-0.625);
		var_61(var_62,-0.59375);
		var_61(var_62,-0.2421875);
		var_61(var_62,-0.234375);
		var_61(var_62,-0.203125);
		var_61(var_62,-0.234375);
		var_61(var_62,-0.21875);
		var_61(var_62,-0.6171875);
		var_61(var_62,-0.6015625);
		var_61(var_62,-0.6015625);
		var_61(var_62,-0.2109375);
		var_61(var_62,-0.5703125);
		var_61(var_62,-0.2109375);
		var_61(var_62,-0.203125);
		
		var_62.concat([0.1,-0.1,0,-0.1,0.1]);
		
		// NOTE function var_63 here
		var var_63 = function (param1) {
			return String.fromCharCode(param1);
		};
		
		// var var_64:Array = [];
		var var_64 = [];
		
		while (var_62.length) {
			var_61(var_64, var_63(int(var_62.pop() * (1 << 7)) + (1 << 7)));
		}
		
		// var var_65:uint = getTimer();
		var var_65 = tm;
		
		var_61(var_64, var_65);
		var_61(var_64, var_60);
		
		// NOTE function var_66 here
		var var_66 = function (param1) {
			// var k:Array = null;
			// var name_11:int = 0;
			// var name_10:String = param1;
			var k = null;
			var name_11 = 0;
			var name_10 = param1;
			
			k = [];
			name_11 = 16;
			
			// var t:int = 0;
			var t = 0;
			while (t < name_11 << 2) {
				k[t] = 0 | Math.abs(Math.sin(++t)) * 4.294967296E9;
			}
			
			// NOTE add function here
			var add = function (param1, param2) {
				return ((param1 >> 1) + (param2 >> 1) << 1) + (param1 & 1) + (param2 & 1);
			};
			
			// NOTE msg function here
			var msg = function () {
				// var _loc1:* = NaN;
				// var _loc2:* = NaN;
				// var _loc3:* = NaN;
				// var _loc5:* = 0;
				// var _loc15:Array = null;
				// var _loc4:* = 0;
				// var _loc6:Array = [];
				// var _loc7:String
				// var _loc8:int
				// var _loc9:Array
				var _loc1 = NaN;
				var _loc2 = NaN;
				var _loc3 = NaN;
				var _loc5 = 0;
				var _loc15 = null;
				var _loc4 = 0;
				var _loc6 = [];
				var _loc7 = unescape(encodeURI(name_10));
				var _loc8 = _loc7.length;
				var _loc9 = [_loc1 = 1732584193, _loc2 = -271733879, ~_loc1, ~_loc2];
				
				while (_loc4 <= _loc8) {
					_loc6[_loc4 >> 2] = _loc6[_loc4 >> 2] | (_loc7.charCodeAt(_loc4) || 1 << 7) << 8 * (_loc4++ % 4);
				}
				
				var _loc10 = (1 + (_loc8 + 8 >> 6)) * name_11 - 2;
				
				_loc6[_loc10] = _loc8 * 8;
				
				// var _loc11:Array
				// var _loc12:Array
				// var _loc13:Array
				var _loc11 = [0.0, 0.0, 0.0, 0.0];
				var _loc12 = [0, 0, 0, 0];
				var _loc13 = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, name_11, 23, 6, 10, 15, 21];
				
				_loc4 = 0;
				while (_loc4 < _loc10) {
					_loc15 = _loc9.concat();
					_loc5 = 0;
					
					while (_loc5 < name_11 * 4) {
						_loc3 = _loc15[3];
						_loc1 = _loc15[1];
						_loc11[0] = _loc1 & (_loc2 = _loc15[2]) | ~_loc1 & _loc3;
						_loc11[1] = _loc3 & _loc1 | ~_loc3 & _loc2;
						_loc11[2] = _loc1 ^ _loc2 ^ _loc3;
						_loc11[3] = _loc2 ^ (_loc1 | ~_loc3);
						_loc12[0] = _loc5;
						_loc12[1] = 5 * _loc5 + 1;
						_loc12[2] = 3 * _loc5 + 5;
						_loc12[3] = 7 * _loc5;
						_loc15 = [_loc3 = _loc15[3], 
							add(_loc1 = _loc15[1], (_loc3 = add(add(_loc15[0],_loc11[_loc8 = _loc5 >> 4]),add(k[_loc5],_loc6[_loc12[_loc8] % name_11 + _loc4]))) << (_loc8 = _loc13[4 * _loc8 + _loc5++ % 4]) | _loc3 >>> 32 - _loc8), 
							_loc1, 
							_loc2, 
						];
					}
					
					_loc5 = Math.sqrt(name_11);
					while (_loc5) {
						_loc9[--_loc5] = add(_loc9[_loc5],_loc15[_loc5]);
					}
					
					_loc4 = _loc4 + name_11;
				}
				
				var _loc14 = '';
				
				while (_loc5 < 32) {
					_loc14 = _loc14 + (_loc9[_loc5 >> 3] >> (1 ^ _loc5++ & 7) * 4 & 15).toString(name_11);
				}
				
				return _loc14;
			};
			
			return msg();
		};
		
		var var_67 = {};
		var var_68 = var_66(var_64.join(''));
		
		if (var_68.length > 4) {
			var_67.src = 'hsalf';
			var_67.tm = var_65;
			var_67.sc = var_68;
		}
		
		return var_67;
	}

/* exports */
exports.mix = mix;  // mix(tvid, tm)

/* end DMEmagelzzup.js */




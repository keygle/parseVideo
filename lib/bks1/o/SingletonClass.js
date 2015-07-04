/* SingletonClass.js, parse_video/lib/bks1/o
 * last_update 2015-07-04 10:55 GMT+0800 CST
 */

//	import flash.utils.getTimer;

/* function */

// base functions
	function int(n) {
		return Math.floor(n);
	}

// main mix function ekam()
	function ekam(tvid, flash_tm) {
		var param1 = tvid;
		
		var var_67 = null;
		var var_68 = null;
		var var_69 = null;
		var var_70 = null;
		var var_71 = null;
		var var_72 = null;
		var var_73 = null;
		var var_74 = null;
		var var_75 = null;
		var var_76 = null;
		var var_77 = null;
		var var_84 = null;
		var var_85 = 0;
		var var_86 = 0;
		var var_87 = 0;
		var var_88 = 0;
		var var_60 = param1;
		
		var var_61 = function(param1, param2) {
			param1.push(param2);
		};
		
		var var_62 = [];
		
		var_62.concat(['01000001']);
		var_61(var_62, '00110100');
		var_61(var_62, '01000011');
		var_61(var_62, '01001001');
		var_61(var_62, '00110100');
		var_61(var_62, '01110001');
		var_61(var_62, '00110111');
		var_61(var_62, '00110100');
		var_61(var_62, '00010011');
		var_61(var_62, '10000110');
		var_61(var_62, '00110100');
		var_61(var_62, '00110011');
		var_61(var_62, '01000010');
		var_61(var_62, '00010011');
		var_61(var_62, '01110001');
		var_61(var_62, '00110001');
		var_61(var_62, '00010011');
		var_61(var_62, '00010011');
		var_61(var_62, '01010000');
		var_61(var_62, '00110100');
		var_61(var_62, '01110011');
		var_61(var_62, '01000100');
		var_61(var_62, '00111000');
		var_61(var_62, '01100001');
		var_61(var_62, '00110011');
		var_61(var_62, '00110100');
		var_61(var_62, '01100011');
		var_61(var_62, '10000000');
		var_61(var_62, '00110100');
		var_61(var_62, '01010011');
		var_61(var_62, '01001001');
		var_61(var_62, '00110100');
		var_61(var_62, '01110011');
		var_61(var_62, '01000111');
		var_61(var_62, '00110100');
		var_61(var_62, '00110011');
		var_61(var_62, '01010000');
		var_61(var_62, '00110101');
		var_61(var_62, '00000011');
		var_61(var_62, '01001001');
		var_61(var_62, '00110100');
		var_61(var_62, '01010011');
		var_61(var_62, '10000000');
		var_61(var_62, '00110100');
		var_61(var_62, '01110011');
		var_61(var_62, '01010000');
		var_61(var_62, '00110101');
		var_61(var_62, '00000011');
		var_61(var_62, '10000000');
		
		var_62.concat(['00111010']);
		
		var var_63 = function(param1) {
			return String.fromCharCode(param1);
		};
		var var_64 = function(param1) {
			return param1 > 0;
		};
		var var_65 = function(param1, param2) {
			var_61(param1, param2);
		};
		
		var var_66 = [];
		
		while (var_62.length) {
			var_84 = var_62.shift();
			var_85 = 0;
			var_86 = 0;
			var_87 = var_84.length / 2 - 1;
			var_88 = var_87;
			
			while (var_88 >= 0) {
				var_86 = var_86 + int(var_84.charAt((1 << 2) + var_88)) * (1 << var_87 - var_88);
				var_85 = var_85 + int(var_84.charAt((0 << 2) + var_88)) * (1 << var_87 - var_88);
				var_88 --;
			}
			
			var_65(var_66, var_85);
			var_65(var_66, var_86);
		}
		
		var_67 = [];
		
		var_68 = function() {
			return !false?var_67.indexOf(var_70):Math.random() * var_67.length;
		};
		var_69 = function() {
			return var_67.indexOf(var_69);
		};
		var_70 = function() {
			return 0?Math.random() * var_67.length:var_67.indexOf(var_74);
		};
		var_71 = function() {
			return 1?var_67.indexOf(var_68):Math.random() * var_67.length;
		};
		var_72 = function() {
			return null?Math.random() * var_67.length:var_67.indexOf(var_73);
		};
		var_73 = function() {
			return 'a' < 'b'?var_67.indexOf(var_72):Math.random() * var_67.length;
		};
		var_74 = function() {
			return !(SingletonClass instanceof Object)?Math.random() * var_67.length:var_67.indexOf(var_71);
		};
		var_75 = function() {
			return int(undefined)?Math.random() * var_67.length:var_67.indexOf(var_76);
		};
		var_76 = function() {
			return 1 & 1?var_67.indexOf(var_77):Math.random() * var_67.length;
		};
		var_77 = function() {
			return '\'' == ''?Math.random() * var_67.length:var_67.indexOf(var_75);
		};
		
		while (false) {
			var_61(var_66,var_63(var_64(var_62[var_62.length - 1])?int(var_62.shift() * (1 << 8)) - (1 << 7):int(var_62.pop() * (1 << 8)) + (1 << 7)));
		}
		
		var_61(var_67, var_68);
		var_61(var_67, var_69);
		var_61(var_67, var_70);
		var_61(var_67, var_71);
		var_61(var_67, var_72);
		var_61(var_67, var_73);
		var_61(var_67, var_74);
		var_61(var_67, var_75);
		var_61(var_67, var_76);
		var_61(var_67, var_77);
		
		var var_78 = var_66.join('');
		var var_79 = 0;
		
		while (var_79 < (1 << 5) * 3) {
			var_66[var_79] = '' + var_67[int(var_78.charAt(var_79))]();
			var_79 ++;
		}
		
		var var_80 = var_66.join('') + flash_tm;
		
		var_61(var_66, var_80);
		var_61(var_66, var_60);
		
		var var_81 = function(param1) {
			var k = null;
			var name_11 = 0;
			var name_10 = param1;
			
			k = [];
			name_11 = 16;
			
			var t = 0;
			
			while (t < name_11 << 2) {
				k[t] = 0 | Math.abs(Math.sin(++t)) * 4.294967296E9;
			}
			
			var add = function(param1, param2) {
				return ((param1 >> 1) + (param2 >> 1) << 1) + (param1 & 1) + (param2 & 1);
			};
			
			var msg = function() {
				var _loc1 = NaN;
				var _loc2 = NaN;
				var _loc3 = NaN;
				var _loc5 = 0;
				var _loc15 = null;
				var _loc4 = 0;
				var _loc6 = [];
				var _loc7 = unescape(encodeURI(name_10));
				var _loc8 = _loc7.length;
				var _loc9 = [_loc1 = 1732584193,_loc2 = -271733879,~_loc1,~_loc2];
				var _loc10 = [0.0,0.0,0.0,0.0];
				var _loc11 = [0,0,0,0];
				var _loc12 = [7,4 * 3,17,22,5,3 * 3,14,20,4,11,name_11,23,2 * 3,10,5 * 3,7 * 3];
				
				while (_loc4 <= _loc8) {
					_loc6[_loc4 >> 2] = _loc6[_loc4 >> 2] | (_loc7.charCodeAt(_loc4) || 1 << 7) << 8 * (_loc4++ % 4);
				}
				
				var _loc13 = (1 + (_loc8 + 8 >> 6)) * name_11 - 2;
				
				_loc6[_loc13] = _loc8 * 8;
				_loc4 = 0;
				
				while (_loc4 < _loc13) {
					_loc15 = _loc9.concat();
					_loc5 = 0;
					
					while (_loc5 < name_11 * 4) {
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
						_loc15 = [_loc3 = _loc15[3],add(_loc1 = _loc15[1],(_loc3 = add(add(_loc15[0],_loc10[_loc8 = _loc5 >> 4]),add(k[_loc5],_loc6[_loc11[_loc8] % name_11 + _loc4]))) << (_loc8 = _loc12[4 * _loc8 + _loc5++ % 4]) | _loc3 >>> 32 - _loc8),_loc1,_loc2];
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
		
		var var_82 = {};
		// var var_83 = var_81(var_66.join(''));
		
		var _raw1 = var_66.join('');
		var var_83 = var_81(_raw1);
		
		if (var_83.length > 4) {
			var_82.src = var_81;
			var_82.tm = var_80;
			var_82.sc = var_83;
			
			var_82.raw = _raw1;
		}
		
		return var_82;
	}

// second mix function
	function sc(main_mix_obj, flash_tm, tvid) {
		var param1 = main_mix_obj;
		
		var _loc2 = param1.tm.split('');
		var _loc3 = [];
		var _loc4 = 0;
		var _loc5 = 0;
		var _loc6 = (1 << 4) * ((1 << 3) - (1 << 1));
		var _loc7 = 0;
		
		while (_loc7 < _loc6) {
			_loc4 = int(_loc2[_loc7]);
			
			_loc5 = _loc5 + _loc4 * _loc4 * _loc4 % 10 * Math.pow(10,2 - _loc7 % 3);
			
			if (_loc7 % 3 == 2) {
				_loc3.push(String.fromCharCode(_loc5));
				_loc5 = 0;
			}
			
			_loc7 ++;
		}
		
		return param1.src(_loc3.join('') + flash_tm + tvid);
	}

// entry mix function
	function mix(tvid, flash_tm) {
		var out = ekam(tvid, flash_tm);
		out.sc_sc = sc(out, flash_tm, tvid);
	}

/* try to export */
try {
	// functions
	exports.mix = ekam;	// ekam(tvid, flash_tm);
	exports.sc = sc;	// sc(main_mix_obj, flash_tm, tvid);
} catch (e) {
}

/* end SingletonClass.js */




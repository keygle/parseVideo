/* SingletonClass.js, parse_video/lib/bks1/o
 * last_update 2015-07-04 10:55 GMT+0800 CST
 */

//	import flash.utils.getTimer;

/* function */

// base functions
	function int(n) {
		return Math.floor(n);
	}

// fix SingletonClass
var SingletonClass = {};

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
			// return !(SingletonClass instanceof Object)?Math.random() * var_67.length:var_67.indexOf(var_71);
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
		// FIXME debug here
		var _raw_before = var_66.join('')
		
		var_61(var_66, var_60);	// TODO NOTE add tvid here
		
		// NOTE var_81 is just the md5_hash function
		var var_81 = function(param1) {};	// TODO
		
		var var_82 = {};
		// var var_83 = var_81(var_66.join(''));
		
		var _raw1 = var_66.join('');	// TODO NOTE here, append var_60
		var var_83 = var_81(_raw1);
		
		// FIXME debug here
		var_82.src = var_81;
		var_82.tm = var_80;
		var_82.sc = var_83;
		
		var_82.raw = _raw1;
		var_82.raw_before = _raw_before;
		
		return var_82;
	}

// second mix function
	function mix_sc(main_mix_obj, flash_tm, tvid) {
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
		
		// return param1.src(_loc3.join('') + flash_tm + tvid);
		var out = {};
		out.raw_before = _loc3.join('');
		out.raw = _loc3.join('') + flash_tm + tvid;
		out.sc = param1.src(out.raw);
		return out;
	}

// entry mix function
	function mix(tvid, flash_tm) {
		var out = {};
		out.ekam = ekam(tvid, flash_tm);
		out.sc = mix_sc(out.ekam, flash_tm, tvid);
		
		return out;
	}

/* try to export */
try {
	// functions
	exports.ekam = ekam;	// ekam(tvid, flash_tm);
	exports.sc = mix_sc;	// mix_sc(main_mix_obj, flash_tm, tvid);
	
	exports.mix = mix;	// mix(tvid, flash_tm);
} catch (e) {
}

/* end SingletonClass.js */




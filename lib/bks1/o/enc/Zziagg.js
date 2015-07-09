/* Zziagg.js, parse_video/lib/bks1/o/enc
 * last_update 2015-07-09 21:57 GMT+0800 CST
 */

//	import flash.utils.Dictionary;
//	import flash.utils.getTimer;

/* function */

// base functions
	function int(n) {
		return Math.floor(n);
	}

// fix Zziagg, fix _dic
var Zziagg = {};
var _dic = null;


// public class Zziagg extends Object
// var _dic:Dictionary = null;

// main mix function ekam()
// public static function kcusu(param1:String) : Object
	function kcusu(tvid, flash_tm) {
		
		var param1 = tvid;
		
		var var_64 = null;
		var var_69 = null;
		var var_70 = null;
		var var_71 = null;
		var var_72 = null;
		var var_73 = null;
		var var_74 = null;
		var var_75 = null;
		var var_76 = null;
		var var_77 = null;
		var var_78 = null;
		var var_79 = null;
		var arrStr = null;
		var var_85 = null;
		var var_86 = 0;
		var var_87 = 0;
		var var_88 = 0;
		var var_89 = 0;
		var var_62 = param1;
		
		// fill _dic start
		if (_dic == null) {
			// _dic = new Dictionary();
			_dic = {};
			
			_dic["cfcd208495d565ef66e7dff9f98764da"] = "f642e92efb79421734881b53e1e1b18b6";
			_dic["c4ca4238a0b923820dcc509a6f75849b"] = "ff457c545a9ded88f18ecee47145a72c0";
			_dic["c81e728d9d4c2f636f067f89cc14862c"] = "fc0c7c76d30bd3dcaefc96f40275bdc0a";
			_dic["eccbc87e4b5ce2fe28308fd9f2a7baf3"] = "f2838023a778dfaecdc212708f721b788";
			_dic["a87ff679a2f3e71d9181a67b7542122c"] = "f9a1158154dfa42caddbd0694a4e9bdc8";
			_dic["e4da3b7fbbce2345d7772b0674a318d5"] = "fd82c8d1619ad8176d665453cfb2e55f0";
			_dic["1679091c5a880faf6fb5e6087eb1b2dc"] = "fa684eceee76fc522773286a895bc8436";
			_dic["8f14e45fceea167a5a36dedd4bea2543"] = "fb53b3a3d6ab90ce0268229151c9bde11";
			_dic["c9f0f895fb98ab9159f51fd0297e236d"] = "f9f61408e3afb633e50cdf1b20de6f466";
			_dic["45c48cce2e2d7fbdea1afc51c7c6ad26"] = "f72b32a1f754ba1c09b3695e0cb6cde7f";
			_dic["0cc175b9c0f1b6a831c399e269772661"] = "fe2ef524fbf3d9fe611d5a8e90fefdc9c";
			_dic["92eb5ffee6ae2fec3ad71c777531578f"] = "fed3d2c21991e3bef5e069713af9fa6ca";
			_dic["4a8a08f09d37b73795649038408b5f33"] = "fac627ab1ccbdb62ec96e702f07f6425b";
			_dic["8277e0910d750195b448797616e091ad"] = "ff899139df5e1059396431415e770c6dd";
			_dic["e1671797c52e15f763380b45e841ec32"] = "f38b3eff8baf56627478ec76a704e9b52";
			_dic["8fa14cdd754f91cc6554c9e71929cce7"] = "fec8956637a99787bd197eacd77acce5e";
			
			_dic["EtvnetLtisneRE"] = new EtvnetLtisenRE();
		}
		// fill _dic end
		
		var var_63 = function(param1, param2) {
			param1.push(param2);
		};
		
		var_64 = [];
		
		// fill var_64 start
		var_63(var_64,"d41d8cd98f00b204e9800998ecf8427e");
		var_63(var_64,"8f14e45fceea167a5a36dedd4bea2543");
		var_63(var_64,"45c48cce2e2d7fbdea1afc51c7c6ad26");
		var_63(var_64,"eccbc87e4b5ce2fe28308fd9f2a7baf3");
		var_63(var_64,"1679091c5a880faf6fb5e6087eb1b2dc");
		var_63(var_64,"c4ca4238a0b923820dcc509a6f75849b");
		var_63(var_64,"c4ca4238a0b923820dcc509a6f75849b");
		var_63(var_64,"92eb5ffee6ae2fec3ad71c777531578f");
		var_63(var_64,"92eb5ffee6ae2fec3ad71c777531578f");
		var_63(var_64,"0cc175b9c0f1b6a831c399e269772661");
		var_63(var_64,"a87ff679a2f3e71d9181a67b7542122c");
		var_63(var_64,"eccbc87e4b5ce2fe28308fd9f2a7baf3");
		var_63(var_64,"a87ff679a2f3e71d9181a67b7542122c");
		var_63(var_64,"45c48cce2e2d7fbdea1afc51c7c6ad26");
		var_63(var_64,"c81e728d9d4c2f636f067f89cc14862c");
		var_63(var_64,"e1671797c52e15f763380b45e841ec32");
		var_63(var_64,"8277e0910d750195b448797616e091ad");
		var_63(var_64,"8fa14cdd754f91cc6554c9e71929cce7");
		var_63(var_64,"1679091c5a880faf6fb5e6087eb1b2dc");
		var_63(var_64,"e4da3b7fbbce2345d7772b0674a318d5");
		var_63(var_64,"c9f0f895fb98ab9159f51fd0297e236d");
		var_63(var_64,"e1671797c52e15f763380b45e841ec32");
		var_63(var_64,"8fa14cdd754f91cc6554c9e71929cce7");
		var_63(var_64,"45c48cce2e2d7fbdea1afc51c7c6ad26");
		var_63(var_64,"a87ff679a2f3e71d9181a67b7542122c");
		var_63(var_64,"8277e0910d750195b448797616e091ad");
		var_63(var_64,"a87ff679a2f3e71d9181a67b7542122c");
		var_63(var_64,"c9f0f895fb98ab9159f51fd0297e236d");
		var_63(var_64,"c81e728d9d4c2f636f067f89cc14862c");
		var_63(var_64,"a87ff679a2f3e71d9181a67b7542122c");
		var_63(var_64,"e4da3b7fbbce2345d7772b0674a318d5");
		var_63(var_64,"8277e0910d750195b448797616e091ad");
		var_63(var_64,"cfcd208495d565ef66e7dff9f98764da");
		var_63(var_64,"37a6259cc0c1dae299a7866489dff0bd");
		// fill var_64 end
		
		var var_65 = function(param1) {
			return String.fromCharCode(param1);
		};
		var var_66 = function(param1) {
			return param1 > 0;
		};
		var var_67 = function(param1, param2) {
			var_63(param1,param2);
		};
		
		var var_68 = [];
		
		// NOTE this may be a dead block
		while ("0" > "1") {	// DEAD block, while (false)
			var_85 = var_64.shift();
			var_86 = 0;
			var_87 = 0;
			var_88 = var_85.length / 2 - 1;
			var_89 = var_88;
			while(var_89 >= 0)
			{
				var_87 = var_87 + int(var_85.charAt((1 << 2) + var_89)) * (1 << var_88 - var_89);
				var_86 = var_86 + int(var_85.charAt((0 << 2) + var_89)) * (1 << var_88 - var_89);
				var_89--;
			}
			var_67(var_68,var_86);
			var_67(var_68,var_87);
		}	// DEAD block end
		
		var_69 = [];
		
		var_70 = function() {
			return true?var_69.indexOf(var_72):Math.random() * var_69.length;
		};
		var_71 = function() {
			return var_69.indexOf(var_71);
		};
		var_72 = function() {
			return 0?Math.random() * var_69.length:var_69.indexOf(var_76);
		};
		var_73 = function() {
			return 1?var_69.indexOf(var_70):Math.random() * var_69.length;
		};
		var_74 = function() {
			return null?Math.random() * var_69.length:var_69.indexOf(var_75);
		};
		var_75 = function() {
			return "a" < "b"?var_69.indexOf(var_74):Math.random() * var_69.length;
		};
		var_76 = function() {
			// return !(Zziagg is Object)?Math.random() * var_69.length:var_69.indexOf(var_73);
			return !(Zziagg instanceof Object)?Math.random() * var_69.length:var_69.indexOf(var_73);
		};
		var_77 = function() {
			return int(undefined)?Math.random() * var_69.length:var_69.indexOf(var_78);
		};
		var_78 = function() {
			return 1 & 1?var_69.indexOf(var_79):Math.random() * var_69.length;
		};
		var_79 = function() {
			return "\'" == ""?Math.random() * var_69.length:var_69.indexOf(var_77);
		};
		
		// NOTE may be a dead block, while (false)
		while (0) {	// DEAD block
			var_63(var_68,var_65(var_66(var_64[var_64.length - 1])?int(var_64.shift() * (1 << 8)) - (1 << 7):int(var_64.pop() * (1 << 8)) + (1 << 7)));
		}	// DEAD block end
		
		var_63(var_69,var_70);
		var_63(var_69,var_71);
		var_63(var_69,var_72);
		var_63(var_69,var_73);
		var_63(var_69,var_74);
		var_63(var_69,var_75);
		var_63(var_69,var_76);
		var_63(var_69,var_77);
		var_63(var_69,var_78);
		var_63(var_69,var_79);
		
		arrStr = var_68.join("") + "7b11c5408ff342318da3e7c97b92e890";
		
		var var_80 = 0;
		
		while (var_80 <= var_68.length) {
			if (var_64.shift() > var_64.pop()) {
				break;
			}
			var_68[var_80] = "" + var_69[int(arrStr.charAt(var_80))]();
			var_80++;
		}
		
		// NOTE var_68.join('') may be the salt string
		
		// NOTE export salt string here
		var _tmp_salt = var_68.join('');
		
		// NOTE flash_tm here
		// var var_81:uint = getTimer();
		var var_81 = flash_tm;
		
		var_63(var_68,var_81);	// NOTE append tm here
		var_63(var_68,var_62);	// NOTE append tvid here
		
		// NOTE var_82 may be the md5_hash function
		var var_82 = function(param1) {
			var k = null;
			var name_11 = 0;
			var name_10 = param1;
			
			k = [];
			name_11 = 16;
			arrStr = '';
			
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
				var _loc7 = unescape(encodeURI(arrStr));
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
			};	// end msg() function
			
			while (var_64.length) {
				arrStr = arrStr + _dic["EtvnetLtisneRE"][_dic[var_64.shift()]]();
			}
			
			arrStr = arrStr + name_10;
			
			return msg();
		};	// end function may be md5_hash
		
		// var var_84 = var_82(var_68.join(""));
		var _tmp_raw = var_68.join('');
		var var_84 = var_82(_tmp_raw);
		// NOTE var_84 should be the string after md5_hash
		//      and var_82 should be the md5_hash function
		
		var var_83 = {};
		// NOTE just export
		var_83.src = var_82;
		var_83.tm = var_81;
		var_83.sc = var_84;
		
		// NOTE add raw and salt string
		var_83.raw = _tmp_raw;
		var_83.salt = _tmp_salt;
		
		// done
		return var_83;
	}
// end main mix function


// class EtvnetLtisneRE extends Object
function EtvnetLtisneRE() {
	
	this.f642e92efb79421734881b53e1e1b18b6 = function() {
		return 0;
	}
	
	this.ff457c545a9ded88f18ecee47145a72c0 = function() {
		return 1;
	}
	
	this.fc0c7c76d30bd3dcaefc96f40275bdc0a = function() {
		return 2;
	}
	
	this.f2838023a778dfaecdc212708f721b788 = function() {
		return 3;
	}
	
	this.f9a1158154dfa42caddbd0694a4e9bdc8 = function() {
		return 4;
	}
	
	this.fd82c8d1619ad8176d665453cfb2e55f0 = function() {
		return 5;
	}
	
	this.fa684eceee76fc522773286a895bc8436 = function() {
		return 6;
	}
	
	this.fb53b3a3d6ab90ce0268229151c9bde11 = function() {
		return 7;
	}
	
	this.f9f61408e3afb633e50cdf1b20de6f466 = function() {
		return 8;
	}
	
	this.f72b32a1f754ba1c09b3695e0cb6cde7f = function() {
		return 9;
	}
	
	this.fe2ef524fbf3d9fe611d5a8e90fefdc9c = function() {
		return 10;
	}
	
	this.fed3d2c21991e3bef5e069713af9fa6ca = function() {
		return 11;
	}
	
	this.fac627ab1ccbdb62ec96e702f07f6425b = function() {
		return 12;
	}
	
	this.ff899139df5e1059396431415e770c6dd = function() {
		return 13;
	}
	
	this.f38b3eff8baf56627478ec76a704e9b52 = function() {
		return 14;
	}
	
	this.fec8956637a99787bd197eacd77acce5e = function() {
		return 15;
	}
}	// end EtvnetLtisneRE class


// class EtvnetLtisenRE extends Object
function EtvnetLtisenRE() {
	
	//
	
	this.f642e92efb79421734881b53e1e1b18b6 = function() {
		return this.var_1.indexOf(this.fec8956637a99787bd197eacd77acce5e).toString(this.var_2);
	}
	
	this.ff457c545a9ded88f18ecee47145a72c0 = function() {
		return this.var_1.indexOf(this.f642e92efb79421734881b53e1e1b18b6).toString(this.var_2);
	}
	
	this.fc0c7c76d30bd3dcaefc96f40275bdc0a = function() {
		return this.var_1.indexOf(this.f38b3eff8baf56627478ec76a704e9b52).toString(this.var_2);
	}
	
	this.f2838023a778dfaecdc212708f721b788 = function() {
		return this.var_1.indexOf(this.ff457c545a9ded88f18ecee47145a72c0).toString(this.var_2);
	}
	
	this.f9a1158154dfa42caddbd0694a4e9bdc8 = function() {
		return this.var_1.indexOf(this.ff899139df5e1059396431415e770c6dd).toString(this.var_2);
	}
	
	this.fd82c8d1619ad8176d665453cfb2e55f0 = function() {
		return this.var_1.indexOf(this.fc0c7c76d30bd3dcaefc96f40275bdc0a).toString(this.var_2);
	}
	
	this.fa684eceee76fc522773286a895bc8436 = function() {
		return this.var_1.indexOf(this.fac627ab1ccbdb62ec96e702f07f6425b).toString(this.var_2);
	}
	
	this.fb53b3a3d6ab90ce0268229151c9bde11 = function() {
		return this.var_1.indexOf(this.f2838023a778dfaecdc212708f721b788).toString(this.var_2);
	}
	
	this.f9f61408e3afb633e50cdf1b20de6f466 = function() {
		return this.var_1.indexOf(this.fed3d2c21991e3bef5e069713af9fa6ca).toString(this.var_2);
	}
	
	this.f72b32a1f754ba1c09b3695e0cb6cde7f = function() {
		return this.var_1.indexOf(this.f9a1158154dfa42caddbd0694a4e9bdc8).toString(this.var_2);
	}
	
	this.fe2ef524fbf3d9fe611d5a8e90fefdc9c = function() {
		return this.var_1.indexOf(this.fe2ef524fbf3d9fe611d5a8e90fefdc9c).toString(this.var_2);
	}
	
	this.fed3d2c21991e3bef5e069713af9fa6ca = function() {
		return this.var_1.indexOf(this.fd82c8d1619ad8176d665453cfb2e55f0).toString(this.var_2);
	}
	
	this.fac627ab1ccbdb62ec96e702f07f6425b = function() {
		return this.var_1.indexOf(this.fa684eceee76fc522773286a895bc8436).toString(this.var_2);
	}
	
	this.ff899139df5e1059396431415e770c6dd = function() {
		return this.var_1.indexOf(this.f72b32a1f754ba1c09b3695e0cb6cde7f).toString(this.var_2);
	}
	
	this.f38b3eff8baf56627478ec76a704e9b52 = function() {
		return this.var_1.indexOf(this.fb53b3a3d6ab90ce0268229151c9bde11).toString(this.var_2);
	}
	
	this.fec8956637a99787bd197eacd77acce5e = function() {
		return this.var_1.indexOf(this.f9f61408e3afb633e50cdf1b20de6f466).toString(this.var_2);
	}
	
	//
	this.var_2 = 1 << 4;
	// super();
	this.var_1 = new Array();
	this.var_1.push(this.f642e92efb79421734881b53e1e1b18b6);
	this.var_1.push(this.ff457c545a9ded88f18ecee47145a72c0);
	this.var_1.push(this.fc0c7c76d30bd3dcaefc96f40275bdc0a);
	this.var_1.push(this.f2838023a778dfaecdc212708f721b788);
	this.var_1.push(this.f9a1158154dfa42caddbd0694a4e9bdc8);
	this.var_1.push(this.fd82c8d1619ad8176d665453cfb2e55f0);
	this.var_1.push(this.fa684eceee76fc522773286a895bc8436);
	this.var_1.push(this.fb53b3a3d6ab90ce0268229151c9bde11);
	this.var_1.push(this.f9f61408e3afb633e50cdf1b20de6f466);
	this.var_1.push(this.f72b32a1f754ba1c09b3695e0cb6cde7f);
	this.var_1.push(this.fe2ef524fbf3d9fe611d5a8e90fefdc9c);
	this.var_1.push(this.fed3d2c21991e3bef5e069713af9fa6ca);
	this.var_1.push(this.fac627ab1ccbdb62ec96e702f07f6425b);
	this.var_1.push(this.ff899139df5e1059396431415e770c6dd);
	this.var_1.push(this.f38b3eff8baf56627478ec76a704e9b52);
	this.var_1.push(this.fec8956637a99787bd197eacd77acce5e);
	//
}	// end EtvnetLtisenRE class


// entry mix function
	function mix(tvid, flash_tm) {
		// just use kcusu()
		return kcusu(tvid, flash_tm);
	}

/* try to export */
try {
	// functions
	exports.kcusu = kcusu;	// kcusu(tvid, flash_tm);
	
	exports.mix = mix;	// mix(tvid, flash_tm);
} catch (e) {
}

/* end Zziagg.js */



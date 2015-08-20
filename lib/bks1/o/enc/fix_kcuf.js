/* fix_kcuf.js, parse_video/lib/bks1/o/enc
 * last_update 2015-08-20 21:33 GMT+0800 CST
 * fix_kcuf: fix Zombie.kcuf 
 */

// fix 1 from package com.qiyi.player.core.model.impls.pub Settings
	function fix_1(kcuf) {
		
		function f9f61408e3afb633e50cdf1b20de6f466() {
			return 0;
		}
		function fa684eceee76fc522773286a895bc8436() {
			return 1;
		}
		function fb53b3a3d6ab90ce0268229151c9bde11() {
			return 12;
		}
		
		// _instance = new Settings(new SingletonClass());
		// Zombie.kcuf.push(_instance.fa684eceee76fc522773286a895bc8436);
		// Zombie.kcuf.push(_instance.fb53b3a3d6ab90ce0268229151c9bde11);
		// Zombie.kcuf.push(_instance.f9f61408e3afb633e50cdf1b20de6f466);
		kcuf.push(fa684eceee76fc522773286a895bc8436);
		kcuf.push(fb53b3a3d6ab90ce0268229151c9bde11);
		kcuf.push(f9f61408e3afb633e50cdf1b20de6f466);
	}

// fix 2 from package com.qiyi.player.core.model.impls.pub Statistics
	function fix_2(kcuf) {
		
		function f72b32a1f754ba1c09b3695e0cb6cde7f() {
			return 11;
		};
		function fac627ab1ccbdb62ec96e702f07f6425b() {
			return 6;
		};
		function fe2ef524fbf3d9fe611d5a8e90fefdc9c() {
			return 7;
		};
		function fed3d2c21991e3bef5e069713af9fa6ca() {
			return 4;
		};
		
		kcuf.push(f72b32a1f754ba1c09b3695e0cb6cde7f);
		kcuf.push(fe2ef524fbf3d9fe611d5a8e90fefdc9c);
		kcuf.push(fed3d2c21991e3bef5e069713af9fa6ca);
		kcuf.push(fac627ab1ccbdb62ec96e702f07f6425b);
	}

// fix 3 from package com.qiyi.player.core.model.utils LogManager
	function fix_3(kcuf) {
		
		function f642e92efb79421734881b53e1e1b18b6() {
			return 15;
		};
		function fc0c7c76d30bd3dcaefc96f40275bdc0a() {
			return 2;
		};
		function ff457c545a9ded88f18ecee47145a72c0() {
			return 8;
		};
		
		kcuf.push(f642e92efb79421734881b53e1e1b18b6);
		kcuf.push(ff457c545a9ded88f18ecee47145a72c0);
		kcuf.push(fc0c7c76d30bd3dcaefc96f40275bdc0a);
	}

// fix 4 from package com.qiyi.player.core.video.render StageVideoManager
	function fix_4(kcuf) {
		
		function ff899139df5e1059396431415e770c6dd() {
			return 14;
		}
		function fec8956637a99787bd197eacd77acce5e() {
			return 5;
		}
		function f38b3eff8baf56627478ec76a704e9b52() {
			return 9;
		}
		
		kcuf.push(ff899139df5e1059396431415e770c6dd);
		kcuf.push(f38b3eff8baf56627478ec76a704e9b52);
		kcuf.push(fec8956637a99787bd197eacd77acce5e);
	}

// fix 5 from package com.qiyi.player.core CoreManager
	function fix_5(kcuf) {
		
		function f2838023a778dfaecdc212708f721b788() {
			return 13;
		}
		function fd82c8d1619ad8176d665453cfb2e55f0() {
			return 10;
		}
		function f9a1158154dfa42caddbd0694a4e9bdc8() {
			return 3;
		}
		
		kcuf.push(f2838023a778dfaecdc212708f721b788);
		kcuf.push(f9a1158154dfa42caddbd0694a4e9bdc8);
		kcuf.push(fd82c8d1619ad8176d665453cfb2e55f0);
	}

// fix list
var fix_list = [
	fix_1, 
	fix_2, 
	fix_3, 
	fix_4, 
	fix_5, 
];

/* try to exports for node.js */
try {
	exports.fix_list = fix_list;
} catch (e) {
}

/* end fix_kcuf.js */



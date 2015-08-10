/* node_utils.js, parse_video/lib/bks1/o/enc
 * node_utils: utils in node.js to test and DEBUG o/enc
 * version 0.0.5.0 test201508102319
 */

/* require import modules */

// node.js modules

// o/enc modules
var _Zombie = require('./Zombie.js');
var _AObject = require('./AObject.js');

var _fix_kcuf = require('./fix_kcuf.js');

/* base functions */

// flash int() function
	function int(n) {
		return Math.floor(n);
	}

// make_a function, make a host funcion
	function make_a_host(to) {
		// init vars
		var out = [];
		var pre = [];
		var rest = to.concat();
		
		// start generate
		make_a(out, pre, rest);
		// done
		return out;
	}
	
	function make_a(out, pre, rest) {
		
		// add one item
		for (var i = 0; i < rest.length; i++) {
			var now = rest[i];
			var rest2 = [].concat(rest.slice(0, i), rest.slice(i + 1, rest.length));
			
			// check rest2
			if (rest2.length < 1) {
				// make one item now
				var one = pre.concat(now);
				// add this item to out
				out.push(one);
			} else {	// increase pre and call sub
				var pre2 = pre.concat(now);
				make_a(out, pre2, rest2);
			}
		}
		// done
	}

/* functions */

// fix kcuf
	function fix_kcuf(fix_order) {
		// make a kcuf Array
		var kcuf = [];
		
		var fix_list = _fix_kcuf.fix_list;
		// use each fix in fix_order
		for (var i = 0; i < fix_order.length; i++) {
			var j = fix_order[i];
			var fix_fun = fix_list[j];
			// do fix it
			fix_fun(kcuf);
		}
		// just set kcuf
		_Zombie.set_kcuf(kcuf);
		// fix done
		return kcuf;
	}

// fix AObject
	function fix_AObject() {
		// just set it
		_Zombie.set_thd(new _AObject.AObject());
	}

// main mix function
	function mix(tvid, flash_tm) {
		// just use core function, without check
		var result = _Zombie.bite(tvid, flash_tm);
		return result;
	}

// DEBUG test functions

// test_one
	function test_one() {
		// NOTE this will not fix AObject and kcuf
		
		var ok_result = {
			'tvid' : '383710900', 
			'tm' : '529', 
			'enc' : 'a0c3dd3cb87cee97f4c0b29a76bc6f14', 
		};	// got salt 7c4d2505ad0544b88c7679c65d6748a1 NOTE this salt is too old
		// http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c&tvId=383710900&vid=8ce624169c9610b27455b6199bf83d28&vinfo=1&tm=529&enc=a0c3dd3cb87cee97f4c0b29a76bc6f14&qyid=58a117c772db7ca5fec28cdb65ee6ab5&puid=&authKey=18900c00f1f10bd54030f2b438441a82&um=0&thdk=&thdt=&tn=0.693233469966799
		
		var tvid = ok_result.tvid;
		var tm = ok_result.tm;
		// just run test
		var out = mix(tvid, tm);
		
		// check result
		var result = (out.sc == ok_result.enc);
		out._result = result;
		
		// done
		return out;
	}

// NOTE test_all: [ OK ] found result with tlist [2,4,0,1,3]

// just use OK test fix kcuf sort [2, 4, 0, 1, 3]
	function gen_ok_test() {
		var ok_sort = [2, 4, 0, 1, 3];
		// init before start test
		fix_kcuf(ok_sort);	// fix kcuf
		// init AObject
		fix_AObject();
		
		// just start test and output result
		var result = test_one();
		result._result = null;	// fix _result OK flag
		// done
		return result;
	}

// test_all
	function test_all() {
		// gen pre-test list
		var fix_list = _fix_kcuf.fix_list;
		var pre_tlist = [];
		for (var i = 0; i < fix_list.length; i++) {
			pre_tlist.push(i);
		}
		// gen test list
		var tlist = make_a_host(pre_tlist);
		// DEBUG info
		console.log('test_all: INFO: gen test list ... length ' + tlist.length);
		
		// fix AObject before test
		fix_AObject();
		
		// check and output all results
		var ok = [];
		
		// check each type
		for (var i = 0; i < tlist.length; i++) {
			// test one
			console.log('test_all: INFO: test ' + (i + 1) + ' of ' + tlist.length + ' ... ');
			
			// fix kcuf
			fix_kcuf(tlist[i]);
			
			var result = test_one();
			if (result._result == true) {
				// test OK
				console.log('test_all: [ OK ] found result with tlist [' + tlist[i] + '] ');
				
				// save tlist[i]
				result._tlist = tlist[i];
				// save results
				ok.push(result);
				
				// FIXME NOTE not test so much
				// break;
			}
		}
		// test all done, output all results
		return ok;
	}

/* exports */

// functions
exports.int = int;	// int(n);

exports.make_a_host = make_a_host;	// make_a_host(to);

exports.fix_kcuf = fix_kcuf;		// fix_kcuf();
exports.fix_AObject = fix_AObject;	// fix_AObject();

exports.mix = mix;	// mix(tvid, flash_tm);

exports.test_one = test_one;	// test_one();
exports.test_all = test_all;	// test_all();

exports.gen_ok_test = gen_ok_test;	// gen_ok_test();

/* end node_utils.js */



/* node_utils.js, parse_video/lib/bks1/o/enc
 * node_utils: utils in node.js to test and DEBUG o/enc
 * version 0.0.1.0 test201507311222
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
			'tvid' : '', 
			'tm' : '', 
			'enc' : '', 
		};
		
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
			if (result._result = true) {
				// test OK
				console.log('test_all: [ OK ] found result with tlist [' + tlist[i] + '] ');
				
				// save tlist[i]
				result._tlist = tlist[i];
				// save results
				ok.push(result);
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

/* end node_utils.js */



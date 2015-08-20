/* MediaDota.js, parse_video/lib/bks1/o/enc
 * last_update 2015-08-20 22:04 GMT+0800 CST
 */

// package com.qiyi.player.core.video.engine.dm.provider
// public class MediaDota extends Object

// NOTE object MediaDota create method
	function MediaDota() {
		// get this to that first
		var that = this;
		
		// private var arr:Array = null;
		// private var n:int;
		that.n = 1 << 4;
		that.arr = new Array();
		
		// NOTE add functions here
		
		// NOTE add main data function here
		that.f0120a4f9196a5f9eb9f523f31f914da7 = function () {
			return that.arr.indexOf(that.f6226f7cbe59e99a90b5cef6f94f966fd).toString(that.n);
		}
		that.f51d4b581d21c20a16147b17c3adc7867 = function () {
			return that.arr.indexOf(that.f0120a4f9196a5f9eb9f523f31f914da7).toString(that.n);
		}
		that.f6a0cf6edf20060344b465706b61719aa = function () {
			return that.arr.indexOf(that.f9fbcd7dce5e3f334ca61dae6ad57415a).toString(that.n);
		}
		that.f490b2834e65737c1fce95e468cc8b8bf = function () {
			return that.arr.indexOf(that.fab0fd361fde5c3625fe76007f204cc04).toString(that.n);
		}
		that.f97b2f1edf640580f66056cc4bfcf6335 = function () {
			return that.arr.indexOf(that.f9abcde3c584628a02620bf796dee1204).toString(that.n);
		}
		that.f54e5d4f408cbc3af74b756eaea2fa199 = function () {
			return that.arr.indexOf(that.f5849253c0c07f8894c9ff2e5b69e834a).toString(that.n);
		}
		that.f5849253c0c07f8894c9ff2e5b69e834a = function () {
			return that.arr.indexOf(that.f6a0cf6edf20060344b465706b61719aa).toString(that.n);
		}
		that.fab0fd361fde5c3625fe76007f204cc04 = function () {
			return that.arr.indexOf(that.f569ef72642be0fadd711d6a468d68ee1).toString(that.n);
		}
		that.f0449904fbf32607bf8ce5c26823dbc29 = function () {
			return that.arr.indexOf(that.fe529a9cea4a728eb9c5828b13b22844c).toString(that.n);
		}
		that.fe529a9cea4a728eb9c5828b13b22844c = function () {
			return that.arr.indexOf(that.f97b2f1edf640580f66056cc4bfcf6335).toString(that.n);
		}
		that.f6226f7cbe59e99a90b5cef6f94f966fd = function () {
			return that.arr.indexOf(that.f490b2834e65737c1fce95e468cc8b8bf).toString(that.n);
		}
		that.f569ef72642be0fadd711d6a468d68ee1 = function () {
			return that.arr.indexOf(that.f51d4b581d21c20a16147b17c3adc7867).toString(that.n);
		}
		that.f0d47b8346d57b12a5807c36fb1f14f3c = function () {
			return that.arr.indexOf(that.f54e5d4f408cbc3af74b756eaea2fa199).toString(that.n);
		}
		that.fff78648be52a4e79513f4e70b266c62a = function () {
			return that.arr.indexOf(that.f0449904fbf32607bf8ce5c26823dbc29).toString(that.n);
		}
		that.f9fbcd7dce5e3f334ca61dae6ad57415a = function () {
			return that.arr.indexOf(that.fff78648be52a4e79513f4e70b266c62a).toString(that.n);
		}
		that.f9abcde3c584628a02620bf796dee1204 = function () {
			return that.arr.indexOf(that.f0d47b8346d57b12a5807c36fb1f14f3c).toString(that.n);
		}
		// NOTE add main data function done
		
		// NOTE push function
		that.f98c956637a99787bd197eacd77acce5e(param1) {
			that.arr.push(param1);
		}
		// NOTE data export function, seek
		that.seek = function (param1) {
			return that.arr[param1]();
		}
	}
// NOTE end MediaDota

// try to export for node.js
try {
	exports.MediaDota = MediaDota;	// new MediaDota();
} catch (e) {
}

/* end MediaDota.js */




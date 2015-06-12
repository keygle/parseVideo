/* node_port.js, part for evparse : EisF Video Parse, evdh Video Parse. 
 * node_port: iqiyi, node_port for DMEmagelzzup 
 */

/* require import modules */
var dp = require('./DMEmagelzzup.js');

/* functions */

/* main function */
	function main() {
		// get args from command line
		var arg = process.argv.slice(2);
		
		// get info for dp
		var tvid = arg[0];
		var tm = parseInt(arg[1]);
		
		// get output with dp
		var info = dp.mix(tvid, tm);
		// output as json
		var out = JSON.stringify(info);
		console.log(out);
		// done
	}

/* start from main */
	main();

/* end node_port.js */



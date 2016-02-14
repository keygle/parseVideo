/* m3u8_encrypt.c, parse_video/lib/e/letv/o/m3u8_encrypt/
 * NOTE do decode in python code is very slow. So write this to speed up. 
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// TODO ERROR process and log ERROR here

/* struct */

typedef struct text {
	int len;
	char * p;
} text;

// for process command line args
#define SM_NORMAL	0	// SM: Start Mode
#define SM_HELP		1	// --help
#define SM_VERSION	2	// --version

typedef struct command_args {
	int start_mode;	// in [SM_NORMAL, SM_HELP, SM_VERSION]
} command_args;


/* def */
#define OK	0
#define ERR	-1
#define FALSE	0
#define TRUE	1

#define STDIN_CHUNK_SIZE	(16 * 1024)	// 16 KB

int p_args(int argc, char ** argv, command_args * out);	// process command line arguments

// print functions
void p_cl_err(void);	// print bad command line format
void p_help(void);	// --help
void p_version(void);	// --version

int _start_normal(void);

// base text functions
int is_str(char * a, char * b);	// if a == b, return True (1)

text init_text_raw(void);
int init_text(text * p);
int free_text(text * p);

// I/O functions
int read_stdin(text * buffer);
int write_stdout(text * buffer);

// core decode functions
int decode_m3u8(text * input, text * output);
int _do_decode(text * raw, text * out);
int _decode_bytes(text * raw, text * out);
int _decode_bytes_v1(text * raw, text * out);


/* main */
int main(int argc, char ** argv) {
	command_args args;
	
	// process args
	if (p_args(argc, argv, &args)) {
		p_cl_err();
		return ERR;
	}
	// check start_mode
	switch(args.start_mode) {
	case SM_HELP:
		p_help();
		
		break;
	case SM_VERSION:
		p_version();
		
		break;
	case SM_NORMAL:
		if (_start_normal()) {
			// NOTE print ERROR here
			fprintf(stderr, "ERROR: unknow decode error \n");
			
			return ERR;
		}
		break;
	default:
		p_cl_err();
		return ERR;
	}
	return OK;
}

int p_args(int argc, char ** argv, command_args * out) {
	// NOTE only support --version and --help now
	if (argc > 2) {
		return ERR;
	}
	// init start_mode
	out -> start_mode = SM_NORMAL;
	if (argc < 2) {
		return OK;
	}
	// check --help, --version
	char * one = argv[1];
	if (is_str(one, "--help")) {
		out -> start_mode = SM_HELP;
	} else if (is_str(one, "--version")) {
		out -> start_mode = SM_VERSION;
	} else {
		return ERR;
	}
	return OK;
}

/* print functions */
void p_cl_err(void) {
	printf("ERROR: bad command line format, please try \"--help\" \n");
}

void p_help(void) {
	// TODO
	printf("WARNING: p_help() not finished \n");
}

void p_version(void) {
	// TODO
	printf("WARNING: p_version() not finished \n");
}


int _start_normal(void) {
	text input = init_text_raw(), output = init_text_raw();
	int ret = ERR;
	
	if (read_stdin(&input)) {
		return ERR;
	}
	
	if (decode_m3u8(&input, &output)) {
		goto clean_up;
	}
	
	if (!write_stdout(&output)) {
		ret = OK;
	}
clean_up:
	free_text(&input);
	free_text(&output);
	
	return ret;
}


/* I/O functions */

int read_stdin(text * buffer) {
	FILE * f = stdin;
	text buf = init_text_raw();	// read buffer
	
	buf.p = 0;
	buf.len = 0;
	
	// init output buffer
	buffer -> p = 0;
	buffer -> len = 0;
	
	// first chunk
	buf.len = STDIN_CHUNK_SIZE;
	buf.p = (char*)malloc(buf.len);
	if (buf.p == 0) {
		return ERR;
	}
	// read loop
	while (1) {
		// check EOF
		if (feof(f)) {
			break;	// read done
		}
		// read it in buffer
		int buf_rest_size = buf.len - buffer -> len;
		// check realloc, grow the buffer
		if (buf_rest_size < 1) {
			buf.len += STDIN_CHUNK_SIZE;
			
			char * new = (char*)realloc(buf.p, buf.len);
			if (new == 0) {	// clean up
				free(buf.p);
				return ERR;
			} else {
				buf.p = new;
			}
		}
		// read data
		int bytes_readed = fread(buf.p + buffer -> len, 1, buf_rest_size, f);
		// update info
		buffer -> len += bytes_readed;
	}
	// check set output
	if (buffer -> len > 0) {
		buffer -> p = buf.p;
	}
	return OK;
}

int write_stdout(text * buffer) {
	fwrite(buffer -> p, 1, buffer -> len, stdout);
	
	return OK;
}

/* base functions */

int init_text(text * p) {
	if (p == 0) {
		return ERR;
	}
	if (p -> len < 1) {
		return ERR;
	}
	p -> p = (char*)malloc(p -> len);
	if (p -> p == 0) {
		return ERR;
	}
	return OK;
}

text init_text_raw(void) {
	text out;
	out.p = 0;
	out.len = 0;
	return out;
}

int free_text(text * p) {
	if (p != 0) {
		if (p -> p != 0) {
			free(p -> p);
		}
		return OK;
	} else {
		return ERR;
	}
}

int is_str(char * a, char * b) {
	if (strcmp(a, b) == 0) {
		return TRUE;
	} else {
		return FALSE;
	}
}

/* core decode functions */

int decode_m3u8(text * input, text * output) {
	return _do_decode(input, output);
}

int _do_decode(text * raw, text * out) {
	char _version[5 + 1] = {0};
	char * version = (char*)&_version;
	
	if (raw -> len < 1) {
		return ERR;
	}
	// check version
	memcpy(version, raw -> p, 5);
	if (is_str(version, "VC_01") || is_str(version, "vc_01")) {
		if (_decode_bytes_v1(raw, out)) {
			return ERR;
		}
	} else if (_decode_bytes(raw, out)) {
		return ERR;
	}
	return OK;
}

int _decode_bytes(text * raw, text * out) {
	// NOTE just copy it here
	out -> len = raw -> len;
	if (init_text(out)) {
		return ERR;
	}
	memcpy(out -> p, raw -> p, raw -> len);
	return OK;
}

int _decode_bytes_v1(text * raw, text * out) {
	text data = init_text_raw();
	text first = init_text_raw();
	text second = init_text_raw();
	text before = init_text_raw();
	
	int ret = ERR;	// return code
	
	// data = raw[5:]
	data.len = raw -> len - 5;
	if (init_text(&data)) {
		goto clean_up;
	}
	memcpy(data.p, raw -> p + 5, data.len);
	
	// first = bytearray(len(data) * 2)
	first.len = data.len * 2;
	if (init_text(&first)) {
		goto clean_up;
	}
	for (int i = 0; i < data.len; i++) {
		first.p[2 * i] = data.p[i] >> 4;
		first.p[2 * i] &= 0x0f;	// NOTE fix BUG here
		
		first.p[2 * i + 1] = data.p[i] & 15;
	}
	
	// second = first[-11:] + first[:-11]
	second.len = first.len;
	if (init_text(&second)) {
		goto clean_up;
	}
	memcpy(second.p, first.p + first.len -11, 11);
	memcpy(second.p + 11, first.p, first.len -11);	// NOTE fix BUG here
	
	// before = bytearray(len(data))
	before.len = data.len;
	if (init_text(&before)) {
		goto clean_up;
	}
	for (int i = 0; i < data.len; i++) {
		before.p[i] = (second.p[2 * i] << 4) + second.p[2 * i + 1];
	}
	// done
	out -> len = before.len;
	out -> p = before.p;
	
	ret = OK;
clean_up:	// try to free memery
	free_text(&data);
	free_text(&first);
	free_text(&second);
	// NOTE not clean before, used as output
	return ret;
}


/* end m3u8_encrypt.c */



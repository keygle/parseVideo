<?php

class Youku {
	//直接获取优酷视频
	public static function parse($url){
        preg_match("#id\_([\w=]+)#", $url, $matches); //id里可以有=号
        if (empty($matches)){
            $html = Base::_cget($url);
            preg_match("#videoId2\s*=\s*\'(\w+)\'#", $html, $matches);
            if(!$matches) return false;
        }

        //根据you vid 获取相应的视频地址
        return static::_getYouku(trim($matches[1]));
	}

    //start 获得优酷视频需要用到的方法
    private static function getSid(){
        $sid = time().(mt_rand(0,9000)+10000);
        return $sid;
    }

    private static function getKey($key1,$key2){
        $a = hexdec($key1);
        $b = $a ^0xA55AA5A5;
        $b = dechex($b);
        return $key2.$b;
    }

    private static function getFileid($fileId,$seed){
        $mixed = static::getMixString($seed);
        $ids = explode("*",rtrim($fileId,'*')); //去掉末尾的*号分割为数组
        $realId = "";
        for ($i=0;$i<count($ids);$i++){
            $idx = $ids[$i];
            $realId .= substr($mixed,$idx,1);
        }  
        return $realId;
    } 

    private static function getMixString($seed){
        $mixed = "";
        $source = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890";
        $len = strlen($source);
        for($i=0;$i<$len;$i++){
            $seed = ($seed * 211 + 30031)%65536;
            $index = ($seed / 65536 * strlen($source));
            $c = substr($source,$index,1);
            $mixed .= $c;
            $source = str_replace($c,"",$source);
        }
        return $mixed;
    }
    private static function yk_d($a){
        if (!$a) {
            return '';
        }
        $f = strlen($a);
        $b = 0;
        $str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
        for ($c = ''; $b < $f;) {
            $e = static::charCodeAt($a, $b++) & 255;
            if ($b == $f) {
                $c .= static::charAt($str, $e >> 2);
                $c .= static::charAt($str, ($e & 3) << 4);
                $c .= '==';
                break;
            }
            $g = static::charCodeAt($a, $b++);
            if ($b == $f) {
                $c .= static::charAt($str, $e >> 2);
                $c .= static::charAt($str, ($e & 3) << 4 | ($g & 240) >> 4);
                $c .= static::charAt($str, ($g & 15) << 2);
                $c .= '=';
                break;
            }
            $h = static::charCodeAt($a, $b++);
            $c .= static::charAt($str, $e >> 2);
            $c .= static::charAt($str, ($e & 3) << 4 | ($g & 240) >> 4);
            $c .= static::charAt($str, ($g & 15) << 2 | ($h & 192) >> 6);
            $c .= static::charAt($str, $h & 63);
        }
        return $c;
    }
    private static function yk_na($a){
        if (!$a) {
            return '';
        }
        $sz = '-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,63,52,53,54,55,56,57,58,59,60,61,-1,-1,-1,-1,-1,-1,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,-1,-1,-1,-1,-1,-1,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1,-1';
        $h = explode(',', $sz);
        $i = strlen($a);
        $f = 0;
        for ($e = ''; $f < $i;) {
            do {
                $c = $h[static::charCodeAt($a, $f++) & 255];
            } while ($f < $i && -1 == $c);
            if (-1 == $c) {
                break;
            }
            do {
                $b = $h[static::charCodeAt($a, $f++) & 255];
            } while ($f < $i && -1 == $b);
            if (-1 == $b) {
                break;
            }
            $e .= static::fromCharCode($c << 2 | ($b & 48) >> 4);
            do {
                $c = static::charCodeAt($a, $f++) & 255;
                if (61 == $c) {
                    return $e;
                }
                $c = $h[$c];
            } while ($f < $i && -1 == $c);
            if (-1 == $c) {
                break;
            }
            $e .= static::fromCharCode(($b & 15) << 4 | ($c & 60) >> 2);
            do {
                $b = static::charCodeAt($a, $f++) & 255;
                if (61 == $b) {
                    return $e;
                }
                $b = $h[$b];
            } while ($f < $i && -1 == $b);
            if (-1 == $b) {
                break;
            }
            $e .= static::fromCharCode(($c & 3) << 6 | $b);
        }
        return $e;
    }
    private static function yk_e($a, $c){
        for ($f = 0, $i, $e = '', $h = 0; 256 > $h; $h++) {
            $b[$h] = $h;
        }
        for ($h = 0; 256 > $h; $h++) {
            $f = (($f + $b[$h]) + static::charCodeAt($a, $h % strlen($a))) % 256;
            $i = $b[$h];
            $b[$h] = $b[$f];
            $b[$f] = $i;
        }
        for ($q = ($f = ($h = 0)); $q < strlen($c); $q++) {
            $h = ($h + 1) % 256;
            $f = ($f + $b[$h]) % 256;
            $i = $b[$h];
            $b[$h] = $b[$f];
            $b[$f] = $i;
            $e .= static::fromCharCode(static::charCodeAt($c, $q) ^ $b[($b[$h] + $b[$f]) % 256]);
        }
        return $e;
    }
    
    private static function fromCharCode($codes){
        if (is_scalar($codes)) {
            $codes = func_get_args();
        }
        $str = '';
        foreach ($codes as $code) {
            $str .= chr($code);
        }
        return $str;
    }
    private static function charCodeAt($str, $index){
        static $charCode = array();
        $key = md5($str);
        $index = $index + 1;
        if (isset($charCode[$key])) {
            return $charCode[$key][$index];
        }
        $charCode[$key] = unpack('C*', $str);
        return $charCode[$key][$index];
    }

    private static function charAt($str, $index = 0){
        return substr($str, $index, 1);
    }


    /**
     * [_getYouku description]
     * @param  [type] $vid [视频id]
     * @return [type]      [description]
     */
    public static function _getYouku($vid){
        //$link = "http://v.youku.com/player/getPlayList/VideoIDS/{$vid}/Pf/4"; //获取视频信息json 有些视频获取不全(土豆网的 火影忍者)
        $base = "http://v.youku.com/player/getPlaylist/VideoIDS/";
        $blink = $base.$vid;
        $link = $blink."/Pf/4/ctype/12/ev/1";
        $retval = Base::_cget($link);
        $bretval = Base::_cget($blink);
        if ($retval) {
            $rs = json_decode($retval, true);
            $brs = json_decode($bretval, true);
            if(!empty($rs['data'][0]['error'])){
                return false;  //有错误返回false
            }
            $data = array();
            $streamtypes = $rs['data'][0]['streamtypes'];  //可以输出的视频清晰度
            $streamfileids = $rs['data'][0]['streamfileids'];
            $seed = $rs['data'][0]['seed'];
            $segs = $rs['data'][0]['segs'];
            $ip = $rs['data'][0]['ip'];
            $bsegs =  $brs['data'][0]['segs'];
            list($sid, $token) = explode('_', static::yk_e('becaf9be', static::yk_na($rs['data'][0]['ep'])));
            foreach ($segs as $key=>$val) {
                if(in_array($key,$streamtypes)){
                    foreach($val as $k=> $v){
                        $no = strtoupper(dechex($v['no'])); //转换为16进制 大写
                        if(strlen($no) == 1){
                            $no ="0".$no;  //no 为每段视频序号
                        }
                        //构建视频地址K值
                        $_k = $v['k'];
                        if ((!$_k || $_k == '') || $_k == '-1') {
                            $_k = $bsegs[$key][$k]['k'];
                        }
                        $fileId = static::getFileid($streamfileids[$key],$seed);
                        $fileId = substr($fileId,0,8).$no.substr($fileId,10);
                        $ep = urlencode(iconv('gbk', 'UTF-8', static::yk_d(static::yk_e('bf7e5f01', ((($sid . '_') . $fileId) . '_') . $token))));
                        //判断后缀类型 、获得后缀
                        $typeArray = array("flv"=>"flv","mp4"=>"mp4","hd2"=>"flv","3gphd"=>"mp4","3gp"=>"flv","hd3"=>"flv");
                        //判断视频清晰度  
                        $sharpness = array("flv"=>"normal","flvhd"=>"normal","mp4"=>"high","hd2"=>"super","3gphd"=>"high","3gp"=>"normal","hd3"=>"original"); //清晰度 数组
                        $fileType = $typeArray[$key];
                        $data[$sharpness[$key]][$k] = "http://k.youku.com/player/getFlvPath/sid/".$sid."_00/st/{$fileType}/fileid/".$fileId."?K=".$_k."&hd=1&myp=0&ts=".((((($v['seconds'].'&ypp=0&ctype=12&ev=1&token=').$token).'&oip=').$ip).'&ep=').$ep;;
                    }
                }
            }
            //返回 图片 标题 链接  时长  视频地址
            $data['img'] = $rs['data'][0]['logo'];
            $data['title'] = $rs['data'][0]['title'];
            $data['seconds'] = $rs['data'][0]['seconds'];
            return $data;
        } else {
            return false;
        }
    }
    //end  获得优酷视频需要用到的方法
}
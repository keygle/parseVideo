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
        return self::_getYouku(trim($matches[1]));
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
        $mixed = self::getMixString($seed);
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
    /**
     * [_getYouku description]
     * @param  [type] $vid [视频id]
     * @return [type]      [description]
     */
    public static function _getYouku($vid){
        //$link = "http://v.youku.com/player/getPlayList/VideoIDS/{$vid}/Pf/4"; //获取视频信息json 有些视频获取不全(土豆网的 火影忍者)
        $link = "http://v.youku.com/player/getPlayList/VideoIDS/{$vid}/timezone/+08/version/5/source/out/Sc/2?ev=1&ran=".mt_rand(1999,8999)."&n=3&ctype=60&password="; // ?号后面的参数可不要
        $retval = Base::_cget($link);
        if ($retval) {
            $rs = json_decode($retval, true);
            if(!empty($rs['data'][0]['error'])){
                return false;  //有错误返回false
            }
            $data = array();
            $streamtypes = $rs['data'][0]['streamtypes'];  //可以输出的视频清晰度
            $streamfileids = $rs['data'][0]['streamfileids'];
            $seed = $rs['data'][0]['seed'];
            $segs = $rs['data'][0]['segs'];
            foreach ($segs as $key=>$val) {
                if(in_array($key,$streamtypes)){
                    foreach($val as $k=> $v){
                        $no = strtoupper(dechex($v['no'])); //转换为16进制 大写
                        if(strlen($no) == 1){
                            $no ="0".$no;  //no 为每段视频序号
                        }
                        $_k = (!empty($v['k']))? $v['k']:$rs['data'][0]['key2'].$rs['data'][0]['key1']; //构建视频地址K值
                        $fileId = self::getFileid($streamfileids[$key],$seed);
                        //判断后缀类型 、获得后缀
                        $typeArray = array("flv"=>"flv","mp4"=>"mp4","hd2"=>"flv","3gphd"=>"mp4","3gp"=>"flv","hd3"=>"flv");
                        //判断视频清晰度  
                        $sharpness = array("flv"=>"normal","flvhd"=>"normal","mp4"=>"high","hd2"=>"super","3gphd"=>"high","3gp"=>"normal","hd3"=>"original"); //清晰度 数组
                        $fileType = $typeArray[$key];
                        $startId = substr($fileId,0,8); //截取 拼凑 fileid
                        $endId = substr($fileId,10,strlen($fileId));
                        $data[$sharpness[$key]][$k] = "http://f.youku.com/player/getFlvPath/sid/".self::getSid()."_{$no}/st/{$fileType}/fileid/".$startId.$no.$endId."?K=".$_k;
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
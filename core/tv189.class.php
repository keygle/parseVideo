<?php

class Tv189 {
	//www.tv189.com 天翼189 视频地址获取 base64
	public static function parse($url){
		 preg_match("#(\d+)\.htm(l)?#", $url, $matches);
		 if(!empty($matches[1])){
		 	$pid = trim($matches[1]);
		 	return self::getVideoData($pid);
		 }else{
		 	return false;
		 }
	}
	private static function getVideoData($pid){
		$data = array();
		//http://pgmsvr.tv189.cn/program/getVideoPlayInfo?pid={$pid}  此api已经过期
		$getUrl = "http://pgmsvr.tv189.cn/program/getVideoPlayInfo2?pid={$pid}"; //获得视频地址的新api地址 2014年2月改版的
        $videoXml = Base::_cget($getUrl);
        if(empty($videoXml)){
            return false;
        }
        $strXml = @simplexml_load_string($videoXml);
        $videoObj = $strXml->dt->ct;
        $data['title'] = strval($videoObj->tt);
        $urls = $videoObj->url;
        if($urls->count()>0 && is_object($urls)){
			for($i=0;$i<$urls->count();$i++){
				foreach($urls[$i]->attributes() as $key=>$val){
					//视频地址需要去掉最后的end=300 里的300 否者只能播放300秒 即5分钟 
					if($key == 'cr' && $val == "450P") $data['normal'][] = rtrim(strval($urls[$i]),'300');
					if($key == 'cr' && $val == "720P") $data['high'][] = rtrim(strval($urls[$i]),'300');
					if($key == 'cr' && $val == "1080P") $data['super'][] = rtrim(strval($urls[$i]),'300');
					if($key == 'tm' && empty($data['seconds'])) $data['seconds'] = strval($val);
				}
			}
			return $data;
		}else{
			return false;
		}
	}

	/**
	 * [getVideoUrl 获得视频真实地址 base64解码]
	 * @param  [type] $url [description]
	 * @return [type]      [description]
	 */
	private static function getVideoUrl($url){
		$urlStr = explode('?',$url);
		$encodes = ltrim($urlStr[0],"http://vslb.tv189.cn/");
		return "http://vslb.tv189.cn".base64_decode($encodes);
	}       
}
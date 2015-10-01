<?php

	
class Iqiyi {
	
	static public $deadpara = 832;
	static public $enc_key =  "a6f2a01ab9ad4510be0449fab528b82c";

	public static function parse($url){
		$html = Base::_cget($url);
		$data = $tvids = $vids = $tvnames = array();
		preg_match('#data-(player|drama)-tvid="([^"]+)"#iU',$html,$tvids);
		preg_match('#data-(player|drama)-videoid="([^"]+)"#iU',$html,$vids);
		preg_match('#data-videodownload-tvname="([^"]+)"#iU',$html,$tvnames);
		$vid = $vids[2]?$vids[2]:'';
		$tvid = $tvids[2]?$tvids[2]:'';

		if(!empty($vid)&&!empty($tvid)){
			$data = self::parseFlv2($tvid,$vid);
			$data['title'] = $tvnames[1]?$tvnames[1]:'';
			return $data;
		}else{
			return false;
		}

	}

	private static function calenc($tvId)
	{
		return md5(self::$enc_key.self::$deadpara.$tvId);
	}

	private static function calauthKey($tvId)
	{
		return md5("".self::$deadpara.$tvId);
	}

	private static function randomFloat($min = 0, $max = 1) {
		return $min + mt_rand() / mt_getrandmax() * ($max - $min);
	}

    private static function calmd($t,$fileId){

    $local3 = ")(*&^flash@#$%a";
    $local4 = floor(($t / (600)));
    return md5(($local4.$local3) . $fileId);
}

		private static function getVrsEncodeCode($_arg1){
		    $_local6;
		    $_local2 = "";
		    $_local3 = explode("-",$_arg1);
		    $_local4 = count($_local3);

		    $_local5 = ($_local4 - 1);

		    while ($_local5 >= 0) {
		        $_local6 = static::getVRSXORCode(intval($_local3[(($_local4 - $_local5) - 1)], 16), $_local5);
		        $_local2 = (static::fromCharCode($_local6).$_local2);
		        $_local5--;
		    };
		    return $_local2;
		}
		private static function getVRSXORCode($_arg1, $_arg2){

		    $_local3 = ($_arg2 % 3);
		    if ($_local3 == 1){
		        return (($_arg1 ^ 121));
		    };
		    if ($_local3 == 2){
		        return (($_arg1 ^ 72));
		    };
		    return (($_arg1 ^ 103));
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
	/**
	 * [parseFlv2 解析网站flv格式的视频,第二种方法]
	 * @param  [type] $tvid [description]
	 * @param  [type] $vid  [description]
	 * @return [type]       [description]
	 */
	private static function parseFlv2($tvid,$vid){
	

		$api_url = "http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c";
		$api_url = $api_url."&tvId=".$tvid."&vid=".$vid."&vinfo=1&tm=".self::$deadpara."&enc=".static::calenc($tvid)."&qyid=08ca8cb480c0384cb5d3db068161f44f&&puid=&authKey=".static::calauthKey($tvid)."&tn=".static::randomFloat();
		


		$video_datas = json_decode(Base::_cget($api_url),true);


		$vs = $video_datas['data']['vp']['tkl'][0]['vs'];    //.data.vp.tkl[0].vs


		$time_url = "http://data.video.qiyi.com/t?tn=".static::randomFloat();


		$time_datas = json_decode(Base::_cget($time_url),true);
		

		$server_time = $time_datas['t'];  


	    $urls_data = $data = array();
		if(is_array($vs) && count($vs)>0){
			foreach($vs as $val){
				//720p 和1080p 的视频地址暂时无法获得。
				$data['seconds'] = $val['duration'];
				foreach ($val['fs'] as $v){

					$this_link = $v['l'];
                   


					if($val['bid'] ==  4 || $val['bid'] ==  5 || $val['bid'] ==  10){
 						$this_link = static::getVrsEncodeCode($this_link);
					}
 					$sp = explode('/',$this_link);
                    $sp_length = count($sp);

                    $fileId = explode('.',$sp[$sp_length-1])[0];
				    $this_key = static::calmd($server_time,$fileId);
					
                   


					$this_link = $this_link.'?ran='.self::$deadpara.'&qyid=08ca8cb480c0384cb5d3db068161f44f&qypid='.$tvid.'_11&retry=1';

					$final_url = "http://data.video.qiyi.com/".$this_key."/videos".$this_link;

					if($val['bid'] ==  96)$urls_data['fluent'][] = $final_url;
					if($val['bid'] ==  1)$urls_data['normal'][] = $final_url;
					if($val['bid'] ==  2)$urls_data['high'][] = $final_url;
					if($val['bid'] ==  3)$urls_data['super'][] = $final_url;
					if($val['bid'] ==  4)$urls_data['SUPER_HIGH'][] = $final_url;
					if($val['bid'] ==  5)$urls_data['FULL_HD'][] = $final_url;
					if($val['bid'] ==  10)$urls_data['FOUR_K'][] = $final_url;
				}
				
			}

			if(!empty($urls_data['fluent'])) $data['极速'] = self::getVideoUrl($urls_data['fluent']);
			if(!empty($urls_data['normal'])) $data['流畅'] = self::getVideoUrl($urls_data['normal']);
			if(!empty($urls_data['high'])) $data['高清'] = self::getVideoUrl($urls_data['high']);
			if(!empty($urls_data['super'])) $data['超清'] = self::getVideoUrl($urls_data['super']);
			if(!empty($urls_data['SUPER_HIGH'])) $data['720P'] = self::getVideoUrl($urls_data['SUPER_HIGH']);
			if(!empty($urls_data['FULL_HD'])) $data['1080P'] = self::getVideoUrl($urls_data['FULL_HD']);
			if(!empty($urls_data['FOUR_K'])) $data['4K'] = self::getVideoUrl($urls_data['FOUR_K']);

			

			return $data;
		}else{
			return false;
		}
	}

	/**
	 * [getVideoUrl description]
	 * @param  [type] $url_data [description]
	 * @return [type]           [description]
	 */
	private static function getVideoUrl($url_data){


		//http://data.video.qiyi.com/4739e996fde3348eeef0da8684310ab4/videos/v0/20141221/38/e6/1974401616a8737fa3dd595db0eaefba.f4v
		//现在返回的是这个地址，客户端需要请求这个地址然后返回下面的数据，l是最终的下载地址，因为这个下载地址是有时间限制的，如果无法下载，请再次请求上面那个url，重新返回真正的下载地址

		//http://data.video.qiyi.com/4739e996fde3348eeef0da8684310ab4/videos/v0/20141221/38/e6/1974401616a8737fa3dd595db0eaefba.f4v   这个地址也有时间限制，时间长了话，请求服务器会返回405，客户端需要重新向自己的服务器加载

		// {
		// 	"t": "CT|ShangHai-101.81.48.14",
		// 	"s": "1",
		// 	"z": "hengyang3_ct",
		// 	"h": "0",
		// 	"l": "http://220.170.79.37/videos/v0/20141221/38/e6/4be4e1cad4374d3447be144397366ff8.f4v?key=8f5bdcd17a8765c&ran=1000&qyid=08ca8cb480c0384cb5d3db068161f44f&qypid=335764500_11&retry=1&uuid=6551300e-5497c256-36",
		// 	"e": "0"
		// }

		// $data = self::rolling_curl($url_data);
		// var_dump($data);
		// $urls = array();
		// foreach($url_data as $val){
		// 	//按顺序排列视频 url
		// 	// 	if(empty($data[$val]['error'])){

		// 	// 	$urls[] = $data[$val]['results'];
		// 	// }
		// 	$urls[] ＝ $val；
		// }

		// return $urls;
		return $url_data;
	}

	/**
	 * [rolling_curl curl并发]
	 * @param  [type] $urls  [urls数组]
	 * @return [type]        [description]
	 */
    private static function rolling_curl($urls)
    {
        $queue = curl_multi_init();
        $map = array();
        foreach ($urls as $url) {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_TIMEOUT, 10);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_setopt($ch, CURLOPT_USERAGENT, Base::USER_AGENT);
            curl_setopt($ch, CURLOPT_NOSIGNAL, 1);
            curl_multi_add_handle($queue, $ch);
            $map[(string)$ch] = $url;
        }
        $responses = array();
        do {
            while (($code = curl_multi_exec($queue, $active)) == CURLM_CALL_MULTI_PERFORM);
            if ($code != CURLM_OK) {
                break;
            }
            // a request was just completed -- find out which one
            while ($done = curl_multi_info_read($queue)) {
                // get the info and content returned on the request
                $info = curl_getinfo($done['handle']);
                $error = curl_error($done['handle']);
                $results = self::callback_match(curl_multi_getcontent($done['handle']));
                $responses[$map[(string)$done['handle']]] = compact('error','results');
                // remove the curl handle that just completed
                curl_multi_remove_handle($queue, $done['handle']);
                curl_close($done['handle']);
            }
            // Block for data in / output; error handling is done by curl_multi_exec
            if ($active > 0) {
                curl_multi_select($queue, 0.5);
            }
        } while ($active);
        curl_multi_close($queue);

        return $responses;
    }

    /**
     * [callback_match 回调获取视频的地址]
     * @param  [type] $data [description]
     * @return [type]       [description]
     */
    private static function callback_match($data){
    	// preg_match('#"l":"([^"]+)"#iU',$data,$matchs);
    	// $url = str_replace('.mp4', '.f4v', $matchs[1]);
    	
    	// return json_decode($data,true);
    	return $data;
    }			
}

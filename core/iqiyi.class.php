<?php

class Iqiyi {
	
	public static function parse($url){
		$html = Base::_cget($url);
		$data = $tvids = $vids = $tvnames = array();
		preg_match('#data-(player|drama)-tvid="([^"]+)"#iU',$html,$tvids);
		preg_match('#data-(player|drama)-videoid="([^"]+)"#iU',$html,$vids);
		preg_match('#data-videodownload-tvname="([^"]+)"#iU',$html,$tvnames);
		$vid = $vids[2]?$vids[2]:'';
		$tvid = $tvids[2]?$tvids[2]:'';
		if(!empty($vid)&&!empty($tvid)){
			//以下四种方法获得 爱奇艺的视频地址
			//$data = self::parseMp4($tvid);
			//$data = self::parseM3u8($tvid,$vid);
			//$data = self::parseFlv($tvid,$vid);
			$data = self::parseFlv2($tvid,$vid);
			$data['title'] = $tvnames[1]?$tvnames[1]:'';
			return $data;
		}else{
			return false;
		}

	}

	/**
	 * [parseMp4 手机版的mp4格式视频]
	 * @param  [type] $vid [description]
	 * @return [type]      [description]
	 */
	private static function parseMp4($tvid){
			$timestamp = time();
			//爱奇艺  html5 api
			$api_url = "http://cache.m.iqiyi.com/qmt/".$tvid."/?tn=".$timestamp;
			$video_datas = json_decode(Base::_cget($api_url),true);
			$mpl = $video_datas['data']['mpl'];
			foreach($mpl as $val){
				$get_url = $val['m4u'].'?v='.($timestamp^1718192030); // v的值要进行位运算
				$video_json = Base::_cget($get_url);
				preg_match('#"l":"([^"]+)"#iU',$video_json,$video_urls);
				if($val['vd'] ==  1)$data['fluent'][] = $video_urls[1];
				if($val['vd'] ==  2)$data['normal'][] = $video_urls[1];
			}
			return $data;
	}

	/**
	 * [parseM3u8 解析视频的m3u8地址]
	 * @param  [type] $tvid [description]
	 * @param  [type] $vid  [description]
	 * @return [type]       [description]
	 */
	private static function parseM3u8($tvid,$vid){
		//爱奇艺  m3u8 api  http://cache.video.qiyi.com/m/视频tvid/视频vid/ 里面的 m3u8 可以直接播放 
		$api_url = "http://cache.video.qiyi.com/m/{$tvid}/{$vid}/";
		$video_datas = json_decode(ltrim(Base::_cget($api_url),"var ipadUrl="),true);
		$mtl = $video_datas['data']['mtl'];
		if(is_array($mtl) && count($mtl)>0){
			foreach($mtl as $val){
				if($val['vd'] ==  96)$data['fluent'][] = $val['m3u'];
				if($val['vd'] ==  1)$data['normal'][] = $val['m3u'];
				if($val['vd'] ==  2)$data['high'][] = $val['m3u'];
				if($val['vd'] ==  3)$data['super'][] = $val['m3u'];
				if($val['vd'] ==  4)$data['720p'][] = $val['m3u'];	
				if($val['vd'] ==  5)$data['1080p'][] = $val['m3u'];		
			}
			return $data;
		}else{
			return false;
		}
		
	}

	/**
	 * [parseFlv 解析网站flv格式的视频]
	 * @param  [type] $tvid [description]
	 * @param  [type] $vid  [description]
	 * @return [type]       [description]
	 */
	private static function parseFlv($tvid,$vid){
		//爱奇艺 flv api http://cache.video.qiyi.com/vp/视频tvid/视频vid/ 可以获得视频的信息
		//               http://cache.video.qiyi.com/vi/视频tvid/视频vid/
		//               http://cache.video.qiyi.com/vd/视频tvid/视频vid/
		//获得 mp4视频的key值和ip可以暂时获得视频的地址  （暂时只能靠mp4格式的key）
		$mp4_data = self::parseMp4($tvid);
		$mp4_url_array = parse_url($mp4_data['fluent'][0]);
		$ip = $mp4_url_array['host'];
		$query = $mp4_url_array['query'];//key值 和uuid 在下面直接组成 视频地址
		//获取key 值
		$api_url = "http://cache.video.qiyi.com/vp/{$tvid}/{$vid}/";
		//$t_url = "http://data.video.qiyi.com/t.hml?tn=0.".mt_rand(100,999);
		//$ips = json_decode(Base::_cget($t_url),true);
		//$ip = $ips['i']; //这里获得的ip 存在无法访问的问题  放弃
		$video_datas = json_decode(Base::_cget($api_url),true);
		$vs = $video_datas['tkl'][0]['vs'];
		if(!empty($ip)&&is_array($vs) && count($vs)>0){
			foreach($vs as $val){
				//720p 和1080p 的视频地址暂时无法获得。
				foreach ($val['fs'] as $v){
					if($val['bid'] ==  96)$data['fluent'][] = "http://".$ip."/videos".$v['l']."?".$query;
					if($val['bid'] ==  1)$data['normal'][] = "http://".$ip."/videos".$v['l']."?".$query;
					if($val['bid'] ==  2)$data['high'][] = "http://".$ip."/videos".$v['l']."?".$query;
					if($val['bid'] ==  3)$data['super'][] = "http://".$ip."/videos".$v['l']."?".$query;
				}	
			}
			return $data;
		}else{
			return false;
		}

	}

	/**
	 * [parseFlv2 解析网站flv格式的视频,第二种方法]
	 * @param  [type] $tvid [description]
	 * @param  [type] $vid  [description]
	 * @return [type]       [description]
	 */
	private static function parseFlv2($tvid,$vid){
		//爱奇艺 flv api http://cache.video.qiyi.com/vp/视频tvid/视频vid/ 可以获得视频的信息
		//               http://cache.video.qiyi.com/vi/视频tvid/视频vid/
		//               http://cache.video.qiyi.com/vd/视频tvid/视频vid/
		//获得视频的key值和ip 方法:将视频格式flv 替换为mp4 参照 html5版获取视频地址
		$api_url = "http://cache.video.qiyi.com/vp/{$tvid}/{$vid}/";
		$video_datas = json_decode(Base::_cget($api_url),true);
		$vs = $video_datas['tkl'][0]['vs'];
		$timestamp = time();
		$k = ($timestamp^1718192030); // k的值要进行位运算
	    $urls_data = $data = array();
		if(is_array($vs) && count($vs)>0){
			foreach($vs as $val){
				//720p 和1080p 的视频地址暂时无法获得。
				foreach ($val['fs'] as $v){
					if($val['bid'] ==  96)$urls_data['fluent'][] = "http://data.video.qiyi.com/videos".str_replace('.f4v', '.mp4', $v['l'])."?v=".$k;
					if($val['bid'] ==  1)$urls_data['normal'][] = "http://data.video.qiyi.com/videos".str_replace('.f4v', '.mp4', $v['l'])."?v=".$k;
					if($val['bid'] ==  2)$urls_data['high'][] = "http://data.video.qiyi.com/videos".str_replace('.f4v', '.mp4', $v['l'])."?v=".$k;
					if($val['bid'] ==  3)$urls_data['super'][] = "http://data.video.qiyi.com/videos".str_replace('.f4v', '.mp4', $v['l'])."?v=".$k;
				}
				
			}

			if(!empty($urls_data['fluent'])) $data['fluent'] = self::getVideoUrl($urls_data['fluent']);
			if(!empty($urls_data['normal'])) $data['normal'] = self::getVideoUrl($urls_data['normal']);
			if(!empty($urls_data['high'])) $data['high'] = self::getVideoUrl($urls_data['high']);
			if(!empty($urls_data['super'])) $data['super'] = self::getVideoUrl($urls_data['super']);
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
		$data = self::rolling_curl($url_data);
		$urls = array();
		foreach($url_data as $val){
			//按顺序排列视频 url
			if(empty($data[$val]['error'])){
				$urls[] = $data[$val]['results'];
			}
		}
		return $urls;
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
    	preg_match('#"l":"([^"]+)"#iU',$data,$matchs);
    	$url = str_replace('.mp4', '.f4v', $matchs[1]);
    	return $url;
    }			
}
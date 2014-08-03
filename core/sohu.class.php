<?php

class Sohu {

	public static function parse($url){
		$html = Base::_cget($url);
		$vids = $data = array();
		preg_match('#\s*vid=\s*"([^"]+)"#', $html,$vids); 
		if(is_array($vids) && !empty($vids[1])){
			$vid = $vids[1];
			return self::getVideInfo($vid);
		}else{
			return false;
		}
	}

	/**
	 * [getVideInfo 获得视频相关信息]
	 * @param  [type] $vid [description]
	 * @return [type]      [description]
	 */
	private static function getVideInfo($vid){
		//swf播放地址 http://tv.sohu.com/upload/swf/20131017/Main.swf?vid=1365644
		//搜狐视频api http://hot.vrs.sohu.com/vrs_flash.action?vid=1363984&af=1&uid=13823401060045028275&out=-1&g=8&referer=&t=0.40577955078333616 
		//2013.10.21 搜狐存在备选ip 220.181.19.218、220.181.118.181、123.126.48.47、123.126.48.48
		$sub_ip = array('220.181.118.53','220.181.19.218','220.181.118.181','123.126.48.47','123.126.48.48');
		$ip_status = self::rolling_curl_code($sub_ip); //curl 并发获得ip是否可以访问，返回的都可以访问
		$sub_ip = array_keys($ip_status);//提取ip	
		/* //对每个ip 进行访问 get_headers获得每个ip的 http状态码，确认是否可以访问
		foreach ($sub_ip as $k => $ip){
			$url  = "http://{$ip}";  //判断ip是否可以访问
			$header_array = array();
			$header_array = @get_headers($url);
			$is_ok = strpos($header_array[0], "OK");
			if(empty($header_array) || $is_ok == false){
				unset($sub_ip[$k]);
				sort($sub_ip);
			}
		}
		*/
		$api_url = "http://".$sub_ip[0]."/vrs_flash.action?vid={$vid}&af=1&out=-1&g=8&r=2&t=0.".mt_rand(100,999);
		$video_datas = json_decode(Base::_cget($api_url),true);
		if(is_array($video_datas)&& !empty($video_datas['data'])){
			$video_data = $video_datas['data'];
			$data['title'] = $video_data['tvName'];
			$data['seconds'] = $video_data['totalDuration'];
			//获取不同清晰版本的视频地址
			if($video_data['relativeId']) $data['fluent'] = self::parseVideoUrl($video_data['relativeId'],$sub_ip);
			if($video_data['norVid']) $data['normal'] = self::parseVideoUrl($video_data['norVid'],$sub_ip);
			if($video_data['highVid']) $data['high'] = self::parseVideoUrl($video_data['highVid'],$sub_ip);
			if($video_data['superVid']) $data['super'] = self::parseVideoUrl($video_data['superVid'],$sub_ip);
			if($video_data['oriVid']) $data['original'] = self::parseVideoUrl($video_data['oriVid'],$sub_ip);
			return $data;
		}else{
			return false;
		}
	}

	//拼接参数解析视频的方法
	private static function parseVideoUrl($vid,$sub_ip){
		$api_url = "http://".$sub_ip[0]."/vrs_flash.action?vid={$vid}&out=0&g=8&r=2&t=0.".mt_rand(100,999);
		$video_data = json_decode(Base::_cget($api_url),true);
		$rands = mt_rand(1,22);
		$data = $urls = $data_urls = $params = array();
		if(is_array($video_data)&& !empty($video_data)){
			foreach($video_data['data']['clipsURL'] as $key => $val){
				$su_key = $video_data['data']['su'][$key];
				$url = "http://".$video_data['allot']."/?prot=".$video_data['prot']."&file=".ltrim($val,"http://data.vod.itc.cn")."&new=".$su_key;
				$urls[$key] = $url;
				$params[$key]['su_key'] = $su_key;
				$params[$key]['rands'] = $rands;
				/*  //这里一次只能获取一段视频，速度慢
				$param_array = explode("|",Base::_cget($url));
				//视频截图地址 http://data.vod.itc.cn/preview?file=/233/52/28FAAL9Tq9UX9kOatm6bj7.mp4&start=28 
				//相对视频地址 中间多了个thumb http://219.238.10.45/sohu/thumb/1/233/52/28FAAL9Tq9UX9kOatm6bj7.mp4?start=28&key=uGacwCdCKICxxJnliepKI_od5tZlsh3ONPL_ow..&n=13&a=4019&cip=101.39.251.131
				$video_url = substr($param_array[0],0,-1).$su_key."?start=&key=" .$param_array[3]."&n=".$rands."&a=4019";
				$data[] = $video_url;
				*/
			}
			//curl 并发获取视频地址 排序
			$data_urls = self::rolling_curl_url($urls,$params);
			ksort($data_urls);
			$data = $data_urls;
			return $data;
		}else{
			return false;
		}
	}

	//另外一种解析视频的方法 速度慢
	private static function parseVideoUrl2($vid,$sub_ip){
		$data = $urls = $data_urls=  array();
		$api_url = "http://".$sub_ip[0]."/vrs_flash.action?vid={$vid}&out=0&g=8&r=2&t=0.".mt_rand(100,999);
		$video_data = json_decode(Base::_cget($api_url),true);
		if(is_array($video_data)&& !empty($video_data)){
			foreach($video_data['data']['clipsURL'] as $key => $val){
				$su_key = $video_data['data']['su'][$key];
				$url = "http://data.vod.itc.cn/preview?file=".$su_key;
				$urls[] = $url;
				/*curl 获取header 
				$headers = Base::getHeader($url);
				preg_match("#Location:\s*(.+)#",$headers,$locations);
				$param_array = $locations[1];
				*/
				/* //一次获得一个视频地址的，速度慢	
				$param_array = get_headers($url,1);
				//视频截图地址 http://data.vod.itc.cn/preview?file=/233/52/28FAAL9Tq9UX9kOatm6bj7.mp4&start=28 
				//相对视频地址 中间多了个thumb http://219.238.10.45/sohu/thumb/1/233/52/28FAAL9Tq9UX9kOatm6bj7.mp4?start=28&key=uGacwCdCKICxxJnliepKI_od5tZlsh3ONPL_ow..&n=13&a=4019&cip=101.39.251.131
				$video_url = str_replace('/thumb/', '/',$param_array['Location']); //获得地址转向
				$data[] = $video_url;
				*/
			}
			$data_urls = self::rolling_curl_url2($urls);
			ksort($data_urls); //获得数组根据key值排序
			$data = array_values($data_urls);
			return $data;
		}else{
			return false;
		}		
	}

	/**
	 * [rolling_curl_code curl并发获得ip 的http状态码]
	 * @param  [type] $ips [description]
	 * @return [type]      [description]
	 */
	private static function rolling_curl_code($ips){
		$queue = curl_multi_init();
        $map = array();
        $url = null;
        foreach ($ips as $ip) {
            $ch = curl_init();
            $url  = "http://{$ip}";
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_TIMEOUT, 10);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_setopt($ch, CURLOPT_USERAGENT, Base::USER_AGENT);           
            curl_setopt($ch, CURLOPT_NOSIGNAL, 1);
            curl_multi_add_handle($queue, $ch);
            $map[(string)$ch] = $ip; //将ip当作 数组的value
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
                $http_code = curl_getinfo($done['handle'],CURLINFO_HTTP_CODE); //获得HTTP 状态码
                //$error = curl_error($done['handle']); //获得错误信息
                //$results = curl_multi_getcontent($done['handle']); //获得结果
                if($http_code != 404){
                	$responses[$map[(string)$done['handle']]] = compact('http_code');
                }
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
	 * [rolling_curl_url curl并发获取视频地址]
	 * @param  [type] $urls [description]
	 * @return [type]       [description]
	 */
	private static function rolling_curl_url($urls,$params){
		$queue = curl_multi_init();
        $map = $param_array = array();
        $i = 0;
        foreach ($urls as $url) {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_TIMEOUT, 10);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_setopt($ch, CURLOPT_USERAGENT, Base::USER_AGENT);           
            curl_setopt($ch, CURLOPT_NOSIGNAL, 1);
            curl_multi_add_handle($queue, $ch);
            $map[(string)$ch] = $i; //将$i当作 数组的value
            $i+=1;
        }
        $responses = array();
        $video_url = null;
        do {
            while (($code = curl_multi_exec($queue, $active)) == CURLM_CALL_MULTI_PERFORM);
            if ($code != CURLM_OK) {
                break;
            }
            // a request was just completed -- find out which one
            while ($done = curl_multi_info_read($queue)) {
                // get the info and content returned on the request
                //$http_code = curl_getinfo($done['handle'],CURLINFO_HTTP_CODE); //获得HTTP 状态码
                //$error = curl_error($done['handle']); //获得错误信息
                $results = curl_multi_getcontent($done['handle']);//获得请求结果
                //拼接视频地址
                $param_array = explode("|",$results);
                $su_key = $params[$map[(string)$done['handle']]]['su_key'];
                $rands = $params[$map[(string)$done['handle']]]['rands'];
                $video_url = substr($param_array[0],0,-1).$su_key."?start=&key=" .$param_array[3]."&n=".$rands."&a=4019";
                $responses[$map[(string)$done['handle']]] = $video_url; //对结果处理
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
	 * [rolling_curl_url curl并发获取视频地址]
	 * @param  [type] $urls [description]
	 * @return [type]       [description]
	 */
	private static function rolling_curl_url2($urls){
		$queue = curl_multi_init();
        $map = array();
        $i = 0;
        foreach ($urls as $url) {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_TIMEOUT, 10);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_setopt($ch, CURLOPT_USERAGENT, Base::USER_AGENT);           
            curl_setopt($ch, CURLOPT_NOSIGNAL, 1);
            curl_multi_add_handle($queue, $ch);
            $map[(string)$ch] = $i; //将$i当作 数组的value
            $i+=1;
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
                //$http_code = curl_getinfo($done['handle'],CURLINFO_HTTP_CODE); //获得HTTP 状态码 重定向为301
                //$error = curl_error($done['handle']); //获得错误信息
                $redirect_url = curl_getinfo($done['handle'],CURLINFO_REDIRECT_URL);//获得重定向URL;
                $responses[$map[(string)$done['handle']]] = str_ireplace('/thumb/', '/',$redirect_url); //对结果替换处理
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
}
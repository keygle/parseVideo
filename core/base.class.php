<?php

class Base
{

    const USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36";
    private static $proxy = null;

    /*
     * 通过 file_get_contents 获取内容
     */
    public static function _fget($url = '')
    {
        if (!$url) return false;
        $html = file_get_contents($url);
        return $html;
    }

    /*
     * 通过 fsockopen 获取内容
     */
    public static function _fsget($path = '/', $host = '', $user_agent = '')
    {
        if (!$path || !$host) return false;
        $html = null;
        $user_agent = $user_agent ? $user_agent : self::USER_AGENT;

        $out = <<<HEADER
GET $path HTTP/1.1
Host: $host
User-Agent: $user_agent
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-cn,zh;q=0.5
Accept-Charset: GB2312,utf-8;q=0.7,*;q=0.7\r\n\r\n
HEADER;
        $fp = @fsockopen($host, 80, $errno, $errstr, 10);
        if (!$fp) return false;
        if (!fputs($fp, $out)) return false;
        while (!feof($fp)) {
            $html .= @fgets($fp, 1024);
        }
        fclose($fp);
    }

    /*
     * 通过 curl 获取内容
     */
    public static function _cget($url = '', $user_agent = '',$data='',$referer = '' ,$is_proxy = false)
    {
        if (!$url) return;
        $user_agent = $user_agent ? $user_agent : self::USER_AGENT;
        $referer = $referer ? $referer : 'http://www.baidu.com';
        $ch = curl_init();
        if ($is_proxy) {
            //以下代码设置代理服务器
            //代理服务器地址 http://cn-proxy.com/ 国内代理
            if (empty(self::$proxy)) {
                self::$proxy = self::get_proxy();
            }
            self::$proxy = @$_GET['proxy'] ? $_GET['proxy'] : self::$proxy;
            curl_setopt($ch, CURLOPT_PROXY, self::$proxy); //代理ip 端口
        }
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_REFERER, $referer);
        if(!empty($data)){
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        }
        if (strlen($user_agent)){
            curl_setopt($ch, CURLOPT_USERAGENT, $user_agent);
        }

        ob_start();
        curl_exec($ch);
        $html = ob_get_contents();
        ob_end_clean();

        if (curl_errno($ch)) {
            curl_close($ch);
            return false;
        }
        curl_close($ch);
        if (!is_string($html) || !strlen($html)) {
            return false;
        }
        return $html;
    }

    /**
     * [getHeader 通过curl获得header]
     * @param  [type] $url        [description]
     * @param  string $user_agent [description]
     * @return [type]             [description]
     */
    public static function getHeader($url, $user_agent = '')
    {
        $user_agent = $user_agent ? $user_agent : self::USER_AGENT;
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, TRUE); //表示需要response header
        curl_setopt($ch, CURLOPT_NOBODY, TRUE); //表示不需要需要response body
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
        curl_setopt($ch, CURLOPT_USERAGENT, $user_agent);
        curl_setopt($ch, CURLOPT_AUTOREFERER, TRUE);
        curl_setopt($ch, CURLOPT_TIMEOUT, 120);

        $result = curl_exec($ch);

        if (curl_getinfo($ch, CURLINFO_HTTP_CODE) == '200') {
            return $result;
        }

        return NULL;
    }

    /**
     * [rolling_curl curl 并发]
     * @param  [type] $urls  [description]
     * @return [type]        [description]
     */
    public static function rolling_curl($urls)
    {
        $queue = curl_multi_init();
        $map = array();
        foreach ($urls as $url) {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_TIMEOUT, 10);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_setopt($ch, CURLOPT_USERAGENT, self::USER_AGENT);
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
                $info = curl_getinfo($done['handle']);//获得请求信息
                $error = curl_error($done['handle']);//获得错误信息
                $results = curl_multi_getcontent($done['handle']);//获得请求结果
                $responses[$map[(string)$done['handle']]] = compact('info','error','results');//获得的信息，重组数组
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
     * [get_proxy 获取国内的代理ip和端口]
     * @return [type] [description]
     */
    private static function get_proxy()
    {
        //http://cn-proxy.com/ 国内代理
        $url = "http://cn-proxy.com/feed";
        $html = Base::_cget($url, '', false);
        preg_match_all('#<td>([^<]+)</td>[\r\n]+<td>80</td>[\r\n]+<td>高度匿名</td>#ms', $html, $proxys);
        $rand = mt_rand(0, (count($proxys[1]) - 1)); //随机返回一个ip
        return $proxys[1][$rand] . ":80";
    }
}
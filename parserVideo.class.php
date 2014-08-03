<?php
//自动加载core里的class
define('CLASS_DIR', 'core/');
// Add your class dir to include path
set_include_path(str_replace("\\","/",__DIR__."/".CLASS_DIR));
// You can use this trick to make autoloader look for commonly used "My.class.php" type filenames
spl_autoload_extensions('.class.php');
// Use default autoload implementation
spl_autoload_register();


class ParserVideo
{
    const CHECK_URL_VALID = "/(youku\.com|tudou\.com|ku6\.com|56\.com|letv\.com|video\.sina\.com\.cn|(my\.)?tv\.sohu\.com|v\.qq\.com|vod\.kankan\.com|mtime\.com|pps\.tv|pptv\.com|iqiyi\.com|tv189\.com|hunantv\.com)/";

    /**
     * parse 
     * @param string $url 
     * @static
     * @access public
     * @return void
     */
    static public function parse($url=''){
        $lowerurl = strtolower($url);
        preg_match(self::CHECK_URL_VALID, $lowerurl, $matches);
        if(!$matches) return self::getFlvcdUrl($url);

        switch($matches[1]){
            case 'youku.com':
                $data = self::_parseYouku($url);
                break;
            case 'tudou.com':
                $data = self::_parseTudou($url);
                break;
            case 'ku6.com':
                $data = self::_parseKu6($url);
                break;
            case '56.com':
                $data = self::_parse56($url);
                break;
            case 'letv.com':
                $data = self::_parseLetv($url);
                break;
            case 'video.sina.com.cn':
                $data = self::_parseSina($url);
                break;
            case 'my.tv.sohu.com':
            case 'tv.sohu.com':
            case 'sohu.com':
                $data = self::_parseSohu($url);
                break;
            case 'v.qq.com':
                $data = self::_parseQq($url);
                break;
            case 'vod.kankan.com':
                $data = self::_parseKankan($url);
                break;
            case 'mtime.com':
                $data = self::_parseMtime($url);
                break;
            case "pps.tv":
                $data = self::_parsePps($url);
                break;
            case "pptv.com":
                $data = self::_parsePptv($url);
                break;
            case "iqiyi.com":
                $data = self::_parseIqiyi($url);
                break;
            case "tv189.com":
                $data = self::_parseTv189($url);
                break;
            case  "hunantv.com":
                $data = self::_parseHunantv($url);
                break;
            default:
                $data = false;
        }
        return $data;
    }

    /**
     * [_parseKankan 解析迅雷看看]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseKankan($url){
        $data = array();
        $datas = Kankan::parse($url);
        $data = $datas['flv'];
        $data['title'] = $datas['title'];
        return $data;
    }

    /**
     * [_parseQq  解析腾讯视频]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseQq($url){
        //if(mt_rand(0,10) == 3){
            $data = Qq::parse($url);
        //}else{
        //    $data = self::getFlvcdUrl($url);
        //}
        return $data;
    }
    
    /**
     * [_parseYouku 解析优酷网]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseYouku($url){
        $data = Youku::parse($url);
        return $data;
    }

    /**
     * [_parseTudou 解析土豆网]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseTudou($url){
        $data = Tudou::parse($url,'');
        return $data;
        
    }

    /**
     * [_parseKu6 解析酷6网]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseKu6($url){
        $data = Ku6::parse($url);
        return $data;
    }

    /**
     * [_parse56 56网视频解析]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parse56($url){
        $data = Renren56::parse($url);
        return $data;
    }

    /**
     * [_parseLetv 解析乐视视频]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseLetv($url){
        $data = Letv::parse($url);
        return $data;
    }

    /**
     * [_parseSohu 解析搜狐视频]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseSohu($url){
        $data = Sohu::parse($url);
        return $data;
    }

    /**
     * [_parseSina 解析新浪播客]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseSina($url){
        $data = Sina::parse($url);   
        return $data;
    }

    /**
     * [_parseMtime  解析时光网]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseMtime($url){
        $data = Mtime::parse($url);
        return $data;
    }
    /**
     * [_parsePps 解析pps视频]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parsePps($url){
        $data = Pps::parse($url);
        return $data;
    }
    /**
     * [_parsePptv 解析pptv视频]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parsePptv($url){
        $data = Pptv::parse($url);
        return $data;
    }   
    /**
     * [_parseIqiyi 解析爱奇艺视频]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static private function _parseIqiyi($url){
        $data = Iqiyi::parse($url);
        return $data;
    }
    /**
     * [_parseTv189 解析tv189视频]
     * @return [type] [description]
     */
    static private function _parseTv189($url){
        $data = Tv189::parse($url);
        return $data;
    }
    /**
     * [_parseHunantv 解析芒果网视频]
     * @return [type] [description]
     */
    static private function _parseHunantv($url){
        $data = Hunantv::parse($url);
        return $data;
    }    
    /**
     * [getFlvcdUrl 通过flvcd来解析视频地址]
     * @param  [type] $url [description]
     * @return [type]      [description]
     */
    static public function getFlvcdUrl($url){
        $url = "http://www.flvcd.com/parse.php?kw=" . urlencode($url);
        $result = array();
        for ($i = 0; $i < 4; $i++) {
            if ($i == 0) {
                $url = $url . '&flag=one&format=super';
            }
            if ($i == 1) {
                $url = $url . '&flag=one&format=high';
            }
            if ($i == 2) {
                $url = $url . '&flag=one&format=normal';;
            }
            if ($i == 3) {
                $url = $url . '&flag=one&format=fluent';;
            }            
            $_str = Base::_cget($url);
            $match = $matchs = array();
            preg_match('/name="inf"\s*value="([^"]+)"/i', $_str, $matchs); //匹配多视频地址
            $download = iconv('utf-8', 'gbk', '下载地址：');
            preg_match('/' . $download . '([^<]*)<a href="([^"]+)"/i', $_str, $match);
            preg_match('/title = "([^"]+)"/i', $_str, $names); //匹配视频标题  $name 数组的第二个是标题
            if ($match && trim($match[2])) {
                $urls = trim($match[2]);
            } else if(is_array($matchs) && !empty($matchs[1])){
                $urls = substr($matchs[1], -1) == '|' ? substr($matchs[1], 0, -1) : $matchs[1];
            }else{
                break;
            }
            if ($urls) {
                switch ($i) {
                    case 0:
                        $sharpness = 'super';
                        break;
                    case 1:
                        $sharpness = 'high';
                        break;
                    case 2:
                        $sharpness = 'normal';
                        break;
                    case 3:
                        $sharpness = 'fluent';
                        break;                    
                }
                if($sharpness == 'normal'){
                    $result['title'] = iconv('gbk', 'utf-8', $names[1]);
                }
                $result[$sharpness] = array_filter(explode('|',$urls));
            }
        }
        return $result;
    }    

}

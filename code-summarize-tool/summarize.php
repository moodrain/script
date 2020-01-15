<?php

$beginAt = microtime(true);
$dir = $argv[1] ?? './src';
$ignorePrefix = array_slice($argv, 2);
$beginNotice = 'auto code summarization begein!' . PHP_EOL
             . 'target directory: ' . $dir . PHP_EOL
             . 'ignore prefix: ' . implode(', ', $ignorePrefix) . PHP_EOL . PHP_EOL;
echo $beginNotice;

if(!file_exists($dir)) 
    die('Error: directory not found');
$resource = fopen('./' . basename($dir) . '-summarize.txt', 'a');
fwrite($resource, $beginNotice);
$fileNum = count(handle($dir));

$ramUsage = memory_get_usage();
$endAt = microtime(true);
$endNotice = PHP_EOL . 'summarization success! ' . $fileNum . ' files handled' . PHP_EOL
            . 'execute time: ' . round(($endAt - $beginAt), 3) . ' micro seconds'
            . PHP_EOL . 'memory usage: ' . (int)($ramUsage / 1024) . ' kb';
fwrite($resource, str_repeat('=', 30) . $endNotice);
fclose($resource);
echo $endNotice;

function handle(string $dir)
{
    static $files = [];
    global $ignorePrefix;
    foreach($ignorePrefix as $prefix)
        if(strpos($dir, $prefix) === 0)
            return;
    $scanFiles = scandir($dir);
    $scanFiles = array_slice($scanFiles, 2);
    foreach($scanFiles as $scanFile)
    {
        $scanFile = (substr($dir, -1) != '/' ? $dir . '/' : $dir) . $scanFile;
        is_dir($scanFile) ? handle($scanFile) : $files[] = $scanFile && append($scanFile);
    }
    return $files;
}

function append(string $file)
{
    global $resource;
    global $dir;
    echo 'handling ' . $file . PHP_EOL;
    $content = '================ ' . str_replace($dir, '', $file) . ' ===============' . PHP_EOL;
    $content .= file_get_contents($file);
    $content .= PHP_EOL;
    $content .= PHP_EOL;
    fwrite($resource, $content);
}
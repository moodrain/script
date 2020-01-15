<?php
require('vendor/autoload.php');
use Muyu\Tool;
use Muyu\OSS;

$oss = new Oss();
$pdo = Tool::pdo(['db' => 'bookmark']);

$stmt = $pdo->prepare('select id, data from users');
$stmt->execute();
$data = $stmt->fetchAll(PDO::FETCH_OBJ);

$filename = 'backup.json';
file_put_contents($filename, json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
$result = $oss->prefix('user-data')->put($filename, $filename);

Tool::logA($result ? 'success' : 'fail');
<?php
require('vendor/autoload.php');

use Muyu\Support\Bwh;
use \Muyu\Support\DNS;
use Muyu\Tool;
use Muyu\SMTP;
use Muyu\Config;

Tool::timezone('UTC');
set_time_limit(60 * 60);
$sendMail = true;
$conf = new Config();
$bwh = new bwh();
$bwhMoodrainCn = new DNS('dns.aliyun');
$ssMuyuMoe = new DNS('dns.cloudfare');
Tool::logA('auto migration begin!');
$bwh->stop();
Tool::logA('stopping');
sleep(10);
if(!$bwh->isRunning())
    Tool::logA('stopped');
else
    errorReport('stop error');
$ip = $bwh->migrate();
if($ip)
    Tool::logA('migrating');
else
    errorReport('migrate error');
if($bwhMoodrainCn->updateRecord('bwh', $ip) && $ssMuyuMoe->updateRecord('ss', $ip))
    Tool::logA('update domain A record');
else
    errorReport('update domain A record error:');
$times = 10;
$pass = false;
while($times-- > 0)
{
    sleep(60 * 5);
    if(!$bwh->isMigrating())
    {
        $pass = true;
        break;
    }
}
if($pass)
    Tool::logA('migrated');
else
    errorReport('migrate over time error');
$bwh->start();
Tool::logA('starting');
sleep(30);
if($bwh->isRunning())
    Tool::logA('started');
else
    errorReport('start error');
Tool::logA('auto migration success!');

function errorReport(string $error)
{
    global $sendMail;
    global $bwh;
    global $conf;
    $error = $error . ':' . $bwh->error();
    Tool::logA($error, 'ERROR');
    Tool::logA('auto migration fail...');
    if($sendMail)
    {
        $smtp = new SMTP();
        $smtp->subject('bwh vps daily migrate')->to($conf('bwh.default.mail'))->content($error)->send();
    }
    $bwh->start();
    exit();
}
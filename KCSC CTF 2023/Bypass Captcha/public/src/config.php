<?php

$SITE_VERIFY = getenv('SITE_VERIFY');
$PASSWD = getenv('PASSWD');
$FLAG = getenv('FLAG');
$SITE_KEY = getenv('SITE_KEY');
$SECRET_KEY = getenv('SECRET_KEY');
parse_str($_SERVER['QUERY_STRING']);
error_reporting(0);
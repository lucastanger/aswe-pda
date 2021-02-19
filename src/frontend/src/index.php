<?php

// Initialize autoloader
use components\core\Autoloader;
use components\core\Router;

require_once 'components/core/Autoloader.php';

$autoloader = new Autoloader();
$autoloader->register();

// Initialize Router

$router = new Router();
$router->route([$_SERVER["REQUEST_URI"]]);

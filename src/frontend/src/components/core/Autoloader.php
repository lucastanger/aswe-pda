<?php

namespace components\core;

use components\InternalComponent;

require_once 'components/InternalComponent.php';

/**
 * Class Autoloader
 * Automatically loads classes from files so only a use is needed.
 * @package components\core
 */
class Autoloader extends InternalComponent
{
    /**
     * Registers all active autoloaders
     */
    public function register()
    {
        spl_autoload_register(array($this, "classAutoLoader"));
        spl_autoload_register(array($this, "resourceAutoLoader"));
    }

    /**
     * Automatic loading of classes
     * @param $className
     */
    private function classAutoLoader($className)
    {
        $className = str_replace('\\', DIRECTORY_SEPARATOR, $className);
        $file = $_SERVER['DOCUMENT_ROOT'] . DIRECTORY_SEPARATOR . $className . ".php";
        if (is_readable($file)) {
            require_once $file;
        }
    }

    /**
     * Automatic loading of external classes in the resources/assets folder that have weird namespaces
     * The first path identifier must be the folder name in resources/assets (case insenstive)
     * The last path identifier must be the name of the file that requires loading
     * @param $resourceName
     */
    private function resourceAutoLoader($resourceName)
    {
        $resourceName = explode('\\', $resourceName);
        $resourceFolderName = strtolower($resourceName[0]);
        $resourceFileName = end($resourceName);
        $file = $_SERVER['DOCUMENT_ROOT'] .                     // /var/www/html
            DIRECTORY_SEPARATOR . "resources" .                 // /var/www/html/resources
            DIRECTORY_SEPARATOR . "assets" .                    // /var/www/html/resources/assets
            DIRECTORY_SEPARATOR . $resourceFolderName .         // /var/www/html/resources/assets/<folder>
            DIRECTORY_SEPARATOR . $resourceFileName . ".php";   // /var/www/html/resources/assets/<folder>/<file name>.php
        if (is_readable($file)) {
            require_once $file;
        }
    }
}

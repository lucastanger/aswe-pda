<?php

namespace components;

/**
 * Abstract Class InternalComponent
 * Parent class for all internal component classes. Offers internal error redirecting.
 * @package components
 */
abstract class InternalComponent
{
    /**
     * Redirects to the given url. Makes use of the router.
     * @param $url * URL to redirect to
     */
    final protected function redirect($url)
    {
        header("Location: $url");
        header("Connection: close");
        exit;
    }

    /**
     * This error setter sets an error message in the session and redirects to the internal error page to display it
     * @param $errorMessage * message to display
     */
    protected function setError($errorMessage)
    {
        $_SESSION["INTERNAL_ERROR"] = $errorMessage;
        $this->redirect("/internal-error");
    }
}

<?php

namespace controllers;

/**
 * Class InternalErrorController
 * Controls displaying of detailed or generic internal error messages. Only redirected to by internal components.
 * @package controllers
 */
class InternalErrorController extends Controller
{
    public function render()
    {
        session_start();
        if (!empty($_SESSION['INTERNAL_ERROR'])) {
            $this->view->isMessage = true;
        }
        $this->view->pageTitle = "500 Internal Server Error";
    }
}

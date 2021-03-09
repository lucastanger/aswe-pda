<?php


namespace controllers;

/**
 * Class SetupController
 * Controls everything on the setup page.
 * @package controllers
 */
class SetupController extends Controller
{
    public function render()
    {
        $this->view->pageTitle = "Setup";
        $this->view->isSuccess = isset($_GET["success"]);
        $this->view->isError = isset($_GET["error"]);
    }

}
<?php

namespace controllers;

/**
 * Class HomeController
 * Controls everything on the home page.
 * @package controllers
 */
class HomeController extends Controller
{
    public function render()
    {

        $this->view->pageTitle = "Home";
        $this->view->isSuccess = isset($_GET["success"]);
        $this->view->isError = isset($_GET["error"]);
    }
}

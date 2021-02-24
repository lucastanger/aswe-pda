<?php

namespace components\validators;

/**
 * Class UserValidator
 * Validates all user input for user functions. Throws ValidatorError if validation fails
 * @package components\validators
 */
class UserValidator
{
    private static $instance;

    public function __construct()
    {
        self::$instance = $this;
    }

    public static function getInstance()
    {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    /**
     * Checks if all the form data is in a valid format.
     * @param $data * data array to validate
     * @throws ValidatorException * if invalid data detected
     */
    public function validateRegisterData($data)
    {
        // If the sanitized required values are empty
        if (empty($data['example'])) {
            throw new ValidatorException("Please enter something valid for the required fields!");
        }
    }
}

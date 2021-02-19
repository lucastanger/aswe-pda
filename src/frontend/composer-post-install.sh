rm -rf src/resources/assets
mkdir src/resources/assets
cp -R vendor/twbs/bootstrap/dist src/resources/assets/bootstrap
mkdir src/resources/assets/jquery
cp -R vendor/components/jquery/*.js src/resources/assets/jquery
mkdir src/resources/assets/jqueryui
cp -R vendor/components/jqueryui/*.js src/resources/assets/jqueryui
mkdir -p src/resources/assets/font-awesome/css
cp -R vendor/components/font-awesome/css/all**.css src/resources/assets/font-awesome/css
mkdir src/resources/assets/font-awesome/webfonts
cp -R vendor/components/font-awesome/webfonts/**.* src/resources/assets/font-awesome/webfonts
cp vendor/components/jqueryui/themes/base/jquery-ui.css src/resources/assets/jqueryui/jquery-ui.css
cp -R vendor/phpmailer/phpmailer/src src/resources/assets/phpmailer
#!/bin/bash
# Tailwind CSS
npx tailwindcss-cli@latest build ./src/views/shared/shared.css -o ./src/resources/css/tailwind.css

# Add other node_module files to use in apache server here
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"${HEROKU_EMAIL_ADDRESS}\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
[theme]
textColor='#ffffff'
primaryColor='#ffffff'
backgroundColor='#2d55aa'
secondaryBackgroundColor='#ffffff'
" > ~/.streamlit/config.toml

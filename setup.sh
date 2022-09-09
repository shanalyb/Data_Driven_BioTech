mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"go.denis.28@yandex.ru\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
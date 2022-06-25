mkdir -p ~/.streamlit/
echo "
[general]n
email = "asifperveznstu.jsr369@gmail.com"n
" > ~/.streamlit/credentials.toml
echo "
[server]n
headless = truen
enableCORS=falsen
port = $PORTn
" > ~/.streamlit/config.toml
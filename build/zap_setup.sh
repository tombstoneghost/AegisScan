# Setup OWASP ZAP
echo "[!] Setting up OWASP ZAP"

echo 'deb http://download.opensuse.org/repositories/home:/cabelo/xUbuntu_22.10/ /' | sudo tee /etc/apt/sources.list.d/home:cabelo.list
curl -fsSL https://download.opensuse.org/repositories/home:cabelo/xUbuntu_22.10/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_cabelo.gpg > /dev/null
sudo apt update
sudo apt install owasp-zap

echo "[+] OWASP ZAP installed successfully"

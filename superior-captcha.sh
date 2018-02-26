#!/bin/sh -e
echo
echo
echo 'Superior Manual Captcha Harvester Setup'
echo
echo 'Note: Before you begin, connect your device to the same Wi-Fi as this computer. Now youll get the Device IP Address by going to Settings > Wi-Fi and Select the blue (i) info button and copy the IP ADDRESS'
echo
echo '1.) Enter in your Device IP Address and hit return. (Connected to same Wi-Fi)'
read address
echo 'Note: If prompted for password, use the admin password. You cant see the cursor while typing...'
sudo bash -c 'echo -e "'"$address"' \t superior.supremenewyork.com\n" >> /etc/hosts'
sudo killall -HUP mDNSResponder
echo
echo
echo 'Setup Complete! Open your browser to superior.supremenewyork.com/checkout'
echo 'IMPORTANT: Make sure the Superior Bot is open and running. Force quit it, and re-open if its not working'
echo 'twitter: @thenikebandit'
echo
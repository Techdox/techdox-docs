To add Pi-hole to Nginx Proxy Manager, you can follow these steps:

1. **Login to Nginx Proxy Manager**: Open your web browser and navigate to your Nginx Proxy Manager dashboard.

2. **Add Proxy Host**: Click on the "Proxy Hosts" tab on the left sidebar and then click the "Add Proxy Host" button.

3. **Configure Proxy Host**:
   - **Domain Names**: Enter `pihole.domain.com` where domain.com is the domain URL you wish to use.
   - **Scheme**: Select `http` from the dropdown menu.
   - **Forward Hostname/IP**: Enter `IP for Pihole`.
   - **Forward Port**: Enter `80`.
   - **Custom Locations**: Leave this field empty.
   - **SSL**: Check this box if you want to enable SSL.
   
4. **Advanced Configuration**:
   - In the "Advanced" section, add the following configuration:
     ```nginx
     location / {
       proxy_pass http://192.168.68.107:80/admin/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_hide_header X-Frame-Options;
       proxy_set_header X-Frame-Options "SAMEORIGIN";
       proxy_read_timeout 90;
     }
     location /admin {
       proxy_pass http://192.168.68.107:80/admin/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_hide_header X-Frame-Options;
       proxy_set_header X-Frame-Options "SAMEORIGIN";
       proxy_read_timeout 90;
     }
     ```
     Replace `192.168.68.107` with the actual IP address of your Pi-hole server.

5. **Save Changes**: Click the "Save" button to apply the configuration.

Now, Nginx Proxy Manager should be set up to forward requests to Pi-hole at `pihole.domainname.com`. Make sure to adjust the domain name and IP address to match your setup.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

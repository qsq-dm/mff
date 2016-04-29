
    server {
        server_name  139.196.6.231;
        listen       80;

        if ($time_iso8601 ~ "^(\d{4})-(\d{2})-(\d{2})") {
            set $year $1;
            set $month $2;
            set $day $3;
        }
        
        access_log /data/dev/$year-$month-$day.log custom;

        error_log  /data/error_dev.log debug;

        set $mobile_request '';
         
        if ($http_user_agent ~* '(Mobile|WebOS)') {
          set $mobile_request '1';
        }
        if ($uri = /) {
        set $mobile_request "${mobile_request}1";
        }
        if ($mobile_request = '11') {
          rewrite / /mobile/ redirect;
          break;
        }

        location /static {
            root   /tmp/meifenfen/dev/;
        }
        location /admin/static {
            root   /tmp/meifenfen/dev/static/;
        }


        location / {
            root   /root/meifenfen;
            uwsgi_pass 127.0.0.1:10002;
            include     uwsgi_params;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

    }

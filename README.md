# Django Boys Tutorial from [DjangoGirls](https://tutorial.djangogirls.org/)

## A `djangoboys` tutorial `with lots of extensions`!!! 💯💯💯

![Djangoboys](assets/images/logo.png)


# Deployment 🚀🚀🚀

## Deploy on Ubuntu 22.04 with Postgres, Nginx and Gunicorn


1. Create server via AWS EC2 or Digital Ocean Droplet, or other similar service
- AWS
 https://awstip.com/how-to-deploy-django-application-on-aws-ubuntu-ec2-25a24ca439e2

2. Prepare server with this setup:
https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04

3. Allow ubuntu user to have sudo privileges
- logged in via ssh
- type `sudo visudo`
- add `username ALL=(ALL) NOPASSWD: ALL` to the file
- save and exit

4. Create ssh keys for server add add to git so server can download repo

5. Download repo

6. Create `.env` file from `.env.sample`:
    cp `.env.sample` `.env`

7. Follow tutorial:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04

8. Check for static files access
`sudo -u www-data stat /home/ubuntu/djangoboys/static`

It it gives the error:
`stat: cannot statx '/home/ubuntu/djangoboys/static': Permission denied`

Then

Add the www-data to the username group:

`sudo gpasswd -a www-data username`

9. If nginx gives this error:
`nginx: [emerg] could not build server_names_hash, you should increase server_names_hash_bucket_size: 64`
`nginx: configuration file /etc/nginx/nginx.conf test failed`

Then

Edit the nginx.conf and on the http block, add this line:

`http{
      server_names_hash_bucket_size  64;
      ...
}`


10. Also check this tutorial in case of errors:
    https://pylessons.com/django-deployment

11. Visit your site and verify deployment

## Follow Along Video Tutorials ⏯️ ⏯️ ⏯️
1. https://www.youtube.com/watch?v=1fjpNXK7yqc
2. https://www.youtube.com/watch?v=7O1H9kr1CsA
3. https://www.youtube.com/watch?v=1D4mn_rO2cM

### Made with ❤️ by @edchelstephens

# Body Shape Exp3c
Deploy tutorial: https://consultantsussex.com/deploy-html-on-heroku/

Step 1: Register on Github
We’ll take it for granted that you can handle registering a free account on Github, just follow the link above…

Step 2: Create New Github Repository
Once you are logged into your new account, just navigate to Repositories and click the “NEW” button in the top right corner. Don’t forget to set your repo to PRIVATE as you don’t want it to be accessible to the public here.

Step 3: Create Some Files
Now you have your new repo, you will need to create a few files to enable your static HTML page to run on Heroku. Below are the minimum three files you will need for the basics of this tutorial.

TIP: You can add any other files in your repo that you want to create a website; like CSS, JS and other HTML pages for internal linking.

	1) composer.json
	Create a new file as composer.json and in that you just need the simple entry of {} you can just copy and paste these two characters if you find that easiest.

	2) index.php
	Next you will need the file index.php and in this you need to add the following line of code:
	<?php include_once("index.html"); ?>
	
	3) index.html
	This last file index.html is the core of your web page and it will contain the HTML content that you want to show on your Heroku app.

Step 4: Register on Heroku
Again, we hope you can handle registering a free account on Heroku (link above).

Step 5: Create New Heroku App
After logging into your new Heroku account, look for the “NEW” dropdown in the top right corner. Click it, then click on “Create new app”. Select a region and give your app a name… Be aware that the name you assign here will become the subdomain of your app for public access. So make it short and relevant to your web page content; eg. my-new-app.herokuapp.com

Step 6: Connect App to Repo
After creating your new app you should be taken directly to the Deploy tab in Heroku. Look for “Deployment method” and select Github. You will then be prompted to enter your repo name. Finalise the process by clicking “connect”.

Step 7: Enable Auto Deploy
This is just a time-saving feature that will mean that when you update your files in the Github Repo, they will automatically push through to your Heroku App.

Step 8: Install PHP Language Buildpack
This step is crucial to deploying your HTML on Heroku and is where you can correct the build log error mentioned above if you have already got this far. Switch to the “Settings” tab in your Heroku app and scroll down to “Buildpacks”. Click on the “Add buildpacks” button and select PHP from the available options.

Step 9: Deploy your HTML on Heroku
Finally you are ready to deploy your new HTML content on your Heroku app. Flip back to the “Deploy” tab and scroll to the bottom. Next to “Manual Deploy” click on the “deploy Branch” button.

Step 10: Enjoy your HTML page on Heroku
Now you can view your new web page on the URL you set up previously eg. my-new-app.herokuapp.com

----------------------- connecting heroku app to heroku-postgres database
https://devcenter.heroku.com/articles/heroku-postgresql 


----------------------- view database using PgAdmin4
https://stackoverflow.com/questions/20410873/how-can-i-browse-my-heroku-database#:~:text=You%20can%20find%20them%20by,to%20login%20to%20the%20DB. 

implement restriction: https://stackoverflow.com/questions/12663639/how-to-hide-databases-that-i-am-not-allowed-to-access/13298802#13298802




------------------------ PHP installation log
To enable PHP in Apache add the following to httpd.conf and restart Apache:
    LoadModule php_module /usr/local/opt/php/lib/httpd/modules/libphp.so

    <FilesMatch \.php$>
        SetHandler application/x-httpd-php
    </FilesMatch>

Finally, check DirectoryIndex includes index.php
    DirectoryIndex index.php index.html

The php.ini and php-fpm.ini file can be found in:
    /usr/local/etc/php/8.1/

To restart php after an upgrade:
  brew services restart php
Or, if you don't want/need a background service you can just run:
  /usr/local/opt/php/sbin/php-fpm --nodaemonize

--------------------------- connect to heroku-postgres using php
https://devcenter.heroku.com/articles/connecting-heroku-postgres#connecting-in-node-js

https://stackoverflow.com/questions/49431345/how-to-remotely-connect-to-heroku-postgresql-database-using

php script log can be viewed on heroku app main page --> top-right corner --> More --> view logs

completed code in receive_data.php, which sends data to heroku-postgres database.

tal.php is an alternative method. it does not use database, instead, it saves each subject's data temporarily on heroku, at my-app-url/subjectID.txt, which will be deleted automatically by heroku frequently

--------------------------- view and export data on pgadmin4
https://hevodata.com/learn/export-data-pgadmin/

  
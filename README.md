
# django Investment website

This is an Investment website built with django web framework




## Features

- Light/dark mode toggle
- Live previews
- Cross platform
- user deposit with paystack integration
- user registration
- buying of plan 
- daily or end or plan earning
- withdrawal

## Demo

https://mavis-investment.herokuapp.com/


## Deployment

To deploy this project run

### Clone this github repository
```bash
  git clone https://github.com/christaiwo/django-investment-website
```

### Enter the project folder
```bash
  cd django-investment-website
```

### Activate virtual enviroment
```bash
  source env/bin/activate
```

### Migrate the database
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
### Create admin account 
```bash
python3 manage.py createsuperuser
```

### Start the cronjob
```bash
python3 manage.py crontab add
```

You are done you can visit the site now from your browser
```bash
http://127.0.0.1:8000/
```



## Authors

- [@christaiwo](https://github.com/christaiwo)


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Feedback

If you have any feedback, please reach out to us at christopherijagbemi@gmail.com


## Support

For support, email christopherijagbemi@gmail.com


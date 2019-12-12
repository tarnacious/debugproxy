from flask_assets import Environment, Bundle

assets = Environment()

homepage_css = Bundle(
    'app/normalize.css',
    Bundle('app/fonts.scss', 'app/homepage.scss', filters='scss'),
    filters="cssmin",
    output='gen/homepage.css')

assets.register('homepage_css', homepage_css)

app_css = Bundle(
    Bundle('app/fonts.scss', 'app/app.scss', filters='cssmin,scss'),
    output='gen/app.css'
)

assets.register('app_css', app_css)

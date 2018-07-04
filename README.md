# Loco

A web app that lets you privately share your location with your team.

Once you login with your Google account, your browser will determine your location and make it visible to everyone else that has logged in.

## Deploy

1. By default, the app uses Google OAuth to log in users. To make that work, you'll need to [set up an OAuth 2.0 client ID](https://support.google.com/cloud/answer/6158849?hl=en) in the Google Developer console. You don't need to enable any APIs on that Google project, so you shouldn't be required to enter billing information. The OAuth client ID and secret should be saved and used for a later step.

   You can use other OAuth-based authentication systems by modifying the call to `oauth.remote_app()` in `location/factory.py`.

1. Set the environment variables `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to the client ID and secret you created above. To limit logins to a particular Google Apps domain, you can set the domain to limit to with the environment variable `ALLOWED_DOMAIN`.

1. You also need to set up a PostgreSQL database to store the user information. Set up a database and set the login information to the `DATABASE_URL` environment variable (e.g. `postgresql://user:pass@host/database`).

1. Finally, use a WSGI server like `gunicorn` to run the app.

## Development

1. Create a Google OAuth client ID/secret as described above. Note that you'll need to expose the app via a real URL using something like [ngrok](https://ngrok.com/) so that the OAuth callback from Google works. I don't think they allow `localhost` as a callback URL.

1. Create a sqlite database and apply the migrations:

   ```
   FLASK_APP=wsgi.py \
   GOOGLE_CLIENT_ID="google-client-id" \
   GOOGLE_CLIENT_SECRET="google-secret" \
   DATABASE_URL="sqlite:///local.db" \
   flask db upgrade
   ```

1. Run the app in developer mode:

   ```
   FLASK_DEBUG=true \
   FLASK_APP=wsgi.py:app \
   GOOGLE_CLIENT_ID="google-client-id" \
   GOOGLE_CLIENT_SECRET="google-secret" \
   DATABASE_URL="sqlite:///local.db" \
   flask run
   ```

1. Browse to [http://localhost:5000](http://localhost:5000)

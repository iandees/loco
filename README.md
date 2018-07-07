# Loco

A web app that lets you privately share your location with your team.

Once you login with your Google or Microsoft account, your browser will determine your location and make it visible to everyone else that has logged in.

## Deploy

1. By default, the app uses Google OAuth to log in users. To make that work, you'll need to [set up an OAuth 2.0 client ID](https://support.google.com/cloud/answer/6158849?hl=en) in the Google Developer console. You don't need to enable any APIs on that Google project, so you shouldn't be required to enter billing information. The OAuth client ID and secret should be saved and used for a later step.

   Note: You can use other OAuth-based authentication systems by creating a new Provider in
   `location/oauth_providers.py` that extends the `OAuthProvider` class, and adding it to the `OAUTH_PROVIDERS` dictionary. You can then choose which provider to use by
   setting the `OAUTH_PROVIDER` environment variable.

1. (Optional) The app can also support Microsoft OAuth to log in users.

    Create an OAuth application by following these instructions to [create an Azure Active Directory web app](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-protocols-oauth-code#register-your-application-with-your-ad-tenant). Don't forget to save the OAuth client ID and secret for the next step.

    You'll also need to set the environment variable `OAUTH_PROVIDER` to `microsoft`.

1. Set the environment variables `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` to the client ID and secret you created above. To limit logins to a particular domain, you can set the domain to limit to with the environment variable `ALLOWED_DOMAIN`.

1. You also need to set up a PostgreSQL database to store the user information. Set up a database and set the login information to the `DATABASE_URL` environment variable (e.g. `postgresql://user:pass@host/database`).

1. Finally, use a WSGI server like `gunicorn` to run the app.

## Development

1. Create an OAuth client ID/secret as described above. You can use `http://localhost:5000/login/authorized` as the callback URL for testing with both Google and Microsoft, but note that some OAuth providers require you to expose the app via a real URL using something like [ngrok](https://ngrok.com/)

1. Create a sqlite database and apply the migrations:

   ```
   FLASK_APP=wsgi.py \
   OAUTH_CLIENT_ID="oauth-client-id" \
   OAUTH_CLIENT_SECRET="oauth-secret" \
   DATABASE_URL="sqlite:///local.db" \
   flask db upgrade
   ```

1. Run the app in developer mode:

   ```
   FLASK_DEBUG=true \
   FLASK_APP=wsgi.py:app \
   OAUTH_CLIENT_ID="oauth-client-id" \
   OAUTH_CLIENT_SECRET="oauth-secret" \
   DATABASE_URL="sqlite:///local.db" \
   flask run
   ```

1. Browse to [http://localhost:5000](http://localhost:5000)

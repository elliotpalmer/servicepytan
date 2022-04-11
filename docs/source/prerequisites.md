# Pre-Requisites

## Requesting Access

Follow the instructions provided on the ServiceTitan developer's Site

[https://developer.servicetitan.io/request-access/](https://developer.servicetitan.io/request-access/)

**Basics**
* Fill out the "Developer Registration Form" if you are a developer
* Email `integrations@servicetitan.com` if you are ServiceTitan Customer

## Login to the Developer Portal
[https://developer.servicetitan.io/signin/](https://developer.servicetitan.io/signin/)

Login using your ServiceTitan credentials.

## Create a New App

1. Fill out the Form:
   * `Application Name` - Name of your application
   * `Organization` - Name of your organization for identification
   * `Homepage` - Your organizations webpage
   * `Tenants` - Should be filled out with your default ID
   * `API Scopes` - Review this list and provide access to only the enpoints needed for maximum security
2. Click "Create App" button
3. Click "Edit" next to your newly created app
4. Take note of the `App ID` under the title and the `Application Key`
   * You will need these later to complete authentication

## Authorizing your App in the ServiceTitan UI
1. Log into the ServiceTitan desktop application
2. Go to `Settings > Integrations > API Application Access`
3. Click the "Connect New App" Button
4. Select your application from the list that pops up
5. Click "Connect"
6. Verify that the permissions match what you expect
7. Click "Allow Access"
8. Take note of `Tenant ID` and `Client ID`
9. Generate a `Client Secret`
   * **WARNING** You can only see this once, so make sure you are ready to copy the `Client Secret` to a secure place or into your configuration file.
   * If you lose your `Client Secret` you can generate a new key. There is a max of 2 active secrets allowed for each application.

## Next Steps
Once you've generated the `Client Secret`, you have completed all of the steps necessary to complete your first request.

*  [Quick Start Guide](./quickstart.md)

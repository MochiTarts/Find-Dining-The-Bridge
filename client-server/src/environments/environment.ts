// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  environment: 'dev',
  mapbox: {
    accessToken:
      'pk.eyJ1IjoiZmluZGRpbmluZyIsImEiOiJja2wydTNybmQwY2I5MzJucmV3c2cyYnJjIn0.TAKkrZdAOdyxPEmFLG5L0w',
  },
  // https://developers.google.com/recaptcha/intro
  captcha: {
    siteKey: '6LdY6ykaAAAAAAwZu-Lpx-uO5P3IV5C8JBlw6vVb',
  },
  googleAnalytics: {
    trackingTag: 'UA-191314943-1'
  },
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.

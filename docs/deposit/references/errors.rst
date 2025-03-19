Error codes and solutions
=========================

In case your attempt to deposit an artefact or metadata failed you'll find here
explanations of the error messages and possible remediation.


401 Unauthorized
----------------

Something went wrong with the credentials you used or the way you used them.

- The API is protected through basic authentication, thus API calls requires username
  and password sent in the Authorization header
- Make sure the credentials you used match the environment you are targeting (staging
  or production)
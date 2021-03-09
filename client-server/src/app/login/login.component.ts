import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { TokenStorageService } from '../_services/token-storage.service';


import { SocialAuthService } from "angularx-social-login";
import { FacebookLoginProvider, GoogleLoginProvider, SocialUser } from "angularx-social-login";


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  form: any = {
    username: null,
    password: null
  };
  isLoggedIn = false;
  isLoginFailed = false;
  errorMessage = '';
  role: string = 'BU';
  user = {};

  constructor(private authService: AuthService, private tokenStorage: TokenStorageService, private socialAuth: SocialAuthService,) { }

  ngOnInit(): void {
    if (this.tokenStorage.getToken()) {
      this.isLoggedIn = true;
      this.role = this.tokenStorage.getUser().role;
    } else {
      this.socialAuth.authState.subscribe((user) => {
        this.user = user;
        console.log(user);
        // we'll get a SocialUser object with the following properties:
        // id, idToken, authToken, email, firstName, lastName, name, photoUrl, provider
        this.isLoggedIn = (user != null);
        if (user != null) {
          this.tokenStorage.setProvider(user.provider);
          switch (user.provider) {
            case 'GOOGLE':
              // send the token to backend to process
              this.authService.googleAuth(user.idToken, user.authToken).subscribe((data) => {
                this.tokenStorage.updateTokenAndUser(data.access_token);
                this.reloadPage();
              }, err => {
                console.log(err);
              })
              break;
            case 'FACEBOOK':
              // send the token to backend to process
              this.authService.facebookAuth(user.id, user.authToken).subscribe((data) => {
                this.tokenStorage.updateTokenAndUser(data.access_token);
                this.reloadPage();
              }, err => {
                console.log(err);
              })
              break;
            default:
              console.log('unrecognized provider: ' + this.provider);
          }

          // not sure if we want to redirect before or after google login...
          // redirect to a role selection page to confirm the role
        }
      });
    }
  }

  onSubmit(): void {
    const { username, password } = this.form;

    this.authService.login(username, password).subscribe(
      data => {

        var token = data.access;
        var errors = [];

        this.tokenStorage.updateTokenAndUser(token);

        this.isLoginFailed = false;
        this.isLoggedIn = true;
        this.role = this.tokenStorage.getUser().role;
        this.reloadPage();

      },
      err => {
        this.errorMessage = err.error.message;
        this.isLoginFailed = true;
      }
    );
  }

  reloadPage(): void {
    window.location.reload();
  }


  signInWithGoogle(): void {
    this.socialAuth.signIn(GoogleLoginProvider.PROVIDER_ID);
  }

  signInWithFB(): void {
    this.socialAuth.signIn(FacebookLoginProvider.PROVIDER_ID);
  }
}
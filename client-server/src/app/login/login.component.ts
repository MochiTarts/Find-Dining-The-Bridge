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
  loginForm: any = {
    username: null,
    password: null
  };
  isLoggedIn = false;
  isLoginFailed = false;
  errorMessage = '';
  infoMessage = '';
  role: string = 'BU';
  user = {};
  mode: number = 0;

  signupForm: any = {
    username: null,
    email: null,
    password1: null,
    password2: null,
    role: null
  };
  isSignupSuccessful = false;
  isSignUpFailed = false;

  constructor(public authService: AuthService, private tokenStorage: TokenStorageService, private socialAuth: SocialAuthService,) { }

  ngAfterViewInit(): void {
    let curTab = document.getElementsByClassName("tab-header")[0];
    let tabPanes = curTab ? curTab.getElementsByTagName("div") : [];

    for (let i = 0; i < tabPanes.length; i++) {
      tabPanes[i].addEventListener("click", function () {
        document.getElementsByClassName("tab-header")[0].getElementsByClassName("active")[0].classList.remove("active");
        tabPanes[i].classList.add("active");

        document.getElementsByClassName("tab-content")[0].getElementsByClassName("active")[0].classList.remove("active");
        document.getElementsByClassName("tab-content")[0].getElementsByClassName("tab-body")[i].classList.add("active");
      });
    }
  }

  ngOnInit(): void {
    // if token is already present then the user is logged in using basic credentials
    if (this.tokenStorage.getToken()) {
      this.isLoggedIn = true;
      this.role = this.tokenStorage.getUser().role;
      // otherwise the user is logged in with third party and need to handle authentication on the backend
    } else {
      this.socialAuth.authState.subscribe((user) => {
        this.user = user;
        console.log(user);
        // we'll get a SocialUser object with the following properties:
        // id, idToken, authToken, email, firstName, lastName, name, photoUrl, provider
        this.isLoggedIn = (user != null);
        if (user != null) {
          this.tokenStorage.setProvider(user.provider);
          // direct authentication to the appropriate view depending on the provider
          switch (user.provider) {
            case 'GOOGLE':
              // send the token to backend to process
              this.authService.googleAuth(user.idToken, user.authToken, this.role).subscribe((data) => {
                this.tokenStorage.updateTokenAndUser(data.access_token);
                this.reloadPage();
              }, err => {
                console.log(err);
              })
              break;
            case 'FACEBOOK':
              // send the token to backend to process
              this.authService.facebookAuth(user.id, user.authToken, this.role).subscribe((data) => {
                this.tokenStorage.updateTokenAndUser(data.access_token);
                this.reloadPage();
              }, err => {
                console.log(err);
              })
              break;
            default:
              console.log('unrecognized provider: ' + user.provider);
              this.tokenStorage.signOut();
              this.reloadPage();
          }

          // not sure if we want to redirect before or after google login...
          // redirect to a role selection page to confirm the role
        }
      }, (err) => {
        console.log(err);
      });
    }
  }

  // signup or login form on submit
  onSubmit(type: string): void {

    if (type == 'login') {
      const { username, password } = this.loginForm;

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
        // login failed
        error => {
          var verifyEmailInfoMessage = 'Please activate your account by verifying your email before you try to login. Email verification is required for us to authenticate you.';
          if (error.error) {
            switch (error.error.code) {
              case 'user_disabled':
                this.infoMessage = verifyEmailInfoMessage;
                break;
              default:
                this.errorMessage = error.error.detail;
            }
          }
          this.isLoginFailed = true;
        }
      );
    } else if (type == 'signup') {
      const { username, email, password1, password2, role } = this.signupForm;

      if (password1 == password2) {
        this.authService.register(username, email, password1, role).subscribe(
          data => {
            console.log(data);
            this.isSignupSuccessful = true;
            this.isSignUpFailed = false;
          },
          // signup failed
          err => {
            console.log(err)
            this.errorMessage = err.error.message;
            this.isSignUpFailed = true;
          }
        );
      }
    }

  }

  reloadPage(): void {
    window.location.reload();
  }


  signInWithGoogle(role: string = ''): void {
    this.role = role;
    this.socialAuth.signIn(GoogleLoginProvider.PROVIDER_ID);
  }

  signInWithFB(role: string = ''): void {
    this.role = role;
    this.socialAuth.signIn(FacebookLoginProvider.PROVIDER_ID);
  }

  googleRoleSelectPopup(): void {
    var googlePopupPanel = document.getElementsByClassName("googlePopupPanel")[0];
    googlePopupPanel.classList.toggle("show");
  }
  facebookRoleSelectPopup(): void {
    var facebookPopupPanel = document.getElementsByClassName("facebookPopupPanel")[0];
    facebookPopupPanel.classList.toggle("show");
  }
}
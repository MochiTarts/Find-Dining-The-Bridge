import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { TokenStorageService } from '../../_services/token-storage.service';

import { SocialAuthService } from "angularx-social-login";
import { FacebookLoginProvider, GoogleLoginProvider, SocialUser } from "angularx-social-login";

import { ChangeDetectionStrategy, ViewEncapsulation } from '@angular/core';
import {
  faGoogle,
  faFacebook
} from '@fortawesome/free-brands-svg-icons';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginComponent implements OnInit {
  faGoogle = faGoogle;
  faFacebook = faFacebook;
  selectedValue: string;

  loginForm: any = {
    username: null,
    password: null
  };
  isLoggedIn = false;
  isLoginFailed = false;
  loginErrorMessage: string = '';
  signupErrorMessage: string = '';
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

  showDetails: boolean = true;
  hide: boolean = true;
  strength: number = 0;

  //pattern = new RegExp(/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/);

  constructor(
    public authService: AuthService, private tokenStorage: TokenStorageService, private socialAuth: SocialAuthService, private ref: ChangeDetectorRef,
    private router: Router
  ) { }

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
      this.authService.updateLoginStatus(true);
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
                this.authService.updateLoginStatus(true);
                this.reloadPage();
              }, err => {
                this.authService.updateLoginStatus(false);
                console.log(err);
              })
              break;
            case 'FACEBOOK':
              // send the token to backend to process
              this.authService.facebookAuth(user.id, user.authToken, this.role).subscribe((data) => {
                this.tokenStorage.updateTokenAndUser(data.access_token);
                this.authService.updateLoginStatus(true);
                this.reloadPage();
              }, err => {
                this.authService.updateLoginStatus(false);
                console.log(err);
              })
              break;
            default:
              console.log('unrecognized provider: ' + user.provider);
              this.authService.updateLoginStatus(false);
              this.tokenStorage.signOut();
              this.reloadPage();
          }
          // redirect to or show profile page if first logged in
        }
      }, (err) => {
        this.authService.updateLoginStatus(false);
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
          this.authService.updateLoginStatus(true);
          this.isLoginFailed = false;
          this.isLoggedIn = true;
          this.role = this.tokenStorage.getUser().role;
          this.router.navigate([''])

        },
        // login failed
        error => {
          this.authService.updateLoginStatus(false);
          var verifyEmailInfoMessage = 'Please activate your account by verifying your email before you try to login. Email verification is required for us to authenticate you.';
          if (error.error) {
            switch (error.error.code) {
              case 'user_disabled':
                this.infoMessage = verifyEmailInfoMessage;
                break;
              default:
                if (error.error.detail == "No active account found with the given credentials"){
                  this.loginErrorMessage = "Incorrect username or password";
                } else {
                  this.loginErrorMessage = error.error.detail;
                }
            }
          }
          this.isLoginFailed = true;
          // manually trigger change detection to have error messages render
          this.ref.detectChanges();
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
            this.ref.detectChanges();
            //let curTab = document.getElementsByClassName("tab-header")[0];
            //let tabPanes = curTab ? curTab.getElementsByTagName("div") : [];
            // switch to login tab
            //tabPanes[1].click();

          },
          // signup failed
          err => {
            console.log(err)
            this.isSignUpFailed = true;
            this.signupErrorMessage = err.error.message;
            // manually trigger change detection to have error messages render
            this.ref.detectChanges();
          }
        );
      } else {
        this.signupErrorMessage = "password did not match!";
        this.isSignUpFailed = true;
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
    var popup = document.getElementsByClassName("popup")[0];
    popup.classList.toggle("show");
  }

  onStrengthChanged(strength: number) {
    this.strength = strength;
  }

  // just in case
  onError(event: any) {
    this.signupErrorMessage = "We're sorry, something went wrong with authentication. If this keeps up, please contact info@finddining.ca for more inquiries.";
    // manually trigger change detection to have error messages render
    this.ref.detectChanges();
  }
}
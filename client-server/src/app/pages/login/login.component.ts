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
import { NgbModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { Title } from '@angular/platform-browser';
import { environment } from 'src/environments/environment';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';

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
 
  public recaptchaForm: FormGroup;

  loginForm: any = {
    username: null,
    password: null
  };
  isLoggedIn = false;
  isLoginFailed = false;
  loginErrorMessage: string = '';

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
  signupErrorMessage: string = '';

  resetForm: any = {
    email: null,
  };
  resetSuccessful = false;
  resetFailed = false;
  resetErrorMessage: string = '';


  showDetails: boolean = true;
  hide: boolean = true;
  strength: number = 0;
  siteKey: string;
  isThirdParty: boolean = false;

  //pattern = new RegExp(/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/);

  constructor(
    public authService: AuthService,
    private tokenStorage: TokenStorageService,
    private socialAuth: SocialAuthService,
    private ref: ChangeDetectorRef,
    private router: Router,
    private modalService: NgbModal,
    private titleService: Title,
    private formBuilder: FormBuilder,
  ) {
    this.siteKey = `${environment.captcha.siteKey}`;
    this.recaptchaForm = this.formBuilder.group({
      recaptcha: [null, Validators.required]
    });
   }

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
    this.titleService.setTitle("Login In / Register | Find Dining Scarborough");
    // if token is already present then the user is logged in using basic credentials
    if (this.tokenStorage.getToken()) {
      this.isLoggedIn = true;
      this.authService.updateLoginStatus(true);
      this.role = this.tokenStorage.getUser().role;
      // otherwise the user is logged in with third party and need to handle authentication on the backend
    } else {
      this.socialAuth.authState.subscribe((user) => {
        this.isThirdParty = true;
        this.user = user;

        // console.log(user);
        // we'll get a SocialUser object with the following properties:
        // id, idToken, authToken, email, firstName, lastName, name, photoUrl, provider
        //this.isLoggedIn = (user != null);
        if (user != null) {
          this.tokenStorage.setProvider(user.provider);
          // direct authentication to the appropriate view depending on the provider
          switch (user.provider) {
            case 'GOOGLE':

              // send the token to backend to process
              this.authService.googleAuth(user.idToken, user.authToken, this.role).subscribe((data) => {
                this.tokenStorage.updateTokenAndUser(data.access_token);
                this.authService.updateLoginStatus(true);
                this.isLoggedIn = true;
                this.modalService.dismissAll();
                this.loginRedirect();
              }, err => {

                this.authService.updateLoginStatus(false);
                this.isLoggedIn = false;
                if (err.error){
                  this.loginErrorMessage = err.error.message;
                  //console.log(this.loginErrorMessage);
                }
                this.isLoginFailed = true;
                this.tokenStorage.signOut();
                // manually trigger change detection to have error messages render
                this.ref.detectChanges();
                //throw err;
              })
              break;
            case 'FACEBOOK':
              // send the token to backend to process
              this.authService.facebookAuth(user.id, user.authToken, this.role).subscribe((data) => {
                this.tokenStorage.updateTokenAndUser(data.access_token);
                this.authService.updateLoginStatus(true);
                this.isLoggedIn = true;
                this.modalService.dismissAll();
                this.loginRedirect();
              }, err => {
                this.authService.updateLoginStatus(false);
                this.isLoggedIn = false;
                if (err.error){
                  this.loginErrorMessage = err.error.message;
                  //console.log(this.loginErrorMessage);
                }
                this.isLoginFailed = true;
                this.tokenStorage.signOut();
                // manually trigger change detection to have error messages render
                this.ref.detectChanges();
              })
              break;
            default:
              // console.log('unrecognized provider: ' + user.provider);
              this.authService.updateLoginStatus(false);
              this.isLoggedIn = false;
              this.tokenStorage.signOut();
              this.reloadPage();
          }
          // redirect to or show profile page if first logged in
        }
      }, (err) => {
        this.authService.updateLoginStatus(false);
        //console.log(err);
      });
    }
  }

  // signup or login form on submit
  onSubmit(type: string): void {

    switch (type) {
      case 'login': {
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
            this.loginRedirect();

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
                  if (error.error.detail == "No active account found with the given credentials") {
                    this.loginErrorMessage = "Incorrect username or password";
                  } else {
                    //this.loginErrorMessage = error.error.detail;
                    this.loginErrorMessage = "Your username or password is incorrect"
                  }
              }
            }
            this.isLoginFailed = true;
            // manually trigger change detection to have error messages render
            this.ref.detectChanges();
          }
        );
        break;
      }
      case 'signup': {
        const { username, email, password1, password2, role } = this.signupForm;

        if (password1 == password2) {
          this.authService.register(username, email, password1, role).subscribe(
            data => {
              // console.log(data);
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
              // console.log(err)
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
        break;
      }
      case 'reset': {
        const { email } = this.resetForm;
        this.authService.resetPasswordEmail(email).subscribe(
          data => {
            // console.log(data);
            this.resetSuccessful = true;
            this.resetFailed = false;
            this.ref.detectChanges();

          },
          // signup failed
          err => {
            // console.log(err)
            this.resetFailed = true;
            this.resetErrorMessage = err.error.message;
            // manually trigger change detection to have error messages render
            this.ref.detectChanges();
          }
        );
        break;
      }
      default:
        console.log('unrecognized submission');
    }

  }

  reloadPage(): void {
    window.location.reload();
  }

  loginRedirect(): void {
    let profileId = this.tokenStorage.getUser().profile_id;

    if (this.role == 'RO') {
      if (profileId == null)
        this.router.navigate(['/restaurant-setup']);
      else
        this.router.navigate(['/restaurant']);
    } else {
      if (profileId == null) {
        this.router.navigate(['/']);
      } else {
        this.router.navigate(['/articles']);
      }
    }
  }


  signInWithGoogle(role: string = ''): void {
    this.role = role;
    this.socialAuth.signIn(GoogleLoginProvider.PROVIDER_ID).then((res) => {
      //this.modalService.dismissAll();
    }).catch(error => {
      console.log(error);
    });
  }

  signInWithFB(role: string = ''): void {
    this.role = role;
    this.socialAuth.signIn(FacebookLoginProvider.PROVIDER_ID).then(() => {
      //this.modalService.dismissAll();
    }).catch(error => {
      console.log(error);
    });
  }

  googleRoleSelectPopup(googleSignUp): void {
    this.modalService.open(googleSignUp, { ariaLabelledBy: 'modal-basic-title', size: 'sm' });
  }
  facebookRoleSelectPopup(facebookSignUp): void {
    this.modalService.open(facebookSignUp, { ariaLabelledBy: 'modal-basic-title', size: 'sm' });
  }
  reCaptchaPopup(reCaptcha): void {
    const modalRef = this.modalService.open(reCaptcha, { ariaLabelledBy: 'modal-basic-title', size: 'sm', keyboard: false, centered: true});
    modalRef.result.then((result) => {
    }, (reason) => {
      // manually trigger changes so that the form logic for the reCaptcha button can be applied immediately
      this.ref.detectChanges();
    });
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

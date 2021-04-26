import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import { AuthService } from '../../_services/auth.service';
import { TokenStorageService } from '../../_services/token-storage.service';

import { SocialAuthService } from "angularx-social-login";
import { FacebookLoginProvider, GoogleLoginProvider, SocialUser } from "angularx-social-login";

import { ChangeDetectionStrategy, ViewEncapsulation } from '@angular/core';
import {
  faGoogle,
  faFacebook
} from '@fortawesome/free-brands-svg-icons';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { Title } from '@angular/platform-browser';
import { environment } from 'src/environments/environment';
import { FormGroup, FormControl, Validators, FormBuilder } from '@angular/forms';
import { MatTabGroup } from '@angular/material/tabs';

const TIMER_REMAIN_KEY: string = 'remaining';

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
  loginErrorMessage: string = null;

  infoMessage = null;
  role: string = 'BU';
  user = {};
  mode: number = 0;
  failLoginAttempts: number = 0;

  signupForm: any = {
    username: null,
    email: null,
    password1: null,
    password2: null,
    role: null
  };
  isSignupSuccessful = false;
  isSignUpFailed = false;
  signupErrorMessage: string = null;
  signupMessage: string = null;

  resetForm: any = {
    email: null,
  };
  resetSuccessful = false;
  resetFailed = false;
  resetErrorMessage: string = null;

  isResendSuccessful = false;
  resendFailed = false;
  resendErrorMessage: string = null;
  resendMessage: string = null;

  resendForm: any = {
    email: null,
  };

  resendReadOnly: boolean = false;

  showDetails: boolean = true;
  hide: boolean = true;
  strength: number = 0;
  siteKey: string;
  isThirdParty: boolean = false;
  timerOn: boolean = false;
  initialTab: string = 'login';
  radioClicked: boolean = false;

  //pattern = new RegExp(/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/);

  @ViewChild(MatTabGroup) tabGroup: MatTabGroup;

  constructor(
    public authService: AuthService,
    private tokenStorage: TokenStorageService,
    private socialAuth: SocialAuthService,
    private ref: ChangeDetectorRef,
    private router: Router,
    private modalService: NgbModal,
    private titleService: Title,
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
  ) {
    this.siteKey = `${environment.captcha.siteKey}`;
    this.recaptchaForm = this.formBuilder.group({
      recaptcha: [null, Validators.required]
    });
    this.route.queryParams.subscribe(params => {
      this.initialTab = params['tab'];

    });
  }

  ngAfterViewInit(): void {
    var tabIndex: number;
    // set the active tab depending on the query param
    switch (this.initialTab) {
      case 'signup':
        tabIndex = 1;
        break;
      case 'reset':
        tabIndex = 2;
        break;
      case 'signin':
      default:
        tabIndex = 0;
    }
    this.tabGroup.selectedIndex = tabIndex;
  }

  ngOnInit(): void {
    this.titleService.setTitle("Login In / Register | Find Dining Scarborough");
    // check for additional param indicating the tab
    // if token is already present then the user is logged in using basic credentials
    if (this.tokenStorage.getToken()) {
      this.isLoggedIn = true;
      this.authService.updateLoginStatus(true);
      this.role = this.tokenStorage.getUser().role;
      this.setTimeRemaining(0);
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
                this.setTimeRemaining(0);
                this.modalService.dismissAll();
                this.role = this.tokenStorage.getUser().role;
                this.loginRedirect();
              }, err => {
                //console.log(err);
                this.authService.updateLoginStatus(false);
                this.isLoggedIn = false;
                var verifyEmailInfoMessage = 'Please activate your account by verifying your email before you try to login. Email verification is required for us to authenticate you.';

                if (err.error) {
                  switch (err.error.code) {
                    case 'user_disabled':
                      this.infoMessage = verifyEmailInfoMessage;
                      break;
                    default:
                      this.loginErrorMessage = err.error.message;
                  }
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
                this.setTimeRemaining(0);
                this.modalService.dismissAll();
                this.role = this.tokenStorage.getUser().role;
                this.loginRedirect();
              }, err => {
                this.authService.updateLoginStatus(false);
                this.isLoggedIn = false;
                if (err.error) {
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
        }
      }, (err) => {
        this.authService.updateLoginStatus(false);
        //console.log(err);
      });
    }
  }

  /**
   * Performs the actions to properly log a user in,
   * sign a user up, resend verification email, or
   * send a password reset email, depending on the 
   * parameter provided. (Makes a http request to
   * the appropriate endpoint)
   * 
   * @param type - determines the action: login, signup, 
   *               resend verification email, or reset password
   */
  onSubmit(type: string): void {

    switch (type) {
      case 'login': {
        const { username, password } = this.loginForm;

        this.authService.login(username, password).subscribe(
          data => {
            var token = data.access;
            this.tokenStorage.updateTokenAndUser(token);
            this.authService.updateLoginStatus(true);
            this.isLoginFailed = false;
            this.isLoggedIn = true;
            this.failLoginAttempts = 0;
            this.role = this.tokenStorage.getUser().role;
            this.loginRedirect();
          },
          // login failed
          error => {
            //console.log(error);
            this.authService.updateLoginStatus(false);
            this.failLoginAttempts += 1;
            var verifyEmailInfoMessage = 'Please activate your account by verifying your email before you try to login. Email verification is required for us to authenticate you.';
            if (error.error) {
              switch (error.error.code) {
                case 'user_disabled':
                  this.infoMessage = verifyEmailInfoMessage;
                  break;
                case 'too_many_request':
                  this.loginErrorMessage = "Too many login attempts. " + error.error.detail;
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
        var { username, email, password1, password2, role } = this.signupForm;
        // set username to be email or the local part of email if not given
        if (username === null || username.trim() == '') {
          // max length for username in Django is 150 characters
          if (email.length > 150) {
            // local part should be less than 64 characters
            username = email.split('@')[0];
            // just in case
            if (username.length > 150) {
              username = username.substr(0, 149)
            }
          } else {
            username = email;
          }
        }

        if (password1 == password2) {
          this.authService.register(username, email, password1, role).subscribe(
            data => {
              //console.log(data);
              this.isSignupSuccessful = true;
              this.isSignUpFailed = false;
              this.signupMessage = data.message;
              this.setTimeRemaining(0);
              document.getElementById('form_link').style.display = 'none';
              // set the registered email to the resend verification email form
              this.resendForm.email = email;
              // make the email field read-only
              this.resendReadOnly = true;
              this.ref.detectChanges();
              //let curTab = document.getElementsByClassName("tab-header")[0];
              //let tabPanes = curTab ? curTab.getElementsByTagName("div") : [];
              // switch to login tab
              //tabPanes[1].click();
            },
            // signup failed
            err => {
              //console.log(err);
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
      case 'resend': {
        const { email } = this.resendForm;
        this.signupMessage = null;
        this.authService.resendVerificationEmail(email).subscribe(
          data => {
            //console.log(data);
            this.resendMessage = data.message;
            this.isResendSuccessful = true;
            this.resendFailed = false;
            this.ref.detectChanges();
          },
          // resend failed
          err => {
            //console.log(err)
            this.resendFailed = true;
            this.resendErrorMessage = err.error.message;
            // manually trigger change detection to have error messages render
            this.ref.detectChanges();
          }
        );
        // cooldown
        this.timerOn = true;
        this.setTimeRemaining(60);
        this.timer(60, 'resend_button');
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
          // reset email request failed
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
      // should never happen
      default:
        console.log('unrecognized submission');
    }

  }

  /**
   * page reload
   */
  reloadPage(): void {
    window.location.reload();
  }

  /**
   * get remaining time from session storage
   * @returns seconds remaining of the timer, null if the time is never set or has been cleared
   */
  public getTimeRemaining(): number | null {
    return parseInt(window.sessionStorage.getItem(TIMER_REMAIN_KEY), 10);
  }

  /**
   * save remaining time to session storage
   * @param remaining - seconds remaining of the timer
   */
  public setTimeRemaining(remaining: number): void {
    window.sessionStorage.removeItem(TIMER_REMAIN_KEY);
    if (remaining > 0) {
      window.sessionStorage.setItem(TIMER_REMAIN_KEY, remaining.toString());
    }
  }

  /**
   * timer 'actualized' on an element
   * @param remaining 
   * @param element_id 
   * @returns None
   */
  timer(remaining: number, element_id: string): void {
    if (remaining % 5 == 0) {
      this.setTimeRemaining(remaining);
    }
    var m = Math.floor(remaining / 60);
    var s = remaining % 60;

    var m_str = m < 10 ? '0' + m : m;
    var s_str = s < 10 ? '0' + s : s;
    var elem = document.getElementById(element_id)
    elem.innerHTML = m_str + ':' + s_str;
    remaining -= 1;

    if (remaining >= 0 && this.timerOn) {
      setTimeout(() => {
        this.timer(remaining, element_id);
      }, 1000);
      return;
    }

    var displayText: string;

    switch (element_id) {
      case 'resend_button':
        displayText = 'Resend verification email'
        break;
      default:
        displayText = 'Submit'
    }
    elem.innerHTML = displayText;
    this.timerOn = false;
    this.ref.detectChanges();
  }

  /**
   * toggle link display text (sets the timer if it was resetted due to refresh)
   * @returns False to prevent link action
   */
  toggleLink(): boolean {
    var link = document.getElementById('form_link');
    if (link.classList.contains('show_signup')) {
      link.classList.remove('show_signup');
      link.innerHTML = "Register for an account?";
      this.isSignupSuccessful = true;
      this.ref.detectChanges();
      if (!this.timerOn) {
        // set timer for send email button if it is still on cooldown 
        var remaining = this.getTimeRemaining();
        if (remaining && remaining > 5) {
          this.timerOn = true;
          // reducing the time to account for time not being counted due to refresh
          this.timer(remaining - 5, 'resend_button');
        }
      }
    } else {
      link.classList.add('show_signup');
      link.innerHTML = "Didn't receive a verification email?";
      this.isSignupSuccessful = false;
      this.ref.detectChanges();
    }
    return false;
  }


  /**
   * Redirects user to the correct page after
   * successful login
   */
  loginRedirect(): void {
    let profileId = this.tokenStorage.getUser().profile_id;

    if (this.role == 'RO') {
      if (profileId == null)
        this.router.navigate(['/restaurant-setup']);
      else
        this.router.navigate(['/restaurant']);
    } else {
      if (profileId == null) {
        this.router.navigate(['/']).then(() => {
          window.location.reload();
        });
      } else {
        this.router.navigate(['/media']).then(() => {
          window.location.reload();
        });
      }
    }
  }


  /**
   * Registers or logs in a user using Google as the 3rd-party
   * provider
   * 
   * @param role - the specified role of the user (BU or RO)
   */
  signInWithGoogle(role: string = ''): void {
    this.role = role;
    this.socialAuth.signIn(GoogleLoginProvider.PROVIDER_ID).then((res) => {
      //this.modalService.dismissAll();
    }).catch(error => {
      console.log(error);
    });
  }

  /**
   * Registers or logs in a user using Facebook as the 3rd-party
   * provider
   * 
   * @param role - the specified role of the user (BU or RO)
   */
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
    const modalRef = this.modalService.open(reCaptcha, { ariaLabelledBy: 'modal-basic-title', size: 'md', keyboard: false, centered: true });
    modalRef.result.then((result) => {
    }, (reason) => {
      // manually trigger changes so that the form logic for the reCaptcha button can be applied immediately
      this.ref.detectChanges();
    });
  }

  closeRecaptchaPopup(modal): void {
    modal.dismiss();
  }

  onStrengthChanged(strength: number) {
    this.strength = strength;
  }

  onRoleChange(event) {
    //console.log(event.value);
    if (!this.radioClicked){
      // show the password field with the strength info when the one of the radio buttons is selected
      // (ngIf doesn't work as both elements need to be rendered first)
      document.getElementById('passwordField').style.display = 'block';
      document.getElementById('passwordInfo').style.display = 'block';
    }

    this.radioClicked = true;
  }

  // just in case
  onError(event: any) {
    //console.log(event);
    this.signupErrorMessage = "We're sorry, something went wrong with authentication. If this keeps up, please contact info@finddining.ca for more inquiries.";
    this.isSignUpFailed = true;
    // manually trigger change detection to have error messages render
    this.ref.detectChanges();
  }
}
